import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class PidsTechModerna:
    def __init__(self):
        self.db = Database()
        self.root = tk.Tk()
        self.root.title("PIDS TECH - Sistema Moderno")
        self.root.geometry("1200x800")
        self.root.configure(bg="#34495e")
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configurar_estilos()
        
        # Variável para controlar a seção atual
        self.secao_atual = "inicio"
        
        # Variável para armazenar ID do componente sendo editado
        self.id_editando = None
        
        self.criar_interface_principal()
        
    def configurar_estilos(self):
        """Configura estilos personalizados"""
        # Configurar cores dos widgets ttk
        self.style.configure("Sidebar.TFrame", background="#2c3e50")
        self.style.configure("Content.TFrame", background="#ecf0f1")
        self.style.configure("Title.TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Arial", 14, "bold"))
        self.style.configure("Menu.TLabel", background="#2c3e50", foreground="#bdc3c7", font=("Arial", 11))
        
    def criar_interface_principal(self):
        """Cria a interface principal com menu lateral"""
        # Frame principal
        main_container = tk.Frame(self.root, bg="#34495e")
        main_container.pack(fill="both", expand=True)
        
        # Sidebar (Menu lateral)
        self.sidebar = tk.Frame(main_container, bg="#2c3e50", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Área de conteúdo
        self.content_area = tk.Frame(main_container, bg="#ecf0f1")
        self.content_area.pack(side="right", fill="both", expand=True)
        
        self.criar_sidebar()
        self.mostrar_inicio()
        
    def criar_sidebar(self):
        """Cria o menu lateral"""
        # Logo/Título
        logo_frame = tk.Frame(self.sidebar, bg="#2c3e50", height=100)
        logo_frame.pack(fill="x", pady=20)
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(
            logo_frame,
            text="PIDS TECH",
            font=("Arial", 20, "bold"),
            fg="#3498db",
            bg="#2c3e50"
        )
        logo_label.pack(expand=True)
        
        # Separador
        tk.Frame(self.sidebar, bg="#34495e", height=2).pack(fill="x", pady=10)
        
        # Botões do menu
        menu_items = [
            ("🏠 Início", "inicio", self.mostrar_inicio),
            ("🔧 Componentes", "componentes", self.mostrar_componentes),
            ("👥 Participantes", "participantes", self.mostrar_participantes),
            ("💝 Doações", "doacoes", self.mostrar_doacoes),
            ("📊 Relatórios", "relatorios", self.mostrar_relatorios),
            ("⚙️ Configurações", "config", self.mostrar_configuracoes),
        ]
        
        self.menu_buttons = {}
        
        for texto, key, command in menu_items:
            btn = tk.Button(
                self.sidebar,
                text=texto,
                font=("Arial", 12),
                bg="#2c3e50",
                fg="#bdc3c7",
                bd=0,
                padx=20,
                pady=15,
                anchor="w",
                activebackground="#34495e",
                activeforeground="#ecf0f1",
                command=command,
                cursor="hand2"
            )
            btn.pack(fill="x", padx=5, pady=2)
            self.menu_buttons[key] = btn
        
        # Separador inferior
        tk.Frame(self.sidebar, bg="#34495e", height=2).pack(side="bottom", fill="x", pady=20)
        
        # Botão Sair
        btn_sair = tk.Button(
            self.sidebar,
            text="❌ Sair",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            bd=0,
            padx=20,
            pady=10,
            activebackground="#c0392b",
            activeforeground="white",
            command=self.sair,
            cursor="hand2"
        )
        btn_sair.pack(side="bottom", fill="x", padx=5, pady=5)
        
        # Atualizar botão ativo inicial
        self.atualizar_botao_ativo("inicio")
        
    def atualizar_botao_ativo(self, secao_ativa):
        """Atualiza visual do botão ativo"""
        # Resetar todos os botões
        for key, btn in self.menu_buttons.items():
            if key == secao_ativa:
                btn.configure(bg="#3498db", fg="white")
            else:
                btn.configure(bg="#2c3e50", fg="#bdc3c7")
        
        self.secao_atual = secao_ativa
        
    def limpar_content_area(self):
        """Limpa a área de conteúdo"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
    def mostrar_inicio(self):
        """Mostra a tela inicial"""
        self.limpar_content_area()
        self.atualizar_botao_ativo("inicio")
        
        # Container principal
        container = tk.Frame(self.content_area, bg="#ecf0f1")
        container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Título de boas-vindas
        titulo = tk.Label(
            container,
            text="Bem-vindo ao PIDS TECH",
            font=("Arial", 28, "bold"),
            fg="#2c3e50",
            bg="#ecf0f1"
        )
        titulo.pack(pady=(0, 20))
        
        # Subtítulo
        subtitulo = tk.Label(
            container,
            text="Sistema de Gerenciamento de Componentes e Participantes",
            font=("Arial", 14),
            fg="#7f8c8d",
            bg="#ecf0f1"
        )
        subtitulo.pack(pady=(0, 40))
        
        # Cards de estatísticas
        stats_frame = tk.Frame(container, bg="#ecf0f1")
        stats_frame.pack(fill="x", pady=20)
        
        # Obter estatísticas do banco
        total_componentes = len(self.db.listar_componentes())
        
        # Card componentes
        self.criar_card_estatistica(
            stats_frame, 
            "🔧 Componentes", 
            str(total_componentes),
            "#3498db",
            0
        )
        
        # Card participantes (placeholder)
        self.criar_card_estatistica(
            stats_frame,
            "👥 Participantes", 
            "Em breve",
            "#e67e22",
            1
        )
        
        # Card doações (placeholder)
        self.criar_card_estatistica(
            stats_frame,
            "💝 Doações", 
            "Em breve",
            "#27ae60",
            2
        )
        
        # Informações do sistema
        info_frame = tk.LabelFrame(
            container, 
            text="Informações do Sistema",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        info_frame.pack(fill="x", pady=(40, 0))
        
        info_text = tk.Text(
            info_frame,
            height=8,
            bg="white",
            fg="#2c3e50",
            font=("Arial", 11),
            wrap="word",
            padx=10,
            pady=10
        )
        info_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        info_content = """
🏢 PIDS TECH - Sistema de Gerenciamento v1.0

📋 Funcionalidades Disponíveis:
• Gerenciamento completo de componentes de hardware
• Cadastro, edição, listagem e exclusão
• Interface moderna e intuitiva
• Banco de dados SQLite integrado

🚀 Em Desenvolvimento:
• Sistema de participantes
• Controle de doações
• Relatórios detalhados
• Sistema de autenticação

💡 Dica: Use o menu lateral para navegar entre as seções do sistema.
        """
        
        info_text.insert("1.0", info_content)
        info_text.configure(state="disabled")
    
    def criar_card_estatistica(self, parent, titulo, valor, cor, coluna):
        """Cria um card de estatística"""
        card = tk.Frame(parent, bg=cor, relief="raised", bd=2)
        card.grid(row=0, column=coluna, padx=10, pady=10, sticky="ew")
        
        # Configurar grid
        parent.grid_columnconfigure(coluna, weight=1)
        
        # Título do card
        titulo_label = tk.Label(
            card,
            text=titulo,
            font=("Arial", 12, "bold"),
            fg="white",
            bg=cor
        )
        titulo_label.pack(pady=(15, 5))
        
        # Valor
        valor_label = tk.Label(
            card,
            text=valor,
            font=("Arial", 20, "bold"),
            fg="white",
            bg=cor
        )
        valor_label.pack(pady=(0, 15))
    
    def mostrar_componentes(self):
        """Mostra a interface de componentes"""
        self.limpar_content_area()
        self.atualizar_botao_ativo("componentes")
        
        # Container principal
        container = tk.Frame(self.content_area, bg="#ecf0f1")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título da seção
        titulo = tk.Label(
            container,
            text="🔧 Gerenciamento de Componentes",
            font=("Arial", 20, "bold"),
            fg="#2c3e50",
            bg="#ecf0f1"
        )
        titulo.pack(pady=(0, 20))
        
        # Frame para formulário
        form_frame = tk.LabelFrame(
            container,
            text="Cadastrar/Editar Componente",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
            padx=20,
            pady=15
        )
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Grid do formulário
        form_grid = tk.Frame(form_frame, bg="#ecf0f1")
        form_grid.pack(fill="x")
        
        # Campo Nome
        tk.Label(form_grid, text="Nome:", font=("Arial", 11, "bold"), bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=5)
        self.nome_entry = tk.Entry(form_grid, font=("Arial", 11), width=30)
        self.nome_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="ew")
        
        # Campo Marca
        tk.Label(form_grid, text="Marca:", font=("Arial", 11, "bold"), bg="#ecf0f1").grid(row=0, column=2, sticky="w", pady=5, padx=(20, 0))
        self.marca_entry = tk.Entry(form_grid, font=("Arial", 11), width=25)
        self.marca_entry.grid(row=0, column=3, padx=(10, 0), pady=5, sticky="ew")
        
        # Campo Status
        tk.Label(form_grid, text="Status:", font=("Arial", 11, "bold"), bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=5)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(
            form_grid,
            textvariable=self.status_var,
            values=["Funcionando", "Defeito", "Descarte"],
            state="readonly",
            font=("Arial", 11),
            width=27
        )
        self.status_combo.grid(row=1, column=1, padx=(10, 0), pady=5, sticky="ew")
        self.status_combo.set("Funcionando")
        
        # Configurar grid
        form_grid.grid_columnconfigure(1, weight=1)
        form_grid.grid_columnconfigure(3, weight=1)
        
        # Frame para botões do formulário
        btn_form_frame = tk.Frame(form_frame, bg="#ecf0f1")
        btn_form_frame.pack(pady=15)
        
        # Estilo dos botões
        btn_style = {"font": ("Arial", 10, "bold"), "padx": 20, "pady": 8, "cursor": "hand2"}
        
        self.btn_cadastrar = tk.Button(
            btn_form_frame,
            text="✅ Cadastrar",
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            command=self.cadastrar_componente,
            **btn_style
        )
        self.btn_cadastrar.pack(side="left", padx=5)
        
        self.btn_atualizar = tk.Button(
            btn_form_frame,
            text="🔄 Atualizar",
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            command=self.atualizar_componente,
            **btn_style
        )
        self.btn_atualizar.pack(side="left", padx=5)
        
        self.btn_limpar = tk.Button(
            btn_form_frame,
            text="🧹 Limpar",
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            command=self.limpar_campos,
            **btn_style
        )
        self.btn_limpar.pack(side="left", padx=5)
        
        # Frame para lista
        lista_frame = tk.LabelFrame(
            container,
            text="Componentes Cadastrados",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        lista_frame.pack(fill="both", expand=True)
        
        # Treeview
        columns = ("ID", "Nome", "Marca", "Status")
        self.tree = ttk.Treeview(lista_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome do Componente")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Nome", width=300, anchor="w")
        self.tree.column("Marca", width=200, anchor="w")
        self.tree.column("Status", width=120, anchor="center")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(lista_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid da lista
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configurar redimensionamento
        lista_frame.grid_rowconfigure(0, weight=1)
        lista_frame.grid_columnconfigure(0, weight=1)
        
        # Bind para seleção
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_componente)
        
        # Frame para botões de ação
        action_frame = tk.Frame(container, bg="#ecf0f1")
        action_frame.pack(pady=15)
        
        tk.Button(
            action_frame,
            text="🗑️ Excluir Selecionado",
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            command=self.excluir_componente,
            **btn_style
        ).pack(side="left", padx=5)
        
        tk.Button(
            action_frame,
            text="🔄 Atualizar Lista",
            bg="#f39c12",
            fg="white",
            activebackground="#e67e22",
            command=self.atualizar_lista,
            **btn_style
        ).pack(side="left", padx=5)
        
        # Carregar dados iniciais
        self.atualizar_lista()
    
    def mostrar_participantes(self):
        """Mostra interface de participantes"""
        self.limpar_content_area()
        self.atualizar_botao_ativo("participantes")
        self.mostrar_em_desenvolvimento("👥 Participantes", "Sistema de gerenciamento de participantes")
    
    def mostrar_doacoes(self):
        """Mostra interface de doações"""
        self.limpar_content_area()
        self.atualizar_botao_ativo("doacoes")
        self.mostrar_em_desenvolvimento("💝 Doações", "Sistema de controle de doações de componentes")
    
    def mostrar_relatorios(self):
        """Mostra interface de relatórios"""
        self.limpar_content_area()
        self.atualizar_botao_ativo("relatorios")
        self.mostrar_em_desenvolvimento("📊 Relatórios", "Sistema de geração de relatórios detalhados")
    
    def mostrar_configuracoes(self):
        """Mostra interface de configurações"""
        self.limpar_content_area()
        self.atualizar_botao_ativo("config")
        self.mostrar_em_desenvolvimento("⚙️ Configurações", "Configurações do sistema e preferências")
    
    def mostrar_em_desenvolvimento(self, titulo, descricao):
        """Mostra tela padrão para funcionalidades em desenvolvimento"""
        container = tk.Frame(self.content_area, bg="#ecf0f1")
        container.pack(fill="both", expand=True)
        
        # Centralizar conteúdo
        center_frame = tk.Frame(container, bg="#ecf0f1")
        center_frame.pack(expand=True)
        
        # Ícone
        icon_label = tk.Label(
            center_frame,
            text="🚧",
            font=("Arial", 60),
            bg="#ecf0f1"
        )
        icon_label.pack(pady=20)
        
        # Título
        titulo_label = tk.Label(
            center_frame,
            text=titulo,
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#ecf0f1"
        )
        titulo_label.pack(pady=10)
        
        # Descrição
        desc_label = tk.Label(
            center_frame,
            text="Em Desenvolvimento",
            font=("Arial", 16),
            fg="#e67e22",
            bg="#ecf0f1"
        )
        desc_label.pack(pady=5)
        
        # Informações
        info_label = tk.Label(
            center_frame,
            text=descricao + "\nEsta funcionalidade estará disponível em breve!",
            font=("Arial", 12),
            fg="#7f8c8d",
            bg="#ecf0f1",
            justify="center"
        )
        info_label.pack(pady=20)
    
    # Métodos de funcionalidade (mesmos da versão anterior)
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
        
        item = self.tree.item(selected_item[0])
        component_id = item['values'][0]
        component_name = item['values'][1]
        
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
            
            self.id_editando = values[0]
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, values[1])
            self.marca_entry.delete(0, tk.END)
            self.marca_entry.insert(0, values[2])
            self.status_var.set(values[3])
            
            self.btn_cadastrar.configure(text="✅ Novo")
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        if hasattr(self, 'nome_entry'):
            self.nome_entry.delete(0, tk.END)
            self.marca_entry.delete(0, tk.END)
            self.status_var.set("Funcionando")
            self.id_editando = None
            self.btn_cadastrar.configure(text="✅ Cadastrar")
    
    def atualizar_lista(self):
        """Atualiza a lista de componentes"""
        if hasattr(self, 'tree'):
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            componentes = self.db.listar_componentes()
            for comp in componentes:
                self.tree.insert("", tk.END, values=comp)
    
    def sair(self):
        """Fecha o aplicativo"""
        resposta = messagebox.askyesno("Sair", "Tem certeza que deseja sair do sistema?")
        if resposta:
            self.db.fechar_conexao()
            self.root.quit()
            self.root.destroy()
    
    def executar(self):
        """Inicia a interface gráfica"""
        # Centralizar janela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.protocol("WM_DELETE_WINDOW", self.sair)
        self.root.mainloop()