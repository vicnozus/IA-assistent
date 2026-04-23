import customtkinter as ctk

# Configuração visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PainelLateral(ctk.CTk):
    def __init__(self):
        super().__init__()

        largura = 400
        altura = 600

        # Pega a resolução do monitor
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)

        # Aplica a geometria (Faltou essa linha no seu original para os números funcionarem!)
        self.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # --- BOTÃO PARA FECHAR (O "X") ---
        # Colocamos ele no topo direito
        self.btn_fechar = ctk.CTkButton(self, text="X", width=30, height=30, 
                                        fg_color="red", hover_color="#8B0000", 
                                        command=self.destroy)
        self.btn_fechar.place(x=360, y=10) # 'place' para fixar no cantinho

        # Título / Cabeçalho
        self.titulo = ctk.CTkLabel(self, text="SISTEMA ASSISTENTE", font=("Courier", 20, "bold"), text_color="#00FFCC")
        self.titulo.pack(pady=(40, 20)) # Aumentei o espaço no topo para não bater no botão

        # Console de Log
        self.console_log = ctk.CTkTextbox(self, width=260, height=200, fg_color="#101010", text_color="#00FF00")
        self.console_log.pack(pady=20)
        self.console_log.insert("0.0", "> Sistema Iniciado...\n> Aguardando entrada...")
        
        # Campo de Entrada
        self.entrada = ctk.CTkEntry(self, placeholder_text="Digite sua ordem...", width=250, height=40)
        self.entrada.pack(pady=10)
        self.entrada.bind("<Return>", self.enviar_comando)

        # Console de Log

        # --- ATALHO DE TECLADO ---
        # Se você apertar a tecla 'Esc', o programa fecha sozinho
        self.bind("<Escape>", lambda e: self.destroy())

    def enviar_comando(self, event):
        comando = self.entrada.get()
        self.console_log.insert("end", f"\n> Processando: {comando}")
        self.console_log.see("end") # Faz o scroll automático para a última linha
        self.entrada.delete(0, 'end')

if __name__ == "__main__":
    app = PainelLateral()
    app.mainloop()