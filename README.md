# 🚀 Launcher V2 - App Manager

> Um gerenciador de aplicações local com interface Web e CLI

## 📁 Estrutura

```
launcher_v2/
├── src/                  # Código-fonte Python
│   ├── app.py           # Funções core
│   ├── main.py          # Menu CLI
│   ├── serve.py         # API Flask
│   └── config.json      # Configuração
├── static/              # Frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
├── docs/                # Documentação
│   ├── README.md
│   ├── FUNCOES.md
│   ├── GUIA_USO.md
│   ├── SEGURANCA.md
│   └── API.md
├── logs/                # Arquivos de log
│   └── log.txt
├── run.bat             # Script de execução
└── .gitignore
```

## 🚀 Início Rápido

### Windows
```bash
# Web Interface
cd src
python serve.py
# Acesse: http://localhost:5000

# CLI
cd src
python main.py
```

### macOS/Linux
```bash
# Web Interface
cd src
python3 serve.py

# CLI
cd src
python3 main.py
```

## 📚 Documentação

| Arquivo | Descrição |
|---------|-----------|
| [docs/FUNCOES.md](docs/FUNCOES.md) | Todas as funções explicadas |
| [docs/GUIA_USO.md](docs/GUIA_USO.md) | Como usar CLI e Web |
| [docs/SEGURANCA.md](docs/SEGURANCA.md) | Análise de segurança |
| [docs/API.md](docs/API.md) | Endpoints da API REST |

## ⚙️ Requisitos

- Python 3.7+
- Flask (para Web)

```bash
pip install flask
```

## 🎯 Features

- ✅ Interface Web responsiva
- ✅ CLI interativa
- ✅ API REST completa
- ✅ Validação de entrada
- ✅ Segurança contra injection
- ✅ Logging de ações
- ✅ Caching em memória

## 🔒 Segurança

⚠️ **Apenas para uso LOCAL**

- Sem autenticação
- Sem HTTPS
- Design apenas intra-rede

Veja [docs/SEGURANCA.md](docs/SEGURANCA.md) para detalhes.

## 📝 Licença

MIT

---

**Última atualização:** 18/01/2026
