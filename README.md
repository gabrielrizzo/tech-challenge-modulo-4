## Tech Challenge Módulo 4

Projeto Python (Flask + LangChain/LangGraph).

### Requisitos

- **Python**: versão **3.10** ou superior
- **Gerenciador de dependências**: recomenda-se **uv** (pois o projeto já possui `pyproject.toml` e `uv.lock`)

### Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd tech-challenge-modulo-4
```

### Instalar dependências (usando `uv`)

- **Instalar o uv** (se ainda não tiver):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- **Instalar as dependências definidas em `pyproject.toml`/`uv.lock`**:

```bash
uv sync
```

Isso criará (ou utilizará) um ambiente virtual e instalará todas as dependências do projeto.

### Ativar o ambiente virtual criado pelo `uv`

```bash
source .venv/bin/activate
```

Se estiver no Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

### Executar o projeto

Com o ambiente ativado na raiz do projeto:

```bash
python main.py
```

Ou, caso você prefira usar o `uv` diretamente:

```bash
uv run python main.py
```

### Variáveis de ambiente

Caso o projeto use variáveis de ambiente (por exemplo, chaves de API para modelos), crie um arquivo `.env` na raiz do projeto e defina as chaves necessárias, por exemplo:

```bash
OPENAI_API_KEY="sua_chave_aqui"
```

Consulte o código (por exemplo `main.py` e a pasta `agents/`) para ver quais variáveis são esperadas.

