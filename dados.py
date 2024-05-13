import json
import os

def carregar_dados(nome_arquivo):
    """Carrega dados de um arquivo JSON."""
    caminho_completo = os.path.join(os.path.dirname(__file__), "data", nome_arquivo)
    try:
        with open(caminho_completo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado em '{caminho_completo}'.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Formato inválido de JSON em '{caminho_completo}'.")
        return None

# Estruturas
estruturas = carregar_dados("data/estruturas.json")

# Soluções
solucoes = carregar_dados("data/solucoes.json")

# Atividades
atividades = carregar_dados("data/atividades.json")