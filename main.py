import os
import sys

from decoradores import emitir_mensagem
from menu import exibir_menu

from conta_bancaria import ContaBancaria

AGENCIA = '0001'
banco = ContaBancaria()
exibir_menu()


def obter_valor_float(mensagem):
    """
    #### Solicita ao usuário um valor numérico e garante que seja um número válido.

    Parâmetros:
    ---
        mensagem (str): Mensagem a ser exibida ao solicitar a entrada do usuário.

    Retorna:
    ---
        float: O valor inserido pelo usuário.
    """
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print(emitir_mensagem(('Aviso', 'Digite um valor válido.')))


def sair():
    """
    #### Encerra a execução do sistema bancário.

    Retorna:
    ---
        None: A função encerra a execução do programa.
    """
    print("\n🔹 Obrigado por usar o Banco D'Paula! Saindo...\n")
    sys.exit()


def iniciar():
    """
    #### Executa o loop principal do sistema bancário, permitindo ao usuário realizar operações.

    O sistema apresenta um menu interativo onde o usuário pode selecionar diferentes operações
    bancárias, como saque, depósito, impressão de extrato, criação de conta, gerenciamento
    de clientes e saída do sistema.

    Retorna:
    ---
        None: A função opera em um loop contínuo até que o usuário selecione a opção de saída.
    """
    opcoes = {
        '1': lambda: banco.sacar(valor=obter_valor_float('Valor do Saque: ')),
        '2': lambda: banco.depositar(obter_valor_float('Informe o valor do depósito: ')),
        '3': banco.imprimir_extrato,
        '4': lambda: banco.criar_conta(AGENCIA, input('Digite (C) para conta corrente ou (P) para conta poupança: ')),
        # '5': lambda: (print("\n🔹 Obrigado por usar o Banco D'Paula! Saindo...\n"), sys.exit())[1],
        '5': sair,
        '6': banco.cadastrar_cliente,
        '7': banco.exibir_cliente,
        '8': banco.atualizar_cliente,
        '9': banco.excluir_cliente
    }

    while True:
        opcao = input('Selecione uma operação: ')
        exibir_menu(opcao)

        if opcao in opcoes:
            resultado = opcoes[opcao]()
            if isinstance(resultado, bool) and resultado:
                print("Operação realizada com sucesso!\n")
        else:
            print(emitir_mensagem(("Alerta", "Opção inválida! Escolha novamente.")))


if __name__ == "__main__":
    iniciar()
