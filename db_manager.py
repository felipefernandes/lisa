from bson.objectid import ObjectId
from datetime import datetime, timezone


class DBManager:
    def __init__(self, mongo):
        self.mongo = mongo

    # Armazena roteiro
    def armazenar_roteiro(self, roteiro):
        novo_roteiro = {
            "conteudo": roteiro,
            "data_criacao": datetime.now(timezone.utc).replace(tzinfo=None)
        }
        result = self.mongo.db.roteiros.insert_one(novo_roteiro)
        return str(result.inserted_id)

    # Metodo para armazenar avaliacao
    def armazenar_avaliacao(self, roteiro_id, avaliacao, comentario):
        nova_avaliacao = {
            "roteiro_id": ObjectId(roteiro_id),
            "avaliacao": avaliacao,
            "comentario": comentario,
            "data_avaliacao": datetime.now(timezone.utc).replace(tzinfo=None)

        }
        self.mongo.db.avaliacoes.insert_one(nova_avaliacao)
