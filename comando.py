import os
import subprocess
import webbrowser
import zipfile

def executar_comando(comando):
    comando = comando.lower()

    if comando.startswith("criar arquivo"):
        nome = comando.replace("criar arquivo", "").strip()

        conteudo = input("O que deseja colocar no arquivo: ")

        with open(nome, "w") as arquivo:
            arquivo.write(conteudo)

        print(f"Arquivo '{nome}' criado com sucesso!")

    elif comando.startswith("extrair"):
        try:
            partes = comando.split(" em ")

            arquivo_zip = partes[0].replace("extrair ", "").strip()
            destino = partes[1].strip()

            os.makedirs(destino, exist_ok=True)

            with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
                zip_ref.extractall(destino)

            print(f"Extraído com sucesso!")

        except Exception as e:
            print("Erro ao extrair:", e)
    
    elif comando.startswith("pesquisar"):
        termo = comando.replace("pesquisar", "").strip()
        termo = termo.replace(" ", "+")

        url = f"https://www.google.com/search?q={termo}"
        print(f"Abrindo busca para: {termo}...")
        webbrowser.open(url)
    
    elif comando.startswith("abrir"):
        app = comando.replace("abrir", "").strip()

        apps = {
            "bloco de notas": "notepad.exe",
            "notepad": "notepad.exe",
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "vscode": "Code.exe",
            "discord": "Discord.exe"
        }

    if app in apps:
        try:
            os.startfile(apps[app])
            print(f"Abrindo {app}...")
        except Exception as e:
            print("Erro ao abrir:", e)
    else:
        print("Aplicativo não conhecido.")

while True:
    cmd = input(">: ")
    executar_comando(cmd)