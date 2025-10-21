import threading
import time
from playsound import playsound

# Uma "bandeira" para controlar a música de fundo
musica_de_fundo_tocando = True


def tocar_musica_base():
    """Toca a música de fundo em um loop infinito, enquanto a flag permitir."""
    while musica_de_fundo_tocando:
        try:
            playsound('sons/base.mp3')
        except:
            try:
                playsound('sons/base.wav')
            except:
                time.sleep(1)


def tocar_efeito_sonoro(nome_do_arquivo):
    """Toca um efeito sonoro curto em uma thread separada."""
    caminho_mp3 = f'sons/{nome_do_arquivo}.mp3'
    caminho_wav = f'sons/{nome_do_arquivo}.wav'

    def tocar():
        try:
            playsound(caminho_mp3)
        except:
            try:
                playsound(caminho_wav)
            except:
                pass

    threading.Thread(target=tocar, daemon=True).start()