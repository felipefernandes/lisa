import json
import os


def carregar_dados(nome_arquivo):
    """Carrega dados de um arquivo JSON."""
    caminho_completo = os.path.join(
        os.path.dirname(__file__), "data", nome_arquivo)
    try:
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado em '{
              caminho_completo}'.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Formato inválido de JSON em '{caminho_completo}'.")
        return None


def criacao_dataframe_solucoes(solucoes):
    try:
        solucoes = dados.carregar_dados("solucoes.json")
        df_solucoes = pln.criar_dataframe(solucoes)
        df_solucoes = pln.adicionar_embeddings(df_solucoes, "solucao")
    except Exception as e:
        print(
            f"Erro ao criar ou adicionar embeddings ao DataFrame de soluções: {str(e)}")
