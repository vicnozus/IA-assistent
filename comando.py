import os
import subprocess
import webbrowser
import zipfile
import win32com.client
from ia_key import inteligencia_assistente 

# --- FUNÇÕES DE APOIO ---

def resolver_atalho(caminho_atalho):
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        atalho = shell.CreateShortcut(caminho_atalho)
        return atalho.TargetPath
    except:
        return caminho_atalho

def buscar_apps_instalados():
    pastas_atalhos = [
        os.path.join(os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs"),
        os.path.join(os.environ["AppData"], "Microsoft", "Windows", "Start Menu", "Programs")
    ]
    
    meus_apps = {}
    for pasta in pastas_atalhos:
        if os.path.exists(pasta):
            for raiz, dirs, arquivos in os.walk(pasta):
                for arquivo in arquivos:
                    if arquivo.endswith(".lnk"):
                        nome_limpo = arquivo.replace(".lnk", "").lower()
                        caminho_completo = os.path.join(raiz, arquivo)
                        meus_apps[nome_limpo] = caminho_completo
    return meus_apps

# Agora sim o catálogo é carregado corretamente
CATALOGO_APPS = buscar_apps_instalados()

# --- AÇÕES DO ASSISTENTE ---

def abrir_app(nome_app):
    nome_app = nome_app.lower()
    encontrado = None
    nome_real = ""
    
    for nome_no_pc in CATALOGO_APPS:
        if nome_app in nome_no_pc:
            encontrado = CATALOGO_APPS[nome_no_pc]
            nome_real = nome_no_pc
            break
            
    if encontrado:
        # Se for atalho (.lnk), resolve para o caminho real (.exe)
        caminho_final = resolver_atalho(encontrado) if encontrado.endswith(".lnk") else encontrado

        print(f"🚀 Tentando abrir: {caminho_final}")
        try:
            os.startfile(caminho_final)
        except Exception as e:
            print(f"⚠️ Erro no startfile, tentando método secundário...")
            os.system(f'start "" "{encontrado}"')

def pesquisar_google(termo):
    url = f"https://www.google.com/search?q={termo.replace(' ', '+')}"
    print(f"🔍 Pesquisando no Google: {termo}")
    webbrowser.open(url)

def criar_arquivo_texto(valor):
    try:
        nome = valor.strip()
        if "." not in nome: nome += ".txt"
        
        conteudo = input(f"O que deseja escrever em '{nome}': ")
        with open(nome, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
        print(f"✅ Arquivo '{nome}' criado com sucesso!")
    except Exception as e:
        print("❌ Erro ao criar o arquivo:", e)

def extrair_zip(valor):
    try:
        # Lógica simples: extrai o zip para uma pasta com o mesmo nome
        destino = valor.replace(".zip", "")
        os.makedirs(destino, exist_ok=True)
        with zipfile.ZipFile(valor, 'r') as zip_ref:
            zip_ref.extractall(destino)
        print(f"✅ Extraído com sucesso para /{destino}!")
    except Exception as e:
        print("❌ Erro ao extrair:", e)

# --- LOOP PRINCIPAL ---
print("Assistente IA Ativo!")

while True:
    comando_usuario = input("\nO que deseja? > ")
    
    if comando_usuario.lower() in ["sair", "parar"]:
        break

    dados = inteligencia_assistente(comando_usuario)

    if dados:
        acao = dados.get("acao")
        valor = dados.get("valor")

        if acao == "abrir_app":
            abrir_app(valor)
        
        elif acao == "pesquisar":
            pesquisar_google(valor)
            
        elif acao == "criar_arquivo":
            criar_arquivo_texto(valor)
            
        elif acao == "extrair_zip":
            extrair_zip(valor)
            
        else:
            print(f"🤔 IA sugeriu '{acao}', mas ainda não implementamos essa função.")
    else:
        print("📴 Falha na conexão com o cérebro.")