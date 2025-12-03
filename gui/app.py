import tkinter as tk
from tkinter import messagebox
import pyglet
import os
import sys
import ctypes  # <--- NOVA BIBLIOTECA DO WINDOWS

from gui.menu import MenuScreen
from gui.game_screen import GameScreen
from gui.score_screen import ScoreScreen
from audio import DJ
from config import NOME_FONTE


class EasyMathApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- 1. CORREÇÃO DE ESCALA (DPI FIX) ---
        # Isso diz ao Windows: "Não dê zoom no meu app, use a resolução real!"
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

        self.title("Easy Math - Final Edition")
        self.configure(bg="black")

        # --- 2. MAXIMIZAÇÃO IMEDIATA ---
        # Tenta o estado 'zoomed' (Padrão Windows)
        try:
            self.state('zoomed')
        except:
            self.attributes('-zoomed', True)

        # --- 3. FORÇA O UPDATE ---
        # Obriga o Tkinter a processar a maximização ANTES de medir o tamanho
        self.update_idletasks()
        self.update()

        # --- 4. AGORA PEGA O TAMANHO REAL ---
        self.largura = self.winfo_width()
        self.altura = self.winfo_height()

        self.meio_w = self.largura // 2
        self.meio_h = self.altura // 2

        # --- PATH FIX ---
        if getattr(sys, 'frozen', False):
            self.base_dir = sys._MEIPASS
        else:
            self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        self.carregar_fonte_customizada()

        self.dj = DJ()
        self.dj.iniciar_musica_fundo()

        self.container = tk.Frame(self, bg="black")
        self.container.pack(fill="both", expand=True)

        self.tela_atual = None
        self.mostrar_menu()

        self.protocol("WM_DELETE_WINDOW", self.sair)

    def resolver_caminho(self, pasta, arquivo):
        return os.path.join(self.base_dir, pasta, arquivo)

    def carregar_fonte_customizada(self):
        path = self.resolver_caminho('imagens', '04B_03__.TTF')
        try:
            pyglet.font.add_file(path)
            self.fonte = NOME_FONTE
        except:
            self.fonte = "Courier"

    def limpar_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_menu(self):
        self.limpar_container()
        self.tela_atual = MenuScreen(self.container, self)

    def iniciar_jogo(self):
        self.limpar_container()
        self.tela_atual = GameScreen(self.container, self)

    def mostrar_recorde(self):
        self.limpar_container()
        self.tela_atual = ScoreScreen(self.container, self)

    def sair(self):
        self.dj.parar_musica()
        self.destroy()