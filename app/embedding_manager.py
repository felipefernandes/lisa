from app.pln import pln_manager


class EmbeddingManager:
    def __init__(self, model):
        self.model = model
        self.df_estruturas = None
        self.df_solucoes = None

    def criar_e_adicionar_embeddings(self, data, *cols):
        try:
            df = pln_manager.criar_dataframe(data)
            for col in cols:
                df = pln_manager.adicionar_embeddings(df, *col)
            return df
        except Exception as e:
            print(f"Erro ao criar/adicionar embeddings: {str(e)}")
            return None

    def process_data(self, estruturas, solucoes):
        self.df_estruturas = self.criar_e_adicionar_embeddings(
            estruturas, ("proposito", "nome"), ("label", ""))
        self.df_solucoes = self.criar_e_adicionar_embeddings(
            solucoes, ("solucao",))
        pln_manager.df_estruturas = self.df_estruturas
