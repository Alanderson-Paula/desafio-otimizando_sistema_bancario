from datetime import datetime

from colorama import Fore, Style, init

init(autoreset=True)


class ContaBancaria:
    """
    #### Representa uma conta bancária simples com funcionalidades básicas de saque, depósito e extrato.
    """

    def __init__(self, saldo=0.0, limite=500, limite_saques=3):
        """
        #### Inicializa a conta bancária com um saldo inicial, limite de saque e número máximo de saques permitidos.

        :param saldo: (float) Saldo inicial da conta.
        :param limite: (float) Limite máximo para cada saque.
        :param limite_saques: (int) Número máximo de saques permitidos por dia.
        """
        self.saldo = saldo
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0
        self.extrato = []

    def sacar(self, valor):
        """
        #### Realiza um saque da conta, verificando saldo disponível, limite de saque e número de saques diários.

        :param valor: (float) Valor a ser sacado.
        :return: (bool) True se o saque foi bem-sucedido, False caso contrário.
        """
        if valor <= 0.0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        if valor and self.saldo == 0.0:
            print(
                'Necessário realizar depósito, saldo em conta igual a R$ 0.0. Utilize a opção 2.')
            return False
        if valor > self.saldo:
            print(
                f"Você não tem saldo suficiente. Saldo atual  em conta R$ {self.saldo:.2f}.")
            return False
        if valor > self.limite:
            print(
                f"Operação falhou! O valor do saque excede o limite de R$ {self.limite:.2f}.")
            return False
        if self.numero_saques >= self.limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False

        self.saldo -= valor
        self.extrato.append(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + Fore.RED + " <= " + Style.RESET_ALL + f"Saque:    R$ {valor:.2f}")
        self.numero_saques += 1
        return True

    def depositar(self, valor):
        """
        #### Realiza um depósito na conta, adicionando o valor ao saldo.

        :param valor: (float) Valor a ser depositado.
        """
        if valor > 0:
            self.saldo += valor
            self.extrato.append(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + Fore.GREEN + " => " + Style.RESET_ALL + f"Depósito: R$ {valor:.2f}")
        else:
            print("Operação falhou! O valor informado é inválido.")
            return None

    def imprimir_extrato(self):
        """
        Exibe o extrato da conta, listando todas as transações realizadas.
        """
        print("\n================ EXTRATO ================\n")
        if not self.extrato:
            print("Não foram realizadas movimentações.")
        else:
            print("\n".join(self.extrato))
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("==========================================\n")
