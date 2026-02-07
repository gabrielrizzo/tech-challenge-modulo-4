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
uv run main.py
```

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:

```bash
OPEN_AI_API_KEY="sua_chave_openai"
OPENROUTER_API_KEY="sua_chave_openrouter"
```

### Endpoints da API

A API roda por padrão em `http://localhost:5001`.

#### Sistema

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações sobre a API e endpoints disponíveis |
| GET | `/health` | Health check com status das dependências |

#### Análise de Texto

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/resume` | Resume textos usando IA |
| POST | `/analyse-psycological-issue` | Análise psicológica NÃO-DIAGNÓSTICA de textos |

**Exemplo de uso:**

```bash
curl -X POST http://localhost:5001/resume \
  -H "Content-Type: application/json" \
  -d '{"text": "Seu texto aqui..."}'
```

#### Análise de Áudio

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/transcribe-audio` | Transcreve áudio para texto |
| POST | `/analyse-audio-psycological-issue` | Análise psicológica NÃO-DIAGNÓSTICA de áudio |

**Parâmetros:**

- `audio_data` (obrigatório): Áudio codificado em base64
- `audio_format` (opcional): Formato do áudio (`wav` ou `mp3`). Default: `wav`

**Exemplo de uso:**

```bash
# Converter áudio para base64
AUDIO_BASE64=$(base64 -i seu_audio.wav)

# Transcrever áudio
curl -X POST http://localhost:5001/transcribe-audio \
  -H "Content-Type: application/json" \
  -d "{\"audio_data\": \"$AUDIO_BASE64\", \"audio_format\": \"wav\"}"

# Análise psicológica de áudio
curl -X POST http://localhost:5001/analyse-audio-psycological-issue \
  -H "Content-Type: application/json" \
  -d "{\"audio_data\": \"$AUDIO_BASE64\", \"audio_format\": \"wav\"}"
```

### Tecnologias

- Flask
- LangChain / LangGraph
- OpenAI (GPT-4o)
- OpenRouter (GPT-4o Audio Preview)

