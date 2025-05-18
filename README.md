# 💚 Mestre Yoda: Chatbot Assistente Sábio com Arquitetura de Agentes 💚

Bem-vindo ao repositório do projeto "Mestre Yoda: Chatbot Assistente Sábio com Arquitetura de Agentes"! Este projeto é um exemplo prático de como construir um chatbot interativo e envolvente, com uma persona bem definida (o sábio Mestre Yoda de Star Wars), utilizando as capacidades da API Google Gemini e o Agent Development Kit (ADK).

O objetivo é criar um assistente virtual que não apenas execute tarefas úteis, como buscar informações ou dar conselhos, mas que o faça mantendo a voz, o tom e o padrão de fala característico do Mestre Yoda, proporcionando uma experiência de usuário única e memorável.

## ✨ Funcionalidades (O Que o Mestre Yoda Pode Fazer por Você) ✨

Nesta versão inicial do chatbot, o Mestre Yoda está equipado para lidar com diferentes tipos de indagações, delegando o trabalho pesado para seus aprendizes especialistas:

* **Buscar Informação (`oInterior`):** Precisa de dados ou fatos encontrados na vasta rede de informações (a internet)? O Mestre Yoda pode consultar seu aprendiz especialista em busca.
* **Contar Histórias (`aExperiência`):** Deseja ouvir uma história simples e criativa? O aprendiz responsável por "a Experiência" pode te ajudar a trilhar uma nova jornada narrativa.
* **Oferecer Conselhos Sábios (`aForça`):** Busca orientação geral ou uma perspectiva ponderada sobre um tópico? O aprendiz sintonizado com "a Força" pode compartilhar sabedoria.

Essas funcionalidades são a base, e a arquitetura permite que o chatbot aprenda e execute muitos outros tipos de tarefas no futuro.

## 🤖 Como Funciona (A Magia da Arquitetura de Agentes) 🤖

Este chatbot não é um único modelo de IA respondendo a tudo. Ele utiliza uma estrutura modular baseada em **Agentes**, um conceito facilitado pelo **Google Agent Development Kit (ADK)**. Agentes são como componentes de IA independentes, cada um com uma especialidade, que podem colaborar para atingir um objetivo maior.

A arquitetura principal empregada aqui é a **Router-Agente**:

1.  **O Agente Mestre Yoda (`YodaMasterAgent`):**
    * **Quem é:** É o Agente principal, a interface com o usuário. Ele *é* o Mestre Yoda.
    * **O Que Faz:** Recebe a indagação do usuário, analisa a intenção por trás da pergunta e decide qual Agente Especialista (seu "aprendiz") é o mais adequado para lidar com aquela tarefa específica. Após o aprendiz retornar um resultado, o Mestre Yoda pega essa informação e a reformula completamente, aplicando sua persona característica antes de apresentar a resposta final ao Padawan (o usuário).
    * **Por que usamos este termo e conceito?** A ideia de um Agente principal que roteia e gerencia a interação é fundamental para criar chatbots complexos com diferentes capacidades. Ele centraliza a lógica de interação e a persona, enquanto delega as habilidades específicas para outros. É o "cérebro" que coordena os "membros" especialistas.
    * **Como a Persona é Aplicada?** A personalidade única do Mestre Yoda é definida principalmente na **instrução (prompt)** deste Agente. Essa instrução descreve seu papel, define as regras de como ele deve falar (ordem das palavras, interjeições, vocabulário) e como ele deve transformar as respostas "neutras" dos aprendizes em sabedoria Yoda.

2.  **Os Agentes Especialistas (Os Aprendizes):** São Agentes focados em uma única tarefa. Eles não têm a persona Yoda e trabalham nos bastidores quando chamados pelo Agente Mestre. O Mestre Yoda os "consulta" como se fossem ferramentas.
    * **`oInterior` (Agente de Informação):**
        * **O Que Faz:** É o especialista em buscar informações factuais. Quando o Mestre Yoda precisa saber algo sobre o mundo, ele consulta este aprendiz.
        * **Por que usamos este termo e conceito?** Separar a função de busca permite que este agente seja otimizado para essa tarefa e use ferramentas específicas (`Google Search`). Se quiséssemos adicionar busca em outras fontes (banco de dados interno, documentos), faríamos isso aqui.
        * **Nome ("oInterior"):** Foi escolhido para representar a busca por conhecimento dentro de um vasto "interior" de dados (a internet), evocando uma sensação de introspecção e descoberta da informação.
    * **`aExperiência` (Agente Contador de Histórias):**
        * **O Que Faz:** É o especialista em criatividade narrativa. Quando o Padawan pede uma história, este aprendiz constrói uma.
        * **Por que usamos este termo e conceito?** Isola a capacidade de geração de texto criativo. Outros tipos de conteúdo (poemas, roteiros curtos) poderiam ser adicionados a este agente.
        * **Nome ("aExperiência"):** Refere-se ao acúmulo de conhecimento e sabedoria passados através de histórias e vivências, algo crucial no universo Jedi.
    * **`aForça` (Agente Conselheiro):**
        * **O Que Faz:** É o especialista em sabedoria e conselhos gerais. Quando o Padawan busca orientação, este aprendiz oferece reflexões ponderadas.
        * **Por que usamos este termo e conceito?** Concentra a lógica de "raciocínio" para conselhos, separada da busca pura ou da criatividade.
        * **Nome ("aForça"):** O termo central no universo Star Wars para o poder, a verdade e a orientação espiritual, perfeito para o agente que dá conselhos sábios.

