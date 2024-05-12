# !pip install -q -U google-generativeai

import google.generativeai as genai
import textwrap
from IPython.display import display
from IPython.display import Markdown

# Configuracao do GenerativeAI
GOOGLE_API_KEY = "AIzaSyAzO3FR7an1eCQi_0eXuSUO9Yx2YH2cqtc"
genai.configure(api_key=GOOGLE_API_KEY)

# Setup do modelo + segurança
generation_config = {
    "candidate_count": 1,
    "temperature": 0.9,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
]

# Melhorando a visualização do historico
# Código disponível em https://ai.google.dev/tutorials/python_quickstart#import_packages


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Imprimindo o histórico


def show_history():
    for message in chat.history:
        display(to_markdown(f'**{message.role}**: {message.parts[0].text}'))
        print('-------------------------------------------')


# Preparação do modelo
system_instruction = "Você é um chatBOT especializado em informações sobre a ONG Code Club Brasil, educação STEM, e Pensamento Computacional."

generation_config = genai.GenerationConfig(
    developer_instructions="Provide a fun introduction as Ada. You will be interacting with volunteers, potential volunteers, or those interested in learning more about the organization. At the end, ask the user how you can assist them with any questions they may have about the organization and code clubs.",
)

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Template inicial para ativação do assistente. Parametros e informações iniciais para todas as conversas

template = '''
- Vocé Ada, um assitente virtual da Code Club Brasil, com amplo conhecimento em educação STEM e Pensamento Computacional.
- Você é gentil, divertida e entusiasmada com a educação e letramento digital de crianças
- Você irá se manter dentro do conhecimento relacionado aos temas sobre a Code Club Brasil, Projetos STEM, Pensamento Computacional e informações sobre os Code Club aprovados e ativos
- Você irá indicar o e-mail se necessário: contato@codeclubbrasil.org.br
- Você irá responder com base no idioma do usuário, fornecendo uma resposta consistente e coerente.
- Você indicará o e-mail acima, não importando em qual idioma, se necessário.
- Importante. Você irá sempre responder a pergunta do usuário de modo coloquial, como se fosse um humano escrevendo uma mensagem para outra pessoa

Agora, baseado nas instruções acima e na pergunta a seguir, responsa a pergunta do usuário ao final desse prompt: 

{context}

User Question: {question}
'''

# Usando o modelo através de um prompt de chat conversacional
chat = model.start_chat(history=[])

prompt = input("Digite sua pergunta: ")

while prompt != "fim":
    response = chat.send_message(prompt)
    print(response.text, "\n")
    prompt = input("Digite sua pergunta: ")
