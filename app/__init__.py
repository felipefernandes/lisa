from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from app.data_manager import DataManager
from app.embedding_manager import EmbeddingManager
from app.roteiro import RoteiroManager
from config_db import init_db
from db_manager import DBManager

app = Flask(__name__)

# Inicialização do MongoDB
mongo = init_db(app)
db_manager = DBManager(mongo)

# Inicialização dos gerenciadores
data_manager = DataManager(
    "estruturas.json", "solucoes.json", "atividades.json")
embedding_manager = EmbeddingManager("models/embedding-001")

# Processamento dos dados
embedding_manager.process_data(data_manager.estruturas, data_manager.solucoes)

# Inicialização do RoteiroManager
roteiro_manager = RoteiroManager(
    data_manager.estruturas, data_manager.atividades)


@app.route("/", methods=["GET", "POST"])
def home():
    try:
        user_input = ""
        if request.method == "POST":
            user_input = request.form.get("user_input")
            roteiro_gerado, resultado_busca = roteiro_manager.gerar_roteiro(
                user_input)
            roteiro_id = db_manager.armazenar_roteiro(roteiro_gerado)
            return render_template("index.html", user_input=user_input, roteiro=roteiro_gerado, resultado_busca=resultado_busca, roteiro_id=roteiro_id)
        return render_template("index.html")
    except Exception as e:
        print(f"Erro no processamento da requisição: {str(e)}")
        return render_template("index.html", user_input=user_input, roteiro="", resultado_busca="")


@app.route("/avaliar", methods=["POST"])
def avaliar():
    try:
        roteiro_id = request.form.get("roteiro_id")
        avaliacao = request.form.get("avaliacao")
        comentario = request.form.get("comentario", "")
        db_manager.armazenar_avaliacao(roteiro_id, avaliacao, comentario)
        return redirect(url_for('home'))
    except Exception as e:
        print(f"Erro ao processar a avaliação: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