3.  **Ferramentas (`Google Search`):**
    * **O Que Faz:** São funcionalidades que os Agentes podem invocar. `Google Search` permite que os Agentes que a possuem busquem informações na web.
    * **Por que usamos este termo e conceito?** Ferramentas expandem as capacidades dos Agentes para interagir com serviços externos ou dados em tempo real.

4.  **Runner e SessionService (Google ADK):**
    * **O Que Fazem:** São componentes do ADK que gerenciam o ciclo de execução dos Agentes. O `Runner` orquestra o fluxo de chamadas entre Agentes e ferramentas. O `SessionService` (neste código, `InMemorySessionService`) mantém o estado da conversa para um usuário específico durante uma sessão.
    * **Por que usamos estes termos e conceitos?** Eles são parte fundamental do framework ADK para gerenciar a complexidade da interação entre múltiplos Agentes em uma conversa.

5.  **Função Auxiliar `call_agent`:**
    * **O Que Faz:** Esta função em Python simplifica o uso do `Runner` para executar um Agente com uma mensagem de entrada e coletar a resposta final que ele gera. Ela itera pelos eventos que o `Runner` emite durante a execução e junta as partes de texto do evento que representa a resposta final.
    * **Por que usamos este termo e conceito?** É uma abstração prática para tornar o código principal mais limpo, evitando repetir a lógica de execução do `Runner` sempre que um Agente precisa ser chamado.

**O Fluxo de Interação:**

Quando você digita uma mensagem:
1.  Seu texto é passado para a função `call_agent`.
2.  `call_agent` usa o `Runner` para executar o `YodaMasterAgent`.
3.  O `YodaMasterAgent` lê sua mensagem e sua própria `instruction` (que inclui as regras de roteamento e persona).
4.  Ele decide se precisa de um aprendiz (ex: `oInterior` para fatos) ou se pode responder diretamente.
5.  Se precisar, ele gera uma "chamada de ferramenta" interna para o aprendiz escolhido.
6.  O `Runner` intercepta essa chamada e executa o Agente Especialista (ex: `oInterior`).
7.  O Agente Especialista realiza sua tarefa (ex: usa `Google Search`) e gera um resultado.
8.  O `Runner` entrega o resultado do Agente Especialista de volta para o `YodaMasterAgent` como um "resultado de ferramenta".
9.  O `YodaMasterAgent` recebe o resultado do aprendiz e, usando sua `instruction`, o traduz e reformula na persona do Mestre Yoda.
10. O `Runner` emite a resposta final gerada pelo `YodaMasterAgent`.
11. A função `call_agent` captura essa resposta final.
12. O código principal exibe a resposta do Mestre Yoda para você.

## 🛠️ O Que Foi Usado (Tecnologia) 🛠️

* **Python 3:** Linguagem de programação.
* **Google Gemini API (`google-genai`):** SDK para acessar os modelos Gemini.
* **Google Agent Development Kit (`google-adk`):** Framework para desenvolvimento de agentes.
* **Modelos Google Gemini (`gemini-2.0-flash`):** Modelos de linguagem que alimentam os Agentes. `gemini-2.0-flash` é um modelo otimizado para velocidade e custo. (Nota: Existem modelos mais recentes como `gemini-1.5-flash-latest` e `gemini-1.5-pro-latest` que podem oferecer diferentes trade-offs de performance, custo e capacidades).
* **Ferramenta Google Search (`google.adk.tools.Google Search`):** Permite busca na web.
* **Google Colab:** Ambiente de execução.

## 🚀 Como Criado e Lições Aprendidas 🚀

O desenvolvimento deste chatbot seguiu um caminho iterativo:

