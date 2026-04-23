import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv() # Isso carrega o arquivo .env
chave = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=chave)

def inteligencia_assistente(comando_usuario):
    # Usando o modelo que o diagnóstico aprovou!
    modelo_vitorioso = 'models/gemini-2.5-flash'
    
    prompt = f"""
    Você é o motor de um assistente de PC.
    Converta o comando do usuário em um JSON puro.
    
    Ações: "pesquisar", "abrir_app", "criar_arquivo", "extrair_zip".
    
    Exemplo: "procure python no google" -> {{"acao": "pesquisar", "valor": "python"}}
    
    Comando do usuário: "{comando_usuario}"
    Responda APENAS o JSON, sem markdown.
    """
    
    try:
        response = client.models.generate_content(
            model=modelo_vitorioso,
            contents=prompt
        )
        
        # Limpeza para garantir que o JSON seja lido corretamente
        texto = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(texto)
        
    except Exception as e:
        print(f"Erro no processamento: {e}")
        return None

if __name__ == "__main__":
    # Teste de fogo!
    teste = inteligencia_assistente("abre o vscode pra mim")
    print(f"Resultado do cérebro: {teste}")