import threading
import time
from audio import tocar_musica_base, musica_de_fundo_tocando
from interface import exibir_abertura, exibir_menu_principal, ler_ultima_pontuacao
from jogo import carregar_perguntas, iniciar_jornada
from config import *


def main():
    """Função principal que controla o fluxo do jogo."""
    exibir_abertura()
    banco_de_perguntas = carregar_perguntas()

    if not banco_de_perguntas:
        input(f"\n{COR_LETRA_AVISO}O jogo não pôde iniciar. Verifique as mensagens de erro.")
        return

    thread_musica = threading.Thread(target=tocar_musica_base, daemon=True)
    thread_musica.start()

    while True:
        escolha = exibir_menu_principal()

        if escolha == '1':
            iniciar_jornada(banco_de_perguntas)
            input(f"\n{COR_LETRA_AVISO}Jornada finalizada! Pressione Enter para voltar ao menu...")

        elif escolha == '2':
            escolha_secundaria = ler_ultima_pontuacao()
            if escolha_secundaria == '1':
                iniciar_jornada(banco_de_perguntas)
                input(f"\n{COR_LETRA_AVISO}Jornada finalizada! Pressione Enter para voltar ao menu...")

        elif escolha == '3':
            print(f"\n{COR_LETRA_TITULO}Obrigado por jogar! Até a próxima! 👋")
            global musica_de_fundo_tocando
            musica_de_fundo_tocando = False
            break

        else:
            # AGORA ESTA LINHA VAI FUNCIONAR PERFEITAMENTE!
            print(f"\n{COR_ERRO_TEXTO}Opção inválida! Por favor, digite 1, 2 ou 3.")
            time.sleep(2)


if __name__ == "__main__":
    main()