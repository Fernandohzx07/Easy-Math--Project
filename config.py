import colorama
from colorama import Fore, Back, Style

# --- PALETA DE CORES "EDIÇÃO DE COLECIONADOR" ---
colorama.init(autoreset=True)

# Cores de Letra
COR_LETRA_TITULO = Fore.YELLOW + Style.BRIGHT
COR_LETRA_PERGUNTA_DESTAQUE = Fore.MAGENTA + Style.BRIGHT
COR_LETRA_OPCAO_TEXTO = Fore.WHITE
COR_LETRA_ALTERNATIVA_DESTAQUE = Fore.YELLOW + Style.BRIGHT
COR_LETRA_INPUT = Fore.YELLOW
COR_LETRA_AVISO = Fore.LIGHTBLACK_EX

# Cores de Bloco (Fundo)
FUNDO_BLOCO_INFO = Back.MAGENTA
FUNDO_BLOCO_CERTO = Back.GREEN
FUNDO_BLOCO_ERRO = Back.RED

# Cores de Status Específicas
COR_PONTOS = Fore.YELLOW + Style.BRIGHT
COR_TEMPO = Fore.CYAN + Style.BRIGHT
COR_CERTO_TEXTO = Fore.GREEN + Style.BRIGHT
COR_ERRO_TEXTO = Fore.RED + Style.BRIGHT #

# --- CONFIGURAÇÕES DO JOGO ---
NIVEIS_DA_JORNADA = ["facil", "medio", "dificil"]
TEMPOS_POR_NIVEL = {"facil": 20, "medio": 15, "dificil": 7}
ARQUIVO_PONTUACAO = "pontuacao.txt"