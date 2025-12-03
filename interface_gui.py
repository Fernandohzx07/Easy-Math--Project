import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import random
import pyglet
import os
import threading
from playsound import playsound


class EasyMathGUI:
    def __init__(self):
        # --- CONFIGURAÇÕES INICIAIS ---
        self.root = tk.Tk()
        self.root.title("Easy Math - Edição 8-Bits")
        self.root.configure(bg="black")

        # Tenta carregar a fonte
        try:
            pyglet.font.add_file('imagens/04B_03__.TTF')
            self.fonte_retro = "04b03"
        except:
            print("Aviso: Fonte padrão usada.")
            self.fonte_retro = "Courier"

        # --- MODO MAXIMIZADO SEGURO ---
        # Maximiza a janela e ATUALIZA O SISTEMA para pegar o tamanho real
        try:
            self.root.state('zoomed')
        except:
            self.root.attributes('-zoomed', True)

        self.root.update_idletasks()  # Força o Windows a calcular o tamanho da janela agora

        # Variáveis de Controle
        self.perguntas = self.carregar_perguntas_json()
        self.perguntas_da_rodada = []
        self.indice_atual = 0
        self.pontuacao = 0
        self.tempo_restante = 0
        self.timer_id = None
        self.musica_ativa = True
        self.power_up_disponivel = True
        self.botoes_opcoes = []

        # Inicia
        self.carregar_assets()
        self.iniciar_musica_fundo()
        self.criar_menu_principal()

        self.root.protocol("WM_DELETE_WINDOW", self.fechar_jogo)
        self.root.mainloop()

    # --- SOM (THREADING PARA NÃO TRAVAR) ---
    def iniciar_musica_fundo(self):
        def _loop_musica():
            while self.musica_ativa:
                try:
                    base_path = os.getcwd()
                    caminho_mp3 = os.path.join(base_path, "sons", "base.mp3")
                    caminho_wav = os.path.join(base_path, "sons", "base.wav")
                    if os.path.exists(caminho_mp3):
                        playsound(caminho_mp3)
                    elif os.path.exists(caminho_wav):
                        playsound(caminho_wav)
                    else:
                        break
                except:
                    pass

        t = threading.Thread(target=_loop_musica, daemon=True)
        t.start()

    def tocar_som(self, nome_arquivo):
        def _play():
            try:
                base_path = os.getcwd()
                caminho_mp3 = os.path.join(base_path, "sons", f"{nome_arquivo}.mp3")
                caminho_wav = os.path.join(base_path, "sons", f"{nome_arquivo}.wav")
                if os.path.exists(caminho_mp3):
                    playsound(caminho_mp3)
                elif os.path.exists(caminho_wav):
                    playsound(caminho_wav)
            except:
                pass

        t = threading.Thread(target=_play, daemon=True)
        t.start()

    def fechar_jogo(self):
        self.musica_ativa = False
        self.root.destroy()

    def carregar_perguntas_json(self):
        try:
            with open('perguntas.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro JSON:\n{e}")
            return []

    def carregar_assets(self):
        # Pega o tamanho real da janela maximizada
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        try:
            # Redimensiona fundos para caber na janela atual
            pil_bg_menu = Image.open("imagens/fundo_menu.png").resize((w, h), Image.NEAREST)
            self.bg_menu = ImageTk.PhotoImage(pil_bg_menu)

            pil_bg_jogo = Image.open("imagens/fundo_jogo.png").resize((w, h), Image.NEAREST)
            self.bg_jogo = ImageTk.PhotoImage(pil_bg_jogo)

            self.img_btn_jogar = ImageTk.PhotoImage(Image.open("imagens/btn_jogar.png"))
            self.img_btn_recorde = ImageTk.PhotoImage(Image.open("imagens/btn_recorde.png"))
            self.img_btn_sair = ImageTk.PhotoImage(Image.open("imagens/btn_sair.png"))

            try:
                self.img_btn_ajuda = ImageTk.PhotoImage(Image.open("imagens/btn_ajuda.png"))
            except:
                self.img_btn_ajuda = self.img_btn_jogar

            self.icon_a = ImageTk.PhotoImage(Image.open("imagens/btn_a.png"))
            self.icon_b = ImageTk.PhotoImage(Image.open("imagens/btn_b.png"))
            self.icon_c = ImageTk.PhotoImage(Image.open("imagens/btn_c.png"))
            self.icon_d = ImageTk.PhotoImage(Image.open("imagens/btn_d.png"))

            # Feedbacks Grandes
            pil_acerto = Image.open("imagens/feedback_acerto.png")
            pil_erro = Image.open("imagens/feedback_erro.png")
            # Aumenta 3x
            self.img_acerto = ImageTk.PhotoImage(
                pil_acerto.resize((pil_acerto.width * 3, pil_acerto.height * 3), Image.NEAREST))
            self.img_erro = ImageTk.PhotoImage(
                pil_erro.resize((pil_erro.width * 3, pil_erro.height * 3), Image.NEAREST))

        except Exception as e:
            print(f"ERRO IMAGENS: {e}")
            self.root.destroy()

    def limpar_tela(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        for widget in self.root.winfo_children():
            # Não remove o TopLevel (popups) aqui, eles se destroem sozinhos
            if isinstance(widget, tk.Canvas) or isinstance(widget, tk.Frame) or isinstance(widget, tk.Label):
                widget.destroy()

    # ================= MENU =================
    def criar_menu_principal(self):
        self.limpar_tela()
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        canvas = tk.Canvas(self.root, width=w, height=h, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.bg_menu, anchor="nw")

        # POSICIONAMENTO RELATIVO (relx, rely) - Funciona em qualquer tela!
        btn_jogar = tk.Button(self.root, image=self.img_btn_jogar, bg="black", bd=0,
                              activebackground="black", command=self.iniciar_partida)
        btn_jogar.place(relx=0.5, rely=0.45, anchor="center")

        btn_recorde = tk.Button(self.root, image=self.img_btn_recorde, bg="black", bd=0,
                                activebackground="black", command=lambda: messagebox.showinfo("Info", "Em breve!"))
        btn_recorde.place(relx=0.5, rely=0.60, anchor="center")

        btn_sair = tk.Button(self.root, image=self.img_btn_sair, bg="black", bd=0,
                             activebackground="black", command=self.fechar_jogo)
        btn_sair.place(relx=0.5, rely=0.75, anchor="center")

    # ================= JOGO =================
    def iniciar_partida(self):
        self.tocar_som("levelup")
        self.pontuacao = 0
        self.power_up_disponivel = True
        self.perguntas_da_rodada = self.perguntas.copy()
        random.shuffle(self.perguntas_da_rodada)
        self.indice_atual = 0
        self.mostrar_pergunta()

    def mostrar_pergunta(self):
        self.limpar_tela()
        self.botoes_opcoes = []

        if self.indice_atual >= len(self.perguntas_da_rodada):
            self.tocar_som("levelup")
            messagebox.showinfo("Fim", f"Pontuação Final: {self.pontuacao}")
            self.criar_menu_principal()
            return

        # Recarrega Power-Up a cada 5 perguntas
        if self.indice_atual > 0 and self.indice_atual % 5 == 0:
            if not self.power_up_disponivel: self.power_up_disponivel = True

        pergunta_atual = self.perguntas_da_rodada[self.indice_atual]
        w = self.root.winfo_width()
        h = self.root.winfo_height()

        canvas = tk.Canvas(self.root, width=w, height=h, highlightthickness=0, bg="black")
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.bg_jogo, anchor="nw")

        try:
            fonte_pergunta = (self.fonte_retro, 28)
        except:
            fonte_pergunta = ("Courier", 28, "bold")

        # Texto da Pergunta (Centro Superior)
        canvas.create_text(w / 2, h * 0.25, text=pergunta_atual['pergunta'],
                           font=fonte_pergunta, fill="white", width=int(w * 0.8), justify="center")

        # --- XP (Canto Superior Direito) ---
        cores_neon = ["#FF00FF", "#00FFFF", "#FFFF00", "#00FF00", "#FF0000", "#FFA500"]
        lbl_pontos = tk.Label(self.root, text=f"XP: {self.pontuacao}",
                              font=(self.fonte_retro, 22), bg="black", fg=random.choice(cores_neon))
        # relx=0.95 (quase na direita), rely=0.05 (topo)
        lbl_pontos.place(relx=0.95, rely=0.05, anchor="ne")

        # --- OPÇÕES ---
        opcoes = pergunta_atual['opcoes'].copy()
        random.shuffle(opcoes)
        icones = [self.icon_a, self.icon_b, self.icon_c, self.icon_d]

        start_y = 0.45  # Começa em 45% da altura
        espacamento = 0.12  # 12% entre botões

        for i, opcao_texto in enumerate(opcoes):
            btn = tk.Button(self.root, image=icones[i], text=f"  {opcao_texto}",
                            font=(self.fonte_retro, 22), bg="black", fg="white", bd=0,
                            activebackground="#333", activeforeground="white", compound="left",
                            anchor="w", width=int(w * 0.4),  # Largura responsiva
                            command=lambda op=opcao_texto: self.verificar_resposta(op,
                                                                                   pergunta_atual['resposta_correta']))

            btn.place(relx=0.5, rely=start_y + (i * espacamento), anchor="center")
            self.botoes_opcoes.append((btn, opcao_texto))

        # --- PILHA ESQUERDA (Power-Up + Tempo) ---
        # 1. Power-Up (Fica acima do número do tempo)
        if self.power_up_disponivel:
            self.btn_ajuda_widget = tk.Button(self.root, image=self.img_btn_ajuda, bg="black", bd=0,
                                              activebackground="black",
                                              command=lambda: self.ativar_power_up(pergunta_atual['resposta_correta']))
            self.btn_ajuda_widget.place(relx=0.05, rely=0.75, anchor="w")

        # 2. Número do Tempo
        self.lbl_numero = tk.Label(self.root, text="", font=(self.fonte_retro, 30), bg="black", fg="white")
        self.lbl_numero.place(relx=0.05, rely=0.87, anchor="w")

        # 3. Barra (Base)
        self.lbl_barra = tk.Label(self.root, text="", font=(self.fonte_retro, 20), bg="black")
        self.lbl_barra.place(relx=0.05, rely=0.92, anchor="w")

        self.tempo_restante = 20
        self.atualizar_cronometro()

    def ativar_power_up(self, resposta_correta):
        if not self.power_up_disponivel: return
        self.tocar_som("levelup")
        self.power_up_disponivel = False
        if hasattr(self, 'btn_ajuda_widget'): self.btn_ajuda_widget.destroy()

        botoes_errados = []
        for btn, texto in self.botoes_opcoes:
            if texto != resposta_correta: botoes_errados.append(btn)

        qtd = min(2, len(botoes_errados))
        if qtd > 0:
            for btn in random.sample(botoes_errados, qtd): btn.place_forget()

    def atualizar_cronometro(self):
        try:
            if not self.lbl_numero.winfo_exists(): return
        except:
            return

        if self.tempo_restante >= 0:
            quadradinhos = "█ " * self.tempo_restante
            cor = "#00FF00"
            if self.tempo_restante <= 10: cor = "#FFFF00"
            if self.tempo_restante <= 5: cor = "#FF0000"

            self.lbl_barra.config(text=quadradinhos, fg=cor)
            self.lbl_numero.config(text=str(self.tempo_restante))

            self.tempo_restante -= 1
            # AQUI ESTÁ A CORREÇÃO DO TRAVAMENTO!
            # Guardamos o ID do after para poder cancelar depois
            self.timer_id = self.root.after(1000, self.atualizar_cronometro)
        else:
            self.verificar_resposta("TEMPO_ESGOTADO", "RESPOSTA_QUALQUER")

    def verificar_resposta(self, escolha, correta):
        # 1. CANCELA O CRONÔMETRO IMEDIATAMENTE
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        acertou = (escolha == correta)
        if acertou:
            self.pontuacao += 10
            img = self.img_acerto
            self.tocar_som("correct")
        else:
            img = self.img_erro
            self.tocar_som("error")

        # 2. MOSTRA FEEDBACK (POPUP SEM BORDAS)
        top = tk.Toplevel(self.root)
        try:
            top.state('zoomed')
        except:
            top.attributes('-zoomed', True)
        top.attributes("-alpha", 0.9)
        top.configure(bg="black")
        top.overrideredirect(True)

        lbl = tk.Label(top, image=img, bg="black")
        lbl.pack(expand=True)

        # 3. AGENDA O FIM DO FEEDBACK (SEM USAR SLEEP!)
        # Daqui a 1500ms (1.5s), ele chama a função fechar_feedback
        self.root.after(1500, lambda: self.fechar_feedback(top))

    def fechar_feedback(self, top_window):
        top_window.destroy()
        self.indice_atual += 1
        self.mostrar_pergunta()


if __name__ == "__main__":
    app = EasyMathGUI()