import os

from colorama import Fore, Style, init

init(autoreset=True)


def exibir_menu(opcao_selecionada=None):
    """
    #### Exibe o menu principal do sistema bancário, destacando a opção selecionada.

    :param opcao_selecionada: (str) Opção atualmente selecionada pelo usuário.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print('╔═════════════════════════════════════════════╗')
    print('║               BANCO D`PAULA                 ║')
    print('╚═════════════════════════════════════════════╝')
    print('╔═════════════════════════════════════════════╗')
    print('║        Selecione uma operação no menu       ║')
    print('╠═════════════════════════════════════════════╣')
    print(f'║ {(Fore.GREEN if opcao_selecionada == "1" else "")} {("✔" if opcao_selecionada == "1" else " ")}        1 - SAQUE{Style.RESET_ALL}                         ║')
    print(f'║ {(Fore.GREEN if opcao_selecionada == "2" else "")} {("✔" if opcao_selecionada == "2" else " ")}        2 - DEPÓSITO{Style.RESET_ALL}                      ║')
    print(f'║ {(Fore.GREEN if opcao_selecionada == "3" else "")} {("✔" if opcao_selecionada == "3" else " ")}        3 - EXTRATO{Style.RESET_ALL}                       ║')
    print(f'║ {(Fore.RED if opcao_selecionada == "4" else "")} {("✔" if opcao_selecionada == "4" else " ")}        4 - SAIR{Style.RESET_ALL}                          ║')
    print('╚═════════════════════════════════════════════╝')
