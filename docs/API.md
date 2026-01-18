# 🎯 API REST Completa - Launcher V2

## Base URL
```
http://localhost:5000
```

---

## 📌 Endpoints

### 1️⃣ GET /api/apps
**Obter todos os apps**

**Método:** GET
**Autenticação:** Nenhuma
**Body:** Vazio

**Resposta (200):**
```json
{
    "success": true,
    "apps": [
        {
            "id": "spotify",
            "nome": "Spotify",
            "caminho": "C:\\Users\\00\\AppData\\Local\\Spotify\\Spotify.exe",
            "processo": "spotify.exe"
        },
        {
            "id": "discord",
            "nome": "Discord",
            "caminho": "C:\\Users\\00\\AppData\\Local\\Discord\\Update.exe",
            "processo": "Discord.exe"
        }
    ],
    "count": 2
}
```

**Exemplo cURL:**
```bash
curl http://localhost:5000/api/apps
```

---

### 2️⃣ POST /api/apps
**Adicionar novo app**

**Método:** POST
**Content-Type:** application/json

**Body:**
```json
{
    "id": "spotify",
    "nome": "Spotify",
    "caminho": "C:\\Users\\00\\AppData\\Local\\Spotify\\Spotify.exe",
    "processo": "spotify.exe"
}
```

**Resposta (201 - Criado):**
```json
{
    "success": true,
    "message": "App 'Spotify' adicionado",
    "app": {
        "id": "spotify",
        "nome": "Spotify",
        "caminho": "C:\\Users\\00\\AppData\\Local\\Spotify\\Spotify.exe",
        "processo": "spotify.exe"
    }
}
```

**Resposta (400 - Erro de Validação):**
```json
{
    "success": false,
    "message": "ID inválido (apenas letras, números, -, _)"
}
```

**Validações:**
- `id`: Obrigatório, único, apenas [a-zA-Z0-9_-], máx 50 chars
- `nome`: Obrigatório, string
- `caminho`: Obrigatório, arquivo deve existir
- `processo`: Obrigatório, string (com .exe)

**Exemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/apps \
  -H "Content-Type: application/json" \
  -d '{
    "id": "spotify",
    "nome": "Spotify",
    "caminho": "C:\\Users\\00\\AppData\\Local\\Spotify\\Spotify.exe",
    "processo": "spotify.exe"
  }'
```

---

### 3️⃣ POST /api/open/<app_id>
**Abrir um app**

**Método:** POST
**Parâmetro:** `app_id` - ID do app

**Resposta (200 - Sucesso):**
```json
{
    "success": true,
    "message": "App spotify aberto"
}
```

**Resposta (400 - Erro):**
```json
{
    "success": false,
    "message": "Erro ao abrir spotify"
}
```

**Possíveis Erros:**
- ID inválido
- App não encontrado
- Caminho não existe
- Permissão negada

**Exemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/open/spotify
```

**Exemplo JavaScript:**
```javascript
fetch('/api/open/spotify', {method: 'POST'})
  .then(r => r.json())
  .then(data => console.log(data))
```

---

### 4️⃣ POST /api/close/<app_id>
**Fechar um app**

**Método:** POST
**Parâmetro:** `app_id` - ID do app

**Resposta (200 - Sucesso):**
```json
{
    "success": true,
    "message": "App spotify fechado"
}
```

**Resposta (400 - Erro):**
```json
{
    "success": false,
    "message": "Erro ao fechar spotify"
}
```

**Nota:** Se o app não está aberto, pode retornar erro

**Exemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/close/spotify
```

---

### 5️⃣ DELETE /api/apps/<app_id>
**Remover um app**

**Método:** DELETE
**Parâmetro:** `app_id` - ID do app

**Resposta (200 - Sucesso):**
```json
{
    "success": true,
    "message": "App 'Spotify' removido"
}
```

**Resposta (404 - Não Encontrado):**
```json
{
    "success": false,
    "message": "App 'spotify' não encontrado"
}
```

**Exemplo cURL:**
```bash
curl -X DELETE http://localhost:5000/api/apps/spotify
```

---

## 📊 Códigos de Status HTTP

| Código | Significado | Exemplo |
|--------|-------------|---------|
| **200** | OK | App aberto com sucesso |
| **201** | Criado | App adicionado |
| **400** | Erro no Cliente | ID inválido, campos faltando |
| **404** | Não Encontrado | App não existe |
| **500** | Erro no Servidor | Erro interno |

---

## 🔄 Fluxo de Integração

### 1. Obter lista de apps
```bash
GET /api/apps
```

### 2. Adicionar novo app
```bash
POST /api/apps
```

### 3. Abrir app
```bash
POST /api/open/spotify
```

### 4. Fechar app
```bash
POST /api/close/spotify
```

### 5. Remover app
```bash
DELETE /api/apps/spotify
```

---

## 💻 Exemplos de Uso

### Python
```python
import requests

base_url = "http://localhost:5000"

# Listar
resp = requests.get(f"{base_url}/api/apps")
print(resp.json())

# Adicionar
data = {
    "id": "spotify",
    "nome": "Spotify",
    "caminho": "C:\\...",
    "processo": "spotify.exe"
}
resp = requests.post(f"{base_url}/api/apps", json=data)
print(resp.json())

# Abrir
resp = requests.post(f"{base_url}/api/open/spotify")
print(resp.json())
```

### JavaScript/Node.js
```javascript
const base_url = "http://localhost:5000";

// Listar
fetch(`${base_url}/api/apps`)
  .then(r => r.json())
  .then(d => console.log(d));

// Adicionar
fetch(`${base_url}/api/apps`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    id: "spotify",
    nome: "Spotify",
    caminho: "C:\\...",
    processo: "spotify.exe"
  })
})
.then(r => r.json())
.then(d => console.log(d));
```

### PowerShell
```powershell
$uri = "http://localhost:5000/api/apps"

# Listar
Invoke-RestMethod -Uri $uri -Method Get

# Adicionar
$body = @{
    id = "spotify"
    nome = "Spotify"
    caminho = "C:\..."
    processo = "spotify.exe"
} | ConvertTo-Json

Invoke-RestMethod -Uri $uri -Method Post -Body $body -ContentType "application/json"

# Abrir
Invoke-RestMethod -Uri "$uri/../open/spotify" -Method Post
```

---

## ⚠️ Tratamento de Erro

**Sempre verificar `success`:**

```javascript
fetch('/api/apps')
  .then(r => r.json())
  .then(data => {
    if (data.success) {
      console.log("Apps:", data.apps);
    } else {
      console.error("Erro:", data.message);
    }
  })
```

---

## 🔒 Limitações de Segurança

⚠️ **Este API é para uso LOCAL apenas**

- Sem autenticação
- Sem HTTPS
- Sem rate limiting
- Sem CORS bloqueado

**Para produção, adicione:**
- [ ] JWT authentication
- [ ] HTTPS/TLS
- [ ] Rate limiting
- [ ] CORS headers
- [ ] Request signing

---

## 📈 Roadmap da API

- [ ] Versioning (v1, v2)
- [ ] Autenticação Bearer Token
- [ ] Paginação para apps
- [ ] Filtros de busca
- [ ] Agendamento de apps
- [ ] Webhooks de eventos
- [ ] Batch operations
- [ ] Health check endpoint
