import customtkinter as ctk
from comando import processar_comando

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class NovaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nova")
        self.geometry("900x550")
        self.minsize(700, 450)

        self.configure(fg_color="#0b0b0f")

        # Layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Menu lateral
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color="#111116", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="NOVA",
            font=("Segoe UI", 28, "bold"),
            text_color="#ff2b2b"
        )
        self.logo.pack(pady=(30, 5))

        self.subtitulo = ctk.CTkLabel(
            self.sidebar,
            text="Assistente Inteligente",
            font=("Segoe UI", 13),
            text_color="#aaaaaa"
        )
        self.subtitulo.pack(pady=(0, 30))

        self.status = ctk.CTkLabel(
            self.sidebar,
            text="● Online",
            text_color="#45ff89",
            font=("Segoe UI", 14)
        )
        self.status.pack(pady=10)

        self.info = ctk.CTkLabel(
            self.sidebar,
            text="Reconhecimento\nde intenção",
            text_color="#777777",
            justify="center"
        )
        self.info.pack(pady=20)

        # Área principal
        self.main = ctk.CTkFrame(self, fg_color="#0b0b0f", corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        self.titulo = ctk.CTkLabel(
            self.main,
            text="Olá, Victor. Como posso ajudar?",
            font=("Segoe UI", 24, "bold"),
            text_color="#ffffff"
        )
        self.titulo.grid(row=0, column=0, sticky="w", pady=(0, 15))

        self.chat = ctk.CTkTextbox(
            self.main,
            fg_color="#15151c",
            text_color="#eeeeee",
            corner_radius=15,
            font=("Segoe UI", 14)
        )
        self.chat.grid(row=1, column=0, sticky="nsew")
        self.chat.insert("end", "Nova: Sistema iniciado com sucesso.\n\n")
        self.chat.configure(state="disabled")

        # Campo de comando
        self.input_frame = ctk.CTkFrame(self.main, fg_color="#0b0b0f")
        self.input_frame.grid(row=2, column=0, sticky="ew", pady=(15, 0))
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entrada = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Digite um comando... ex: abra o navegador",
            height=45,
            fg_color="#15151c",
            border_color="#ff2b2b",
            text_color="#ffffff",
            font=("Segoe UI", 14)
        )
        self.entrada.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entrada.bind("<Return>", self.enviar_comando)

        self.botao = ctk.CTkButton(
            self.input_frame,
            text="Enviar",
            height=45,
            fg_color="#b80000",
            hover_color="#ff2b2b",
            font=("Segoe UI", 14, "bold"),
            command=self.enviar_comando
        )
        self.botao.grid(row=0, column=1)

    def escrever_chat(self, texto):
        self.chat.configure(state="normal")
        self.chat.insert("end", texto + "\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def enviar_comando(self, event=None):
        comando = self.entrada.get().strip()

        if not comando:
            return

        self.entrada.delete(0, "end")

        self.escrever_chat(f"Você: {comando}")

        # Processar o comando e obter a resposta
        resposta = processar_comando(comando)

        self.escrever_chat(f"Nova: {resposta}")


if __name__ == "__main__":
    app = NovaApp()
    app.mainloop()