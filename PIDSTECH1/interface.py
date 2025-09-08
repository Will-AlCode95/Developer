import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class PidsTechGUI:
    def __init__(self):
        self.db = Database()
        self.root = tk.Tk()
        self.root.title("PIDS TECH - Sistema de Componentes")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.criar_interface()
        self.atualizar_lista()
    
    def criar_interface(self):
        """Cria toda a interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="PIDS TECH - Sistema de Componentes",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame para formulário
        form_frame = ttk.LabelFrame(main_frame, text="Cadastrar/Editar Componente", padding="10")
        form_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Campos do formulário
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nome_entry = ttk.Entry(form_frame, width=30)
        self.nome_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Marca:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.marca_entry = ttk.Entry(form_frame, width=30)
        self.marca_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Status:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(
            form_frame, 
            textvariable=self.status_var,
            values=["Funcionando", "Defeito", "Descarte"],
            state="readonly",
            width=27
        )
        self.status_combo.grid(row=2, column=1, padx=(10, 0), pady=5, sticky=(tk.W, tk.E))
        self.status_combo.set("Funcionando")  # Valor padrão
        
        # Botões do formulário
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.btn_cadastrar = ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar_componente)
        self.btn_cadastrar.grid(row=0, column=0, padx=5)
        
        self.btn_atualizar = ttk.Button(btn_frame, text="Atualizar", command=self.atualizar_componente)
        self.btn_atualizar.grid(row=0, column=1, padx=5)
        
        self.btn_limpar = ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos)
        self.btn_limpar.grid(row=0, column=2, padx=5)
        
        # Frame para lista de componentes
        lista_frame = ttk.LabelFrame(main_frame, text="Componentes Cadastrados", padding="10")
        lista_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Treeview para mostrar componentes
        columns = ("ID", "Nome", "Marca", "Status")
        self.tree = ttk.Treeview(lista_frame, columns=columns, show="headings", height=12)
        
        # Configurar colunas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        
        # Scrollbar para a lista
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid da lista e scrollbar
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind para seleção na lista
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_componente)
        
        # Botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(action_frame, text="Excluir Selecionado", command=self.excluir_componente).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="Atualizar Lista", command=self.atualizar_lista).grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, text="Sair", command=self.sair).grid(row=0, column=2, padx=5)
        
        # Configurar redimensionamento
        main_frame.columnconfigure(1, weight=1)
        lista_frame.columnconfigure(0, weight=1)
        lista_frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Variável para armazenar ID do componente sendo editado
        self.id_editando = None
    
    def cadastrar_componente(self):
        """Cadastra um novo componente"""
        nome = self.nome_entry.get().strip()
        marca = self.marca_entry.get().strip()
        status = self.status_var.get()
        
        if not nome:
            messagebox.showerror("Erro", "Nome do componente é obrigatório!")
            return
        
        if not status:
            messagebox.showerror("Erro", "Status é obrigatório!")
            return
        
        if self.db.cadastrar_componente(nome, marca, status):
            messagebox.showinfo("Sucesso", "Componente cadastrado com sucesso!")
            self.limpar_campos()
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar componente!")
    
    def atualizar_componente(self):
        """Atualiza um componente existente"""
        if not self.id_editando:
            messagebox.showwarning("Aviso", "Selecione um componente para atualizar!")
            return
        
        novo_status = self.status_var.get()
        
        if not novo_status:
            messagebox.showerror("Erro", "Status é obrigatório!")
            return
        
        if self.db.atualizar_componente(self.id_editando, novo_status):
            messagebox.showinfo("Sucesso", "Componente atualizado com sucesso!")
            self.limpar_campos()
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro", "Erro ao atualizar componente!")
    
    def excluir_componente(self):
        """Exclui o componente selecionado"""
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um componente para excluir!")
            return
        
        # Obter ID do componente selecionado
        item = self.tree.item(selected_item[0])
        component_id = item['values'][0]
        component_name = item['values'][1]
        
        # Confirmar exclusão
        resposta = messagebox.askyesno(
            "Confirmar Exclusão", 
            f"Tem certeza que deseja excluir o componente:\n'{component_name}'?"
        )
        
        if resposta:
            if self.db.excluir_componente(component_id):
                messagebox.showinfo("Sucesso", "Componente excluído com sucesso!")
                self.limpar_campos()
                self.atualizar_lista()
            else:
                messagebox.showerror("Erro", "Erro ao excluir componente!")
    
    def selecionar_componente(self, event):
        """Preenche o formulário com dados do componente selecionado"""
        selected_item = self.tree.selection()
        
        if selected_item:
            item = self.tree.item(selected_item[0])
            values = item['values']
            
            # Preencher campos
            self.id_editando = values[0]
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, values[1])
            self.marca_entry.delete(0, tk.END)
            self.marca_entry.insert(0, values[2])
            self.status_var.set(values[3])
            
            # Mudar texto do botão
            self.btn_cadastrar.configure(text="Novo")
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.nome_entry.delete(0, tk.END)
        self.marca_entry.delete(0, tk.END)
        self.status_var.set("Funcionando")
        self.id_editando = None
        self.btn_cadastrar.configure(text="Cadastrar")
    
    def atualizar_lista(self):
        """Atualiza a lista de componentes"""
        # Limpar lista atual
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar componentes
        componentes = self.db.listar_componentes()
        for comp in componentes:
            self.tree.insert("", tk.END, values=comp)
    
    def sair(self):
        """Fecha o aplicativo"""
        self.db.fechar_conexao()
        self.root.quit()
        self.root.destroy()
    
    def executar(self):
        """Inicia a interface gráfica"""
        # Configurar evento de fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.sair)
        self.root.mainloop()