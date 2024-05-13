# -*- coding: utf-8 -*-
"""
LiSA - Assistente Virtual para Roteiros de Retrospectivas
"""

import dados
import pln
import roteiro
import google.generativeai as genai
from config import GEMINIKEY

# Carregamento de Dados
estruturas = dados.carregar_dados("estruturas.json")
solucoes = dados.carregar_dados("solucoes.json")
atividades = dados.carregar_dados("atividades.json")

# Configuração do GenerativeAI
genai.configure(api_key=GEMINIKEY)

# Inicializando o modelo de embeddings
model = "models/embedding-001"

# ---- Criação dos DataFrames ----

df_estruturas = pln.criar_dataframe(estruturas)
df_estruturas = pln.adicionar_embeddings(df_estruturas, "proposito", "nome")
df_estruturas = pln.adicionar_embeddings(df_estruturas, "label", "")

df_solucoes = pln.criar_dataframe(solucoes)
df_solucoes = pln.adicionar_embeddings(df_solucoes, "solucao")

# ---- Configuração do Modelo Generativo ----

model_generative_config = {
    "temperature": 2,
    "candidate_count": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

model_generative_safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_instruction = "Seu nome é Lisa. Uma assistente virtual, com habilidades de um Coach profissional e experiente facilitadora de reuniões e atividades presenciais e online com amplo conhecimento de aplicação de Estruturas Libertadoras. Você irá se manter dentro do conhecimento relacionado.Você irá responder com base no idioma do usuário, fornecendo uma resposta consistente e coerente. Você não usará o termo 'sprint' para tornar suas respostas mais abrangentes a diferentes contextos, como times que utilizam metodologia Kanban, por exemplo. Sempre pergunte ao usuário se ele deseja mais alguma informação e o lembre que a palavra-chave para terminar a conversa é 'fim'"

model_generative = genai.GenerativeModel("gemini-1.5-pro-latest",
                                         generation_config=model_generative_config,
                                         system_instruction=system_instruction,
                                         safety_settings=model_generative_safety_settings)

chat = model_generative.start_chat(history=[
    {"role": "user", "parts": ["Se apresente."]},
])


def update_chat_history(chat, role, message):
    """Adiciona uma nova entrada ao histórico da conversa."""
    chat.history.append({"role": role, "parts": [message]})

# ---- Interação com o Usuário ----


print(f"Olá eu sou Lisa!👋\n Uma assistente virtual especialista em criar roteiros para retrospectivas.")
print()
print("A seguir, você pode descrever o contexto da sua equipe/time, e em seguida me fazer perguntas sobre detalhes da execução de cada uma das atividades, ok?")
print("-"*25)

user_prompt = input(
    "Descreva o contexto recente do time/equipe que deseja criar um roteiro: ")
roteiro_gerado, resultado_busca = roteiro.gerar_roteiro(
    user_prompt, estruturas, atividades)
roteiro.print_roteiro(roteiro_gerado)

update_chat_history(
    chat, "user", f"Solicito a criação de um roteiro de retrospectiva para {user_prompt}")
update_chat_history(chat, "model", f"{roteiro_gerado}")

print("-"*25)
print("Gostou do seu roteiro? Se quiser mais detalhes sobre as atividades é só me perguntar, \nou se desejar terminar a conversa, envie a mensagem 'fim'.")
print()

while True:
    user_prompt = input(">>> ")
    if user_prompt.strip().lower() == "fim":
        print("Até mais! 👋")
        break
    resposta = chat.send_message(user_prompt)
    print(resposta.text)
