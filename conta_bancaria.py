from datetime import datetime

from brazilcep import exceptions, get_address_from_cep
from colorama import Fore, Style, init
from decoradores import emitir_mensagem, log_transacao

init(autoreset=True)


class ContaBancaria:
    """
    #### Classe responsável pela gestão de contas bancárias, oferecendo operações como saque, depósito e consulta de extrato.

    Esta classe gerencia clientes e contas bancárias, permitindo cadastrar novos clientes, criar contas,
    realizar transações financeiras e exibir informações detalhadas sobre contas e clientes.

    Funcionalidades principais:
        - Cadastrar clientes e contas bancárias.
        - Buscar e filtrar clientes por CPF.
        - Realizar transações financeiras, como saque e depósito.
        - Exibir o extrato bancário e detalhes das contas cadastradas.

    Métodos:
        - cadastrar_cliente(cpf=None): Cadastra um novo cliente no sistema, validando o CPF e obtendo endereço pelo CEP.
        - criar_conta(agencia, tipo_conta='c'): Cria uma conta bancária associada a um cliente existente.
        - buscar_conta(agencia, numero_conta): Busca uma conta bancária com base na agência e número da conta.
        - sacar(valor): Realiza um saque na conta, validando saldo, limites diários e regras de segurança.
        - depositar(valor): Permite o depósito de um valor na conta informada.
        - imprimir_extrato(): Exibe o extrato detalhado das transações realizadas na conta.
        - atualizar_cliente(): Atualiza os dados cadastrais de um cliente, como nome e endereço.
        - excluir_cliente(): Remove um cliente do sistema, caso esteja cadastrado.
        - filtrar_cliente(cpf): Busca um cliente pelo CPF e retorna seus dados.
        - exibir_cliente(): Exibe informações detalhadas de um cliente e suas contas.

    Exemplo de uso:
        >>> banco = ContaBancaria()
        >>> banco.cadastrar_cliente(cpf="12345678900")
        Informe o nome completo: Maria Oliveira
        Informe a data de nascimento (dd/mm/aaaa): 10/08/1990
        Informe o CEP: 01001000
        Cidade: São Paulo, UF: SP
        Rua: Praça da Sé, Número: 120
        Bairro: Sé - CEP: 01001-000

        ──────────────────────────────────────────────────
        Cliente Maria Oliveira cadastrado com sucesso.

        >>> banco.criar_conta(agencia="0001", tipo_conta="c")
        Conta Corrente criada com sucesso! Número: 1

        >>> banco.depositar(500)
        Depósito de R$ 500.00 realizado com sucesso!

        >>> banco.sacar(valor=200)
        Saque de R$ 200.00 realizado com sucesso!

        >>> banco.imprimir_extrato()
        ──────────────── EXTRATO ────────────────
        ✅ Depósito: R$ 500.00
        ❌ Saque:    R$ 200.00
        Saldo: R$ 300.00
        ──────────────────────────────────────────

    Observações:
        - Apenas clientes cadastrados podem ter contas bancárias.
        - Transações seguem limites pré-definidos para saque e depósitos.
        - O extrato detalha todas as movimentações financeiras da conta.

    """

    def __init__(self, saldo=0.0, limite=500, limite_saques=3, agencia='0001'):
        self.saldo = saldo
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0
        self.extrato = []
        self.contas = []
        self.clientes = []
        self.contador_contas = {"corrente": 1000, "poupanca": 5000}
        self.AGENCIA = agencia

    @log_transacao
    def sacar(self, *, valor):
        """
        Realiza um saque em uma conta bancária, aplicando regras de validação.

        O saque é permitido apenas se as seguintes condições forem atendidas:
        - A conta informada existe no sistema.
        - O valor do saque é positivo.
        - O saldo da conta é suficiente para cobrir o saque.
        - O valor do saque não ultrapassa o limite permitido.
        - O número máximo de saques diários ainda não foi atingido.

        O método solicita o número da conta ao usuário e verifica se ela existe. Caso
        contrário, exibe um aviso. Se a conta for válida, são feitas as verificações
        adicionais mencionadas acima. Em caso de erro, mensagens de aviso são exibidas.

        Este método está decorado com `@log_transacao`, registrando a execução da
        transação com um timestamp.

        Parâmetros:
        ---
            valor (float): O valor a ser sacado.

        Retorna:
        ---
            bool: `True` se o saque for realizado com sucesso, `False` caso contrário.

        Exemplo:
            >>> conta.sacar(valor=100.00)
            Informe o número da conta: 12345
            ⚠  Operação falhou! O saque excede o limite de R$ 500.00.
            False
        """
        numero_conta = input('Informe o número da conta: ').strip()
        conta = self.buscar_conta(self.AGENCIA, numero_conta=numero_conta)

        if not conta:
            print(emitir_mensagem(('Aviso', 'Conta não encontrada.')))
            return False

        if valor <= 0:
            print(emitir_mensagem(
                ('Aviso', 'Operação falhou! O valor informado é inválido.')))
            return False
        if valor > conta["saldo"]:
            print(emitir_mensagem(
                ('Aviso', f'Saldo insuficiente. Saldo atual: R$ {conta["saldo"]:.2f}.')))
            return False
        if valor > self.limite:
            print(emitir_mensagem(
                ('Aviso', f'Operação falhou! O saque excede o limite de R$ {self.limite:.2f}.')))
            return False
        if conta.get("saques_diarios", 0) >= self.limite_saques:
            print(emitir_mensagem(
                ('Aviso', 'Operação falhou! Número máximo de saques diário excedido.')))
            return False

        # Realiza o saque
        conta["saldo"] -= valor
        conta.setdefault("extrato", []).append(
            f'   {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}' + Fore.RED + " <= " + Style.RESET_ALL + f'Saque:    R$ {valor:.2f}')
        conta["saques_diarios"] = conta.get("saques_diarios", 0) + 1

        print(f'\nSaque de R$ {valor:.2f} realizado com sucesso!')
        return True

    @log_transacao
    def depositar(self, valor):
        """
        Realiza um depósito em uma conta bancária, validando a operação.

        O método solicita ao usuário o número da conta para a qual o depósito será feito.
        Caso a conta não seja encontrada, exibe uma mensagem de aviso e encerra a operação.
        Além disso, o depósito só será realizado se o valor informado for positivo.

        Se o depósito for bem-sucedido, o saldo da conta será atualizado e o registro
        da transação será armazenado no extrato da conta.

        Este método está decorado com `@log_transacao`, garantindo que a transação seja
        registrada com um timestamp.

        Parâmetros:
        ---
            valor (float): O valor a ser depositado.

        Retorna:
        ---
            bool: `True` se o depósito for realizado com sucesso, `False` caso contrário.

        Exemplo:
            >>> conta.depositar(200.00)
            Informe o número da conta: 12345
            Depósito de R$ 200.00 realizado com sucesso!
            True
        """
        numero_conta = input('Informe o número da conta: ').strip()
        conta = self.buscar_conta(self.AGENCIA, numero_conta=numero_conta)

        if not conta:
            print(emitir_mensagem(('Aviso', 'Conta não encontrada.')))
            return False

        if valor <= 0:
            print(emitir_mensagem(
                ('Alerta', 'Operação falhou! O valor informado é inválido.')))
            return False

        # Realiza o depósito
        conta["saldo"] += valor
        conta.setdefault("extrato", []).append(
            f'   {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}' + Fore.GREEN + " => " + Style.RESET_ALL + f'Depósito: R$ {valor:.2f}')

        print(f'\nDepósito de R$ {valor:.2f} realizado com sucesso!')
        return True

    @log_transacao
    def imprimir_extrato(self):
        """
        Exibe o extrato de uma conta bancária, listando todas as transações realizadas.

        O método solicita ao usuário o número da conta e verifica sua existência no sistema.
        Se a conta for encontrada, imprime todas as transações registradas no extrato. Caso
        não haja movimentações, exibe uma mensagem informando que não foram realizadas transações.

        Além das transações, o saldo atual da conta é exibido ao final do extrato.

        Este método está decorado com `@log_transacao`, garantindo que a consulta do extrato
        seja registrada com um timestamp.

        Parâmetros:
        ---
            Nenhum.

        Retorna:
        ---
            None: O método apenas imprime o extrato na tela.

        Exemplo:
            >>> conta.imprimir_extrato()
            Informe o número da conta: 12345

            ═════════════════════ EXTRATO ════════════════════

               06/09/2024 14:30:00 => Depósito: R$ 200.00
               06/09/2024 15:00:00 => Saque: R$ 50.00

              ───────────────────────
               Saldo: R$ 150.00
            ════════════════════════════════════════════════
        """
        numero_conta = input('Informe o número da conta: ').strip()
        conta = self.buscar_conta(self.AGENCIA, numero_conta=numero_conta)

        if not conta:
            print(emitir_mensagem(('Aviso', 'Conta não encontrada.')))
            return

        print('\n═════════════════════ EXTRATO ════════════════════\n')

        extrato = conta.get("extrato", [])
        if not extrato:
            print(emitir_mensagem(('Aviso', 'Não foram realizadas movimentações.')))
        else:
            print('\n'.join(extrato))

        print('\n')
        n = len(f"{conta['saldo']:.2f}")
        print(f'{" "}',  '─' * (n + 13))
        print(f'   Saldo: R$ {conta["saldo"]:.2f}')
        print('═' * 50, '\n')

    def cadastrar_cliente(self, cpf=None):
        """
        #### Cadastra um novo cliente no banco.

        Se o CPF já estiver cadastrado, o sistema informa e não realiza um novo cadastro.
        Caso contrário, solicita os dados pessoais do cliente e tenta obter o endereço automaticamente
        via API de consulta de CEP. Se o CEP não for encontrado, permite a entrada manual do endereço.

        Parâmetros:
        ---
            cpf (str, opcional): CPF do cliente. Se não for informado, será solicitado via input.

        Exceções tratadas:
            - Se o cliente já estiver cadastrado, exibe uma mensagem e interrompe o cadastro.
            - Se o CEP não for encontrado, solicita o endereço manualmente.

        Exemplo de uso:

            >>> banco = ContaBancaria()
            >>> banco.cadastrar_cliente()
            Informe o CPF (Somente Números): 12345678900
            Informe o nome completo: João da Silva
            Informe a data de nascimento (dd/mm/aaaa): 15/06/1985
            Informe o CEP: 01001000
            Cidade: São Paulo, UF: SP
            Rua: Praça da Sé, Número: 100
            Bairro: Sé - CEP: 01001-000

            ──────────────────────────────────────────────────
            Cliente João da Silva cadastrado com sucesso.
        """
        if cpf is None:
            cpf = input('\nInforme o CPF (Somente Números): ')

        if self.filtrar_cliente(cpf):
            print('Cliente já cadastrado.')
            return

        nome = input('Informe o nome completo: ')
        data_nascimento = input('Informe a data de nascimento (dd/mm/aaaa): ')
        try:
            cep = input('Informe o CEP: ')
            endereco = get_address_from_cep(cep)
            numero = input('Número da residência: ')

            print(f'\nCidade: {endereco["city"]}, UF: {endereco["uf"]}')
            print(f'Rua: {endereco["street"]}, Número: {numero}')
            print(
                f'Bairro: {endereco["district"]} - CEP: {endereco["cep"]}\n')

            endereco_completo = (endereco["street"], numero, endereco["district"],
                                 endereco["city"], endereco["uf"], cep)
            print('─' * 50)
        except exceptions.BrazilCEPException:
            print(emitir_mensagem(
                ('Erro', 'CEP não encontrado, informe o endereço manualmente.')))
            endereco_completo = tuple(input(
                'Informe o endereço completo (Rua, número, bairro, cidade, estado, CEP): ').split(','))

        self.clientes.append({'nome': nome, 'data_nascimento': data_nascimento,
                             'cpf': cpf, 'endereco': endereco_completo})
        print(f'Cliente {nome} cadastrado com sucesso.')

    def filtrar_cliente(self, cpf):
        """
        #### Busca um cliente no banco de dados pelo CPF.

        Parâmetros:
        ---
            cpf (str): O CPF do cliente a ser pesquisado.

        Retorna:
        ---
            dict | None: Retorna um dicionário com os dados do cliente se encontrado, ou None caso contrário.

        Exemplo de uso:

            >>> banco = ContaBancaria()
            >>> cliente = banco.filtrar_cliente("12345678900")
            >>> if cliente:
            ...     print(f"Cliente encontrado: {cliente['nome']}")
            ... else:
            ...     print("Cliente não encontrado.")
        """
        for cliente in self.clientes:
            if cliente['cpf'] == cpf:
                return cliente
        return None

    def exibir_cliente(self):
        """
        #### Exibe as informações de um cliente cadastrado no banco, incluindo suas contas, se houver.

        Solicita o CPF do cliente e exibe seu nome, data de nascimento, endereço e contas bancárias associadas.
        Se o cliente não tiver conta, é dada a opção de criar uma nova conta.

        Entrada:
        ---
            - O usuário deve fornecer o CPF do cliente.

        Exceções tratadas:
            - Se o cliente não for encontrado, exibe um aviso.
            - Se o cliente não possuir contas, oferece a opção de criar uma conta corrente.

        Exemplo de uso:

            >>> banco = ContaBancaria()
            >>> banco.exibir_cliente()
            Informe o CPF do cliente: 12345678900

            ──────────────────────────────────────────────────
            Nome: João da Silva
            Data de nascimento: 15/06/1985
            Endereço: Rua A, 123, Centro

            🔹 Conta: 1001 (Corrente)
            Saldo: R$ 5000.00
            ──────────────────────────────────────────────────
        """
        cpf = input('\nInforme o CPF do cliente: ').strip()
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print(emitir_mensagem(('Alerta', 'Cliente não encontrado.')))
            return

        contas_cliente = [conta for conta in self.contas if conta.get(
            'cliente', {}).get('cpf') == cpf]

        print('\n')
        print('─' * 50)
        print(f"Nome: {cliente['nome']}")
        print(f"Data de nascimento: {cliente['data_nascimento']}")
        print(f"Endereço: {', '.join(cliente['endereco'])}")

        if contas_cliente:
            for conta in contas_cliente:
                print(
                    f"\n🔹 Conta: {conta['numero_conta']} ({conta['tipo_conta'].capitalize()})")
                print(f"   Saldo: R$ {conta['saldo']:.2f}\n")
        else:
            print('\n')
            print(emitir_mensagem(
                ('Alerta', 'Cliente ainda não possui uma conta cadastrada.')))
            opcao = input(
                'Deseja criar uma conta corrente para o cliente? (S/N): ').strip().lower()
            if opcao == 's':
                self.criar_conta(self.AGENCIA)
            else:
                print(emitir_mensagem(('Erro', 'Criação de conta cancelada.')))
                return None

        print('─' * 50)
        print('\n')

    def atualizar_cliente(self):
        """
        #### Atualiza os dados de um cliente cadastrado no banco.

        Solicita o CPF do cliente e permite a atualização do nome e endereço. Se o cliente não for encontrado, exibe uma mensagem de aviso.

        Entrada:
        ---
            - O usuário deve fornecer o CPF do cliente.
            - Opcionalmente, pode atualizar o nome e/ou o endereço (separado por vírgulas).

        Exceções tratadas:
            - Se o cliente não existir, a operação é cancelada com um aviso.

        Exemplo de uso:

            >>> banco = ContaBancaria()
            >>> banco.atualizar_cliente()
            Informe o CPF do cliente: 12345678900
            Novo nome (ou pressione Enter para manter o mesmo): João da Silva
            Novo endereço (ou pressione Enter para manter o mesmo): Rua A, 123, Centro
            Dados do cliente atualizados com sucesso.
        """
        cpf = input('\nInforme o CPF do cliente: ')
        cliente = self.filtrar_cliente(cpf)
        if cliente:
            novo_nome = input(
                'Novo nome (ou pressione Enter para manter o mesmo): ')
            novo_endereco = input(
                'Novo endereço (ou pressione Enter para manter o mesmo): ')

            if novo_nome:
                cliente['nome'] = novo_nome
            if novo_endereco:
                cliente['endereco'] = tuple(novo_endereco.split(','))

            print('Dados do cliente atualizados com sucesso.')
        else:
            print(emitir_mensagem(('Aviso', 'Cliente não encontrado.')))

    def excluir_cliente(self):
        """
        #### Remove um cliente do banco de dados.

        Solicita o CPF do cliente a ser excluído. Se o cliente existir, ele será removido da lista de clientes. Caso contrário, exibe um aviso.

        Entrada:
        ---
            - O usuário deve fornecer o CPF do cliente a ser excluído.

        Exceções tratadas:
            - Se o cliente não for encontrado, a operação é cancelada com um aviso.

        Exemplo de uso:

            >>> banco = ContaBancaria()
            >>> banco.excluir_cliente()
            Informe o CPF do cliente a ser excluído: 12345678900
            Cliente excluído com sucesso.
        """
        cpf = input('\nInforme o CPF do cliente a ser excluído: ')
        cliente = self.filtrar_cliente(cpf)
        if cliente:
            opcao = input(
                f'Deseja excluir o cliente {cliente["nome"].title()}?\nTodas as contas vinculadas serâo excluidas? (S/N): ').strip().lower()
            if opcao == 's':
                self.clientes.remove(cliente)

                # Remove todas as contas vinculadas a esse cliente
                self.contas = [
                    conta for conta in self.contas if conta["cliente"]["cpf"] != cpf]

                print(emitir_mensagem(
                    ('Aviso', 'Cliente e contas associadas excluídos com sucesso.')))
        else:
            print(emitir_mensagem(('Aviso', 'Cliente não encontrado.')))

    def criar_conta(self, agencia, tipo_conta: str = 'c'):
        """
        #### Cria uma nova conta bancária para um cliente existente ou permite o cadastro de um novo cliente.

        Parâmetros:
        ---
            agencia (str): O número da agência onde a conta será criada.
            tipo_conta (str, opcional): O tipo de conta a ser criada. Pode ser:
                - 'c' para conta corrente (padrão)
                - 'p' para conta poupança

        Retorna:
        ---
            dict | None: Retorna um dicionário contendo os dados da conta criada, ou None se a criação for cancelada ou inválida.

        Exceções tratadas:
            - Se o cliente não for encontrado, permite o cadastro de um novo cliente.
            - Se o tipo de conta informado for inválido, a operação é cancelada.

        Exemplo de uso:

            >>> banco = ContaBancaria()
            >>> nova_conta = banco.criar_conta('1234', 'p')
            Conta Poupança criada com sucesso! Número: 1001
        """
        cpf = input('\nInforme o CPF (Somente Números): ').strip()
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print(emitir_mensagem(('Aviso', 'Usuário não localizado no banco.')))
            opcao = input(
                'Deseja cadastrar um novo cliente? (S/N): ').strip().lower()
            if opcao == 's':
                self.cadastrar_cliente()
                cliente = self.filtrar_cliente(cpf)
            else:
                print(emitir_mensagem(('Aviso', 'Criação de conta cancelada.')))
                return None

        if tipo_conta.lower() == 'c':
            tipo_conta = 'corrente'
        elif tipo_conta.lower() == 'p':
            tipo_conta = 'poupanca'
        else:
            print(emitir_mensagem(('Erro', 'Tipo de conta inválido!')))
            return None

        numero_conta = self.contador_contas[tipo_conta]
        self.contador_contas[tipo_conta] += 1

        conta = {
            'agencia': agencia,
            'numero_conta': numero_conta,
            'cliente': cliente,
            'tipo_conta': tipo_conta,
            'saldo': 0.0,
            'extrato': []
        }
        self.contas.append(conta)

        print(
            f'Conta {tipo_conta.capitalize()} criada com sucesso! Número: {numero_conta}\n')
        return conta

    def buscar_conta(self, agencia, /, *, numero_conta):
        """
        #### Busca uma conta bancária pelo número da agência e número da conta.

        Percorre a lista de contas cadastradas e retorna a conta correspondente à
        agência e ao número da conta informados. Caso a conta não seja encontrada,
        retorna None.

        Parâmetros:
        ---
            agencia (str): Número da agência bancária. Deve ser passado como um argumento posicional.
            numero_conta (str): Número da conta bancária. Deve ser passado como um argumento nomeado.

        Retorna:
        ---
            dict | None: Retorna um dicionário com os dados da conta se encontrada, ou None caso contrário.

        Exemplo de uso:

            >>> banco = ContaBancaria()
            >>> conta = banco.buscar_conta('1234', numero_conta='1001')
            >>> if conta:
            ...     print("Conta encontrada:", conta)
            ... else:
            ...     print("Conta não encontrada.")
        """
        for conta in self.contas:
            if str(conta["agencia"]) == agencia and str(conta["numero_conta"]) == numero_conta:
                return conta
        return None
