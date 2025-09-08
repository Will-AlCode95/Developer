import sqlite3
import os

class Database:
    def __init__(self, db_name="pids_tech.db"):
        self.db_name = db_name
        self.conexao = None
        self.cursor = None
        self.conectar()
        self.criar_tabelas()
    
    def conectar(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.conexao = sqlite3.connect(self.db_name)
            self.cursor = self.conexao.cursor()
            print(f"✅ Conectado ao banco de dados: {self.db_name}")
        except Exception as e:
            print(f"❌ Erro ao conectar com o banco: {e}")
    
    def criar_tabelas(self):
        """Cria as tabelas se não existirem"""
        try:
            # Tabela de administradores
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS adm (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT UNIQUE NOT NULL,
                    login TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL
                )
            """)
            
            # Tabela de participantes
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS participantes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    turma TEXT
                )
            """)
            
            # Tabela de componentes
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS componentes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    marca TEXT,
                    status TEXT CHECK(status IN ('Funcionando','Defeito','Descarte')) NOT NULL
                )
            """)
            
            # Tabela de doações
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS doacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    componente_id INTEGER,
                    doador TEXT,
                    receptor TEXT,
                    data TEXT,
                    FOREIGN KEY (componente_id) REFERENCES componentes(id)
                )
            """)
            
            self.conexao.commit()
            print("✅ Tabelas criadas/verificadas com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
    
    def cadastrar_componente(self, nome, marca, status):
        """Cadastra um novo componente"""
        try:
            self.cursor.execute(
                "INSERT INTO componentes (nome, marca, status) VALUES (?, ?, ?)", 
                (nome, marca, status)
            )
            self.conexao.commit()
            return True
        except Exception as e:
            print(f"❌ Erro ao cadastrar componente: {e}")
            return False
    
    def listar_componentes(self):
        """Lista todos os componentes"""
        try:
            self.cursor.execute("SELECT * FROM componentes")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Erro ao listar componentes: {e}")
            return []
    
    def buscar_componente_por_id(self, id_componente):
        """Busca um componente específico pelo ID"""
        try:
            self.cursor.execute("SELECT * FROM componentes WHERE id=?", (id_componente,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"❌ Erro ao buscar componente: {e}")
            return None
    
    def atualizar_componente(self, id_componente, novo_status):
        """Atualiza o status de um componente"""
        try:
            self.cursor.execute(
                "UPDATE componentes SET status=? WHERE id=?", 
                (novo_status, id_componente)
            )
            self.conexao.commit()
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar componente: {e}")
            return False
    
    def excluir_componente(self, id_componente):
        """Exclui um componente"""
        try:
            self.cursor.execute("DELETE FROM componentes WHERE id=?", (id_componente,))
            self.conexao.commit()
            return True
        except Exception as e:
            print(f"❌ Erro ao excluir componente: {e}")
            return False
    
    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados"""
        if self.conexao:
            self.conexao.close()
            print("✅ Conexão com banco de dados encerrada!")
    
    def __del__(self):
        """Destrutor para garantir que a conexão seja fechada"""
        self.fechar_conexao()