import json
import os


class DataManager:
    def __init__(self, estruturas_path, solucoes_path, atividades_path):
        self.estruturas_path = estruturas_path
        self.solucoes_path = solucoes_path
        self.atividades_path = atividades_path
        self.estruturas = self.carregar_dados(self.estruturas_path)
        self.solucoes = self.carregar_dados(self.solucoes_path)
        self.atividades = self.carregar_dados(self.atividades_path)

    def carregar_dados(self, nome_arquivo):
        """Carrega dados de um arquivo JSON."""
        caminho_completo = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", nome_arquivo)
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
