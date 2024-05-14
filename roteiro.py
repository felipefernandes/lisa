import random
import pln


def encontrar_estrutura_adequada(estruturas_dict, label_alvo):
    """Encontra a primeira estrutura com o label desejado."""
    for nome, data in estruturas_dict.items():
        if data["label"] == label_alvo:
            return data
    return None


def gerar_roteiro(prompt, estruturas, atividades):
    """Gera um roteiro de retrospectiva."""
    # Usar a função busca para obter sugestões de ELs
    resultado_busca = pln.busca(prompt, pln.df_estruturas)
    if "Estruturas recomendadas:" in resultado_busca:
        estruturas_recomendadas_nomes = resultado_busca.split(
            "Estruturas recomendadas: ")[1].strip().split(", ")
    else:
        estruturas_recomendadas_nomes = [resultado_busca.split(
            "Estrutura recomendada: ")[1].strip()]

    # Encontrar as ELs na lista de estruturas usando os nomes recomendados
    estruturas_recomendadas = [
        estrutura for estrutura in estruturas if estrutura["nome"] in estruturas_recomendadas_nomes]

    # Converter a lista de estruturas para dicionário
    estruturas_dict = {estrutura["nome"]
        : estrutura for estrutura in estruturas}

    # Encontrar as ELs adequadas para cada seção
    reflexao_estrutura = encontrar_estrutura_adequada(
        estruturas_dict, "Revelar")
    decisao_estrutura = encontrar_estrutura_adequada(
        estruturas_dict, "Analisar")

    # Gerar roteiro
    roteiro = {}
    roteiro["Abertura"] = random.choice(list(atividades["abertura"].items()))
    roteiro["Reflexão e Colhendo Dados"] = (reflexao_estrutura["nome"], {
        "descricao": reflexao_estrutura["proposito"],
        "formacao": "Variável",
        "duracao": reflexao_estrutura["duracao"]
    }) if reflexao_estrutura else random.choice(list(atividades["reflexao"].items()))

    roteiro["Decidindo o que fazer"] = (decisao_estrutura["nome"], {
        "descricao": decisao_estrutura["proposito"],
        "formacao": "Variável",
        "duracao": decisao_estrutura["duracao"]
    }) if decisao_estrutura else random.choice(list(atividades["decisao"].items()))

    roteiro["Fechamento"] = random.choice(
        list(atividades["fechamento"].items()))

    return roteiro, resultado_busca


def print_roteiro(roteiro):
    """Imprime o roteiro de forma organizada."""
    print("# Retrospectiva (roteiro)\n")
    for secao, (atividade, detalhes) in roteiro.items():
        print(f"## {secao}")
        print(f"**Duração:** {detalhes['duracao']} min\n")
        print(f"**Formação:** {detalhes['formacao']}\n")
        print(f"**Atividade:** {atividade}\n")
        print(f"{detalhes['descricao']}")
        print()
