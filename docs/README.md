# 🚀 Launcher V2 - Gerenciador de Apps

Versão refatorada com segurança, interface funcional e escalabilidade.

## 📋 Estrutura

```
launcher_v2/
├── config.json          # Base de dados dos apps
├── log.txt             # Registro de ações
├── app.py              # Funções principais (SEGURAS)
├── main.py             # Menu CLI interativo
├── serve.py            # API Flask local
└── static/
    ├── index.html      # Interface web bonita
    ├── css/style.css   # Estilos responsivos
    └── js/app.js       # Lógica frontend com segurança
```

## 🔒 Segurança Implementada

✅ **Validação de Entrada**
- Whitelist de caracteres (alfanuméricos, underscore, hífen)
- Máximo 50 caracteres por ID

✅ **Proteção contra Injeção**
- Uso de `subprocess` ao invés de `os.system()`
- `shell=False` em todas as execuções

✅ **Sanitização**
- Escape HTML no JavaScript
- Validação de estrutura JSON

✅ **Logging**
- Registro de todas as ações em `log.txt`
- Timestamps e status das operações

✅ **Cache em Memória**
- Config carregado uma vez, reutilizado
- Reduz leitura de disco

## 🎯 Como Usar

### CLI (Terminal)
```bash
python main.py
```
Menu interativo para abrir/fechar apps

### Web (API Local)
```bash
python serve.py
# Acesse http://localhost:5000
```

## 📝 Arquivo config.json

```json
{
    "apps": [
        {
            "id": "brave",
            "nome": "Brave Browser",
            "caminho": "C:\\...",
            "processo": "brave.exe"
        }
    ]
}
```

## 📊 Log de Ações (log.txt)

```
[2026-01-18 10:30:45] ABRIR - brave - SUCESSO
[2026-01-18 10:35:12] FECHAR - discord - SUCESSO
[2026-01-18 10:36:00] ABRIR - vscode - CAMINHO_INVÁLIDO
```

## ✨ Características

- ✅ Apps definidos em JSON (fácil de modificar)
- ✅ Menu CLI interativo
- ✅ API REST local
- ✅ Interface web responsiva
- ✅ Validação e sanitização de entrada
- ✅ Proteção contra injeção de comando
- ✅ Sistema de logging completo
- ✅ Cache em memória
- ✅ Sem hardcoding de caminhos
- ✅ Debounce nos botões (evita cliques múltiplos)

## 🚀 Visão Futura

Preparado para:
- Adicionar autenticação (usuário/senha)
- Sistema de permissões por usuário
- Agendamento de apps
- Notificações
- API REST completa para terceiros
- Sincronização em nuvem
- Dashboard com gráficos
- Integração com Windows Task Scheduler

## 🛠️ Desenvolvido com

- Python 3.x
- Flask (Web)
- JSON (Armazenamento)
- JavaScript vanilla (Frontend)
