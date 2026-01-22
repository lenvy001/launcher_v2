"""
Web App Launcher (Python)
Gerenciador de Aplicativos - Local com segurança contra injeção de comando
"""

import json
import os
import subprocess
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "src", "config.json")
LOG_PATH = os.path.join(BASE_DIR, "logs", "log.txt")

# Cache em memória
_config_cache = None
_cache_timestamp = None


def log_acao(acao, app_id, status):
    """Registra ações em log"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem = f"[{timestamp}] {acao.upper()} - {app_id} - {status}\n"
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(mensagem)
    except Exception as e:
        print(f"⚠️  Erro ao registrar log: {e}")


def validar_app_id(app_id):
    """Valida ID contra injeção de comando - apenas alfanuméricos e underscore"""
    if not re.match(r'^[a-zA-Z0-9_-]+$', app_id):
        return False
    if len(app_id) > 50:
        return False
    return True


def load_config(force_reload=False):
    """Carrega config com cache em memória"""
    global _config_cache, _cache_timestamp
    
    if _config_cache and not force_reload:
        return _config_cache
    
    try:
        if not os.path.exists(CONFIG_PATH):
            print(f"❌ Arquivo não encontrado: {CONFIG_PATH}")
            return {"apps": []}
        
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        if "apps" not in config:
            config["apps"] = []
        
        _config_cache = config
        _cache_timestamp = datetime.now()
        return config
    except json.JSONDecodeError:
        print(f"❌ JSON inválido: {CONFIG_PATH}")
        return {"apps": []}
    except Exception as e:
        print(f"❌ Erro ao carregar config: {e}")
        return {"apps": []}


def save_config(config):
    """Salva config e atualiza cache"""
    global _config_cache
    
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        _config_cache = config
    except Exception as e:
        print(f"❌ Erro ao salvar config: {e}")


# ============================================
# FUNÇÕES DE CONTROLE DE APPS - SEGURAS
# ============================================

def abrir_app(app_id):
    """Abre app com validação de segurança"""
    if not validar_app_id(app_id):
        print(f"❌ ID inválido: {app_id}")
        log_acao("abrir", app_id, "ID_INVÁLIDO")
        return False
    
    config = load_config()
    app = next((a for a in config['apps'] if a['id'] == app_id), None)
    
    if not app:
        print(f"❌ App com id '{app_id}' não encontrado")
        log_acao("abrir", app_id, "NÃO_ENCONTRADO")
        return False
    
    try:
        caminho = app['caminho']
        if not os.path.exists(caminho):
            print(f"❌ Caminho não encontrado: {caminho}")
            log_acao("abrir", app_id, "CAMINHO_INVÁLIDO")
            return False
        
        subprocess.Popen(caminho, shell=False)
        print(f"✅ Abrindo {app['nome']}...")
        log_acao("abrir", app_id, "SUCESSO")
        return True
    except Exception as e:
        print(f"❌ Erro ao abrir app: {e}")
        log_acao("abrir", app_id, f"ERRO: {str(e)}")
        return False


def fechar_app(app_id):
    """Fecha app com validação de segurança"""
    if not validar_app_id(app_id):
        print(f"❌ ID inválido: {app_id}")
        log_acao("fechar", app_id, "ID_INVÁLIDO")
        return False
    
    config = load_config()
    app = next((a for a in config['apps'] if a['id'] == app_id), None)
    
    if not app:
        print(f"❌ App com id '{app_id}' não encontrado")
        log_acao("fechar", app_id, "NÃO_ENCONTRADO")
        return False
    
    try:
        processo = app['processo']
        
        if not validar_app_id(processo.replace('.exe', '')):
            print(f"❌ Processo inválido: {processo}")
            log_acao("fechar", app_id, "PROCESSO_INVÁLIDO")
            return False
        
        subprocess.run(
            ["taskkill", "/im", processo, "/f"],
            capture_output=True,
            timeout=5,
            shell=False
        )
        print(f"✅ Fechando {app['nome']}...")
        log_acao("fechar", app_id, "SUCESSO")
        return True
    except subprocess.TimeoutExpired:
        print(f"⚠️  Timeout ao fechar app")
        log_acao("fechar", app_id, "TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ Erro ao fechar app: {e}")
        log_acao("fechar", app_id, f"ERRO: {str(e)}")
        return False


def listar_apps():
    """Lista todos os apps"""
    config = load_config()
    
    if not config['apps']:
        print("❌ Nenhum app cadastrado")
        return
    
    print("\n📋 Apps disponíveis:")
    for i, app in enumerate(config['apps'], 1):
        print(f"  {i}. [{app['id']}] {app['nome']}")


def get_app_por_numero(numero):
    """Retorna ID do app pelo número"""
    config = load_config()
    try:
        app = config['apps'][numero - 1]
        return app['id']
    except IndexError:
        return None


def get_todos_apps():
    """Retorna lista de todos os apps"""
    config = load_config()
    return config.get('apps', [])


# ============================================
# BUSCA AUTOMATICA DE CAMINHO
# ============================================

def buscar_app_automatico(app_name):
    """
    Busca automaticamente o caminho de um aplicativo em locais comuns do Windows.
    """
    if not app_name:
        return None

    locais_busca = [
        Path(os.environ.get('ProgramFiles', 'C:\\Program Files')),
        Path(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')),
        Path(os.path.expanduser('~\\AppData\\Local')),
        Path(os.path.expanduser('~\\AppData\\Roaming')),
        Path(os.path.expanduser('~\\Desktop')),
        Path(os.path.expanduser('~\\Downloads')),
    ]

    nome = app_name.lower()

    for local in locais_busca:
        if not local.exists():
            continue
        try:
            for exe_file in local.rglob(f"{nome}*.exe"):
                if exe_file.is_file():
                    return str(exe_file)
        except PermissionError:
            continue

    return None


def obter_caminho_auto(app_id, nome):
    """Tenta obter caminho automatico usando nome e/ou id."""
    caminho = buscar_app_automatico(nome)
    if caminho:
        return caminho
    return buscar_app_automatico(app_id)


def adicionar_app(app_id, nome, caminho=None, processo=None):
    """
    Adiciona app com busca automatica de caminho quando necessario.

    Returns:
        (bool, str, dict|None): sucesso, mensagem, app
    """
    if not validar_app_id(app_id):
        return False, "ID invalido (apenas letras, numeros, -, _)", None

    config = load_config(force_reload=True)
    if any(a['id'] == app_id for a in config.get('apps', [])):
        return False, f"App com id '{app_id}' ja existe", None

    if not caminho:
        caminho = obter_caminho_auto(app_id, nome)
        if not caminho:
            return False, "Nao foi possivel encontrar o caminho automaticamente", None

    if not os.path.exists(caminho):
        return False, f"Caminho nao existe: {caminho}", None

    if not processo:
        processo = os.path.basename(caminho)

    novo_app = {
        "id": app_id,
        "nome": nome,
        "caminho": caminho,
        "processo": processo
    }

    config.setdefault("apps", []).append(novo_app)
    save_config(config)
    log_acao("adicionar", app_id, "SUCESSO")
    return True, f"App '{nome}' adicionado", novo_app
