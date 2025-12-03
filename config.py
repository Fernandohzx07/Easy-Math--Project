# config.py
import os

# --- 1. CONFIGURAÇÕES DE JOGO ---
NIVEIS_CONFIG = {
    "facil":   {"tempo": 12, "cor": "#00FF00"},
    "medio":   {"tempo": 18, "cor": "#FFFF00"},
    "dificil": {"tempo": 30, "cor": "#FF0000"}
}

# --- 2. NOMES DOS ARQUIVOS (EXATAMENTE COMO NA SUA PASTA) ---
IMG_FUNDO_MENU = "fundo_menu.png"
IMG_FUNDO_JOGO = "fundo_jogo.png"

IMG_BTN_JOGAR = "btn_jogar.png"
IMG_BTN_RECORDE = "btn_recorde.png"
IMG_BTN_SAIR = "btn_sair.png"

IMG_BTN_POWERUP = "btn_ajuda.png"
IMG_FEEDBACK_ACERTO = "feedback_acerto.png"
IMG_FEEDBACK_ERRO = "feedback_erro.png"

# Os botões A, B, C, D são carregados automaticamente como btn_a.png, etc.

# --- 3. CONFIGURAÇÃO DA FONTE ---
NOME_FONTE = "04b03"