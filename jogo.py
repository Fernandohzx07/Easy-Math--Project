# jogo.py
import json
import random


class LogicaJogo:
    def __init__(self):
        self.perguntas = self._carregar_json()
        self.pontuacao = 0

    def _carregar_json(self):
        try:
            with open('perguntas.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def filtrar_perguntas(self, nivel):
        # Filtra perguntas do nível escolhido
        lista = [p for p in self.perguntas if p['nivel'] == nivel]
        random.shuffle(lista)
        return lista

    def salvar_recorde(self):
        try:
            with open("pontuacao.txt", 'w') as f:
                f.write(str(self.pontuacao))
        except:
            pass

    def ler_recorde(self):
        try:
            with open("pontuacao.txt", 'r') as f:
                return f.read()
        except:
            return "0"