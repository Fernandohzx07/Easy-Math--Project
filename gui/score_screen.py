# gui/score_screen.py
import tkinter as tk
from PIL import Image, ImageTk
from jogo import LogicaJogo
from config import IMG_FUNDO_MENU


class ScoreScreen:
    def __init__(self, parent, controller):
        logic = LogicaJogo()
        recorde = logic.ler_recorde()

        # Correção: Adicionado "imagens"
        path_bg = controller.resolver_caminho("imagens", IMG_FUNDO_MENU)
        bg = Image.open(path_bg).resize((controller.largura, controller.altura), Image.NEAREST)
        self.bg_img = ImageTk.PhotoImage(bg)

        canvas = tk.Canvas(parent, width=controller.largura, height=controller.altura, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        canvas.create_text(controller.meio_w, controller.meio_h - 50, text="RECORD ATUAL",
                           font=(controller.fonte, 50), fill="#FFFF00")

        canvas.create_text(controller.meio_w, controller.meio_h + 50, text=f"{recorde} XP",
                           font=(controller.fonte, 80), fill="#00FF00")

        btn = tk.Button(parent, text="VOLTAR", font=(controller.fonte, 20), bg="black", fg="white",
                        command=controller.mostrar_menu)
        btn.place(relx=0.5, rely=0.8, anchor="center")