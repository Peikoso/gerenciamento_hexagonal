<div align="center">

# 🔷 Gerenciamento Hexagonal

**Sistema de gerenciamento de propostas, metas e contrapartidas construído com Arquitetura Hexagonal**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)](https://python-poetry.org)

*Projeto de faculdade / iniciação científica — por [João Martins](mailto:joaommn1998@gmail.com)*

</div>

---

## 📌 Visão Geral

Este projeto implementa um sistema de **gerenciamento de propostas** seguindo o padrão de **Arquitetura Hexagonal** (Ports & Adapters), garantindo que a lógica de negócio fique completamente isolada de frameworks e tecnologias externas.

O domínio gerencia:
- 📋 **Propostas** de gerenciamento
- 🎯 **Metas** com indicadores quantitativos
- 📊 **Indicadores qualitativos e quantitativos**
- 💰 **Contrapartidas** e aprovações administrativas
- 📎 **Arquivos** vinculados a metas, qualitativos e contrapartidas
- 💬 **Comentários** associados às entidades
- 📄 **Relatórios** consolidados

---

## 🧩 Arquitetura Hexagonal (Ports & Adapters)

O coração do projeto é a separação em camadas com **inversão de dependência**:

```
┌─────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE                             │
│                                                                 │
│   ┌─────────────┐    ┌─────────────────────────────────────┐    │
│   │   FastAPI    │    │   SQLAlchemy Repositories            │    │
│   │   Quart      │    │   (Adapters de saída)               │    │
│   │  (Adapters   │    │                                     │    │
│   │  de entrada) │    │   Implementam as interfaces          │    │
│   └──────┬───────┘    │   abstratas do Domain                │    │
│          │            └──────────────┬──────────────────────┘    │
│          │                           │                           │
│  ┌───────▼───────────────────────────▼──────────────────────┐   │
│  │                    APPLICATION                            │   │
│  │                                                           │   │
│  │   Services (Use Cases)          Interfaces (Ports)        │   │
│  │   ┌──────────────────┐         ┌───────────────────┐     │   │
│  │   │ MetaServiceImpl  │────────▶│ MetaServices(ABC) │     │   │
│  │   │ PropostaImpl     │         │ PropostaServices  │     │   │
│  │   │ QualitativoImpl  │         │ ...               │     │   │
│  │   └──────────────────┘         └───────────────────┘     │   │
│  │              │                                            │   │
│  │   ┌──────────▼─────────────────────────────────────┐     │   │
│  │   │                   DOMAIN                        │     │   │
│  │   │                                                 │     │   │
│  │   │  Models (Pydantic)    Repositories (ABC/Ports)  │     │   │
│  │   │  Exceptions           Validations               │     │   │
│  │   │  Domain Services                                │     │   │
│  │   │                                                 │     │   │
│  │   │  ★ Sem dependência de framework externo ★       │     │   │
│  │   └─────────────────────────────────────────────────┘     │   │
│  └───────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Princípios aplicados

| Princípio | Como é aplicado |
|---|---|
| **Ports** (Portas) | Interfaces abstratas (`ABC`) em `domain/repositories/` e `application/services/interfaces/` |
| **Adapters** (Adaptadores) | Implementações concretas em `infrastructure/repositories/sqlalchemy/` e `infrastructure/handler/` |
| **Inversão de Dependência** | Services recebem repositórios por injeção via `application/dependencies.py` |
| **Domínio Puro** | Modelos Pydantic sem acoplamento a banco ou framework |
| **Handlers Intercambiáveis** | FastAPI e Quart como adaptadores HTTP substituíveis |

---

## 📂 Estrutura de Diretórios

```
gerenciamento_hexagonal/
│
├── domain/                          # 🟡 Núcleo — sem dependências externas
│   ├── models/                      #    Entidades (Pydantic): Proposta, Meta, etc.
│   ├── repositories/                #    Ports de saída (interfaces abstratas)
│   ├── services/                    #    Regras de domínio (validações, arquivo)
│   └── exceptions/                  #    Exceções de negócio
│
├── application/                     # 🟢 Orquestração — use cases
│   ├── services/                    #    Implementações dos serviços
│   │   ├── interfaces/              #    Ports de entrada (interfaces abstratas)
│   │   └── gerenciamento/           #    Use cases: meta, proposta, qualitativo...
│   └── dependencies.py              #    Composição: conecta ports ↔ adapters
│
├── infrastructure/                  # 🔵 Mundo externo — adapters
│   ├── handler/
│   │   ├── fastapi/                 #    Adapter HTTP (FastAPI + rotas)
│   │   └── quart/                   #    Adapter HTTP alternativo (Quart)
│   ├── repositories/
│   │   └── sqlalchemy/              #    Adapter de persistência (SQLAlchemy ORM)
│   ├── database/                    #    Configuração do banco (async sessions)
│   ├── alembic/                     #    Migrações de banco de dados
│   └── settings.py                  #    Configurações via variáveis de ambiente
│
└── tests/                           # 🧪 Testes unitários e de integração
    ├── domain/
    ├── services/
    └── infrastructure/
```

---

## ⚡ Tecnologias

| Categoria | Tecnologia | Descrição |
|---|---|---|
| **Linguagem** | Python 3.12+ | Tipagem moderna, `async/await` |
| **Web (Adapter)** | FastAPI | Framework web assíncrono principal |
| **Web (Adapter)** | Quart | Framework alternativo (intercambiável) |
| **ORM (Adapter)** | SQLAlchemy 2.x | Mapeamento objeto-relacional assíncrono |
| **Migrações** | Alembic | Versionamento de schema do banco |
| **Validação** | Pydantic v2 | Modelos de domínio e DTOs |
| **Configuração** | Pydantic Settings | Variáveis de ambiente via `.env` |
| **Banco (async)** | AsyncPG / aiosqlite | Drivers assíncronos para PostgreSQL e SQLite |
| **Testes** | Pytest + pytest-asyncio | Testes assíncronos com cobertura |
| **Linter** | Ruff | Linting e formatação rápida |
| **Task Runner** | Taskipy | Scripts simplificados via Poetry |

---

## 🚀 Como Rodar

### Pré-requisitos

- **Python 3.12+**
- **Poetry** instalado ([guia de instalação](https://python-poetry.org/docs/#installation))

### 1. Clonar o repositório

```bash
git clone https://github.com/seuusuario/gerenciamento-hexagonal.git
cd gerenciamento-hexagonal
```

### 2. Instalar dependências

```bash
poetry install
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite+aiosqlite:///./gerenciamento.db
```

> Para PostgreSQL: `DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/gerenciamento`

### 4. Executar migrações

```bash
poetry run alembic upgrade head
```

### 5. Rodar a aplicação

**FastAPI** (principal):
```bash
poetry run task run
```

**Quart** (alternativo):
```bash
poetry run task run-quart
```

A API estará disponível em `http://localhost:8000` com documentação interativa em `http://localhost:8000/docs`.

---

## 🧪 Testes

```bash
# Lint + Testes com cobertura
poetry run task test
```

O relatório de cobertura HTML será gerado automaticamente após os testes.

---

## 🔄 Fluxo de uma Requisição

```
Cliente HTTP
    │
    ▼
┌──────────────────────┐
│  FastAPI / Quart     │  ← Adapter de entrada (infrastructure/handler)
│  (Rota + Controller) │
└──────────┬───────────┘
           │ chama
           ▼
┌──────────────────────┐
│  Application Service │  ← Use Case (application/services)
│  (ex: MetaServiceImpl)│
└──────────┬───────────┘
           │ usa interface abstrata
           ▼
┌──────────────────────┐
│  Domain Repository   │  ← Port de saída (domain/repositories - ABC)
│  (interface)         │
└──────────┬───────────┘
           │ implementado por
           ▼
┌──────────────────────┐
│  SQLAlchemy Repo     │  ← Adapter de saída (infrastructure/repositories)
│  (implementação)     │
└──────────┬───────────┘
           │
           ▼
       Banco de Dados
```

---

## 📝 Licença

Projeto acadêmico desenvolvido pelo LAPSID para fins de estudo, pesquisa e iniciação científica.

---

