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

### Frontend Web

O projeto inclui uma interface web moderna e responsiva para facilitar o uso da API.

**Acesse o frontend em:** `http://localhost:5001/frontend`

#### Funcionalidades do Frontend:
- 📤 **Upload de áudio**: Envie arquivos MP3 ou WAV diretamente do navegador
- 🎯 **Transcrição**: Converta áudio em texto
- 🧠 **Análise Psicológica**: Análise detalhada do conteúdo
- 😊 **Detecção de Emoção**: Identifique emoções no áudio
- 📚 **Biblioteca de Áudios**: Acesse e analise os áudios de exemplo
- 🎨 **Design Moderno**: Interface dark com animações suaves

Para mais detalhes, consulte: [Front/README.md](Front/README.md)

### Endpoints da API

A API roda por padrão em `http://localhost:5001`.

#### Sistema

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações sobre a API e endpoints disponíveis |
| GET | `/health` | Health check com status das dependências |
| GET | `/frontend` | Interface web do projeto |
| GET | `/list-audios` | Lista arquivos de áudio disponíveis |
| GET | `/audio/<filename>` | Serve arquivo de áudio específico |

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
| POST | `/predict-emotion` | Detecta emoção presente no áudio |

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

### Audios utilizados para teste

Segue a relação dos base64 com a origem dos audios utilizados contidos no diretório `audios`:

[https://www.youtube.com/watch?v=dwfTKWKc2so](https://www.youtube.com/watch?v=dwfTKWKc2so) -> base64-pt-br-fearful.txt

[https://www.youtube.com/watch?v=I9thtEjSb44&t=91s](https://www.youtube.com/watch?v=I9thtEjSb44&t=91s) -> base64-pt-br-sad.txt

[https://www.youtube.com/watch?v=Hd2GBfneepk&list=PLxlQ6wmJ-XT_alzF3TnfhnnhZgWqH3GRH](https://www.youtube.com/watch?v=Hd2GBfneepk&list=PLxlQ6wmJ-XT_alzF3TnfhnnhZgWqH3GRH) -> base64-pt-br-angry.txt

[https://www.youtube.com/watch?v=CBPBsKs1E04](https://www.youtube.com/watch?v=CBPBsKs1E04) -> base64-pt-br-angry-2.txt

[Link dataset que geramos no Huggin Face](https://datasets-server.huggingface.co/cached-assets/brunoretiro/womanhealthfiap/--/3441b0d17d337325e1fdb799602c8f193890a1e5/--/default/train/0/audio/audio.mp3?Expires=1770861449&Signature=q61Y1MNtrH9PlhI-3hF67U~w2fgDY8Q88klQ5tmEwt3-WDVKk0COQ6ifMcMHuHahrWlc6Tv12J4lDkUhH0en~9vNKGKCzmLP~7bTALGQOXB7knzr4Xf5fJixuHB3y8Ygj1POaNiVd1tT8bSbkBIL16IEU4TywT64jTwzr~9Qct58E7qb2FvxkHWR0EVjgEsm6tS8V-ZaIyb7wesy3mTE6mOyr~hPtHTpFsNvCqgWQt-jiejwwTnVwivxBiWkXYAPrwn6~mw~v85ofuoB42JG~bDSjn0OEYF-IH2RdyG-SxG5b3zyeKLgQUsfvfz3emXppwkfFsZhxfFomjWnyE7xFw__&Key-Pair-Id=K3EI6M078Z3AC3) -> base64-en-neutral.txt


