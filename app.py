from flask import Flask, render_template, request
import roteiro
import dados
import pln

app = Flask(__name__)

# Carregamento de Dados (movido para cá para ser global)
estruturas = dados.carregar_dados("estruturas.json")
solucoes = dados.carregar_dados("solucoes.json")
atividades = dados.carregar_dados("atividades.json")

# ---- Criação dos DataFrames ----
df_estruturas = pln.criar_dataframe(estruturas)
df_estruturas = pln.adicionar_embeddings(df_estruturas, "proposito", "nome")
df_estruturas = pln.adicionar_embeddings(df_estruturas, "label", "")

df_solucoes = pln.criar_dataframe(solucoes)
df_solucoes = pln.adicionar_embeddings(df_solucoes, "solucao")

pln.df_estruturas = df_estruturas  # Atribuindo o valor à variável global

# Inicializando o modelo de embeddings (movido para cá para ser global)
model = "models/embedding-001"


def gerar_roteiro(user_input):
    return f"Roteiro gerado com base na entrada: {user_input}"


@app.route("/", methods=["GET", "POST"])
def home():
    user_input = ""
    if request.method == "POST":
        user_input = request.form.get("user_input")
        roteiro_gerado, resultado_busca = roteiro.gerar_roteiro(
            user_input, estruturas, atividades)
        return render_template("index.html", user_input=user_input, roteiro=roteiro_gerado, resultado_busca=resultado_busca)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
