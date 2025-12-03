# Easy Math - 🎮

> **Projeto de Software Interdisciplinar - UFRPE**

**Desenvolvedores:** Davi Fernando e Ismael Barros
**Docente Responsável:** Cleyton Magalhães

O **Easy Math** é um jogo educativo e interativo desenvolvido em Python, projetado para auxiliar crianças — com foco especial naquelas com TDAH e autismo — no aprendizado da matemática.

O projeto evoluiu de um protótipo em terminal para uma **aplicação gráfica (GUI) completa**, transformando o estudo em uma experiência visual envolvente. Através de uma estética *Pixel Art* (8-bits), sons imersivos e mecânicas de gamificação, o jogo busca fortalecer o conhecimento matemático básico de forma dinâmica e divertida.

---

## 📋 REQUISITOS FUNCIONAIS

### 1ª Lançamento
* **RF001** - Menu Principal
* **RF002** - Menu alternativo
* **RF003** - Sistema de questões e respostas personalizadas
* **RF004** - Diferentes níveis de dificuldade nas questões
* **RF005** - POWER-UP DE AJUDA (50/50)
* **RF006** - Sistema de pontuação tipo (XP)

### 2ª Lançamento
* **RF007** - Implementação de interface gráfica
* **RF008** - Otimização do tempo (Perguntas e Respostas)
* **RF009** - Correções de bugs e problemas futuros
* **RF010** - Premiações estratégicas em forma de ícone ao terminar o jogo

---

## 🏗️ ARQUITETURA E FUNCIONALIDADES

O projeto foi reestruturado utilizando uma arquitetura modular organizada em pacotes, separando a lógica de negócios, a interface visual e o gerenciamento de recursos.

### 1. Interface Gráfica (GUI) e UX
Substituímos o terminal por uma janela interativa utilizando a biblioteca **Tkinter**.
* **Design Responsivo:** O jogo detecta a resolução do monitor e se adapta automaticamente, rodando em modo maximizado/tela cheia sem distorção.
* **Identidade Visual 8-Bits:** Uso de fontes customizadas (*Arcade*) e imagens em *Pixel Art* para botões, fundos e ícones.
* **Feedback Visual:** Telas de *pop-up* animadas indicam acertos e erros instantaneamente.

### 2. Gerenciamento do Jogo (`jogo.py` e `config.py`)
* **Banco de Questões (JSON):** As perguntas são carregadas externamente, permitindo fácil edição e expansão do conteúdo.
* **Sistema de Níveis:** Progressão automática pelos níveis `Fácil`, `Médio` e `Difícil`, com ajuste dinâmico do tempo para resposta.
* **Persistência de Dados:** O recorde (XP) do jogador é salvo localmente em `pontuacao.txt` e exibido no "Hall da Fama".

### 3. Gamificação
* **XP e Score:** Pontuação em tempo real exibida na interface.
* **Cronômetro Visual:** Uma barra de tempo dinâmica que muda de cor (Verde > Amarelo > Vermelho) conforme o tempo se esgota.
* **Power-Up 50/50:** Botão estratégico que elimina duas alternativas incorretas. O recurso é recarregável a cada mudança de nível/fase.

### 4. Sistema de Áudio (`audio.py`)
* **Trilha Sonora:** Música de fundo em *loop* para imersão.
* **Efeitos Sonoros (SFX):** Sons distintos para acerto, erro, *level up* e uso de poderes.
* **Execução Assíncrona:** Uso de `threading` para garantir que o áudio não trave a interface gráfica.

---

## 🛠️ TECNOLOGIAS UTILIZADAS

| Tecnologia | Descrição |
| :--- | :--- |
| **Python 3.13** | Linguagem base do projeto. |
| **Tkinter** | Biblioteca padrão utilizada para construção da Interface Gráfica (GUI). |
| **JSON** | Formato utilizado para o banco de dados de perguntas. |
| **Git/GitHub** | Controle de versão e hospedagem do código. |
| **Canva** | Utilizado para a criação dos assets visuais (botões, fundos, ícones). |

---

## 📚 BIBLIOTECAS E DEPENDÊNCIAS

Para elevar o nível do projeto, utilizamos bibliotecas externas específicas:

| Biblioteca | Utilidade no Projeto |
| :--- | :--- |
| **`Pillow (PIL)`** | Manipulação avançada de imagens. Permite redimensionar os fundos para tela cheia e carregar texturas nos botões. |
| **`pyglet`** | Carregamento de fontes customizadas (`.ttf`) diretamente da pasta do projeto, sem necessidade de instalação no Windows. |
| **`playsound`** | Reprodução de arquivos de áudio (`.mp3` e `.wav`). |
| **`threading`** | Utilizado para executar o áudio em paralelo, evitando o congelamento da interface gráfica. |
| **`os` & `sys`** | Gerenciamento de caminhos de arquivos, garantindo que o jogo encontre as imagens e sons em qualquer computador. |

---

## 🚀 INSTALAÇÃO E EXECUÇÃO

Para rodar o **Easy Math - Final Edition**, é necessário instalar as bibliotecas de suporte gráfico e sonoro.

1.  **Instale as dependências:**
    Abra o terminal na pasta do projeto e execute:
    ```bash
    pip install playsound==1.2.2 Pillow pyglet
    ```

2.  **Execute o jogo:**
    ```bash
    python main.py
    ```

---

## 📂 ESTRUTURA DE ARQUIVOS

```text
Easy-Math--Project/
│
├── main.py            # Ponto de entrada (Maestro)
├── config.py          # Configurações globais e nomes de arquivos
├── jogo.py            # Lógica matemática e regras
├── audio.py           # Controle de som
│
├── gui/               # Módulo de Interface Gráfica
│   ├── app.py         # Gerenciador da Janela Principal
│   ├── menu.py        # Tela de Menu
│   ├── game_screen.py # Tela do Jogo
│   └── score_screen.py # Tela de Recorde
│
├── sons/              # Arquivos de áudio (.mp3/.wav)
├── imagens/           # Assets visuais (.png) e Fonte (.ttf)
└── perguntas.json     # Banco de dados

[Acessar Fluxogramas do Projeto](https://drive.google.com/drive/folders/1aC-CnkMrmFKynfO_pQoCciapgDVbFtEl?usp=drive_link)
