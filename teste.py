import os
import win32com.client

def testar_abertura_chrome():
    # 1. Caminho que deu erro antes (o atalho do Menu Iniciar)
    # Nota: O 'r' antes das aspas evita problemas com as barras invertidas \
    caminho_atalho = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"

    print(f"--- Iniciando Teste de Automação ---")
    
    if not os.path.exists(caminho_atalho):
        print("❌ Erro: O arquivo de atalho não foi encontrado nesse caminho.")
        return

    try:
        # 2. Usando a biblioteca para 'traduzir' o atalho
        shell = win32com.client.Dispatch("WScript.Shell")
        atalho = shell.CreateShortcut(caminho_atalho)
        
        caminho_real = atalho.TargetPath
        print(f"✅ Sucesso! O atalho aponta para: {caminho_real}")

        # 3. Executando o .exe real
        print("🚀 Tentando disparar o processo...")
        os.startfile(caminho_real)
        print("🏁 Comando enviado ao Windows!")

    except Exception as e:
        print(f"❌ Falha no teste: {e}")

if __name__ == "__main__":
    testar_abertura_chrome()