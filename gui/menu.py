import tkinter as tk
from PIL import Image, ImageTk
from config import *


class MenuScreen:
    def __init__(self, parent, controller):
        self.controller = controller

        # --- FUNDO (Estica para o tamanho do monitor) ---
        path_bg = controller.resolver_caminho("imagens", IMG_FUNDO_MENU)
        pil_bg = Image.open(path_bg)
        pil_bg = pil_bg.resize((controller.largura, controller.altura), Image.NEAREST)
        self.bg_img = ImageTk.PhotoImage(pil_bg)

        canvas = tk.Canvas(parent, width=controller.largura, height=controller.altura, highlightthickness=0, bg="black")
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        # --- BOTÕES ---
        self.imgs = {}
        for nome, arquivo in [("jogar", IMG_BTN_JOGAR), ("rec", IMG_BTN_RECORDE), ("sair", IMG_BTN_SAIR)]:
            path = controller.resolver_caminho("imagens", arquivo)
            self.imgs[nome] = ImageTk.PhotoImage(Image.open(path))

        # Posições Relativas (Funcionam em qualquer tela)
        btn_j = tk.Button(parent, image=self.imgs["jogar"], bg="black", bd=0, activebackground="black",
                          command=controller.iniciar_jogo)
        btn_j.place(relx=0.5, rely=0.45, anchor="center")

        btn_r = tk.Button(parent, image=self.imgs["rec"], bg="black", bd=0, activebackground="black",
                          command=controller.mostrar_recorde)
        btn_r.place(relx=0.5, rely=0.60, anchor="center")

        btn_s = tk.Button(parent, image=self.imgs["sair"], bg="black", bd=0, activebackground="black",
                          command=controller.sair)
        btn_s.place(relx=0.5, rely=0.75, anchor="center")