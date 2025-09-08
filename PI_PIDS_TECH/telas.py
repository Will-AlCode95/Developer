import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import banco


def limpar_tree(tree: ttk.Treeview) -> None:
    """Remove todas as linhas de um Treeview."""
    for item in tree.get_children():
        tree.delete(item)


class TabAdministrador(ttk.Frame):
    """Aba para gerenciamento de administradores."""

    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self._montar_interface()

    def _montar_interface(self) -> None:
        # Formulário de cadastro
        frm = ttk.LabelFrame(self, text="Cadastro de Administrador")
        frm.pack(fill="x", pady=5)

        ttk.Label(frm, text="Nome:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.e_nome = ttk.Entry(frm, width=30)
        self.e_nome.grid(row=0, column=1, sticky="we", padx=4, pady=4)

        ttk.Label(frm, text="Senha:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.e_senha = ttk.Entry(frm, show="*", width=30)
        self.e_senha.grid(row=1, column=1, sticky="we", padx=4, pady=4)

        ttk.Button(frm, text="Salvar", command=self.salvar).grid(row=2, column=0, columnspan=2, pady=6)

        # Área de busca
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", pady=4)
        ttk.Label(search_frame, text="Buscar nome:").pack(side="left")
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(search_frame, text="Pesquisar", command=self.listar).pack(side="left", padx=4)

        # Tabela de visualização
        self.tree = ttk.Treeview(self, columns=("id", "nome"), show="headings", height=8)
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.pack(fill="both", expand=True, pady=6)

        # Botões de ação
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Atualizar Senha", command=self.atualizar_senha).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir).pack(side="left", padx=4)

        self.listar()

    def salvar(self) -> None:
        nome = self.e_nome.get().strip()
        senha = self.e_senha.get().strip()
        if not nome or not senha:
            messagebox.showwarning("Atenção", "Preencha nome e senha.")
            return
        banco.admin_inserir(nome, senha)
        self.e_nome.delete(0, tk.END)
        self.e_senha.delete(0, tk.END)
        self.listar()
        messagebox.showinfo("Sucesso", "Administrador cadastrado.")

    def listar(self) -> None:
        """Lista administradores filtrando pelo conteúdo do campo de busca."""
        filtro = self.search_var.get().strip().lower()
        dados = banco.admin_listar()
        limpar_tree(self.tree)
        for row in dados:
            if not filtro or filtro in str(row[1]).lower():
                self.tree.insert("", tk.END, values=row)

    def atualizar_senha(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um administrador.")
            return
        item = self.tree.item(sel[0], "values")
        ida = int(item[0])
        nova = simpledialog.askstring("Atualizar senha", "Nova senha:", show="*")
        if nova:
            banco.admin_atualizar_senha(ida, nova)
            messagebox.showinfo("Sucesso", "Senha atualizada.")

    def excluir(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um administrador.")
            return
        item = self.tree.item(sel[0], "values")
        ida = int(item[0])
        if messagebox.askyesno("Confirmação", "Excluir administrador?"):
            banco.admin_excluir(ida)
            self.listar()


class TabComponentes(ttk.Frame):
    """Aba para gerenciamento de componentes/periféricos."""

    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self._montar_interface()

    def _montar_interface(self) -> None:
        frm = ttk.LabelFrame(self, text="Cadastro de Componente")
        frm.pack(fill="x", pady=5)

        ttk.Label(frm, text="Nome:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.e_nome = ttk.Entry(frm, width=30)
        self.e_nome.grid(row=0, column=1, sticky="we", padx=4, pady=4)

        ttk.Label(frm, text="Marca:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.e_marca = ttk.Entry(frm, width=30)
        self.e_marca.grid(row=1, column=1, sticky="we", padx=4, pady=4)

        ttk.Label(frm, text="Status:").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        self.c_status = ttk.Combobox(frm, values=["Funcionando", "Descartado"], state="readonly", width=28)
        self.c_status.grid(row=2, column=1, sticky="we", padx=4, pady=4)

        ttk.Button(frm, text="Salvar", command=self.salvar).grid(row=3, column=0, columnspan=2, pady=6)

        # Área de busca
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", pady=4)
        ttk.Label(search_frame, text="Buscar nome/marca:").pack(side="left")
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(search_frame, text="Pesquisar", command=self.listar).pack(side="left", padx=4)

        # Tabela
        self.tree = ttk.Treeview(self, columns=("id", "nome", "marca", "status"), show="headings", height=8)
        for col, txt in zip(("id", "nome", "marca", "status"), ("ID", "Nome", "Marca", "Status")):
            self.tree.heading(col, text=txt)
        self.tree.pack(fill="both", expand=True, pady=6)

        # Ações
        bfrm = ttk.Frame(self)
        bfrm.pack(fill="x")
        ttk.Button(bfrm, text="Atualizar Status", command=self.atualizar_status).pack(side="left", padx=4)
        ttk.Button(bfrm, text="Excluir", command=self.excluir).pack(side="left", padx=4)

        self.listar()

    def salvar(self) -> None:
        nome = self.e_nome.get().strip()
        marca = self.e_marca.get().strip()
        status = self.c_status.get().strip()
        if not nome or not status:
            messagebox.showwarning("Atenção", "Nome e Status são obrigatórios.")
            return
        banco.comp_inserir(nome, marca, status)
        # Limpar campos
        self.e_nome.delete(0, tk.END)
        self.e_marca.delete(0, tk.END)
        self.c_status.set("")
        self.listar()
        messagebox.showinfo("Sucesso", "Componente cadastrado.")

    def listar(self) -> None:
        filtro = self.search_var.get().strip().lower()
        dados = banco.comp_listar()
        limpar_tree(self.tree)
        for row in dados:
            # row: (id, nome, marca, status)
            if not filtro or filtro in str(row[1]).lower() or (row[2] and filtro in row[2].lower()):
                self.tree.insert("", tk.END, values=row)

    def atualizar_status(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um componente.")
            return
        item = self.tree.item(sel[0], "values")
        idc = int(item[0])
        novo = simpledialog.askstring("Atualizar status", "Novo status (Funcionando/Descartado):")
        if novo in ("Funcionando", "Descartado"):
            banco.comp_atualizar_status(idc, novo)
            self.listar()
        else:
            messagebox.showwarning("Atenção", "Valor inválido.")

    def excluir(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um componente.")
            return
        item = self.tree.item(sel[0], "values")
        idc = int(item[0])
        if messagebox.askyesno("Confirmação", "Excluir componente?"):
            banco.comp_excluir(idc)
            self.listar()


class TabParticipantes(ttk.Frame):
    """Aba para gerenciamento de participantes."""

    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self._montar_interface()

    def _montar_interface(self) -> None:
        frm = ttk.LabelFrame(self, text="Cadastro de Participante")
        frm.pack(fill="x", pady=5)

        ttk.Label(frm, text="Nome:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.e_nome = ttk.Entry(frm, width=30)
        self.e_nome.grid(row=0, column=1, sticky="we", padx=4, pady=4)

        ttk.Label(frm, text="Turma:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.e_turma = ttk.Entry(frm, width=30)
        self.e_turma.grid(row=1, column=1, sticky="we", padx=4, pady=4)

        ttk.Button(frm, text="Salvar", command=self.salvar).grid(row=2, column=0, columnspan=2, pady=6)

        # Busca
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", pady=4)
        ttk.Label(search_frame, text="Buscar nome/turma:").pack(side="left")
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(search_frame, text="Pesquisar", command=self.listar).pack(side="left", padx=4)

        self.tree = ttk.Treeview(self, columns=("id", "nome", "turma"), show="headings", height=8)
        for col, txt in zip(("id", "nome", "turma"), ("ID", "Nome", "Turma")):
            self.tree.heading(col, text=txt)
        self.tree.pack(fill="both", expand=True, pady=6)

        bfrm = ttk.Frame(self)
        bfrm.pack(fill="x")
        ttk.Button(bfrm, text="Atualizar Turma", command=self.atualizar_turma).pack(side="left", padx=4)
        ttk.Button(bfrm, text="Excluir", command=self.excluir).pack(side="left", padx=4)

        self.listar()

    def salvar(self) -> None:
        nome = self.e_nome.get().strip()
        turma = self.e_turma.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Nome é obrigatório.")
            return
        banco.part_inserir(nome, turma)
        self.e_nome.delete(0, tk.END)
        self.e_turma.delete(0, tk.END)
        self.listar()
        messagebox.showinfo("Sucesso", "Participante cadastrado.")

    def listar(self) -> None:
        filtro = self.search_var.get().strip().lower()
        dados = banco.part_listar()
        limpar_tree(self.tree)
        for row in dados:
            # row: (id, nome, turma)
            nome = str(row[1]).lower()
            turma = str(row[2]).lower() if row[2] else ""
            if not filtro or filtro in nome or filtro in turma:
                self.tree.insert("", tk.END, values=row)

    def atualizar_turma(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um participante.")
            return
        item = self.tree.item(sel[0], "values")
        idp = int(item[0])
        nova = simpledialog.askstring("Atualizar turma", "Nova turma:")
        if nova is not None:
            banco.part_atualizar_turma(idp, nova)
            self.listar()

    def excluir(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um participante.")
            return
        item = self.tree.item(sel[0], "values")
        idp = int(item[0])
        if messagebox.askyesno("Confirmação", "Excluir participante?"):
            banco.part_excluir(idp)
            self.listar()


class TabPessoa(ttk.Frame):
    """Aba para gerenciamento de pessoas (físicas e jurídicas)."""

    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self._montar_interface()

    def _montar_interface(self) -> None:
        frm = ttk.LabelFrame(self, text="Cadastro de Pessoa")
        frm.pack(fill="x", pady=5)

        ttk.Label(frm, text="Tipo:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.c_tipo = ttk.Combobox(frm, values=["Fisica", "Juridica"], state="readonly", width=28)
        self.c_tipo.grid(row=0, column=1, sticky="we", padx=4, pady=4)

        ttk.Label(frm, text="Nome:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.e_nome = ttk.Entry(frm, width=30)
        self.e_nome.grid(row=1, column=1, sticky="we", padx=4, pady=4)

        ttk.Label(frm, text="CPF:").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        self.e_cpf = ttk.Entry(frm, width=30)
        self.e_cpf.grid(row=2, column=1, sticky="we", padx=4, pady=4)

        ttk.Label(frm, text="CNPJ:").grid(row=3, column=0, sticky="w", padx=4, pady=4)
        self.e_cnpj = ttk.Entry(frm, width=30)
        self.e_cnpj.grid(row=3, column=1, sticky="we", padx=4, pady=4)

        ttk.Button(frm, text="Salvar", command=self.salvar).grid(row=4, column=0, columnspan=2, pady=6)

        # Busca
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", pady=4)
        ttk.Label(search_frame, text="Buscar nome/CPF/CNPJ:").pack(side="left")
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(search_frame, text="Pesquisar", command=self.listar).pack(side="left", padx=4)

        cols = ("id", "tipo", "nome", "cpf", "cnpj")
        headers = ("ID", "Tipo", "Nome", "CPF", "CNPJ")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c, h in zip(cols, headers):
            self.tree.heading(c, text=h)
        self.tree.pack(fill="both", expand=True, pady=6)

        bfrm = ttk.Frame(self)
        bfrm.pack(fill="x")
        ttk.Button(bfrm, text="Atualizar Nome", command=self.atualizar_nome).pack(side="left", padx=4)
        ttk.Button(bfrm, text="Excluir", command=self.excluir).pack(side="left", padx=4)

        self.listar()

    def salvar(self) -> None:
        tipo = self.c_tipo.get().strip()
        nome = self.e_nome.get().strip()
        cpf = self.e_cpf.get().strip() or None
        cnpj = self.e_cnpj.get().strip() or None
        if not tipo or not nome:
            messagebox.showwarning("Atenção", "Tipo e Nome são obrigatórios.")
            return
        try:
            banco.pessoa_inserir(tipo, nome, cpf, cnpj)
            # Limpar campos
            self.c_tipo.set("")
            self.e_nome.delete(0, tk.END)
            self.e_cpf.delete(0, tk.END)
            self.e_cnpj.delete(0, tk.END)
            self.listar()
            messagebox.showinfo("Sucesso", "Pessoa cadastrada.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def listar(self) -> None:
        filtro = self.search_var.get().strip().lower()
        dados = banco.pessoa_listar()
        limpar_tree(self.tree)
        for row in dados:
            # row: (id, tipo, nome, cpf, cnpj)
            nome = str(row[2]).lower()
            cpf = row[3].lower() if row[3] else ""
            cnpj = row[4].lower() if row[4] else ""
            if not filtro or filtro in nome or filtro in cpf or filtro in cnpj:
                self.tree.insert("", tk.END, values=row)

    def atualizar_nome(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma pessoa.")
            return
        item = self.tree.item(sel[0], "values")
        idp = int(item[0])
        novo = simpledialog.askstring("Atualizar nome", "Novo nome:")
        if novo:
            banco.pessoa_atualizar_nome(idp, novo)
            self.listar()

    def excluir(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma pessoa.")
            return
        item = self.tree.item(sel[0], "values")
        idp = int(item[0])
        if messagebox.askyesno("Confirmação", "Excluir pessoa?"):
            try:
                banco.pessoa_excluir(idp)
                self.listar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))


class TabTransferencia(ttk.Frame):
    """Aba para gerenciamento de transferências."""

    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self._montar_interface()

    def _montar_interface(self) -> None:
        frm = ttk.LabelFrame(self, text="Registro de Transferência")
        frm.pack(fill="x", pady=5)

        ttk.Label(frm, text="ID Doador (opcional):").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.e_doador = ttk.Entry(frm, width=30)
        self.e_doador.grid(row=0, column=1, sticky="we", padx=4, pady=4)

        ttk.Label(frm, text="ID Destinatário (opcional):").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.e_dest = ttk.Entry(frm, width=30)
        self.e_dest.grid(row=1, column=1, sticky="we", padx=4, pady=4)

        ttk.Label(frm, text="ID Componente:").grid(row=2, column=0, sticky="w", padx=4, pady=4)
        self.e_comp = ttk.Entry(frm, width=30)
        self.e_comp.grid(row=2, column=1, sticky="we", padx=4, pady=4)

        ttk.Label(frm, text="Tipo:").grid(row=3, column=0, sticky="w", padx=4, pady=4)
        self.c_tipo = ttk.Combobox(frm, values=["Doação", "Recebimento", "Transferência Interna"], state="readonly", width=28)
        self.c_tipo.grid(row=3, column=1, sticky="we", padx=4, pady=4)

        ttk.Label(frm, text="Data (YYYY-MM-DD):").grid(row=4, column=0, sticky="w", padx=4, pady=4)
        self.e_data = ttk.Entry(frm, width=30)
        self.e_data.grid(row=4, column=1, sticky="we", padx=4, pady=4)

        ttk.Button(frm, text="Salvar", command=self.salvar).grid(row=5, column=0, columnspan=2, pady=6)

        # Busca
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", pady=4)
        ttk.Label(search_frame, text="Buscar por componente/doador/destinatário/tipo:").pack(side="left")
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(search_frame, text="Pesquisar", command=self.listar).pack(side="left", padx=4)

        cols = (
            "id",
            "data",
            "tipo",
            "id_comp",
            "componente",
            "id_doador",
            "doador",
            "id_dest",
            "destinatario",
        )
        headers = (
            "ID",
            "Data",
            "Tipo",
            "ID Comp",
            "Componente",
            "ID Doador",
            "Doador",
            "ID Dest",
            "Destinatário",
        )
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c, h in zip(cols, headers):
            self.tree.heading(c, text=h)
        self.tree.pack(fill="both", expand=True, pady=6)

        bfrm = ttk.Frame(self)
        bfrm.pack(fill="x")
        ttk.Button(bfrm, text="Atualizar Tipo", command=self.atualizar_tipo).pack(side="left", padx=4)
        ttk.Button(bfrm, text="Excluir", command=self.excluir).pack(side="left", padx=4)

        self.listar()

    def salvar(self) -> None:
        doador = self.e_doador.get().strip() or None
        dest = self.e_dest.get().strip() or None
        comp = self.e_comp.get().strip()
        tipo = self.c_tipo.get().strip()
        data = self.e_data.get().strip()
        if not comp or not tipo or not data:
            messagebox.showwarning("Atenção", "ID Componente, Tipo e Data são obrigatórios.")
            return
        try:
            id_doador = int(doador) if doador else None
            id_dest = int(dest) if dest else None
            id_comp = int(comp)
        except ValueError:
            messagebox.showwarning("Atenção", "IDs devem ser números inteiros.")
            return
        try:
            banco.transf_inserir(id_doador, id_dest, id_comp, tipo, data)
            # limpar campos
            self.e_doador.delete(0, tk.END)
            self.e_dest.delete(0, tk.END)
            self.e_comp.delete(0, tk.END)
            self.c_tipo.set("")
            self.e_data.delete(0, tk.END)
            self.listar()
            messagebox.showinfo("Sucesso", "Transferência registrada.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def listar(self) -> None:
        filtro = self.search_var.get().strip().lower()
        dados = banco.transf_listar()
        limpar_tree(self.tree)
        for row in dados:
            # row: (id, data, tipo, id_comp, componente, id_doador, doador, id_dest, dest)
            data = row[1].lower()
            tipo = row[2].lower()
            comp_name = row[4].lower() if row[4] else ""
            doador = row[6].lower() if row[6] else ""
            dest = row[8].lower() if row[8] else ""
            if not filtro or filtro in data or filtro in tipo or filtro in comp_name or filtro in doador or filtro in dest:
                self.tree.insert("", tk.END, values=row)

    def atualizar_tipo(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma transferência.")
            return
        item = self.tree.item(sel[0], "values")
        idt = int(item[0])
        novo = simpledialog.askstring(
            "Atualizar tipo",
            "Novo tipo (Doação/Recebimento/Transferência Interna):",
        )
        if novo in ("Doação", "Recebimento", "Transferência Interna"):
            banco.transf_atualizar_tipo(idt, novo)
            self.listar()
        else:
            messagebox.showwarning("Atenção", "Valor inválido.")

    def excluir(self) -> None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma transferência.")
            return
        item = self.tree.item(sel[0], "values")
        idt = int(item[0])
        if messagebox.askyesno("Confirmação", "Excluir transferência?"):
            try:
                banco.transf_excluir(idt)
                self.listar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))


class App(ttk.Notebook):
    """Janela principal contendo todas as abas."""

    def __init__(self, root: tk.Tk):
        super().__init__(root)
        root.title("PIDS Tech - CRUD (SQLite + Tkinter)")
        root.geometry("960x640")
        self.pack(fill="both", expand=True)
        # Criar abas
        self.add(TabAdministrador(self), text="Administradores")
        self.add(TabComponentes(self), text="Componentes")
        self.add(TabParticipantes(self), text="Participantes")
        self.add(TabPessoa(self), text="Pessoas")
        self.add(TabTransferencia(self), text="Transferências")