import os
import time
from config import *

def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_abertura():
    """Exibe a abertura animada do jogo."""
    limpar_tela()
    boot_messages = ["Inicializando sistema Easy Math...", "Carregando Módulo de Gamificação...", "Verificando Banco de Questões...", "Tudo pronto!"]
    for msg in boot_messages:
        print(f"{COR_LETRA_AVISO}{msg}")
        time.sleep(0.7)
    time.sleep(1)
    limpar_tela()
    titulo_easy = "E A S Y"
    titulo_math = "M A T H"
    print("\n\n")
    print(" " * 15, end="")
    for char in titulo_easy:
        print(f"{COR_LETRA_TITULO}{char}", end="", flush=True)
        time.sleep(0.1)
    time.sleep(0.3)
    print(" ", end="")
    for char in titulo_math:
        print(f"{COR_CERTO_TEXTO}{char}", end="", flush=True)
        time.sleep(0.1)
    for _ in range(3):
        print(f"{Style.BRIGHT}_", end="", flush=True)
        time.sleep(0.3)
        print("\b ", end="", flush=True)
        time.sleep(0.3)
    print("\n\n")

def exibir_menu_principal():
    """Exibe o menu principal e retorna a escolha do jogador."""
    limpar_tela()
    print(f"{FUNDO_BLOCO_INFO}{' ' * 30}")
    print(f"{FUNDO_BLOCO_INFO}  {COR_LETRA_TITULO}EASY MATH - MENU PRINCIPAL{Style.RESET_ALL}{FUNDO_BLOCO_INFO}  ")
    print(f"{FUNDO_BLOCO_INFO}{' ' * 30}\n")
    print(f"{COR_LETRA_ALTERNATIVA_DESTAQUE}1){Style.RESET_ALL} Iniciar Novo Jogo")
    print(f"{COR_LETRA_ALTERNATIVA_DESTAQUE}2){Style.RESET_ALL} Ver Última Pontuação")
    print(f"{COR_LETRA_ALTERNATIVA_DESTAQUE}3){Style.RESET_ALL} Sair do Jogo")
    escolha = input(f"\n{COR_LETRA_INPUT}>> Digite sua escolha: ")
    return escolha

def ler_ultima_pontuacao():
    """Lê e exibe a última pontuação. Se não houver, oferece um novo jogo."""
    limpar_tela()
    try:
        with open(ARQUIVO_PONTUACAO, 'r') as f:
            ultima_pontuacao = f.read()
            print(f"{Back.YELLOW}{Fore.BLACK}{'~' * 30}")
            print(f"{Back.YELLOW}{Fore.BLACK}  HALL DA FAMA - ÚLTIMA JOGADA  ")
            print(f"{Back.YELLOW}{Fore.BLACK}{'~' * 30}\n")
            print(f"   Sua última pontuação foi: {COR_PONTOS}{ultima_pontuacao} PONTOS! ✨\n")
            input(f"{COR_LETRA_AVISO}Pressione Enter para voltar ao menu...")
            return None
    except FileNotFoundError:
        ### A CORREÇÃO ESTÁ AQUI! ###
        print(f"{COR_LETRA_AVISO}Você ainda não tem nenhuma pontuação registrada. Hora de jogar!\n")
        print(f"{COR_LETRA_ALTERNATIVA_DESTAQUE}1){Style.RESET_ALL} Iniciar um novo desafio agora!")
        print(f"{COR_LETRA_ALTERNATIVA_DESTAQUE}2){Style.RESET_ALL} Voltar ao menu principal")
        escolha = input(f"\n{COR_LETRA_INPUT}>> O que você quer fazer? ")
        return escolha