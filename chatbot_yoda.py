%pip -q install google-genai google-adk

import os
from google.colab import userdata
os.environ["GOOGLE_API_KEY"] = userdata.get('GOOGLE_API_KEY')

from google import genai
from google.adk.agents import Agent # LlmAgent é a classe base por trás de Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search # Ferramenta de busca útil para vários agentes
from google.genai import types
from IPython.display import display, Markdown, HTML
import textwrap
import warnings

warnings.filterwarnings("ignore")

client = genai.Client()

# --- Funções Auxiliares ---

def call_agent(agent: Agent, message_text: str) -> str:
    """Chama um agente com uma mensagem e retorna a resposta final."""
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    try:
        # Itera pelos eventos. APENAS acumula o texto final.
        for event in runner.run(user_id="user1", session_id="session1", new_message=content):
            if event.is_final_response():
                for part in event.content.parts:
                    if part.text is not None:
                        final_response += part.text
                        if part != event.content.parts[-1]:
                            final_response += "\n"
            # Linhas de DEBUG (devem ficar comentadas para não aparecerem na saída final):
            # if event.is_tool_code():
            #      print(f"\n[DEBUG] Chamando aprendiz: {event.tool_code.tool_code}")
            # elif event.is_tool_result():
            #      print(f"\n[DEBUG] Resultado do aprendiz: {event.tool_result.tool_result}")


    except Exception as e:
         print(f"\n[ERRO NA API] Detalhes: {e}")
         final_response = f"Hmm, um problema com a Força tivemos: {e}. Sua indagação completa, responder não pude."

    return final_response # Retorna APENAS a resposta final acumulada

def to_markdown(text):
    """Formata texto para exibição em Markdown com indentação."""
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# --- Definição dos Agentes Especialistas ---

def create_information_agent():
    """Agente especialista em buscar e fornecer informações."""
    return Agent(
        name="oInterior",
        model="gemini-2.0-flash",
        instruction="""
        Você é um assistente focado em buscar informações precisas e factuais usando a ferramenta de busca.
        Responda à pergunta do usuário diretamente com base nos resultados da busca.
        Se não encontrar a resposta exata, diga que a informação não foi encontrada.
        Não adicione opiniões ou informações fora do escopo da busca.
        Sua resposta deve ser clara e objetiva.
        """,
        description="Busca informações usando o Google.",
        tools=[google_search]
    )

def create_storytelling_agent():
    """Agente especialista em criar histórias simples."""
    return Agent(
        name="aExperiência",
        model="gemini-2.0-flash",
        instruction="""
        Você é um contador de histórias criativo. Crie uma história simples e apropriada para crianças ou adultos,
        com base na solicitação do usuário. A história deve ter um início, meio e fim.
        Não adicione a persona Yoda. Apenas crie a história.
        """,
        description="Cria histórias simples e criativas.",
        tools=[]
    )

def create_advice_agent():
    """Agente especialista em dar conselhos gerais."""
    return Agent(
        name="aForça",
        model="gemini-2.0-flash",
        instruction="""
        Você é um conselheiro gentil e sábio. Forneça conselhos gerais e ponderados sobre o tópico
        mencionado pelo usuário. Se a pergunta for complexa ou sobre tópicos sensíveis
        (saúde, finanças pessoais específicas, etc.), diga que não pode dar conselhos específicos sobre isso,
        mas pode oferecer sabedoria geral. Mantenha um tom calmo e encorajador.
        Não adicione a persona Yoda. Apenas dê o conselho.
        """,
        description="Oferece conselhos gerais e sábios.",
        tools=[google_search]
    )

# --- Definição do Agente Mestre (Yoda Router) ---

def create_yoda_master_agent():
    """Agente principal que age como Mestre Yoda, roteia para especialistas e aplica a persona."""

    information_agent = create_information_agent()
    storytelling_agent = create_storytelling_agent()
    advice_agent = create_advice_agent()

    return Agent(
        name="YodaMasterAgent",
        model="gemini-2.0-flash",
        instruction="""
        Você é o Mestre Yoda. Sua tarefa é ajudar crianças e idosos com diversas indagações e tarefas.
        Você deve analisar a solicitação do usuário e determinar qual de seus aprendizes (agentes especialistas)
        é o mais adequado para realizar a tarefa.
        Use as 'tools' (que são seus aprendizes) disponíveis para chamar o aprendiz correto.
        O nome da ferramenta a ser chamada deve ser EXATAMENTE o 'name' do agente especialista (ex: oInterior, aExperiência).
        O input para a ferramenta deve ser a solicitação relevante do usuário para aquele aprendiz.

        Após receber a resposta do aprendiz, você deve traduzi-la e apresentá-la ao usuário
        UTILIZANDO COMPLETAMENTE A SUA PERSONA DO MEStre YODA.
        Siga rigorosamente o padrão de fala do Mestre Yoda:
        - Ordem de palavras incomum (Objeto-Sujeito-Verbo ou Verbo-Objeto-Sujeito). Ex: "Fazer ou não fazer. Tentativa não há."
        - Use frases sábias, calmas, às vezes enigmáticas.
        - Inclua interjeições como "Hmm," "Simmm," "Curioso." "HIHIHIHI."
        - Refira-se ao usuário como "Padawan."
        - Mencione A Força ("A Força é forte em você," "Sinta a Força," etc.) quando apropriado.
        - Adapte a complexidade da resposta para a possível idade do Padawan (simples para crianças, mais detalhado para idosos, mas sempre na persona Yoda).
        - Se não souber como responder ou qual aprendiz usar, diga algo no estilo Yoda que indique isso.
        - NUNCA quebre a persona. TUDO que você disser deve soar como Yoda.

        Aprendizes disponíveis (tools que você pode chamar):
        - Name: oInterior
          Description: Use este aprendiz para buscar informações factuais e responder perguntas que precisam de dados do mundo real.

        - Name: aExperiência
          Description: Use este aprendiz para criar histórias simples e criativas baseadas na solicitação do Padawan.

        - Name: aForça
          Description: Use este aprendiz para fornecer conselhos gerais e sábios sobre um tópico.

        Se a solicitação do usuário não se encaixar em nenhum aprendiz, responda diretamente na sua persona Yoda,
        talvez com uma sabedoria geral ou uma observação sobre a natureza da pergunta.
        """,
        description="Agente principal que age como Mestre Yoda, roteia tarefas e aplica a persona.",
        tools=[]
    )

# --- Fluxo Principal do Chatbot ---

print("💚 Iniciando o Chatbot Mestre Yoda... Sua sabedoria, buscar eu vou. 💚")

yoda_master = create_yoda_master_agent()

print("\n--- ✨ Sabedoria do Mestre Yoda ✨ ---\n")
display(to_markdown("Pronto para ajudar, o Mestre Yoda está. Sua pergunta qual é, Padawan?"))
print("\n--------------------------------------------------------------")


while True:
    user_query = input("❓ Digite sua indagação, Padawan (ou 'sair'): ")

    if user_query.lower() == 'sair':
        print("Adeus, Padawan. Que a Força com você esteja.")
        break

    if not user_query:
        print("Hmm, o que você precisa, Padawan?")
        continue

    print("🧠 Hmm, pensando o Mestre Yoda está...")

    # call_agent retorna APENAS a resposta final
    yoda_response = call_agent(yoda_master, user_query)

    # display(to_markdown(...)) exibe APENAS o que call_agent retornou
    print("\n--- ✨ Sabedoria do Mestre Yoda ✨ ---\n")
    display(to_markdown(yoda_response))
    print("\n--------------------------------------------------------------")
