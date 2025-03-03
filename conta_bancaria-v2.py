import os
from datetime import datetime

from colorama import Fore, Style, init

init(autoreset=True)

contador_contas = {'corrente': 1}
tipo_conta = 'corrente'


def exibir_menu(opcao_selecionada=None):
    """
    #### Exibe o menu principal do sistema bancário, destacando a opção selecionada.

    :param opcao_selecionada: (str) Opção atualmente selecionada pelo usuário.
    """
    print('╔════════════════════════════════════════════════╗')
    print('║               BANCO D`PAULA                    ║')
    print('╚════════════════════════════════════════════════╝')
    print('╔════════════════════════════════════════════════╗')
    print('║        Selecione uma operação no menu          ║')
    print('╠════════════════════════════════════════════════╣')
    print(f'║ {(Fore.LIGHTGREEN_EX if opcao_selecionada == "1" else "")}{("✔" if opcao_selecionada == "1" else " ")} 1 - SAQUE{Style.RESET_ALL}         {(Fore.LIGHTGREEN_EX if opcao_selecionada == "6" else "")}{("✔" if opcao_selecionada == "6" else " ")} 6 - CRIAR CONTA CORRENTE{Style.RESET_ALL} ║')

    print(f'║ {(Fore.LIGHTGREEN_EX if opcao_selecionada == "2" else "")}{("✔" if opcao_selecionada == "2" else " ")} 2 - DEPÓSITO{Style.RESET_ALL}      {(Fore.LIGHTGREEN_EX if opcao_selecionada == "7" else "")}{("✔" if opcao_selecionada == " " else " ")}                  {Style.RESET_ALL}        ║')

    print(f'║ {(Fore.LIGHTGREEN_EX if opcao_selecionada == "3" else "")}{("✔" if opcao_selecionada == "3" else " ")} 3 - EXTRATO{Style.RESET_ALL}       {(Fore.LIGHTGREEN_EX if opcao_selecionada == "8" else "")}{("✔" if opcao_selecionada == " " else " ")}                  {Style.RESET_ALL}        ║')

    print(f'║ {(Fore.LIGHTGREEN_EX if opcao_selecionada == "4" else "")}{("✔" if opcao_selecionada == "4" else " ")} 4 - CRIAR USUÁRIO{Style.RESET_ALL}  {(Fore.LIGHTGREEN_EX if opcao_selecionada == "9" else "")}{("✔" if opcao_selecionada == " " else " ")}                   {Style.RESET_ALL}      ║')

    print(f'║ {(Fore.LIGHTRED_EX if opcao_selecionada == "5" else "")}{("✔" if opcao_selecionada == "5" else " ")} 5 - SAIR{Style.RESET_ALL}          {(Fore.LIGHTGREEN_EX if opcao_selecionada == "10" else "")}{("✔" if opcao_selecionada == "  " else " ")}                   {Style.RESET_ALL}       ║')

    print('╚════════════════════════════════════════════════╝')


