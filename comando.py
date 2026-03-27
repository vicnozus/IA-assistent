import os
import subprocess
import webbrowser
import zipfile
from intencao import pesquisar, comando_, extr, apps_

def tem_palavra(lista, comando):
    palavras = comando.split()
    return any(p in palavras for p in lista)

def executar_comando(comando):
    comando = comando.lower()

    if tem_palavra(comando_, comando):
        nome = comando.replace("criar arquivo", "").strip()

        conteudo = input("O que deseja colocar no arquivo: ")

        with open(nome, "w") as arquivo:
            arquivo.write(conteudo)

        print(f"Arquivo '{nome}' criado com sucesso!")

    elif tem_palavra(extr, comando):
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
    
    if tem_palavra(pesquisar, comando):
        termo = comando.replace("pesquisar", "").strip()
        termo = termo.replace(" ", "+")

        url = f"https://www.google.com/search?q={termo}"
        print(f"Abrindo busca para: {termo}...")
        webbrowser.open(url)
    
    elif tem_palavra(apps_, comando):
        app = comando.replace("abrir", "").strip()

        apps = {
            "bloco de notas": "notepad.exe",
            "notepad": "notepad.exe",
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "vscode": "Code.exe",
            "discord": "Discord.exe",
            "calculadora": "calc.exe"
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
