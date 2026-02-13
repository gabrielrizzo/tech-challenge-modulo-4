# 🔐 Página de Configuração de Chaves de IA

Página web para gerenciar as chaves de API necessárias para o funcionamento do projeto.

## 🎯 Funcionalidades

### ✅ Recursos Implementados

1. **Verificação Automática do .env**
   - Detecta se o arquivo `.env` existe
   - Mostra quais chaves estão configuradas
   - Indica chaves faltantes

2. **Criação/Atualização de Chaves**
   - Cria arquivo `.env` se não existir
   - Atualiza chaves existentes
   - Mantém chaves não modificadas

3. **Validação de Formato**
   - OpenAI: deve começar com `sk-`
   - OpenRouter: deve começar com `sk-or-v1-`
   - Validação em tempo real

4. **Segurança**
   - Campos de senha mascarados
   - Botão de visualização temporária
   - Chaves parcialmente ocultas ao carregar

5. **Testes de Conectividade**
   - Teste da chave OpenRouter
   - Health check completo da API
   - Resultados visuais detalhados

## 🚀 Como Usar

### Acessar a Página

```
http://localhost:5001/config
```

Ou clique no botão **"🔐 Configurar Chaves de API"** na página principal.

### Primeira Configuração

Se o arquivo `.env` **não existe**:

1. Acesse `/config`
2. Você verá: **"⚠️ Arquivo .env não encontrado!"**
3. Preencha pelo menos a **OpenRouter API Key** (obrigatória)
4. Clique em **"💾 Salvar Configurações"**
5. O arquivo `.env` será criado automaticamente
6. **Reinicie o servidor Flask**

### Atualizar Chaves Existentes

Se o arquivo `.env` **já existe**:

1. Acesse `/config`
2. Você verá: **"✅ Arquivo .env encontrado!"**
3. Os campos mostrarão as chaves mascaradas: `sk-or-v1-••••abc1`
4. Preencha APENAS as chaves que deseja atualizar
5. Deixe em branco para manter a chave atual
6. Clique em **"💾 Salvar Configurações"**
7. **Reinicie o servidor Flask**

## 🔑 Sobre as Chaves

### OpenRouter API Key (Obrigatória) 🌐

**Status:** ⚠️ **ESSENCIAL** para funcionamento

**Usado para:**
- ✅ Transcrição de áudio (`/transcribe-audio`)
- ✅ Análise psicológica de áudio (`/analyse-audio-psycological-issue`)
- ✅ Análise completa de paciente (`/analyse-patient-psychological-issue`)

**Formato:** `sk-or-v1-[40 caracteres hexadecimais]`

**Como obter:**
1. Acesse: https://openrouter.ai/
2. Crie uma conta
3. Vá em **Keys**
4. Crie uma nova API key
5. Copie e cole na página de configuração

**Modelo usado:** `openai/gpt-4o-audio-preview`

### OpenAI API Key (Opcional) 🤖

**Status:** ℹ️ **Atualmente não utilizada**

**Configurada para uso futuro**

**Formato:** `sk-[48+ caracteres]`

**Como obter:**
1. Acesse: https://platform.openai.com/api-keys
2. Crie uma conta
3. Crie uma nova API key
4. Copie e cole na página de configuração

## 🧪 Testando a Configuração

### Teste 1: OpenRouter

Clique em **"🌐 Testar OpenRouter"**

**Resultado esperado:**
```
✅ OpenRouter está funcionando!
Chave válida e conectada.
```

**Se der erro:**
- Verifique se a chave está correta
- Verifique se começa com `sk-or-v1-`
- Verifique se reiniciou o servidor

### Teste 2: Health Check

Clique em **"❤️ Health Check da API"**

**Resultado esperado:**
```
✅ Status: HEALTHY

Dependências:
OpenAI: ✅ ou ❌
OpenRouter: ✅
Flask: ✅
LangChain: ✅
```

## 📁 Estrutura de Arquivos

```
Front/
├── config.html          # Página HTML de configuração
├── config-styles.css    # Estilos específicos
├── config-script.js     # Lógica JavaScript
└── CONFIG.md           # Este arquivo
```