1.  **Estrutura Inicial:** Configuração do ambiente, instalação das bibliotecas e obtenção da API Key. Criação da estrutura básica de um Agente simples.
2.  **Implementação da Arquitetura:** Definição dos Agentes Especialistas e do Agente Mestre Router. Configuração da função auxiliar `call_agent` para orquestrar a execução.
3.  **Injeção da Persona:** Definição detalhada da `instruction` do `YodaMasterAgent` para moldar sua personalidade e padrão de fala.
4.  **Roteamento e Integração:** Aprimoramentos na `instruction` do Mestre Yoda para melhorar sua capacidade de identificar a intenção do usuário, chamar o aprendiz correto e, crucialmente, integrar a resposta do aprendiz de forma coerente na resposta final. Lições foram aprendidas sobre a importância de instruções claras e, por vezes, assertivas para guiar o comportamento do modelo LLM subjacente na tomada de decisão e na formatação da saída.
5.  **Tratamento de Saída:** Ajustes para garantir que apenas a resposta final e formatada pelo Mestre Yoda fosse exibida, controlando a visibilidade de processos internos como a sintaxe da chamada de ferramentas (mesmo que o código fornecido aqui não inclua a filtragem mais avançada desenvolvida posteriormente para resolver vazamentos específicos).

## 💡 Possibilidades de Aprimoramento (O Futuro do Padawan) 💡

Este projeto é um excelente ponto de partida e pode ser significativamente aprimorado:

* **Mais Habilidades:** Adicionar novos Agentes Especialistas para expandir os tipos de tarefas que o chatbot pode realizar (ex: calcular, traduzir, definir palavras, etc.).
* **Modelos Gemini:** Experimentar com diferentes modelos (`gemini-1.5-flash-latest` para otimização de custo/velocidade, `gemini-1.5-pro-latest` para tarefas que exigem raciocínio mais complexo ou criatividade) para Agentes específicos, incluindo o Mestre Yoda.
* **Roteamento Mais Robusto:** Refinar as regras de roteamento na instrução do Agente Mestre para lidar melhor com indagações ambíguas ou complexas.
* **Gerenciamento de Conversa:** Implementar um gerenciamento de sessão mais persistente para que o Mestre Yoda se lembre do contexto de turnos anteriores na conversa.
* **Tratamento de Erros:** Melhorar o tratamento de erros da API (`429 RESOURCE_EXHAUSTED` e outros) com lógica de retentativa ou mensagens de erro mais informativas no estilo Yoda.
* **Interface do Usuário:** Desenvolver uma interface web (usando Flask, Streamlit, ou ferramentas semelhantes) ou de desktop para uma experiência mais polida que o console do Colab.
* **Filtragem de Saída:** Adicionar código explícito (como filtragem com regex na função `call_agent`) para garantir que nenhuma sintaxe interna de ferramenta ou depuração vaze para a resposta final apresentada ao usuário.
* **Testes:** Implementar testes automatizados para as decisões de roteamento e a consistência da persona.

## 🛠️ Configuração e Como Rodar (O Caminho para a Sabedoria) 🛠️

Para executar o Chatbot Mestre Yoda no seu Google Colab, siga estes passos:

1.  **Obtenha sua API Key do Google Gemini:**
    * Acesse o [Google AI Studio](https://aistudio.google.com/).
    * Crie ou faça login com sua conta Google.
    * Gere sua API Key no painel. [Clique aqui para gerar uma API Key](https://aistudio.google.com/app/apikey).
2.  **Prepare o Ambiente no Google Colab:**
    * Abra o Google Colab ([colab.research.google.com](https://colab.research.google.com/)) e crie um novo notebook.
    * Copie e cole o código Python completo deste repositório nas células do notebook.
    * **Armazene sua API Key de forma segura:** No menu lateral esquerdo do Colab, clique no ícone da chave (`🔑`). Clique em "Add a new secret". Crie uma credencial com o nome **`GOOGLE_API_KEY`** (é crucial que seja exatamente este nome) e cole o valor da API Key que você obteve. Certifique-se de que o acesso a este notebook está ativado.
3.  **Execute as Células:**
    * Execute a primeira célula que instala as bibliotecas: `%pip -q install google-genai google-adk`.
    * Execute a célula seguinte que importa as bibliotecas e carrega a API Key do `userdata`.
    * Execute as células que definem as funções auxiliares e os Agentes (`create_..._agent`).
    * Execute a última célula que contém o loop `while True` para iniciar a interação com o chatbot.

O chatbot começará a rodar no output do Colab. Você verá a saudação inicial do Mestre Yoda e poderá digitar suas perguntas. Para encerrar o chatbot, digite `sair` quando solicitado.

## 📜 Licença

Este projeto está sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

Que a Força guie seus aprendizados e projetos! 🙏
