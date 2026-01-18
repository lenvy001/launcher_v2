# 📚 Documentação Explícita de Funções - Launcher V2

## 🔧 app.py - Funções Principais

### 1. `log_acao(acao, app_id, status)`
**Propósito:** Registra todas as ações em arquivo de log

**Parâmetros:**
- `acao` (str): Tipo de ação (ex: "abrir", "fechar", "adicionar")
- `app_id` (str): ID do aplicativo afetado
- `status` (str): Status da ação (ex: "SUCESSO", "ERRO", "NÃO_ENCONTRADO")

**Retorno:** Nada

**Exemplo:**
```python
log_acao("abrir", "spotify", "SUCESSO")
# Resultado no log.txt: [2026-01-18 10:30:45] ABRIR - spotify - SUCESSO
```

**Uso Interno:** Chamada por todas as funções de controle

---

### 2. `validar_app_id(app_id)`
**Propósito:** Valida ID para prevenir injeção de comando

**Parâmetros:**
- `app_id` (str): ID a ser validado

**Retorno:** 
- `True` se válido (apenas alfanuméricos, -, _)
- `False` se inválido

**Exemplo:**
```python
validar_app_id("spotify")        # True
validar_app_id("spotify-123")    # True
validar_app_id("spotify;rm /")   # False (injeção!)
validar_app_id("app_id_muito_longo_com_muitos_caracteres_que_ultrapassa_50")  # False
```

**Segurança:** Whitelist de caracteres + limite de 50 caracteres

---

### 3. `load_config(force_reload=False)`
**Propósito:** Carrega configuração do JSON com cache em memória

**Parâmetros:**
- `force_reload` (bool): Se True, recarrega do disco mesmo com cache

**Retorno:** 
- `dict`: Configuração com chave "apps" (lista)
- `{"apps": []}` se erro

**Exemplo:**
```python
config = load_config()
print(config['apps'])  # [{"id": "spotify", "nome": "Spotify", ...}, ...]

# Forçar recarregar do disco
config = load_config(force_reload=True)
```

**Performance:** Cache reduz I/O de disco

---

### 4. `save_config(config)`
**Propósito:** Salva configuração no JSON e atualiza cache

**Parâmetros:**
- `config` (dict): Dicionário com chave "apps"

**Retorno:** Nada (exceção capturada internamente)

**Exemplo:**
```python
config = load_config()
config['apps'].append({
    "id": "new_app",
    "nome": "New App",
    "caminho": "C:\\...",
    "processo": "app.exe"
})
save_config(config)
```

---

### 5. `abrir_app(app_id)`
**Propósito:** Abre um aplicativo de forma segura

**Parâmetros:**
- `app_id` (str): ID do app no JSON

**Retorno:**
- `True` se sucesso
- `False` se erro

**Exemplo:**
```python
if abrir_app("spotify"):
    print("Spotify aberto com sucesso")
else:
    print("Erro ao abrir Spotify")
```

**Segurança:** 
- Valida ID
- Verifica se arquivo existe
- Usa subprocess com shell=False

---

### 6. `fechar_app(app_id)`
**Propósito:** Fecha um aplicativo usando taskkill

**Parâmetros:**
- `app_id` (str): ID do app no JSON

**Retorno:**
- `True` se sucesso
- `False` se erro

**Exemplo:**
```python
if fechar_app("spotify"):
    print("Spotify fechado")
else:
    print("Spotify não estava aberto")
```

**Método:** `taskkill /im process.exe /f`

---

### 7. `listar_apps()`
**Propósito:** Exibe lista formatada de apps

**Parâmetros:** Nenhum

**Retorno:** Nada (imprime no console)

**Exemplo:**
```python
listar_apps()
# Output:
# 📋 Apps disponíveis:
#   1. [spotify] Spotify
#   2. [discord] Discord
#   3. [vscode] Visual Studio Code
```

---

### 8. `get_app_por_numero(numero)`
**Propósito:** Retorna ID do app pelo número na lista

**Parâmetros:**
- `numero` (int): Posição na lista (1-indexado)

**Retorno:**
- `str`: ID do app
- `None` se índice inválido

**Exemplo:**
```python
listar_apps()  # Mostra 1. [spotify] ...
app_id = get_app_por_numero(1)  # "spotify"
```

---

### 9. `get_todos_apps()`
**Propósito:** Retorna lista de todos os apps

**Parâmetros:** Nenhum

**Retorno:** `list` de apps

**Exemplo:**
```python
apps = get_todos_apps()
for app in apps:
    print(f"{app['nome']}: {app['caminho']}")
```

---

## 🌐 serve.py - Rotas da API

### 1. `GET /api/apps`
**Propósito:** Retorna lista de todos os apps

**Resposta (200):**
```json
{
    "success": true,
    "apps": [
        {"id": "spotify", "nome": "Spotify", "caminho": "...", "processo": "spotify.exe"}
    ],
    "count": 1
}
```

**Uso:** Carrega apps na página web

---

### 2. `POST /api/apps`
**Propósito:** Adiciona novo app

**Body esperado:**
```json
{
    "id": "spotify",
    "nome": "Spotify",
    "caminho": "C:\\Program Files\\Spotify\\spotify.exe",
    "processo": "spotify.exe"
}
```

