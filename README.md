#  Análise de Sentimentos em Áudios de Consultas Psicológicas

> **IA para Dev — Fase 4 | Tech Challenge FIAP**

API REST multimodal que recebe áudios de consultas psicológicas, transcreve o conteúdo, classifica emoções na fala e gera análises psicológicas não-diagnósticas estruturadas em JSON — tudo orquestrado via LangChain/LangGraph.

## 👥 Equipe

| Nome | RM |
|------|-----|
| Bruno Amorim | RM365279 |
| Gabriel Rizzo | RM366033 |
| Mauricio Magnani | RM365929 |
| Vinicius Martins | RM365278 |
| Gerson Luiz | RM366284 |

---

## 🏗️ Arquitetura

A solução é uma **API REST** desenvolvida com Flask (Python 3.10+), exposta na porta `5001`, que recebe áudios codificados em base64 e executa um pipeline multimodal de análise. A orquestração dos modelos de IA é feita via **LangChain/LangGraph**, com chamadas a provedores externos (OpenRouter) e inferência local (HuggingFace Transformers + PyTorch).

### Pipeline Principal

O endpoint central `/analyse-patient-psychological-issue` orquestra três módulos em sequência:

1. **Transcrição** — O áudio em base64 é enviado ao modelo GPT-4o Audio Preview (via OpenRouter), que retorna o texto transcrito no idioma original.

2. **Classificação de Emoção** — O áudio é processado pelo modelo Whisper Large V3 fine-tuned para Speech Emotion Recognition (`firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3`), usando `librosa` para pré-processamento e PyTorch para inferência local, retornando o label da emoção detectada (`angry`, `sad`, `fearful`, `neutral`, etc.).

3. **Análise Psicológica** — A transcrição (texto) e a emoção (label) são combinadas e enviadas ao GPT-4o via LangChain `PromptTemplate`, gerando uma análise psicológica não-diagnóstica estruturada em JSON.

### Fluxo de Dados

```
Áudio (base64) → Transcrição (texto) + Classificação (emoção)
                         ↓
              Análise Psicológica (JSON estruturado)
```

O resultado final agrega as três saídas em um único payload JSON contendo: `transcription`, `emotion` e `resume` (análise completa).

---

## 📡 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Informações sobre a API e endpoints disponíveis |
| `GET` | `/health` | Health check com status das dependências |
| `POST` | `/transcribe-audio` | Transcreve áudio (base64) para texto |
| `POST` | `/predict-emotion` | Classifica emoção do áudio via Whisper SER |
| `POST` | `/analyse-audio-psycological-issue` | Análise psicológica direta do áudio |
| `POST` | `/analyse-patient-psychological-issue` | **Pipeline completo:** transcrição + emoção + análise |

---

## 🤖 Modelos Aplicados

### Áudio → Texto (Transcrição)

- **Modelo:** GPT-4o Audio Preview (`openai/gpt-4o-audio-preview`)
- **Provedor:** OpenRouter (`openrouter.ai/api/v1`)
- **Integração:** LangChain `ChatOpenAI` com `HumanMessage` contendo content type `input_audio`
- **Temperature:** `0.0` (determinístico para transcrição fiel)

O áudio é enviado diretamente em base64 dentro do payload da mensagem, sem necessidade de salvar arquivos temporários.

### Áudio → Emoção (Classificação)

- **Modelo:** `firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3`
- **Base:** OpenAI Whisper Large V3 fine-tuned para Speech Emotion Recognition
- **Framework:** HuggingFace Transformers (`AutoModelForAudioClassification` + `AutoFeatureExtractor`)
- **Inferência:** PyTorch (CPU ou CUDA quando disponível)

O pipeline utiliza `librosa` para carregar o áudio, normaliza para até 30 segundos com padding, e o modelo retorna logits mapeados para labels de emoção (`angry`, `sad`, `fearful`, `neutral`, `happy`, etc.) via argmax.

### Texto + Emoção → Análise Psicológica

- **Modelo:** GPT-4o (`openai/gpt-4o` via OpenRouter)
- **Integração:** LangChain `PromptTemplate` com chain (`prompt | llm`)
- **Temperature:** `0.5` (balanceamento entre criatividade e consistência)
- **Output:** JSON estruturado com `response_format: json_object`

