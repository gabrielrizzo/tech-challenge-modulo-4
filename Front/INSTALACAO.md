# 🚀 Guia de Instalação e Uso - Frontend

## Passo 1: Instalar Dependências

Certifique-se de que está na raiz do projeto e execute:

```bash
uv sync
```

Isso instalará todas as dependências necessárias, incluindo o `flask-cors` que foi adicionado para permitir requisições do frontend.

## Passo 2: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (se ainda não existir):

```bash
OPEN_AI_API_KEY="sua_chave_openai"
OPENROUTER_API_KEY="sua_chave_openrouter"
```

## Passo 3: Iniciar o Servidor

Execute o servidor Flask:

```bash
python main.py
```

Ou usando o uv:

```bash
uv run main.py
```

Você verá uma mensagem indicando que o servidor está rodando em `http://0.0.0.0:5001`

## Passo 4: Acessar o Frontend

Abra seu navegador e acesse:

```
http://localhost:5001/frontend
```

## 🎯 Como Usar

### Opção 1: Upload de Novo Áudio

1. **Selecionar Arquivo**
   - Clique no botão "Escolher arquivo MP3 ou WAV"
   - Selecione um arquivo de áudio do seu computador
   - Formatos suportados: `.mp3` e `.wav`

2. **Preview**
   - Após selecionar, um player de áudio aparecerá
   - Você pode ouvir o áudio antes de enviar

3. **Escolher Análise**
   - **🎯 Transcrever Áudio**: Converte o áudio em texto
   - **🧠 Análise Psicológica**: Realiza análise psicológica NÃO-DIAGNÓSTICA
   - **😊 Detectar Emoção**: Identifica a emoção presente no áudio

4. **Ver Resultado**
   - O resultado aparecerá na seção abaixo dos botões
   - Um spinner indicará que o processamento está em andamento

### Opção 2: Usar Áudios da Biblioteca

1. **Navegar pela Biblioteca**
   - Role até a seção "Biblioteca de Áudios"
   - Você verá cards com todos os áudios disponíveis na pasta `audios/`

2. **Ouvir Áudio**
   - Cada card possui um player integrado
   - Clique em play para ouvir o áudio

3. **Analisar**
   - Clique em um dos botões abaixo do player:
     - 🎯 Transcrever
     - 🧠 Analisar
     - 😊 Emoção
   - O resultado aparecerá na seção de resultados no topo da página

## 📊 Tipos de Análise

### 1. Transcrição (🎯)
Converte o áudio em texto usando IA da OpenAI.

**Exemplo de resposta:**
```
📝 Transcrição:

Olá, meu nome é João e estou muito feliz hoje...
```

### 2. Análise Psicológica (🧠)
Realiza uma análise psicológica NÃO-DIAGNÓSTICA do conteúdo do áudio.

**Exemplo de resposta:**
```
🧠 Análise Psicológica:

A análise do discurso revela...
- Tom emocional: positivo
- Temas principais: ...
```

### 3. Detecção de Emoção (😊)
Identifica a emoção predominante no áudio.

**Exemplo de resposta:**
```
😊 Emoção Detectada:

😊 happy
```

Emoções possíveis:
- 😠 angry (raiva)
- 😢 sad (tristeza)
- 😊 happy (felicidade)
- 😐 neutral (neutro)
- 😨 fearful (medo)
- 🤢 disgust (nojo)
- 😲 surprised (surpresa)

## 🔧 Troubleshooting

### Problema: "Erro ao carregar biblioteca de áudios"

**Solução:**
1. Verifique se o servidor Flask está rodando
2. Acesse `http://localhost:5001/health` para verificar o status
3. Verifique se existem arquivos `.mp3` ou `.wav` na pasta `audios/`

### Problema: "Erro ao processar áudio"

**Solução:**
1. Verifique se as chaves de API estão configuradas no `.env`
2. Verifique se o arquivo é um MP3 ou WAV válido
3. Abra o console do navegador (F12) para ver detalhes do erro
4. Verifique os logs do servidor Flask no terminal

### Problema: CORS Error

**Solução:**
1. Certifique-se de que instalou as dependências: `uv sync`
2. Verifique se `flask-cors` está listado em `pyproject.toml`
3. Reinicie o servidor Flask

### Problema: Botões desabilitados

**Solução:**
1. Certifique-se de que selecionou um arquivo de áudio
2. Aguarde a conversão para base64 completar
3. Verifique se o arquivo é MP3 ou WAV válido

## 💡 Dicas

1. **Tamanho do Arquivo**: Arquivos muito grandes podem demorar para processar
2. **Qualidade**: Áudios com melhor qualidade produzem melhores resultados
3. **Idioma**: A API funciona melhor com português e inglês
4. **Tempo de Processamento**: Análises psicológicas podem levar mais tempo

## 🎨 Recursos do Frontend

- ✅ Design responsivo (funciona em mobile e desktop)
- ✅ Tema dark moderno
- ✅ Animações suaves
- ✅ Feedback visual de loading
- ✅ Mensagens de erro amigáveis
- ✅ Preview de áudio antes do envio
- ✅ Conversão automática para base64
- ✅ Biblioteca de áudios integrada

## 📱 Compatibilidade

O frontend é compatível com:
- ✅ Chrome/Edge (recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ✅ Navegadores modernos que suportam ES6+

## 🔐 Segurança

- Os áudios são convertidos para base64 no navegador
- Nenhum arquivo é armazenado permanentemente no servidor
- As chaves de API ficam apenas no servidor (não são expostas ao frontend)

## 📞 Suporte

Em caso de dúvidas ou problemas:
1. Verifique este guia primeiro
2. Consulte o README principal do projeto
3. Verifique os logs do servidor Flask
4. Abra o console do navegador (F12) para ver erros JavaScript

---

**FIAP - Pós-Graduação em Inteligência Artificial | Tech Challenge Módulo 4 | 2026**
