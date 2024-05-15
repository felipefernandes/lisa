import pln
import dados
import roteiro
from flask import Flask, render_template, request

app = Flask(__name__)

# Carregamento de Dados (movido para cá para ser global)
try:
    estruturas = dados.carregar_dados("estruturas.json")
    solucoes = dados.carregar_dados("solucoes.json")
    atividades = dados.carregar_dados("atividades.json")
except Exception as e:
    print(f"Erro ao carregar dados: {str(e)}")

# ---- Criação dos DataFrames ----
try:
    df_estruturas = pln.criar_dataframe(estruturas)
    df_estruturas = pln.adicionar_embeddings(
        df_estruturas, "proposito", "nome")
    df_estruturas = pln.adicionar_embeddings(df_estruturas, "label", "")
except Exception as e:
    print(
        f"Erro ao criar ou adicionar embeddings ao DataFrame de estruturas: {str(e)}")

try:
    df_solucoes = pln.criar_dataframe(solucoes)
    df_solucoes = pln.adicionar_embeddings(df_solucoes, "solucao")
except Exception as e:
    print(
        f"Erro ao criar ou adicionar embeddings ao DataFrame de soluções: {str(e)}")

pln.df_estruturas = df_estruturas  # Atribuindo o valor à variável global

# Inicializando o modelo de embeddings (movido para cá para ser global)
model = "models/embedding-001"


def gerar_roteiro(user_input):
    try:
        return f"Roteiro gerado com base na entrada: {user_input}"
    except Exception as e:
        print(f"Erro na função: {str(e)}")
        return f"Erro ao gerar roteiro: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def home():
    try:
        user_input = ""
        if request.method == "POST":
            user_input = request.form.get("user_input")
            roteiro_gerado, resultado_busca = roteiro.gerar_roteiro(
                user_input, estruturas, atividades)
            return render_template("index.html", user_input=user_input, roteiro=roteiro_gerado, resultado_busca=resultado_busca)
        return render_template("index.html")
    except Exception as e:
        print(f"Erro no processamento da requisição: {str(e)}")
        return render_template("index.html", user_input=user_input, roteiro="", resultado_busca="")


if __name__ == "__main__":
    app.run(debug=True)
