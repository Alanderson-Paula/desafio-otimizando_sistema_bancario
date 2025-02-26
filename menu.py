import os

from colorama import Back, Fore, Style, init

init(autoreset=True)


def exibir_menu(opcao_selecionada: str = None) -> None:
    """
    #### Exibe o menu principal do sistema bancário, destacando a opção selecionada.

    Esta função imprime no terminal um menu interativo, permitindo ao usuário visualizar
    as operações disponíveis no sistema bancário. Caso uma opção esteja selecionada,
    ela será destacada para melhor visualização.

    Parâmetros:
    ---
        opcao_selecionada: (str) Código da opção atualmente selecionada pelo usuário.
                               Se None, o menu será exibido sem destaques.
    """
    # os.system('cls' if os.name == 'nt' else 'clear')
    print('╔════════════════════════════════════════════════╗')
    print(F'║{Back.CYAN + Fore.BLACK + Style.BRIGHT}                BANCO D`PAULA                   {Style.RESET_ALL}║')
    # print('╠════════════════════════════════════════════════╣')
    print('║            Selecione uma Operação              ║')
    print('╠════════════════════╦═══════════════════════════╣')
    print(f'║ {(Fore.LIGHTGREEN_EX if opcao_selecionada == "1" else "")}{("✔" if opcao_selecionada == "1" else " ")} 1 - SAQUE{Style.RESET_ALL}        ║{(Fore.LIGHTGREEN_EX if opcao_selecionada == "6" else "")} {("✔" if opcao_selecionada == "6" else " ")} 6 - CADASTRAR CLIENTE{Style.RESET_ALL}   ║')

    print(f'║ {(Fore.LIGHTGREEN_EX if opcao_selecionada == "2" else "")}{("✔" if opcao_selecionada == "2" else " ")} 2 - DEPÓSITO{Style.RESET_ALL}     ║{(Fore.LIGHTGREEN_EX if opcao_selecionada == "7" else "")} {("✔" if opcao_selecionada == "7" else " ")} 7 - EXIBIR CLIENTE{Style.RESET_ALL}      ║')

    print(f'║ {(Fore.LIGHTGREEN_EX if opcao_selecionada == "3" else "")}{("✔" if opcao_selecionada == "3" else " ")} 3 - EXTRATO{Style.RESET_ALL}      ║{(Fore.LIGHTGREEN_EX if opcao_selecionada == "8" else "")} {("✔" if opcao_selecionada == "8" else " ")} 8 - ATUALIZAR CLIENTE{Style.RESET_ALL}   ║')

    print(f'║ {(Fore.LIGHTGREEN_EX if opcao_selecionada == "4" else "")}{("✔" if opcao_selecionada == "4" else " ")} 4 - CRIAR CONTA{Style.RESET_ALL}  ║{(Fore.LIGHTGREEN_EX if opcao_selecionada == "9" else "")} {("✔" if opcao_selecionada == "9" else " ")} 9 - EXCLUIR CLIENTE{Style.RESET_ALL}     ║')

    print(f'║ {(Fore.LIGHTRED_EX if opcao_selecionada == "5" else "")}{("✔" if opcao_selecionada == "5" else " ")} 5 - SAIR{Style.RESET_ALL}         ║{(Fore.LIGHTGREEN_EX if opcao_selecionada == "10" else "")} {("✔" if opcao_selecionada == "  " else " ")}                   {Style.RESET_ALL}      ║')

    print('╚════════════════════╩═══════════════════════════╝')