## 🔧 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/config` | Serve a página de configuração |
| GET | `/config/check` | Verifica se .env existe |
| GET | `/config/get` | Retorna chaves atuais (mascaradas) |
| POST | `/config/save` | Salva/atualiza chaves |
| GET | `/config/test-openrouter` | Testa chave OpenRouter |

### Exemplo de Requisição

```javascript
// Salvar configurações
fetch('http://localhost:5001/config/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        openai_key: 'sk-...',
        openrouter_key: 'sk-or-v1-...'
    })
});
```

## ⚠️ Importante

### 1. Reiniciar o Servidor

**Após salvar as chaves, você DEVE reiniciar o servidor Flask:**

```bash
# Pressione CTRL+C no terminal
# Depois execute novamente:
python main.py
```

**Por quê?**
O Flask carrega as variáveis de ambiente apenas na inicialização. Mudanças no `.env` só têm efeito após reiniciar.

### 2. Segurança

- ✅ O arquivo `.env` está no `.gitignore`
- ✅ Nunca commite o `.env` no Git
- ✅ Nunca compartilhe suas chaves publicamente
- ✅ Use `.env.example` para documentar variáveis necessárias

### 3. Backup

Antes de modificar chaves existentes, faça backup:

```bash
# Windows PowerShell
copy .env .env.backup

# Linux/Mac
cp .env .env.backup
```

## 🎨 Interface

### Cores e Estados

| Estado | Cor | Significado |
|--------|-----|-------------|
| 🟢 Verde | `#10b981` | Chave configurada e funcionando |
| 🟡 Amarelo | `#f59e0b` | Aviso ou chave opcional não configurada |
| 🔴 Vermelho | `#ef4444` | Erro ou chave obrigatória faltando |
| 🔵 Azul | `#6366f1` | Informação ou estado normal |

### Elementos da Interface

1. **Status Card** - Mostra estado atual do `.env`
2. **Form Card** - Formulário de configuração
3. **Info Card** - Informações sobre as chaves
4. **Test Card** - Testes de conectividade

## 🐛 Troubleshooting

### Problema: "Erro ao verificar configurações"

**Causa:** API não está rodando

**Solução:**
```bash
python main.py
```

### Problema: Chaves não estão sendo salvas

**Causa:** Permissões de arquivo

**Solução (Linux/Mac):**
```bash
chmod 644 .env
```

**Solução (Windows):**
- Verifique se o arquivo não está aberto em outro programa
- Verifique permissões da pasta

### Problema: Após salvar, as funcionalidades não funcionam

**Causa:** Servidor não foi reiniciado

**Solução:**
1. Pressione `CTRL+C` no terminal do Flask
2. Execute `python main.py` novamente

### Problema: "Formato inválido para chave"

**Causa:** Chave não está no formato correto

**Solução:**
- OpenRouter deve começar com: `sk-or-v1-`
- OpenAI deve começar com: `sk-`
- Copie e cole a chave completa sem espaços

## 📊 Fluxo de Uso

```
1. Acessar /config
       ↓
2. Verificar status do .env
       ↓
   .env existe?
   ↙         ↘
 SIM         NÃO
   ↓           ↓
Atualizar   Criar novo
   ↓           ↓
3. Preencher chaves
       ↓
4. Salvar
       ↓
5. Reiniciar servidor
       ↓
6. Testar configuração
       ↓
7. Usar aplicação
```

## 💡 Dicas

1. **Use o teste de OpenRouter** antes de usar o app
2. **Mantenha um backup** do `.env`
3. **Configure em ambiente de desenvolvimento** primeiro
4. **Use `.env.example`** para documentar variáveis necessárias
5. **Verifique o health check** regularmente

## 🔗 Links Úteis

- [OpenRouter - Criar Conta](https://openrouter.ai/)
- [OpenRouter - Documentação](https://openrouter.ai/docs)
- [OpenAI - API Keys](https://platform.openai.com/api-keys)
- [python-dotenv - Documentação](https://pypi.org/project/python-dotenv/)

---

**FIAP - Pós-Graduação em Inteligência Artificial | Tech Challenge Módulo 4 | 2026**
