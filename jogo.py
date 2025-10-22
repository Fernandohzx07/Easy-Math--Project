# jogo.py
import json
import random
import time
import threading
from config import *
from audio import tocar_efeito_sonoro
from interface import limpar_tela


def carregar_perguntas():
    # ...(sem mudanças)...
    try:
        with open('perguntas.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print(f"{FUNDO_BLOCO_ERRO}{Fore.WHITE} ERRO: 'perguntas.json' não encontrado! ")
        return []
    except json.JSONDecodeError:
        print(f"{FUNDO_BLOCO_ERRO}{Fore.WHITE} ERRO: 'perguntas.json' contém um erro! ")
        return []


def salvar_pontuacao(pontuacao):
    # ...(sem mudanças)...
    with open(ARQUIVO_PONTUACAO, 'w') as f:
        f.write(str(pontuacao))


def iniciar_nivel(todas_as_perguntas, nivel_escolhido, pontuacao_anterior, tempo_limite):
    """Gerencia a execução de um nível completo do jogo, agora com Power-Up 50/50!"""
    perguntas_do_nivel = [p for p in todas_as_perguntas if p['nivel'] == nivel_escolhido]
    random.shuffle(perguntas_do_nivel)

    pontuacao_nivel = 0
    total_de_perguntas = len(perguntas_do_nivel)
    ### NOVO: Controle do Power-Up ###
    power_up_disponivel = True

    for i, pergunta_atual in enumerate(perguntas_do_nivel):
        opcoes_atuais = list(pergunta_atual['opcoes'])  # Cria uma cópia para podermos modificar

        # Loop para redesenhar a tela caso o 50/50 seja usado
        while True:
            limpar_tela()
            pontuacao_atual_hud = pontuacao_anterior + pontuacao_nivel
            print(
                f"{FUNDO_BLOCO_INFO}{COR_LETRA_OPCAO_TEXTO} NÍVEL: {Style.BRIGHT}{nivel_escolhido.upper()}{Style.NORMAL} | PONTUAÇÃO: {COR_PONTOS}{pontuacao_atual_hud}{Style.RESET_ALL}{FUNDO_BLOCO_INFO} | PERGUNTA {i + 1}/{total_de_perguntas} ")

            ### NOVO: Exibe o status do Power-Up ###
            if power_up_disponivel:
                print(f"{FUNDO_BLOCO_CERTO} POWER-UP 50/50 DISPONÍVEL! Digite '50' para usar! ")
            else:
                print(f"{FUNDO_BLOCO_ERRO} POWER-UP 50/50 JÁ USADO NESTE NÍVEL! ")

            print()
            print(f"{COR_LETRA_PERGUNTA_DESTAQUE}>> {pergunta_atual['pergunta']}")
            print()

            mapa_opcoes = {}
            letras = "abcd"
            for j, opcao in enumerate(opcoes_atuais):
                letra_opcao = letras[j]
                mapa_opcoes[letra_opcao] = opcao
                print(
                    f"  {COR_LETRA_ALTERNATIVA_DESTAQUE}{letra_opcao}){Style.RESET_ALL} {COR_LETRA_OPCAO_TEXTO}{opcao}")

            print()
            resposta_container = []

            def obter_input():
                resposta = input().lower()
                if resposta:
                    resposta_container.append(resposta)

            thread_input = threading.Thread(target=obter_input)
            thread_input.daemon = True
            thread_input.start()

            tempo_restante = tempo_limite
            while tempo_restante >= 0 and not resposta_container:
                prompt_line = f" {COR_TEMPO}Tempo: {tempo_restante:02d}s{Style.RESET_ALL} {COR_LETRA_INPUT}| Digite sua resposta ou '50' para ajuda: "
                print(f"\r{prompt_line}", end="")
                if tempo_restante == 0: break
                time.sleep(1)
                tempo_restante -= 1

            # Sai do loop principal se o jogador respondeu ou o tempo acabou
            if resposta_container:
                resposta_usuario = resposta_container[0]
                ### NOVO: Lógica para ativar o 50/50 ###
                if resposta_usuario == '50' and power_up_disponivel:
                    power_up_disponivel = False
                    tocar_efeito_sonoro('levelup')  # Som de power-up!

                    resposta_correta = pergunta_atual['resposta_correta']
                    # Pega todas as opções incorretas
                    opcoes_incorretas = [opt for opt in opcoes_atuais if opt != resposta_correta]
                    # Embaralha e escolhe uma para manter
                    random.shuffle(opcoes_incorretas)
                    opcao_mantida = opcoes_incorretas[0]

                    # Atualiza a lista de opções para ter apenas a correta e uma incorreta
                    opcoes_atuais = [resposta_correta, opcao_mantida]
                    random.shuffle(opcoes_atuais)  # Embaralha as duas restantes

                    # Continua o loop para redesenhar a tela com as novas opções
                    continue
                else:
                    break  # Sai do loop para validar a resposta
            else:
                break  # Sai do loop se o tempo acabou

        # O resto da lógica de validação continua aqui...
        print("\n" * 2)
        limpar_tela()
        pontuacao_atual_hud = pontuacao_anterior + pontuacao_nivel
        print(
            f"{FUNDO_BLOCO_INFO}{COR_LETRA_OPCAO_TEXTO} NÍVEL: {Style.BRIGHT}{nivel_escolhido.upper()}{Style.NORMAL} | PONTUAÇÃO: {COR_PONTOS}{pontuacao_atual_hud}{Style.RESET_ALL}{FUNDO_BLOCO_INFO} | RESULTADO DA PERGUNTA {i + 1} ")
        print()

        if resposta_container:
            resposta_usuario = resposta_container[0]
            if resposta_usuario in mapa_opcoes:
                opcao_escolhida = mapa_opcoes[resposta_usuario]
                if opcao_escolhida == pergunta_atual['resposta_correta']:
                    pontuacao_nivel += 10
                    tocar_efeito_sonoro('correct')
                    print(f"{FUNDO_BLOCO_CERTO}{Fore.WHITE} ISSO! RESPOSTA CORRETA! +{COR_PONTOS}10 PONTOS 🔥 ")
                else:
                    tocar_efeito_sonoro('error')
                    print(
                        f"{FUNDO_BLOCO_ERRO}{Fore.WHITE} QUASE! A resposta certa era '{COR_LETRA_ALTERNATIVA_DESTAQUE}{pergunta_atual['resposta_correta']}'. ")
            elif resposta_usuario == '50' and not power_up_disponivel:
                tocar_efeito_sonoro('error')
                print(f"{FUNDO_BLOCO_ERRO}{Fore.WHITE} POWER-UP JÁ USADO! Você precisa responder! ")
            else:
                tocar_efeito_sonoro('error')
                print(f"{FUNDO_BLOCO_ERRO}{Fore.WHITE} '{resposta_usuario}' não vale! Lembre-se: a, b, c ou d. ")
        else:
            tocar_efeito_sonoro('error')
            print(
                f"{FUNDO_BLOCO_ERRO}{Fore.WHITE} ZEROU O CRONÔMETRO! ⏰ A resposta era '{pergunta_atual['resposta_correta']}'. ")
        time.sleep(3)
    return pontuacao_nivel


def iniciar_jornada(banco_de_perguntas):
    # ...(sem mudanças)...
    pontuacao_total = 0
    for nivel_atual in NIVEIS_DA_JORNADA:
        tempo_do_nivel = TEMPOS_POR_NIVEL[nivel_atual]
        pontos_ganhos = iniciar_nivel(banco_de_perguntas, nivel_atual, pontuacao_total, tempo_do_nivel)
        pontuacao_total += pontos_ganhos
        if nivel_atual != NIVEIS_DA_JORNADA[-1]:
            limpar_tela()
            tocar_efeito_sonoro('levelup')
            print(f"{FUNDO_BLOCO_CERTO}{'=' * 47}")
            print(f"{FUNDO_BLOCO_CERTO}{Fore.WHITE}  MANDOU BEM DEMAIS! {COR_LETRA_TITULO}LEVEL UP! 🚀        ")
            print(f"{FUNDO_BLOCO_CERTO}{Fore.WHITE}  Sua pontuação agora é: {COR_PONTOS}{pontuacao_total}           ")
            print(f"{FUNDO_BLOCO_CERTO}{'=' * 47}")
            time.sleep(4)
    limpar_tela()
    salvar_pontuacao(pontuacao_total)
    if pontuacao_total >= 270:
        tocar_efeito_sonoro('levelup')
        print(f"{Back.CYAN}{Fore.WHITE}{'*' * 60}")
        print(f"{Back.CYAN}{Fore.YELLOW + Style.BRIGHT}** NÍVEL LENDÁRIO ATINGIDO! VOCÊ É IMBATÍVEL! 👑    **")
        print(
            f"{Back.CYAN}{Fore.WHITE}** PONTUAÇÃO FINAL: {Back.WHITE + Fore.BLACK} {pontuacao_total} PONTOS! {Style.RESET_ALL}{Back.CYAN} **")
        print(f"{Back.CYAN}{Fore.WHITE}{'*' * 60}")
    elif pontuacao_total >= 200:
        tocar_efeito_sonoro('levelup')
        print(f"{Back.GREEN}{Fore.WHITE}{'#' * 55}")
        print(f"{Back.GREEN}{Fore.YELLOW + Style.BRIGHT}##     VOCÊ É UM MONSTRO DA MATEMÁTICA! BRABO! 🔥     ##")
        print(
            f"{Back.GREEN}{Fore.WHITE}##     PONTUAÇÃO FINAL: {Back.WHITE + Fore.BLACK} {pontuacao_total} PONTOS! {Style.RESET_ALL}{Back.GREEN} ##")
        print(f"{Back.GREEN}{Fore.WHITE}{'#' * 55}")
    elif pontuacao_total > 100:
        tocar_efeito_sonoro('levelup')
        print(f"{Back.YELLOW}{Fore.BLACK}{'~' * 55}")
        print(f"{Back.YELLOW}{Fore.BLACK}~~     MANDOU BEM DEMAIS! TÁ VIRANDO MESTRE! ✨      ~~")
        print(
            f"{Back.YELLOW}{Fore.BLACK}~~     PONTUAÇÃO FINAL: {Back.BLACK + Fore.WHITE} {pontuacao_total} PONTOS! {Style.RESET_ALL}{Back.YELLOW} ~~")
        print(f"{Back.YELLOW}{Fore.BLACK}{'~' * 55}")
    else:
        tocar_efeito_sonoro('error')
        print(f"{Back.BLUE}{Fore.WHITE}{'-' * 60}")
        print(f"{Back.BLUE}{Fore.WHITE}--   BOA TENTATIVA! CADA ERRO É UM PASSO PRA VITÓRIA! 🚀   --")
        print(
            f"{Back.BLUE}{Fore.WHITE}--   PONTUAÇÃO FINAL: {Back.WHITE + Fore.BLACK} {pontuacao_total} PONTOS! {Style.RESET_ALL}{Back.BLUE} --")
        print(f"{Back.BLUE}{Fore.WHITE}--   Continue treinando, você chega lá! 🎮                    --")
        print(f"{Back.BLUE}{Fore.WHITE}{'-' * 60}")