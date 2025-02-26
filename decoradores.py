from datetime import datetime
from functools import wraps

from colorama import Fore, Style, init

init(autoreset=True)


def log_transacao(func):
    """
    #### Um decorador para registrar a execução de uma função com um timestamp,
    #### mas apenas se a função retornar True.

    Este decorador imprime a data e hora atuais no formato `DD/MM/AAAA HH:MM:SS`,
    seguidas do nome da função formatado com espaços e capitalizado.

    Parâmetros:
    ---
        func (callable): A função a ser decorada.

    Retorna:
    ---
        callable: Uma função envelope que executa a função original e registra a transação.

    Exemplo:
    ---

        >>> @log_transacao
        ... def minha_funcao():
        ...     return "Executando..."
        ...
        >>> minha_funcao()
        24/02/2025 14:30:00: Minha Funcao
        ────────────────────────────────────────────────────
        'Executando...'
    """
    @wraps(func)
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        if resultado:
            print(
                f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: {func.__name__.replace("_", " ").title()}')
            print('─' * 50)
            print('\n')
        # return resultado  # Retorna o valor original da função

    return envelope


def mens_alertas(func):
    """
    #### Um decorador para formatar mensagens de alerta com base no tipo de comando.

    A função decorada deve receber uma tupla `(comando, mensagem)`, onde `comando`
    define o tipo de alerta e `mensagem` é o texto a ser exibido.

    Cores atribuídas:
        - "Alerta": Mensagem amarela, ícone vermelho.
        - "Aviso": Mensagem verde, ícone vermelho.
        - "Erro": Mensagem vermelha, ícone amarelo.
        - Outros comandos: Sem formatação especial.

    Parâmetros:
    ---
        func (callable): A função a ser decorada.

    Retorna:
    ---
        callable: Uma função envelope que aplica a formatação de cor à mensagem.

    Exemplo:
    ---

        >>> @mens_alertas
        ... def emitir_mensagem(msg):
        ...     return msg
        ...
        >>> print(emitir_mensagem(("Aviso", "Processo concluído com sucesso!")))
        ⚠  Processo concluído com sucesso!
    """
    @wraps(func)
    def envelope(*args):
        comando, mensagem = args[0]
        # Definindo cores com base no comando
        if comando == "Alerta":
            var1, var2 = Fore.YELLOW, Fore.RED
        elif comando == "Aviso":
            var1, var2 = Fore.GREEN, Fore.RED
        elif comando == "Erro":
            var1, var2 = Fore.RED, Fore.YELLOW
        else:
            var1, var2 = Fore.BLACK, Fore.BLACK

        resultado = f"\n{var1}⚠  {var2}{mensagem}{Style.RESET_ALL}\n"
        return resultado
    return envelope


@mens_alertas
def emitir_mensagem(*args):
    """
    #### Retorna a mensagem recebida sem modificações.

    Esta função serve como um intermediário para processar ou formatar mensagens
    quando utilizada em conjunto com decoradores, como `@mens_alertas`.

    Parâmetros:
    ---
        *args (tuple): A mensagem a ser retornada. Uma tupla contendo um comando e uma mensagem para formatação adicional.

    Retorna:
    ---
        str: A mensagem original sem alterações.

    Exemplo:

        >>> emitir_mensagem("Sistema iniciado com sucesso.")
        'Sistema iniciado com sucesso.'

        >>> emitir_mensagem(("aviso", "Operação concluída."))
        ('aviso', 'Operação concluída.')

    """
    return args
