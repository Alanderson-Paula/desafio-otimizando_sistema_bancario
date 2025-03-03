# 🏦 Desafio Sistema Bancário Otimizado - Banco D'Paula

Este projeto implementa um **Sistema Bancário Otimizado** com funcionalidades básicas, incluindo **saque**, **depósito** e **extrato**. Esta é a segunda versão do projeto, que traz melhorias e novas funcionalidades em relação à versão anterior.

## 📌 Funcionalidades

- Realizar **saques** dentro de um limite estabelecido.
- Efetuar **depósitos** na conta.
- Exibir um **extrato detalhado** das transações, incluindo data e hora.
- Interface interativa via terminal com **menu dinâmico**, destacando a opção selecionada.
- **Cadastro de usuários** e **criação de contas correntes**.

## ⚙️ Regras de Negócio

1. 🏧 **Saque**:
   - O valor do saque deve ser positivo e não pode exceder o saldo disponível.
   - Existe um limite máximo de saque por transação.
   - O número de saques diários é limitado a três.

2. 💰 **Depósito**:
   - O valor do depósito deve ser positivo.

3. 📝 **Extrato**:
   - Exibe todas as transações realizadas, incluindo saques e depósitos, com data e hora.
   - Mostra o saldo atual da conta.

4. 📝 **Cadastro de Usuários**:
   - Permite cadastrar novos clientes com nome, CPF, data de nascimento e endereço.

5. 📝 **Criação de Contas Correntes**:
   - Permite criar contas correntes para clientes cadastrados.
   - Uma conta pertence a apenas um usuário, mas o usuário pode movimentar mais de uma conta.

## 🛠️ Tecnologias Utilizadas

- **Python** (versão 3.x)
- **Colorama** para destacar opções do menu
- **Datetime** para registrar data e hora das transações

## 📌 Estrutura do Código

### 🔹 Funções Principais

- `exibir_menu(opcao_selecionada=None)`: Exibe o menu principal do sistema bancário, destacando a opção selecionada.
- `sacar(valor)`: Realiza um saque da conta, verificando saldo disponível, limite de saque e número de saques diários.
- `depositar(valor)`: Realiza um depósito na conta, adicionando o valor ao saldo.
- `imprimir_extrato()`: Exibe o extrato da conta, listando todas as transações realizadas.
- `criar_usuario()`: Cadastra um novo cliente no sistema.
- `filtrar_cliente(cpf)`: Filtra e retorna um cliente pelo CPF.
- `criar_conta_corrente()`: Cria uma nova conta corrente para um cliente cadastrado.
- `iniciar()`: Inicia o loop principal do sistema bancário, permitindo ao usuário selecionar operações.

## 📌 Desafio

O desafio consiste em implementar um sistema bancário otimizado que permita ao usuário realizar operações básicas de saque, depósito e consulta de extrato,porém, agora iremos implementar funções. Nesse desafio optei deixar a interface mais interativa e fácil de usar, destacando a opção selecionada no menu. Além disso, o sistema deve permitir o cadastro de novos usuários e a criação de contas correntes.

## 📌 Relação entre `conta_bancaria-v1.py` e `conta_bancaria-v2.py`

A versão 2 (`conta_bancaria-v2.py`) é uma evolução da versão 1 (`conta_bancaria-v1.py`). As principais diferenças e melhorias incluem:

- **Interface de Usuário**: A versão 2 possui uma interface de menu mais dinâmica e interativa, utilizando a biblioteca `Colorama` para destacar as opções selecionadas.
- **Estrutura do Código**: A versão 2 organiza melhor o código, separando as funcionalidades em funções específicas (`sacar`, `depositar`, `imprimir_extrato`, `criar_usuario`, `criar_conta_corrente`).
- **Regras de Negócio**: A versão 2 implementa regras de negócio mais robustas, como limite de saques diários e verificação de saldo antes de realizar um saque.
- **Cadastro de Usuários e Contas**: A versão 2 adiciona funcionalidades para cadastrar novos usuários e criar contas correntes.
- **Documentação**: A versão 2 inclui documentação mais detalhada das funções e regras de negócio.

## 📌 Melhorias Futuras

- Implementação de **múltiplas contas**.
- Armazenamento das transações em um **banco de dados**.
- Interface gráfica para melhor experiência do usuário.

---
## 📄 Licença
Este projeto está sob a licença MIT. Sinta-se livre para modificá-lo e usá-lo conforme necessário.

<br><br><br><br><br>
🚀 Desenvolvido com 💙 por 𝒜𝓁𝒶𝓃𝒹𝑒𝓇𝓈𝑜𝓃 𝒯𝒶𝒹𝑒𝓊 𝒹𝑒 𝒫𝒶𝓊𝓁𝒶
