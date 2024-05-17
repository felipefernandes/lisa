from flask import Flask, render_template, request
from app.data_manager import DataManager
from app.embedding_manager import EmbeddingManager
from app.roteiro import RoteiroManager

app = Flask(__name__)

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
            return render_template("index.html", user_input=user_input, roteiro=roteiro_gerado, resultado_busca=resultado_busca)
        return render_template("index.html")
    except Exception as e:
        print(f"Erro no processamento da requisição: {str(e)}")
        return render_template("index.html", user_input=user_input, roteiro="", resultado_busca="")


if __name__ == "__main__":
    app.run(debug=True)
