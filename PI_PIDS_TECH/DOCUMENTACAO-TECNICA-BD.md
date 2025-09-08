# 📘 Documentação Técnica — Banco de Dados `pids_tech`

## 💡 Introdução
O banco de dados `pids_tech` foi projetado para apoiar a gestão de componentes doados, transferidos e recebidos no contexto do projeto **PIDS Tech**. Ele permite o rastreamento detalhado das movimentações de hardware, identificando doadores, destinatários e participantes do programa.

---

## 🗂️ Estrutura do Banco de Dados

| Tabela                   | Descrição                                               |
|--------------------------|---------------------------------------------------------|
| `administrador`          | Armazena os dados de autenticação de professores.        |
| `componente_periferico`  | Contém informações sobre peças e periféricos.            |
| `participantespt`        | Lista os estudantes que participam do PIDS Tech.         |
| `pessoa`                 | Registra tanto doadores físicos quanto jurídicos.        |
| `transferencia`          | Controla doações, recebimentos e transferências internas.|

---

## 🔎 Modelagem

### Entidades principais:
- **Administrador**: Gerencia o sistema.
- **Pessoa**: Representa quem doa ou recebe os componentes.
- **Componente Periférico**: Itens físicos que circulam.
- **Participantes PIDS Tech**: Alunos envolvidos.
- **Transferência**: Histórico de movimentações.

---

## ⚙️ Regras de Negócio

- **Pessoa Física**: Preenche o campo `CPF` e deixa `CNPJ` como `NULL`.
- **Pessoa Jurídica**: Preenche o campo `CNPJ` e deixa `CPF` como `NULL`.
- O campo `status` de `componente_periferico` define se o item está **Funcionando** ou **Descartado**.
- O campo `tipo_operacao` da tabela `transferencia` define claramente o tipo da movimentação:  
  `Doação`, `Recebimento` ou `Transferência Interna`.

---

## 🔗 Relacionamentos

- `transferencia.id_doador` → Chave estrangeira referenciando `pessoa.id_pessoa`.
- `transferencia.id_destinatario` → Chave estrangeira referenciando `pessoa.id_pessoa`.
- `transferencia.id_componente` → Chave estrangeira referenciando `componente_periferico.id_componente`.

---

## 💾 Scripts de Teste

Inclui comandos `INSERT` para popular o banco com dados de exemplo e `SELECT` para consultas frequentes:

### Exemplos de Consultas:

- Listar todas as transferências com nomes:
```sql
SELECT t.id_transferencia, p1.nome AS doador, p2.nome AS destinatario, c.nome AS componente, t.tipo_operacao, t.data_transferencia
FROM transferencia t
LEFT JOIN pessoa p1 ON t.id_doador = p1.id_pessoa
LEFT JOIN pessoa p2 ON t.id_destinatario = p2.id_pessoa
LEFT JOIN componente_periferico c ON t.id_componente = c.id_componente
ORDER BY t.data_transferencia DESC;
```
---

## ✒️Considerações Finais

Esse modelo busca manter a consistência dos dados através de:
Chaves primárias e estrangeiras bem definidas.
Enumerações para padronizar status e tipos.
Índices para otimizar buscas em campos críticos.
Este banco de dados é uma base sólida para o desenvolvimento de sistemas de gestão de doações e controle de inventário no contexto educacional e social promovido pelo PIDS Tech.

