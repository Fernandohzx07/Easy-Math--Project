## (EASY MATH Project) 🎮

## Repositório EASY MATH - Projeto de Software Interdisciplinar

Desenvolvedores: Davi Fernando e Ismael Barros

Docente Responsável: Cleyton Magalhães

O Easy Math é um game educativo e interativo, projetado para auxiliar crianças com dificuldades no aprendizado de matemática.
O objetivo é transformar o estudo em uma experiência envolvente e divertida, 
prendendo a atenção dos pequenos através de um modelo de jogo de 1 pergunta com 4 alternativas.
O projeto busca fortalecer o conhecimento matemático básico das crianças, fornecendo uma plataforma dinâmica que se adapta ao ritmo de cada uma.

REQUISITOS FUNCIONAIS

## 1ª Release

• RF001 - Menu Principal 

• RF002 - Menu alternativo

• RF003 - Sistema de questões e respostas personalizadas

• RF004 - Diferentes níveis de dificuldade nas questões

• RF005 - POWER-UP DE AJUDA (50/50)

• RF006 - Sistema de pontuação tipo (XP)

## 2ª Release

• RF007 - Implementação de interface gráfica

• RF008 - Desafios finais para níveis avançados

• RF009 - Correções de bugs e futuros problemas

• RF010 - premiações estratégicas em forma de ícone ao terminar o jogo


## ENTREGAS 

1° VA 22/10/2025 ✅ 

## PRINCIPAIS FUNÇÕES DO CÓDIGO

### Fluxo Principal e Menu

-   `main()`: Orquestra todo o fluxo do jogo, funcionando como a "Torre de Controle" que chama os outros módulos.
-   `exibir_menu_principal()`: Exibe o menu com as opções de "Iniciar Novo Jogo", "Ver Última Pontuação" e "Sair".
-   `ler_ultima_pontuacao()`: Lê e exibe a pontuação salva em `pontuacao.txt`. Caso não exista, oferece um atalho para iniciar um novo jogo.

### Gerenciamento do Jogo e Níveis

-   `iniciar_jornada()`: Controla a progressão do jogador através dos níveis definidos (`fácil`, `médio`, `difícil`).
-   `iniciar_nivel()`: Executa a lógica de um nível completo, gerenciando as perguntas, o cronômetro, a pontuação e o Power-Up.
-   `carregar_perguntas()`: Carrega a base de conhecimento do jogo a partir do arquivo `perguntas.json`.
-   `salvar_pontuacao()`: Salva a pontuação final do jogador em `pontuacao.txt` para consulta futura.

### Gamificação e Interatividade

-   **Sistema de Pontuação:** Concede +10 pontos por acerto e exibe a pontuação total em tempo real no HUD.
-   **Cronômetro Regressivo:** Cada nível possui um tempo limite decrescente (`20s`, `15s`, `7s`), criando um desafio de agilidade. Esta função é implementada com **`threading`** para não travar o jogo.
-   **Power-Up 50/50:** Uma ajuda estratégica que o jogador pode usar uma vez por nível para eliminar duas alternativas incorretas.
-   **Finais Múltiplos:** Ao final da jornada, o jogo exibe uma de quatro telas de resultado diferentes, com base na pontuação final do jogador, incentivando a rejogabilidade.

### Interface e Experiência do Usuário (UX)

-   `exibir_abertura()`: Apresenta uma tela de título animada, com efeito de "boot-up" para criar uma atmosfera de videogame.
-   `limpar_tela()`: Mantém a interface limpa e focada, limpando o terminal a cada nova pergunta ou tela.
-   **Feedback Visual:** Utiliza um sistema de cores vibrantes e blocos de fundo (`Back`) para dar feedback instantâneo (verde para acerto, vermelho para erro, magenta para informações).

### Áudio e Imersão

-   `tocar_musica_base()`: Toca uma música de fundo em loop contínuo durante todo o jogo para manter o jogador engajado.
-   `tocar_efeito_sonoro()`: Toca efeitos sonoros específicos para acerto (`correct`), erro (`error`) e avanço de nível (`levelup`), criando reforço auditivo.

## TECNOLOGIAS UTILIZADAS

| Tecnologia                  | Utilidade                                                                                    |
| :-------------------------- | :------------------------------------------------------------------------------------------- |
| **Python 3.13** | Linguagem principal de desenvolvimento do sistema.                                           |
| **JSON** | Utilizado como banco de dados leve para armazenar as perguntas, alternativas, níveis e respostas. |
| **Git, GitHub, GitHub Desktop** | Controle de versão, hospedagem do repositório e interface visual para commits e sincronização. |
| **Draw.io** | Ferramenta utilizada para o design e documentação dos fluxogramas do projeto.                |

## BIBLIOTECAS

| Biblioteca   | Utilidade                                                                                                                    |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **`colorama`** | Essencial para a estilização de textos e fundos no terminal com cores, criando a identidade visual do jogo.                  |
| **`playsound`** | Responsável por toda a imersão sonora, tocando a música de fundo e os efeitos sonoros.                                       |
| **`threading`** | O destaque técnico do projeto. Usado para executar o cronômetro, a captura de input e os sons de forma paralela, sem travar a interface. |
| **`json`** | Para carregar e decodificar o arquivo `perguntas.json`, transformando-o em dados utilizáveis pelo Python.                     |
| **`os`** | Utilizado para interagir com o sistema operacional, especificamente para limpar a tela do terminal (`os.system`).            |
| **`time`** | Fundamental para controlar o ritmo do jogo, criar pausas (`time.sleep`) e animar a interface.                                |
| **`random`** | Peça-chave da gamificação, usada para embaralhar a ordem das perguntas e das alternativas em cada rodada.                      |

## INSTALAÇÃO NECESSÁRIA

Para garantir que a experiência de cores e sons funcione perfeitamente, é necessário instalar duas bibliotecas. Utilize o seguinte comando no seu terminal, dentro da pasta do projeto, antes de rodar o programa:

```bash
pip install colorama playsound==1.2.2
```

## COMO EXECUTAR

Após a instalação das bibliotecas, execute o jogo a partir do terminal com o comando:

```bash
python main.py
```

## FLUXOGRAMAS DO PROJETO

A documentação visual do fluxo lógico de cada Requisito Funcional pode ser acessada no link abaixo:

[Acessar Fluxogramas do Projeto](https://drive.google.com/drive/folders/1aC-CnkMrmFKynfO_pQoCciapgDVbFtEl?usp=drive_link)
