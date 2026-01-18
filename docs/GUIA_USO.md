# 🎓 Guia de Uso Rápido - Launcher V2

## 🚀 Inicializar

### Via Web (Recomendado)
```bash
cd c:\vs code\launcher_v2
python serve.py
# Acesse http://localhost:5000
```

### Via CLI (Terminal)
```bash
cd c:\vs code\launcher_v2
python main.py
```

---

## 📝 Exemplos de Uso

### Adicionar App (Web)
1. Clique em "➕ Adicionar App"
2. Preencha:
   - **ID:** `spotify` (sem espaços, números ok)
   - **Nome:** `Spotify`
   - **Caminho:** `C:\Users\00\AppData\Local\Spotify\Spotify.exe`
   - **Processo:** `spotify.exe`
3. Clique "Adicionar"

### Adicionar App (API)
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

### Listar Apps (API)
```bash
curl http://localhost:5000/api/apps
```

**Resposta:**
```json
{
    "success": true,
    "apps": [
        {
            "id": "spotify",
            "nome": "Spotify",
            "caminho": "C:\\...",
            "processo": "spotify.exe"
        }
    ],
    "count": 1
}
```

### Abrir App
```bash
curl -X POST http://localhost:5000/api/open/spotify
```

### Fechar App
```bash
curl -X POST http://localhost:5000/api/close/spotify
```

### Deletar App
```bash
curl -X DELETE http://localhost:5000/api/apps/spotify
```

---

## 📊 Log de Ações

Ver `log.txt`:
```
[2026-01-18 10:30:45] ABRIR - spotify - SUCESSO
[2026-01-18 10:35:12] FECHAR - discord - SUCESSO
```

---

## 🔒 Validações

❌ **IDs INVÁLIDOS:**
- `spotify; rm -r /` (injeção)
- `123456789-muito-longo-ultrapassa-50-caracteres`
- `spotify@discord` (caracteres especiais)

✅ **IDs VÁLIDOS:**
- `spotify`
- `discord_app`
- `app-123`
- `VS_Code`

---

## ⚠️ Solução de Problemas

### Apps não aparecem
- Verifique se `config.json` existe
- Verifique se tem permissão de leitura
- Recarregue a página

### Erro ao adicionar
- Verifique se ID já existe
- Verifique caminho do executável
- Verifique nome do processo (com .exe)

### App não abre
- Verifique caminho em config.json
- Verifique se arquivo existe
- Veja log.txt para erro específico

---

## 📁 Estrutura de Arquivos

```
launcher_v2/
├── config.json          # Apps cadastrados
├── log.txt             # Histórico de ações
├── app.py              # Funções principais
├── main.py             # Menu CLI
├── serve.py            # API Flask
├── FUNCOES.md          # Esta documentação
└── static/
    ├── index.html      # Interface web
    ├── css/style.css   # Estilos
    └── js/app.js       # Lógica frontend
```

---

## 🔌 Integração com Outros Programas

Como usar o Launcher em seus scripts:

```python
from app import abrir_app, fechar_app, load_config

# Abrir app
abrir_app("spotify")

# Listar todos
config = load_config()
for app in config['apps']:
    print(f"{app['nome']}: {app['caminho']}")

# Fechar app
fechar_app("discord")
```

---

## 📈 Visão Futura

Preparado para:
- [ ] Autenticação de usuários
- [ ] Permissões por usuário
- [ ] Agendamento de apps
- [ ] Notificações desktop
- [ ] Dashboard com gráficos
- [ ] Sincronização em nuvem
- [ ] Integração com Task Scheduler
- [ ] API REST completa

---

## 💡 Dicas

1. **IDs únicos:** Use nomes descritivos e únicos
2. **Caminho:** Copie do Gerenciador de Tarefas
3. **Processo:** Verifique em Gerenciador de Tarefas
4. **Backup:** Faça cópia de `config.json` regularmente
5. **Log:** Verifique `log.txt` para debug

---

## 📞 Suporte

Erros? Verifique:
1. `log.txt` para mensagem de erro
2. `config.json` para estrutura
3. Caminho do executável
4. Permissões do arquivo
