import os

from colorama import Fore, Style, init
from menu import exibir_menu

from conta_bancaria import ContaBancaria

init(autoreset=True)

# Criando uma instância da conta
conta = ContaBancaria()
exibir_menu()


def iniciar():
    """
    #### Inicia o loop principal do sistema bancário, permitindo ao usuário selecionar operações.
    """
    while True:
        opcao = input('Selecione uma operação: ')
        exibir_menu(opcao)

        if opcao == '1':
            try:
                valor = float(input('Valor do Saque: '))
                if conta.sacar(valor):
                    print(f"Saque de R$ {valor:.2f} realizado com sucesso!\n")
            except ValueError:
                print('Digite um valor vàlido')
                valor = float(input('Valor do Saque: '))
                if conta.sacar(valor):
                    print(f"Saque de R$ {valor:.2f} realizado com sucesso!\n")
        elif opcao == '2':
            try:
                valor = float(input('Informe o valor do depósito: '))
                # dep = conta.depositar(valor)
                if conta.depositar(valor):
                    print(f"Depósito de R$ {valor:.2f} realizado com sucesso!\n")
                else:
                    valor = float(input('Informe novamente o valor do depósito: '))
                    if conta.depositar(valor):
                        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!\n")
            except ValueError:
                print('Digite um valor vàlido')
                valor = float(input('Informe o valor do depósito: '))
                if conta.depositar(valor):
                    print(f"Depósito de R$ {valor:.2f} realizado com sucesso!\n")

        elif opcao == '3':
            conta.imprimir_extrato()
        elif opcao == '5':
            print("\n   Obrigado por usar o Banco D'Paula! Saindo...\n")
            break
        else:
            print("Opção inválida! Escolha novamente.\n")


if __name__ == "__main__":
    iniciar()
