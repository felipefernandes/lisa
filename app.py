import pln
import dados
import roteiro
from flask import Flask, render_template, request

app = Flask(__name__)

# ---- Criação dos DataFrames ----


def criacao_dataframe_estruturas(estruturas):
    try:
        df_estruturas = pln.criar_dataframe(estruturas)
        df_estruturas = pln.adicionar_embeddings(
            df_estruturas, "proposito", "nome")
        df_estruturas = pln.adicionar_embeddings(df_estruturas, "label", "")

        pln.df_estruturas = df_estruturas  # Atribuindo o valor à variável global
    except Exception as e:
        print(
            f"Erro ao criar ou adicionar embeddings ao DataFrame de estruturas: {str(e)}")


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

            atividades = dados.carregar_dados("atividades.json")
            estruturas = dados.carregar_dados("estruturas.json")
            criacao_dataframe_estruturas(estruturas)

            roteiro_gerado, resultado_busca = roteiro.gerar_roteiro(
                user_input, estruturas, atividades)

            return render_template("index.html", user_input=user_input, roteiro=roteiro_gerado, resultado_busca=resultado_busca)
        return render_template("index.html")
    except Exception as e:
        print(f"Erro no processamento da requisição: {str(e)}")
        return render_template("index.html", user_input=user_input, roteiro="", resultado_busca="")


if __name__ == "__main__":
    app.run(debug=True)
