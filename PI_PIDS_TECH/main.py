import tkinter as tk
from tkinter import messagebox
import banco
from telas import App


def tela_login() -> None:
    """Exibe uma janela de login e, ao autenticar, inicializa a aplicação principal."""
    login_root = tk.Tk()
    login_root.title("Login - PIDS Tech")
    login_root.geometry("300x160")
    login_root.resizable(False, False)

    # Widgets de login
    tk.Label(login_root, text="Usuário:").grid(row=0, column=0, padx=10, pady=(20, 5), sticky="e")
    usuario_entry = tk.Entry(login_root, width=25)
    usuario_entry.grid(row=0, column=1, pady=(20, 5))

    tk.Label(login_root, text="Senha:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    senha_entry = tk.Entry(login_root, show="*", width=25)
    senha_entry.grid(row=1, column=1, pady=5)

    def tentar_login() -> None:
        nome = usuario_entry.get().strip()
        senha = senha_entry.get().strip()
        if banco.admin_validar(nome, senha):
            # Autenticação bem-sucedida: fechar tela de login e abrir app
            login_root.destroy()
            root = tk.Tk()
            # Criar app com root
            App(root)
            root.mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")

    entrar_btn = tk.Button(login_root, text="Entrar", command=tentar_login)
    entrar_btn.grid(row=2, column=0, columnspan=2, pady=15)

    # Permitir pressionar Enter para logar
    senha_entry.bind("<Return>", lambda event: tentar_login())
    usuario_entry.focus()
    login_root.mainloop()


if __name__ == "__main__":
    # Garante que as tabelas existam
    banco.criar_tabelas()
    # Cria administrador padrão caso não exista
    banco.admin_create_default()
    # Inicia tela de login
    tela_login()