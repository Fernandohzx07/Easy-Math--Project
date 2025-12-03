# audio.py
import os
import threading
import time
from playsound import playsound

class DJ:
    def __init__(self):
        self.musica_ativa = True

    def iniciar_musica_fundo(self):
        self.musica_ativa = True
        def _loop():
            while self.musica_ativa:
                try:
                    base = os.getcwd()
                    mp3 = os.path.join(base, "sons", "base.mp3")
                    if os.path.exists(mp3): playsound(mp3)
                    else: break
                except: time.sleep(1)
        threading.Thread(target=_loop, daemon=True).start()

    def parar_musica(self):
        self.musica_ativa = False

    def tocar_sfx(self, nome):
        def _play():
            try:
                base = os.getcwd()
                caminho = os.path.join(base, "sons", f"{nome}.mp3")
                if os.path.exists(caminho): playsound(caminho)
                else: playsound(os.path.join(base, "sons", f"{nome}.wav"))
            except: pass
        threading.Thread(target=_play, daemon=True).start()