INTENCOES = {
    "pesquisar": {
        "acao": "pesquisar",
        "gatilhos": ["pesquisar", "pesquisa", "buscar", "busca", "procurar", "procura", "encontrar", "encontra", "procure", "pesquise"]
    },
    "abrir_app": {
        "acao": "abrir_app",
        "gatilhos": ["abrir", "abra", "abre", "abri"]
    },
    "criar_arquivo": {
        "acao": "criar_arquivo",
        "gatilhos": ["criar", "crie", "fazer", "faça", "faz"],
        "obrigatorias": ["arquivo"]
    },
    "extrair_zip": {
        "acao": "extrair_zip",
        "gatilhos": ["extrair", "extraia", "descompactar", "descompacte"]
    }
}

PALAVRAS_IGNORAR = [
    "o", "a", "os", "as",
    "um", "uma", "é", "são",
    "para", "pra", "mim",
    "por", "favor", "pa",
    "porfavor", "que", "qual", "quais",
    "me", "minha", "meu",
]


def limpar_valor(valor):
    palavras = valor.lower().split()
    palavras_filtradas = []

    for palavra in palavras:
        if palavra not in PALAVRAS_IGNORAR:
            palavras_filtradas.append(palavra)

    return " ".join(palavras_filtradas).strip()


def interpretar_local(comando):
    comando = comando.lower().strip()
    palavras = comando.split()

    for nome_intencao, dados in INTENCOES.items():
        gatilhos = dados["gatilhos"]
        obrigatorias = dados.get("obrigatorias", [])

        encontrou_gatilho = False
        gatilho_usado = ""

        for gatilho in gatilhos:
            if gatilho in palavras:
                encontrou_gatilho = True
                gatilho_usado = gatilho
                break

        if not encontrou_gatilho:
            continue

        for obrigatoria in obrigatorias:
            if obrigatoria not in palavras:
                continue

        valor = comando.replace(gatilho_usado, "").strip()

        for obrigatoria in obrigatorias:
            valor = valor.replace(obrigatoria, "").strip()

        valor = limpar_valor(valor)

        return {
            "acao": dados["acao"],
            "valor": valor
        }

    return None