# Gerenciamento Hexagonal

  **Descrição:** Projeto de faculdade / iniciação científica utilizando Arquitetura Hexagonal, FastAPI, SQLAlchemy e Pydantic.

---

## 📌 Visão Geral

Este projeto implementa um sistema seguindo o **padrão de Arquitetura Hexagonal** (Ports & Adapters), permitindo que a lógica de negócio fique isolada de frameworks e tecnologias externas.  
A aplicação é organizada em camadas para facilitar manutenção, escalabilidade e troca de dependências sem impactar o núcleo do sistema.

### Estrutura do Projeto

- **Domain:** Contém as entidades, validações e interfaces de repositório.  
- **Application / Services:** Implementa a lógica de negócio e coordena operações entre repositórios e handlers.  
- **Infrastructure / Handlers:** Implementa adaptadores externos, incluindo FastAPI e Quart para exposição de APIs, persistência com SQLAlchemy e banco de dados assíncrono.  
- **Migrations:** Alembic para versionamento de banco de dados.

---

## ⚡ Tecnologias Utilizadas

- **Python 3.12+**
- **FastAPI** - Framework web assíncrono.
- **Quart** - Framework alternativo para testes de handlers assíncronos.
- **SQLAlchemy 2.x** - ORM para abstração do banco de dados.
- **Alembic** - Migrações de banco de dados.
- **Pydantic / Pydantic-settings** - Validação de dados e configuração.
- **AsyncPG / aiosqlite** - Conexão assíncrona com PostgreSQL ou SQLite.
- **Greenlet** - Suporte para operações assíncronas em SQLAlchemy.

---

## 🏗️ Como Rodar

### 1. Clonar o projeto

```bash
git clone https://github.com/seuusuario/gerenciamento-hexagonal.git
cd gerenciamento-hexagonal
````

### 2. Instalar dependências

```bash
poetry install
```

### 3. Rodar a aplicação

#### FastAPI:

```bash
poetry run task run
```

#### Quart:

```bash
poetry run task run-quart
```

---

## 📂 Estrutura de Diretórios

```
gerenciamento_hexagonal/
│
├── domain/                 # Entidades e interfaces do domínio
├── application/            # Serviços e regras de negócio
├── infrastructure/
│   ├── handler/            # Handlers FastAPI / Quart
│   ├── repository/         # Implementações de repositório (SQLAlchemy)
│   └── alembic/            # Migrações do banco
└── pyproject.toml          # Configuração do Poetry e dependências
```

---

## 🧩 Arquitetura Hexagonal

O projeto segue o modelo **Ports & Adapters**, garantindo:

* **Desacoplamento** da lógica de negócio com frameworks e bancos de dados.
* **Flexibilidade** para trocar ORM, banco ou framework web sem alterar o core.
* **Organização modular**, facilitando manutenção e testes.

---

