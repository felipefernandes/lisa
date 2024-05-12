import pandas as pd
import numpy as np
import google.generativeai as genai
from google.colab import userdata

# Configuração do GenerativeAI
GOOGLE_API_KEY = userdata.get('GEMINIKEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Inicializando o modelo de embeddings
model = "models/embedding-001"

def criar_dataframe(dados):
    """Cria um DataFrame a partir de uma lista de dicionários."""
    return pd.DataFrame(dados)

def adicionar_embeddings(df, coluna_conteudo, coluna_titulo=''):
    """Adiciona embeddings a um DataFrame."""
    if coluna_titulo:
        df["Embeddings"] = df.apply(
            lambda row: genai.embed_content(model=model, content=row[coluna_conteudo], title=row[coluna_titulo], task_type="RETRIEVAL_DOCUMENT")["embedding"], 
            axis=1
        )
    else:
        df["Embeddings"] = df.apply(
            lambda row: genai.embed_content(model=model, content=row[coluna_conteudo], task_type="RETRIEVAL_DOCUMENT")["embedding"],
            axis=1
        )
    return df

def buscar_indice_mais_similar(embeddings, base):
    """Encontra o índice da entrada mais similar na base."""
    produtos_escalares = np.dot(np.stack(base['Embeddings']), embeddings)
    return np.argmax(produtos_escalares)

def buscar_solucao_consulta(consulta, base, model):
    """Busca a solução mais similar à consulta."""
    embedding_da_consulta = genai.embed_content(model=model, content=consulta, task_type="RETRIEVAL_QUERY")["embedding"]
    indice = buscar_indice_mais_similar(embedding_da_consulta, base)
    return base.iloc[indice]['solucao']

def gerar_e_buscar_consulta(consulta, base, model, limite_relevancia=0.6):
    """Gera embeddings da consulta e busca estruturas relevantes."""
    embedding_da_consulta = genai.embed_content(model=model, content=consulta, task_type="RETRIEVAL_QUERY")["embedding"]
    produtos_escalares = np.dot(np.stack(base['LabelEmbeddings']), embedding_da_consulta)
    indices_relevantes = np.where(produtos_escalares >= limite_relevancia)[0]
    resultados_relevantes = base.iloc[indices_relevantes]['nome'].tolist()
    return resultados_relevantes[:3] if resultados_relevantes else [base.iloc[np.argmax(produtos_escalares)]['nome']]