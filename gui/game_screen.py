import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from jogo import LogicaJogo
from config import *


class GameScreen:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.logic = LogicaJogo()

        self.niveis = ["facil", "medio", "dificil"]
        self.nivel_idx = 0
        self.perguntas_atuais = []
        self.idx_pergunta = 0
        self.tempo_restante = 0
        self.timer_id = None
        self.power_up_ativo = True
        self.botoes_opcoes = []

        self.cores_neon = ["#FF00FF", "#00FFFF", "#FFFF00", "#00FF00", "#FF0000", "#FFA500"]

        self.carregar_imagens()

        self.canvas = tk.Canvas(parent, width=controller.largura, height=controller.altura,
                                highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_jogo, anchor="nw")

        # --- LAYOUT FINAL (AJUSTE FINO) ---

        # 1. XP (Topo Direito)
        self.lbl_xp = tk.Label(parent, text="XP: 0", font=(controller.fonte, 22), bg="black", fg="white")
        self.lbl_xp.place(x=controller.largura - 250, y=40, anchor="nw")

        # 2. NÍVEL (Centro)
        self.lbl_nivel = tk.Label(parent, text="", font=(controller.fonte, 30), bg="black")
        self.lbl_nivel.place(x=controller.meio_w, y=80, anchor="center")

        # 3. PILHA ESQUERDA (Tempo e PowerUp)
        # AJUSTE: Desci para -110 (Fica mais perto do chão, mas seguro)
        pos_y_base = controller.altura - 110

        # Barra
        self.lbl_tempo_bar = tk.Label(parent, text="", font=(controller.fonte, 20), bg="black")
        self.lbl_tempo_bar.place(x=50, y=pos_y_base, anchor="w")

        # Número (40px acima da barra)
        self.lbl_tempo_num = tk.Label(parent, text="", font=(controller.fonte, 30), bg="black", fg="white")
        self.lbl_tempo_num.place(x=50, y=pos_y_base - 40, anchor="w")

        # Botão PowerUP (120px acima da base)
        self.btn_ajuda = tk.Button(parent, image=self.img_ajuda, bg="black", bd=0, activebackground="black",
                                   command=self.usar_powerup)
        self.btn_ajuda.place(x=50, y=pos_y_base - 120, anchor="w")

        self.iniciar_nivel()

    def carregar_imagens(self):
        # Garante que o fundo usa o tamanho TOTAL da tela
        w, h = self.controller.largura, self.controller.altura
        resolver = self.controller.resolver_caminho

        bg = Image.open(resolver("imagens", IMG_FUNDO_JOGO)).resize((w, h), Image.NEAREST)
        self.bg_jogo = ImageTk.PhotoImage(bg)

        self.icones = [ImageTk.PhotoImage(Image.open(resolver("imagens", f"btn_{l}.png"))) for l in
                       ['a', 'b', 'c', 'd']]

        acerto = Image.open(resolver("imagens", IMG_FEEDBACK_ACERTO))
        self.img_acerto = ImageTk.PhotoImage(acerto.resize((acerto.width * 2, acerto.height * 2), Image.NEAREST))

        erro = Image.open(resolver("imagens", IMG_FEEDBACK_ERRO))
        self.img_erro = ImageTk.PhotoImage(erro.resize((erro.width * 2, erro.height * 2), Image.NEAREST))

        try:
            self.img_ajuda = ImageTk.PhotoImage(Image.open(resolver("imagens", IMG_BTN_POWERUP)))
        except:
            self.img_ajuda = self.icones[0]

    def iniciar_nivel(self):
        if self.nivel_idx >= len(self.niveis):
            self.logic.salvar_recorde()
            self.controller.dj.tocar_sfx("levelup")
            messagebox.showinfo("VITORIA", f"VOCÊ ZEROU O EASY MATH!\nPONTUAÇÃO: {self.logic.pontuacao}")
            self.controller.mostrar_menu()
            return

        nivel = self.niveis[self.nivel_idx]
        self.tempo_max = NIVEIS_CONFIG[nivel]["tempo"]
        self.perguntas_atuais = self.logic.filtrar_perguntas(nivel)
        self.idx_pergunta = 0
        self.power_up_ativo = True

        self.animar_nivel_texto(nivel.upper(), NIVEIS_CONFIG[nivel]["cor"])

    def animar_nivel_texto(self, texto, cor, count=0):
        if count < 6:
            txt = texto if count % 2 == 0 else ""
            self.lbl_nivel.config(text=txt, fg=cor)
            self.parent.after(300, lambda: self.animar_nivel_texto(texto, cor, count + 1))
        else:
            self.lbl_nivel.config(text="")
            self.controller.dj.tocar_sfx("levelup")
            self.mostrar_proxima_pergunta()

    def mostrar_proxima_pergunta(self):
        if self.idx_pergunta >= len(self.perguntas_atuais):
            self.nivel_idx += 1
            self.iniciar_nivel()
            return

        if self.power_up_ativo:
            # Atualiza a posição aqui também!
            self.btn_ajuda.place(x=50, y=(self.controller.altura - 110) - 120, anchor="w")
        else:
            self.btn_ajuda.place_forget()

        q = self.perguntas_atuais[self.idx_pergunta]

        for btn, _ in self.botoes_opcoes: btn.destroy()
        self.botoes_opcoes = []

        self.canvas.delete("texto_pergunta")
        self.canvas.create_text(self.controller.meio_w, self.controller.altura * 0.25,
                                text=q['pergunta'], font=(self.controller.fonte, 28), fill="white",
                                width=int(self.controller.largura * 0.8), justify="center", tag="texto_pergunta")

        opcoes = q['opcoes'].copy()
        random.shuffle(opcoes)

        start_y = self.controller.altura * 0.45
        for i, op in enumerate(opcoes):
            w_btn = int(self.controller.largura * 0.4)
            btn = tk.Button(self.parent, image=self.icones[i], text=f"  {op}",
                            font=(self.controller.fonte, 22), bg="black", fg="white", bd=0,
                            activebackground="#333", activeforeground="white", compound="left",
                            anchor="w", width=w_btn,
                            command=lambda o=op: self.verificar(o, q['resposta_correta']))

            btn.place(x=self.controller.meio_w, y=start_y + (i * (self.controller.altura * 0.12)), anchor="center")
            self.botoes_opcoes.append((btn, op))

        cor_nova = random.choice(self.cores_neon)
        self.lbl_xp.config(text=f"XP: {self.logic.pontuacao}", fg=cor_nova)

        self.tempo_restante = self.tempo_max
        self.atualizar_timer()

    def atualizar_timer(self):
        if self.timer_id: self.parent.after_cancel(self.timer_id)
        try:
            if not self.lbl_tempo_num.winfo_exists(): return
        except:
            return

        if self.tempo_restante >= 0:
            color = "#00FF00"
            if self.tempo_restante < 5:
                color = "#FF0000"
            elif self.tempo_restante < 10:
                color = "#FFFF00"

            self.lbl_tempo_bar.config(text="█ " * self.tempo_restante, fg=color)
            self.lbl_tempo_num.config(text=f"{self.tempo_restante}", fg="white")

            self.tempo_restante -= 1
            self.timer_id = self.parent.after(1000, self.atualizar_timer)
        else:
            self.verificar("TEMPO_ESGOTADO", "RESPOSTA_QUALQUER")

    def verificar(self, escolha, correta):
        if self.timer_id: self.parent.after_cancel(self.timer_id)

        acertou = (escolha == correta)
        if acertou:
            self.logic.pontuacao += 10
            img = self.img_acerto
            self.controller.dj.tocar_sfx("correct")
        else:
            img = self.img_erro
            self.controller.dj.tocar_sfx("error")

        self.top_feedback = tk.Toplevel(self.parent)
        try:
            self.top_feedback.state('zoomed')
        except:
            self.top_feedback.attributes('-zoomed', True)
        self.top_feedback.attributes("-alpha", 0.9)
        self.top_feedback.configure(bg="black")
        self.top_feedback.overrideredirect(True)

        lbl = tk.Label(self.top_feedback, image=img, bg="black")
        lbl.pack(expand=True)

        self.animar_feedback(0)

    def animar_feedback(self, step):
        try:
            if not self.top_feedback.winfo_exists(): return
        except:
            return

        if step < 6:
            alpha = 1.0 if step % 2 == 0 else 0.0
            self.top_feedback.attributes("-alpha", alpha)
            self.parent.after(150, lambda: self.animar_feedback(step + 1))
        else:
            self.top_feedback.destroy()
            self.idx_pergunta += 1
            self.mostrar_proxima_pergunta()

    def usar_powerup(self):
        self.power_up_ativo = False
        self.btn_ajuda.place_forget()
        self.controller.dj.tocar_sfx("levelup")

        q = self.perguntas_atuais[self.idx_pergunta]
        correta = q['resposta_correta']
        errados = [btn for btn, txt in self.botoes_opcoes if txt != correta]
        if len(errados) >= 2:
            for b in random.sample(errados, 2): b.destroy()