**Resposta (201 - Sucesso):**
```json
{
    "success": true,
    "message": "App 'Spotify' adicionado",
    "app": {...}
}
```

**Resposta (400 - Erro):**
```json
{
    "success": false,
    "message": "App com id 'spotify' já existe"
}
```

**Validações:**
- Todos os campos obrigatórios
- ID válido (sem injeção)
- ID único (não duplicado)

---

### 3. `POST /api/open/<app_id>`
**Propósito:** Abre um app

**Parâmetro:** `app_id` na URL (ex: `/api/open/spotify`)

**Resposta (200):**
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

---

### 4. `POST /api/close/<app_id>`
**Propósito:** Fecha um app

**Parâmetro:** `app_id` na URL

**Resposta:** Similar ao open

---

### 5. `DELETE /api/apps/<app_id>`
**Propósito:** Remove um app da configuração

**Parâmetro:** `app_id` na URL

**Resposta (200):**
```json
{
    "success": true,
    "message": "App 'Spotify' removido"
}
```

**Resposta (404):**
```json
{
    "success": false,
    "message": "App 'spotify' não encontrado"
}
```

---

## 💻 main.py - Menu CLI

### 1. `exibir_menu_principal()`
**Propósito:** Mostra menu de opções

**Saída:**
```
==================================================
     🚀 LAUNCHER V2 - GERENCIADOR DE APPS
==================================================
  1. 🚀 Abrir app
  2. 🛑 Fechar app
  3. 📋 Listar apps
  4. ❌ Sair
==================================================
```

---

### 2. `menu_abrir()`
**Propósito:** Interface para abrir um app

**Fluxo:**
1. Lista apps
2. Pede número
3. Chama `abrir_app()`

---

### 3. `menu_fechar()`
**Propósito:** Interface para fechar um app

**Fluxo:**
1. Lista apps
2. Pede número
3. Chama `fechar_app()`

---

### 4. `main()`
**Propósito:** Loop principal do programa

**Fluxo:**
```
while True:
    - Mostra menu
    - Lê input (1-4)
    - Executa ação correspondente
    - Se 4: sai
```

---

## 🌐 Frontend (JavaScript)

### 1. `carregarApps()`
**Propósito:** Busca apps da API

**Ação:** Faz GET `/api/apps` e renderiza

---

### 2. `abrirModalAdicionar()`
**Propósito:** Abre form para adicionar app

---

### 3. `enviarFormulario(event)`
**Propósito:** Valida e envia novo app

**Validação:**
- Todos campos preenchidos
- ID em minúsculas
- POST para `/api/apps`

---

### 4. `abrirApp(appId)`
**Propósito:** POST `/api/open/<id>`

**Debounce:** Previne múltiplos cliques

---

### 5. `fecharApp(appId)`
**Propósito:** POST `/api/close/<id>`

**Debounce:** 2 segundos entre cliques

---

### 6. `deletarApp(appId, appNome)`
**Propósito:** DELETE `/api/apps/<id>`

**Confirmação:** Pede confirmação antes

---

## 📁 Estrutura do config.json

```json
{
    "apps": [
        {
            "id": "spotify",
            "nome": "Spotify",
            "caminho": "C:\\Program Files\\Spotify\\spotify.exe",
            "processo": "spotify.exe"
        }
    ]
}
```

**Campos:**
- `id`: Identificador único (alfanumérico, -, _)
- `nome`: Nome exibido
- `caminho`: Caminho do executável
- `processo`: Nome do processo para fechar

---

## 📊 Arquivo log.txt

```
[2026-01-18 10:30:45] ABRIR - spotify - SUCESSO
[2026-01-18 10:35:12] FECHAR - discord - SUCESSO
[2026-01-18 10:36:00] ABRIR - vscode - CAMINHO_INVÁLIDO
[2026-01-18 10:37:15] ADICIONAR - telegram - SUCESSO
[2026-01-18 10:38:20] DELETAR - vscode - SUCESSO
```

**Campos:**
- Timestamp
- Tipo de ação (maiúscula)
- App ID
- Status

---

## 🔒 Segurança Implementada

| Função | Segurança |
|--------|-----------|
| `validar_app_id()` | Whitelist + limite 50 chars |
| `abrir_app()` | subprocess shell=False |
| `fechar_app()` | subprocess shell=False |
| `load_config()` | Try-except JSON |
| Frontend | Escape HTML + debounce |

---

## 🚀 Fluxo Completo de Uso

### Adicionar App (Web)
1. Clica "➕ Adicionar App"
2. Preenche form
3. POST `/api/apps`
4. app.py: Valida → Salva JSON
5. Sucesso → Recarrega apps

### Abrir App
1. Clica "▶️ Abrir" no card
2. POST `/api/open/spotify`
3. app.py: Valida ID → Encontra app → subprocess.Popen()
4. Registra em log.txt
5. Feedback ao usuário

### Fechar App
1. Clica "⏹️ Fechar"
2. POST `/api/close/spotify`
3. app.py: taskkill
4. Registra em log.txt

### Deletar App
1. Clica "✕" no card
2. Confirmação
3. DELETE `/api/apps/spotify`
4. Config atualizado
5. Recarrega lista

---

## 📞 Suporte

Todas as funções têm:
✅ Docstring explicativa
✅ Tratamento de erro
✅ Logging de ações
✅ Validação de entrada
✅ Exemplos de uso