def sacar(*, saldo, valor,  extrato, limite, numero_saques, limite_saque):
    """
    #### Realiza um saque da conta, verificando saldo disponível, limite de saque e número de saques diários.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saque
    valor_valido = valor > 0
    conta_zerada = valor != 0 and saldo == 0

    if conta_zerada:
        print(
            'Necessário realizar depósito, saldo em conta igual a R$ 0.0. Utilize a opção 2.')

    elif excedeu_saldo:
        print(
            f"Você não tem saldo suficiente. Saldo atual  em conta R$ {saldo:.2f}.")

    elif excedeu_limite:
        print(
            f"Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor_valido:
        saldo -= valor
        extrato.append(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + Fore.RED + " <= " + Style.RESET_ALL + f"Saque:    R$ {valor:.2f}")
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!\n")
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques


def depositar(valor, extrato, saldo, contas, /):
    """
    #### Realiza um depósito na conta, adicionando o valor ao saldo.
    """

    if valor > 0:
        saldo += valor
        extrato.append(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + Fore.GREEN + " => " + Style.RESET_ALL + f"Depósito: R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!\n")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato


def imprimir_extrato(saldo, /, *, extrato):
    """
    #### Exibe o extrato da conta, listando todas as transações realizadas.
    """
    largura_total: int = 46
    titulo = 'EXTRATO'
    tamanho_titulo = len(titulo)
    espacos_laterais = (largura_total - tamanho_titulo - 2) // 2
    espacos_restantes = largura_total - \
        (espacos_laterais * 2) - tamanho_titulo - 2
    print("\n" + "═" * espacos_laterais +
          f" {titulo} " + "═" * (espacos_laterais + espacos_restantes) + "\n")
    if not extrato:
        print("Não foram realizado movimentações.")
    else:
        print("\n".join(extrato))
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("═" * largura_total + "\n")


def criar_usuario(usuarios):
    """
    #### Cria um novo usuário no banco, solicitando informações como nome, CPF, data de nascimento e endereço.
    """
    cpf = input('Informe o CPF (Somente Números): ').strip()

    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print('Usuário já cadastrado no banco!')
        return

    nome = input('\nInforme o Nome: ').strip()
    data_nascimento = input(
        'Informe a data de nascimento (dd/mm/aaa): ').strip()
    endereco = input(
        'Informe o seu endereco(Rua, numero - bairro - cidade/uf): ').strip()

    usuario = {
        'nome': nome,
        'cpf': cpf,
        'data_nascimento': data_nascimento,
        'endereco': endereco
    }

    usuarios.append(usuario)
    print('Usuário cadastrado com sucesso!\n')


def filtrar_usuario(cpf, usuarios):
    """
    #### Filtra um usuário pelo CPF, retornando o usuário caso encontrado ou None caso contrário.
    """
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    return None


def criar_conta_corrente(agencia, usuarios, contas):
    """
    #### Cria uma nova conta corrente no banco, associando a um usuário já cadastrado.
    """

    cpf = input('\nInforme o CPF (Somente Números): ').strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print('Usuário não localizado no banco.')
        opcao = input(
            'Deseja cadastrar um novo usuario? (S/N): ').strip().lower()
        if opcao == 's':
            criar_usuario(usuarios)
        else:
            print('Criação de conta cancelada.\n')
            return

    numero_conta = contador_contas[tipo_conta]
    contador_contas[tipo_conta] += 1

    conta = {
        'agencia': agencia,
        'numero_conta': numero_conta,
        'usuario': usuario,
        'tipo_conta': tipo_conta,
    }

    contas.append(conta)

    print(
        f'Conta {tipo_conta.capitalize()} criada com sucesso! Número: {numero_conta}\n')


def iniciar():
    """
    #### Inicia o loop principal do sistema bancário, permitindo ao usuário selecionar operações.
    """
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    saldo = 0.0
    limite = 500
    numero_saques = 0
    extrato = []
    usuarios = []
    contas = []

    exibir_menu()

    while True:
        opcao = input('Selecione uma operação: ')
        exibir_menu(opcao)

        if opcao == '1':
            valor = float(input('Valor do Saque: '))
            saldo, extrato, numero_saques = sacar(valor=valor,
                                                  saldo=saldo,
                                                  limite=limite,
                                                  numero_saques=numero_saques,
                                                  extrato=extrato,
                                                  limite_saque=LIMITE_SAQUES)

        elif opcao == '2':
            valor = float(input('Informe o valor do depósito: '))
            saldo, extrato = depositar(
                valor, extrato, saldo, contas)

        elif opcao == '3':
            imprimir_extrato(saldo, extrato=extrato)

        elif opcao == '4':
            criar_usuario(usuarios)

        elif opcao == '5':
            print("\nObrigado por usar o Banco D'Paula! Saindo...\n")
            break

        elif opcao == '6':
            criar_conta_corrente(AGENCIA, usuarios, contas)

        else:
            print("Opção inválida! Escolha novamente.\n")


if __name__ == "__main__":
    iniciar()
