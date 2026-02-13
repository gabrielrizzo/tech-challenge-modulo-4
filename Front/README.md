# Frontend - Tech Challenge Módulo 4

Interface web para análise psicológica de áudio usando IA.

## 🎯 Funcionalidades

### 1. Upload de Áudio
- Suporte para arquivos **MP3** e **WAV**
- Conversão automática para Base64
- Preview do áudio antes do envio
- Quatro tipos de análise disponíveis:
  - **🎯 Transcrever Áudio**: Converte áudio em texto
  - **🧠 Análise Psicológica**: Análise psicológica NÃO-DIAGNÓSTICA do conteúdo
  - **😊 Detectar Emoção**: Identifica a emoção presente no áudio
  - **🔬 Análise Completa**: Executa transcrição + emoção + análise psicológica em uma única operação

### 2. Biblioteca de Áudios
- Listagem automática dos áudios na pasta `audios/`
- Player integrado para ouvir os áudios
- Botões de análise rápida para cada áudio
- Ícones indicativos baseados no nome do arquivo

## 🚀 Como Usar

### Pré-requisitos

1. Certifique-se de que a API está rodando:
```bash
# Na raiz do projeto
python main.py
```

A API deve estar rodando em `http://localhost:5001`

2. Instale as dependências (se ainda não instalou):
```bash
uv sync
```

### Acessando o Frontend

Abra seu navegador e acesse:
```
http://localhost:5001/frontend
```

### Usando o Frontend

#### Opção 1: Upload de Novo Áudio

1. Clique em "Escolher arquivo MP3 ou WAV"
2. Selecione um arquivo de áudio do seu computador
3. O áudio será exibido em um player para preview
4. Escolha uma das opções de análise:
   - **Transcrever**: Para obter o texto do áudio
   - **Análise Psicológica**: Para análise detalhada
   - **Detectar Emoção**: Para identificar a emoção

#### Opção 2: Usar Áudios da Biblioteca

1. Role até a seção "Biblioteca de Áudios"
2. Clique no player para ouvir o áudio
3. Clique em um dos botões de análise abaixo do player
4. O resultado aparecerá na seção de resultados acima

## 🎨 Design

O frontend utiliza:
- **HTML5** puro
- **CSS3** com variáveis CSS e gradientes modernos
- **JavaScript ES6+** (ECMAScript puro, sem frameworks)
- Design responsivo para mobile e desktop
- Tema escuro moderno
- Animações suaves

## 📁 Estrutura de Arquivos

```
Front/
├── index.html      # Estrutura HTML principal
├── styles.css      # Estilos CSS
├── script.js       # Lógica JavaScript
└── README.md       # Este arquivo
```

## 🔧 Configuração da API

O frontend se comunica com os seguintes endpoints:

- `POST /transcribe-audio` - Transcrição de áudio
- `POST /analyse-audio-psycological-issue` - Análise psicológica
- `POST /predict-emotion` - Detecção de emoção
- `GET /list-audios` - Lista áudios disponíveis
- `GET /audio/<filename>` - Serve arquivo de áudio

## 🐛 Troubleshooting

### A biblioteca de áudios não carrega
- Verifique se a API está rodando em `http://localhost:5001`
- Verifique se existem arquivos `.mp3` ou `.wav` na pasta `audios/`
- Abra o console do navegador (F12) para ver possíveis erros

### Erro ao enviar áudio
- Certifique-se de que o arquivo é MP3 ou WAV válido
- Verifique se as chaves de API estão configuradas no `.env`
- Verifique o console do navegador para detalhes do erro

### CORS Error
- A dependência `flask-cors` deve estar instalada
- Execute `uv sync` para instalar as dependências

## 📝 Notas Técnicas

### Conversão Base64
O JavaScript converte os arquivos de áudio para Base64 usando a API `FileReader` do navegador:
```javascript
const reader = new FileReader();
reader.readAsDataURL(file);
```

### Formato de Requisição
```json
{
  "audio_data": "base64_string_here",
  "audio_format": "mp3" // ou "wav"
}
```

## 🎓 FIAP - Pós-Graduação

Projeto desenvolvido para o Tech Challenge do Módulo 4.

### Tecnologias Utilizadas
- HTML5
- CSS3 (Flexbox, Grid, Variables)
- JavaScript ES6+ (Fetch API, Async/Await, FileReader)
- Flask (Backend)
- OpenAI GPT-4o (IA)
