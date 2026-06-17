pesquisar = ["pesquisar", "pesquisa", "busca", "buscar", "procura", "procurar"]
comando_arquivo = ["criar", "crie", "faça", "faz"]
extrair = ["extrair", "extraia"]
apps = ["abrir", "abri", "abra", "abre"]


def interpretar_local(comando):
    comando = comando.lower().strip()

    for palavra in pesquisar:
        if palavra in comando:
            valor = comando.replace(palavra, "").strip()
            return {"acao": "pesquisar", "valor": valor}

    for palavra in apps:
        if palavra in comando:
            valor = comando.replace(palavra, "").strip()
            return {"acao": "abrir_app", "valor": valor}

    for palavra in comando_arquivo:
        if palavra in comando and "arquivo" in comando:
            valor = comando.replace(palavra, "").replace("arquivo", "").strip()
            return {"acao": "criar_arquivo", "valor": valor}

    for palavra in extrair:
        if palavra in comando:
            valor = comando.replace(palavra, "").strip()
            return {"acao": "extrair_zip", "valor": valor}

    return None

def limpar_valor(valor):
    palavras_ignorar = ["o", "a", "os", "as", "um", "uma", "para", "pra", "mim", "por", "favor"]
    
    palavras = valor.lower().split()
    palavras_filtradas = [p for p in palavras if p not in palavras_ignorar]

    return " ".join(palavras_filtradas).strip()