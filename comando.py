"""Ações executadas pela Nova, sem código específico da interface."""

import os
from functools import lru_cache
from pathlib import Path
import zipfile

import requests
import win32com.client

from ia_key import inteligencia_assistente
from intencao import interpretar_local, limpar_valor


def resolver_atalho(caminho_atalho):
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        return shell.CreateShortcut(str(caminho_atalho)).TargetPath
    except Exception:
        return str(caminho_atalho)


@lru_cache(maxsize=1)
def buscar_apps_instalados():
    """Monta o catálogo apenas quando for necessário abrir um aplicativo."""
    pastas_atalhos = [
        Path(os.environ.get("ProgramData", "")) / "Microsoft/Windows/Start Menu/Programs",
        Path(os.environ.get("AppData", "")) / "Microsoft/Windows/Start Menu/Programs",
    ]
    apps = {}
    for pasta in pastas_atalhos:
        if pasta.exists():
            for atalho in pasta.rglob("*.lnk"):
                apps.setdefault(atalho.stem.casefold(), atalho)
    return apps


def abrir_app(nome_app):
    nome_app = limpar_valor(nome_app).casefold()
    if not nome_app:
        return "Me diga qual aplicativo você quer abrir."

    encontrados = [
        (nome, caminho) for nome, caminho in buscar_apps_instalados().items() if nome_app in nome
    ]
    if not encontrados:
        return f"Não encontrei um aplicativo chamado '{nome_app}'."

    nome_real, caminho = min(encontrados, key=lambda item: (len(item[0]), item[0]))
    try:
        os.startfile(str(caminho))
        return f"Abrindo aplicativo: {nome_real}."
    except OSError as erro:
        return f"Não consegui abrir '{nome_real}': {erro}."


def pesquisar_wikipedia(termo):
    termo = limpar_valor(termo)
    if not termo:
        return "Me diga o que você quer pesquisar."

    try:
        url = "https://pt.wikipedia.org/w/api.php"
        headers = {"User-Agent": "NovaAssistente/1.0"}
        busca = requests.get(
            url,
            params={"action": "query", "list": "search", "srsearch": termo, "format": "json", "utf8": 1},
            headers=headers,
            timeout=10,
        )
        busca.raise_for_status()
        resultados = busca.json().get("query", {}).get("search", [])
        if not resultados:
            return "Não encontrei nada sobre isso. Tente outro termo."

        resumo = requests.get(
            url,
            params={
                "action": "query", "prop": "extracts", "exintro": True, "explaintext": True,
                "titles": resultados[0]["title"], "format": "json", "utf8": 1,
            },
            headers=headers,
            timeout=10,
        )
        resumo.raise_for_status()
        for pagina in resumo.json().get("query", {}).get("pages", {}).values():
            texto = pagina.get("extract", "").strip()
            if texto:
                return texto[:800] + ("..." if len(texto) > 800 else "")
        return "Encontrei a página, mas ela não tem resumo disponível."
    except requests.RequestException:
        return "Não consegui pesquisar agora. Verifique sua conexão e tente novamente."
    except ValueError:
        return "A Wikipédia retornou uma resposta inválida. Tente novamente."


def preparar_nome_arquivo(nome):
    """Aceita apenas um nome de arquivo, evitando escrita em pastas arbitrárias."""
    nome = limpar_valor(nome).strip()
    if not nome:
        raise ValueError("Me diga o nome do arquivo.")
    caminho = Path(nome)
    if caminho.name != nome or nome in {".", ".."}:
        raise ValueError("Use apenas um nome de arquivo, sem pastas.")
    return caminho.with_suffix(caminho.suffix or ".txt")


def criar_arquivo_texto(nome, conteudo):
    try:
        caminho = preparar_nome_arquivo(nome)
        caminho.write_text(conteudo, encoding="utf-8")
        return f"Arquivo '{caminho.name}' criado com sucesso."
    except (OSError, ValueError) as erro:
        return f"Não consegui criar o arquivo: {erro}"


def extrair_zip(valor):
    try:
        arquivo_zip = Path(limpar_valor(valor))
        if arquivo_zip.suffix.casefold() != ".zip":
            return "Me informe um arquivo com extensão .zip."
        destino = arquivo_zip.with_suffix("")
        destino.mkdir(exist_ok=True)
        destino_resolvido = destino.resolve()
        with zipfile.ZipFile(arquivo_zip) as zip_ref:
            for membro in zip_ref.infolist():
                destino_membro = (destino / membro.filename).resolve()
                if not destino_membro.is_relative_to(destino_resolvido):
                    return "O ZIP contém um caminho inseguro e não foi extraído."
            zip_ref.extractall(destino)
        return f"ZIP extraído com sucesso para '{destino}'."
    except (OSError, zipfile.BadZipFile) as erro:
        return f"Não consegui extrair o ZIP: {erro}"


def processar_comando(comando_usuario):
    dados = interpretar_local(comando_usuario) or inteligencia_assistente(comando_usuario)
    if not isinstance(dados, dict):
        return "Não consegui entender esse comando."

    acao = dados.get("acao")
    valor = dados.get("valor", "")
    if not isinstance(valor, str):
        return "O comando recebido está em um formato inválido."

    if acao == "abrir_app":
        return abrir_app(valor)
    if acao == "pesquisar":
        return pesquisar_wikipedia(valor)
    if acao == "extrair_zip":
        return extrair_zip(valor)
    if acao == "criar_arquivo":
        return "Diga o nome do arquivo e, em seguida, o conteúdo que deseja salvar."
    return "Ainda não sei realizar essa ação."
