# 🔧 Troubleshooting - Players de Áudio Não Funcionam

## Diagnóstico Passo a Passo

### Passo 1: Verificar se a API está rodando

1. Abra o terminal na raiz do projeto
2. Execute:
```bash
python main.py
```

3. Você deve ver algo como:
```
 * Running on http://0.0.0.0:5001
```

### Passo 2: Testar a API

Abra o navegador e acesse:
```
http://localhost:5001/health
```

**Resultado esperado:** JSON com status da API

```
http://localhost:5001/test-audio
```

**Resultado esperado:** Lista de arquivos de áudio com seus caminhos

### Passo 3: Usar Página de Teste

Acesse a página de diagnóstico:
```
http://localhost:5001/frontend/test-audio.html
```

Esta página tem 4 testes:
1. **Teste de Conectividade** - Verifica se a API responde
2. **Teste de Listagem** - Verifica se consegue listar os áudios
3. **Teste de Reprodução Direta** - Players com URLs hardcoded
4. **Teste de Carregamento Dinâmico** - Carrega e exibe todos os áudios

### Passo 4: Verificar Console do Navegador

1. Pressione `F12` para abrir DevTools
2. Vá na aba **Console**
3. Procure por erros em vermelho
4. Vá na aba **Network**
5. Recarregue a página
6. Veja se as requisições para `/audio/...` estão retornando **200 OK** ou erro

## Problemas Comuns

### ❌ Problema: "Failed to load resource: net::ERR_CONNECTION_REFUSED"

**Causa:** API não está rodando

**Solução:**
```bash
# Na raiz do projeto
python main.py
```

### ❌ Problema: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Causa:** CORS não configurado

**Solução:**
1. Verifique se `flask-cors` está instalado:
```bash
uv sync
```

2. Reinicie a API:
```bash
python main.py
```

### ❌ Problema: "404 Not Found" para arquivos de áudio

**Causa:** Arquivos não encontrados ou caminho incorreto

**Solução:**
1. Verifique se os arquivos existem:
```bash
# Windows PowerShell
dir audios\*.mp3
dir audios\*.wav

# Linux/Mac
ls audios/*.mp3
ls audios/*.wav
```

2. Acesse diretamente no navegador:
```
http://localhost:5001/audio/pt-br-angry.mp3
```

Se baixar o arquivo = ✅ Funcionando
Se der erro 404 = ❌ Problema no caminho

### ❌ Problema: Player aparece mas não toca

**Causa:** Formato de áudio não suportado ou arquivo corrompido

**Solução:**
1. Tente abrir o arquivo diretamente:
```
http://localhost:5001/audio/pt-br-angry.mp3
```

2. Verifique o formato do arquivo:
```bash
# Windows PowerShell
Get-Item audios\pt-br-angry.mp3 | Select-Object Name, Length

# Linux/Mac
file audios/pt-br-angry.mp3
```

### ❌ Problema: "The element has no supported sources"

**Causa:** Navegador não consegue carregar o áudio

**Solução:**
1. Verifique se está acessando via `http://localhost:5001/frontend`
2. NÃO abra o arquivo HTML diretamente (file:///)
3. Use Chrome ou Edge (melhor suporte)

## Teste Manual Rápido

### Teste 1: API Funcionando?
```bash
curl http://localhost:5001/health
```
**Esperado:** JSON com status

### Teste 2: Listagem Funcionando?
```bash
curl http://localhost:5001/list-audios
```
**Esperado:** JSON com lista de áudios

### Teste 3: Áudio Acessível?
```bash
curl -I http://localhost:5001/audio/pt-br-angry.mp3
```
**Esperado:** HTTP/1.1 200 OK

### Teste 4: CORS Habilitado?
Abra o Console do navegador e execute:
```javascript
fetch('http://localhost:5001/health')
  .then(r => r.json())
  .then(d => console.log('✅ CORS OK:', d))
  .catch(e => console.error('❌ CORS Error:', e));
```

## Checklist de Verificação

- [ ] API está rodando em http://localhost:5001
- [ ] `uv sync` foi executado (flask-cors instalado)
- [ ] Arquivos MP3/WAV existem na pasta `audios/`
- [ ] Acessando via `http://localhost:5001/frontend` (não file:///)
- [ ] Console do navegador não mostra erros CORS
- [ ] Network tab mostra 200 OK para requisições de áudio
- [ ] Testou a página de diagnóstico (test-audio.html)

## Solução Alternativa

Se mesmo assim não funcionar, você pode servir os áudios de outra forma:

### Opção 1: Usar servidor HTTP simples separado

Em outro terminal, na pasta do projeto:
```bash
# Python 3
python -m http.server 8000

# Acesse:
http://localhost:8000/audios/pt-br-angry.mp3
```

### Opção 2: Modificar o script.js

Se os áudios funcionarem via servidor HTTP simples, modifique a URL base:
```javascript
// Em script.js, linha 2
const API_BASE_URL = 'http://localhost:8000';
```

## Logs Úteis

### Ver logs da API Flask
Os logs aparecem no terminal onde você executou `python main.py`

Procure por:
```
GET /audio/pt-br-angry.mp3 - 200 OK    ← Sucesso
GET /audio/pt-br-angry.mp3 - 404       ← Arquivo não encontrado
GET /audio/pt-br-angry.mp3 - 500       ← Erro no servidor
```

### Ver logs do navegador
1. F12 → Console
2. Procure por mensagens de erro
3. F12 → Network → Filtrar por "audio"
4. Clique em cada requisição para ver detalhes

## Ainda Não Funciona?

Se seguiu todos os passos e ainda não funciona, me envie:

1. **Saída do terminal** onde rodou `python main.py`
2. **Screenshot do Console** do navegador (F12)
3. **Screenshot da aba Network** mostrando as requisições
4. **Resultado de:**
```bash
curl http://localhost:5001/test-audio
```

---

**Dica:** A página `test-audio.html` é sua melhor amiga para diagnosticar o problema! 🔍
