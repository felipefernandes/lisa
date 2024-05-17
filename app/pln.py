import pandas as pd
import numpy as np
import google.generativeai as genai
from config import GEMINIKEY

# Configuração do GenerativeAI
genai.configure(api_key=GEMINIKEY)


class PLNManager:
    def __init__(self, model):
        self.model = model

    def criar_dataframe(self, dados):
        """Cria um DataFrame a partir de uma lista de dicionários."""
        return pd.DataFrame(dados)

    def adicionar_embeddings(self, df, coluna_conteudo, coluna_titulo=''):
        """Adiciona embeddings a um DataFrame."""
        if coluna_titulo:
            df["Embeddings"] = df.apply(
                lambda row: genai.embed_content(
                    model=self.model, content=row[coluna_conteudo], title=row[coluna_titulo], task_type="RETRIEVAL_DOCUMENT")["embedding"],
                axis=1
            )
        else:
            df["Embeddings"] = df.apply(
                lambda row: genai.embed_content(
                    model=self.model, content=row[coluna_conteudo], task_type="RETRIEVAL_DOCUMENT")["embedding"],
                axis=1
            )
        return df

    def buscar_indice_mais_similar(self, embeddings, base):
        """Encontra o índice da entrada mais similar na base."""
        produtos_escalares = np.dot(np.stack(base['Embeddings']), embeddings)
        return np.argmax(produtos_escalares)

    def buscar_solucao_consulta(self, consulta, base):
        """Busca a solução mais similar à consulta."""
        embedding_da_consulta = genai.embed_content(
            model=self.model, content=consulta, task_type="RETRIEVAL_QUERY")["embedding"]
        indice = self.buscar_indice_mais_similar(embedding_da_consulta, base)
        return base.iloc[indice]['solucao']

    def gerar_e_buscar_consulta(self, consulta, base, limite_relevancia=0.6):
        """Gera embeddings da consulta e busca estruturas relevantes."""
        embedding_da_consulta = genai.embed_content(
            model=self.model, content=consulta, task_type="RETRIEVAL_QUERY")["embedding"]
        produtos_escalares = np.dot(
            np.stack(base['Embeddings']), embedding_da_consulta)
        indices_relevantes = np.where(
            produtos_escalares >= limite_relevancia)[0]
        resultados_relevantes = base.iloc[indices_relevantes]['nome'].tolist()
        if resultados_relevantes:
            return f"Estruturas recomendadas: {', '.join(resultados_relevantes[:3])}"
        else:
            return f"Estrutura recomendada: {base.iloc[np.argmax(produtos_escalares)]['nome']}"


# Instância global de PLNManager
pln_manager = PLNManager("models/embedding-001")


def busca(prompt, df_estruturas):
    """
    Função principal para realizar a busca de estruturas libertadoras relevantes 
    com base no prompt do usuário.
    """
    return pln_manager.gerar_e_buscar_consulta(prompt, df_estruturas)
