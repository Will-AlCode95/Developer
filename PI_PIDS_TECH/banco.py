import sqlite3

# Nome do arquivo de banco de dados
DB_NAME = "pids_tech.db"

def conectar():
    """Abre uma conexão com o banco de dados SQLite e habilita chaves estrangeiras."""
    con = sqlite3.connect(DB_NAME)
    # Habilitar chaves estrangeiras para garantir integridade referencial
    con.execute("PRAGMA foreign_keys = ON")
    return con


def criar_tabelas():
    """Cria todas as tabelas necessárias se ainda não existirem."""
    con = conectar()
    cur = con.cursor()

    # Tabela de administradores
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS administrador (
            id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL
        )
        """
    )

    # Tabela de componentes/periféricos
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS componente_periferico (
            id_componente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            marca TEXT,
            status TEXT CHECK(status IN ('Funcionando','Descartado')) NOT NULL
        )
        """
    )

    # Tabela de participantes
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS participantespt (
            id_participante INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT
        )
        """
    )

    # Tabela de pessoas (físicas ou jurídicas)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS pessoa (
            id_pessoa INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT CHECK(tipo IN ('Fisica','Juridica')) NOT NULL,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE,
            cnpj TEXT UNIQUE
        )
        """
    )

    # Tabela de transferências
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS transferencia (
            id_transferencia INTEGER PRIMARY KEY AUTOINCREMENT,
            id_doador INTEGER,
            id_destinatario INTEGER,
            id_componente INTEGER NOT NULL,
            tipo_operacao TEXT CHECK(tipo_operacao IN ('Doação','Recebimento','Transferência Interna')) NOT NULL,
            data_transferencia TEXT NOT NULL,
            FOREIGN KEY (id_componente) REFERENCES componente_periferico(id_componente) ON DELETE CASCADE,
            FOREIGN KEY (id_doador) REFERENCES pessoa(id_pessoa) ON DELETE SET NULL,
            FOREIGN KEY (id_destinatario) REFERENCES pessoa(id_pessoa) ON DELETE SET NULL
        )
        """
    )

    con.commit()
    con.close()


# ----- Funções de administrador -----

def admin_inserir(nome: str, senha: str) -> None:
    """Insere um novo administrador."""
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO administrador (nome, senha) VALUES (?, ?)", (nome, senha))
    con.commit()
    con.close()


def admin_listar():
    """Lista todos os administradores retornando (id, nome)."""
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id_professor, nome FROM administrador ORDER BY id_professor")
    dados = cur.fetchall()
    con.close()
    return dados


def admin_atualizar_senha(id_professor: int, nova_senha: str) -> None:
    """Atualiza a senha de um administrador."""
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE administrador SET senha=? WHERE id_professor=?",
        (nova_senha, id_professor),
    )
    con.commit()
    con.close()


def admin_excluir(id_professor: int) -> None:
    """Exclui um administrador."""
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM administrador WHERE id_professor=?", (id_professor,))
    con.commit()
    con.close()


def admin_validar(nome: str, senha: str) -> bool:
    """Verifica se existe um administrador com o nome e senha informados."""
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "SELECT id_professor FROM administrador WHERE nome=? AND senha=?",
        (nome, senha),
    )
    resultado = cur.fetchone()
    con.close()
    return resultado is not None


def admin_count() -> int:
    """Retorna a quantidade de registros na tabela administrador."""
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM administrador")
    count = cur.fetchone()[0]
    con.close()
    return count


def admin_create_default() -> None:
    """Cria um administrador padrão se nenhum existir.

    Se a tabela estiver vazia, será criado um administrador com login 'admin' e senha 'admin'.
    """
    if admin_count() == 0:
        # Usuario padrão
        admin_inserir("admin", "admin")


# ----- Funções de componentes -----

def comp_inserir(nome: str, marca: str, status: str) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO componente_periferico (nome, marca, status) VALUES (?, ?, ?)",
        (nome, marca, status),
    )
    con.commit()
    con.close()


def comp_listar():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "SELECT id_componente, nome, marca, status FROM componente_periferico ORDER BY id_componente"
    )
    dados = cur.fetchall()
    con.close()
    return dados


def comp_atualizar_status(id_componente: int, novo_status: str) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE componente_periferico SET status=? WHERE id_componente=?",
        (novo_status, id_componente),
    )
    con.commit()
    con.close()


def comp_excluir(id_componente: int) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM componente_periferico WHERE id_componente=?", (id_componente,))
    con.commit()
    con.close()


# ----- Funções de participantes -----

def part_inserir(nome: str, turma: str) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO participantespt (nome, turma) VALUES (?, ?)", (nome, turma)
    )
    con.commit()
    con.close()


def part_listar():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "SELECT id_participante, nome, turma FROM participantespt ORDER BY id_participante"
    )
    dados = cur.fetchall()
    con.close()
    return dados


def part_atualizar_turma(id_participante: int, nova_turma: str) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE participantespt SET turma=? WHERE id_participante=?",
        (nova_turma, id_participante),
    )
    con.commit()
    con.close()


def part_excluir(id_participante: int) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "DELETE FROM participantespt WHERE id_participante=?", (id_participante,)
    )
    con.commit()
    con.close()


# ----- Funções de pessoa -----

def pessoa_inserir(tipo: str, nome: str, cpf: str | None = None, cnpj: str | None = None) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO pessoa (tipo, nome, cpf, cnpj) VALUES (?, ?, ?, ?)",
        (tipo, nome, cpf, cnpj),
    )
    con.commit()
    con.close()


def pessoa_listar():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "SELECT id_pessoa, tipo, nome, cpf, cnpj FROM pessoa ORDER BY id_pessoa"
    )
    dados = cur.fetchall()
    con.close()
    return dados


def pessoa_atualizar_nome(id_pessoa: int, novo_nome: str) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE pessoa SET nome=? WHERE id_pessoa=?", (novo_nome, id_pessoa))
    con.commit()
    con.close()


def pessoa_excluir(id_pessoa: int) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM pessoa WHERE id_pessoa=?", (id_pessoa,))
    con.commit()
    con.close()


# ----- Funções de transferência -----

def transf_inserir(
    id_doador: int | None,
    id_destinatario: int | None,
    id_componente: int,
    tipo_operacao: str,
    data_transferencia: str,
) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO transferencia (
            id_doador,
            id_destinatario,
            id_componente,
            tipo_operacao,
            data_transferencia
        ) VALUES (?, ?, ?, ?, ?)
        """,
        (id_doador, id_destinatario, id_componente, tipo_operacao, data_transferencia),
    )
    con.commit()
    con.close()


def transf_listar():
    con = conectar()
    cur = con.cursor()
    # Juntar tabelas para apresentar nomes legíveis
    cur.execute(
        """
        SELECT t.id_transferencia, t.data_transferencia, t.tipo_operacao,
               t.id_componente,
               c.nome AS componente,
               t.id_doador,
               pd.nome AS doador,
               t.id_destinatario,
               pr.nome AS destinatario
        FROM transferencia t
        LEFT JOIN componente_periferico c ON c.id_componente = t.id_componente
        LEFT JOIN pessoa pd ON pd.id_pessoa = t.id_doador
        LEFT JOIN pessoa pr ON pr.id_pessoa = t.id_destinatario
        ORDER BY t.id_transferencia
        """
    )
    dados = cur.fetchall()
    con.close()
    return dados


def transf_atualizar_tipo(id_transferencia: int, novo_tipo: str) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "UPDATE transferencia SET tipo_operacao=? WHERE id_transferencia=?",
        (novo_tipo, id_transferencia),
    )
    con.commit()
    con.close()


def transf_excluir(id_transferencia: int) -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "DELETE FROM transferencia WHERE id_transferencia=?", (id_transferencia,)
    )
    con.commit()
    con.close()