O prompt gera análises não-diagnósticas com regras rígidas: linguagem cautelosa, evidências primeiro, triagem de risco, disclaimer obrigatório e score de confiabilidade.

### Clientes Configurados

O projeto utiliza dois provedores de LLM: **OpenAI direta** (GPT-3.5-turbo como fallback) e **OpenRouter** como gateway principal para GPT-4o e GPT-4o Audio Preview. Todos configurados via LangChain `ChatOpenAI` com variáveis de ambiente para as API keys.

---

## 🧪 Resultados e Testes

### Dataset de Teste

| Áudio | Emoção Esperada | Origem |
|-------|----------------|--------|
| `pt-br-angry` | Raiva | YouTube (consulta com relato agressivo) |
| `pt-br-angry-2` | Raiva | YouTube (relato emocional intenso) |
| `pt-br-sad` | Tristeza | YouTube (relato de luto/perda) |
| `pt-br-fearful` | Medo | YouTube (relato de violência doméstica) |
| `en-neutral` | Neutro | Dataset HuggingFace (consulta padrão) |

### Estrutura do JSON de Saída

| Campo | Descrição |
|-------|-----------|
| `disclaimer` | Aviso obrigatório de que a análise é não-diagnóstica |
| `text_summary` | Resumo neutro do conteúdo transcrito (1–3 frases) |
| `observed_cues` | Lista de sinais emocionais observados com categoria e relevância |
| `possible_interpretations` | Interpretações cautelosas sem rótulo diagnóstico |
| `alternative_explanations_and_limitations` | Explicações alternativas (mín. 3 itens) |
| `risk_screening` | Triagem de risco: automutilação, suicídio, violência, perigo iminente |
| `confiability_score` | Score 0–100 com label (`low`/`medium`/`high`) e justificativa |
| `follow_up_questions_for_clinician` | 3–8 perguntas sugeridas para o psicólogo |
| `recommendation` | Recomendação personalizada baseada na emoção detectada |

### Anomalias Detectadas

O sistema demonstrou capacidade de identificar os seguintes padrões nos áudios de teste:

- **Sinais de depressão pós-parto** — Detectados em áudios com emoção `sad`, com `observed_cues` relacionados a fadiga, desesperança e isolamento social.
- **Indicadores de violência doméstica** — Identificados em áudios `fearful`, com triagem de risco ativada para `violence_or_imminent_danger_signals`.
- **Ansiedade e estresse agudo** — Detectados em áudios `angry`, com recomendações de técnicas de respiração e busca por apoio profissional.
- **Triagem de risco automática** — O campo `risk_screening` classificou corretamente sinais de `self-harm` como `possible`/`likely` quando o conteúdo indicava situações de perigo.

### Disclaimer e Segurança

Todas as respostas incluem um **disclaimer obrigatório** indicando que a análise é não-diagnóstica e deve ser utilizada exclusivamente por um psicólogo certificado. O prompt foi projetado com regras non-negotiable para evitar rótulos diagnósticos e utilizar linguagem cautelosa.

---

## ⚙️ Stack Tecnológica

| Tecnologia | Papel no Projeto |
|------------|-----------------|
| **Flask 3.1+** | Framework web (API REST) |
| **LangChain / LangGraph** | Orquestração de LLMs e pipelines de prompts |
| **OpenAI GPT-4o** | Análise psicológica não-diagnóstica (via OpenRouter) |
| **GPT-4o Audio Preview** | Transcrição de áudio (via OpenRouter) |
| **Whisper Large V3** (fine-tuned) | Classificação de emoções em fala (HuggingFace) |
| **PyTorch + Transformers** | Inferência do modelo de emoções |
| **librosa** | Pré-processamento de áudio |
| **Python 3.10+ / uv** | Runtime e gerenciamento de dependências |

---

## 🔗 Artefatos

- **Repositório GitHub:** [github.com/gabrielrizzo/tech-challenge-modulo-4](https://github.com/gabrielrizzo/tech-challenge-modulo-4)
- **Datasets HuggingFace:**
  - [TTS Dataset](https://huggingface.co/datasets/brunoretiro/saude-mulher-openai-tts)
  - [Health Dataset](https://huggingface.co/datasets/brunoretiro/womanhealthfiap)
- **Vídeo Demonstrativo:** *(inserir link do YouTube)*

---

> **Fevereiro 2026** — FIAP IA para Dev
