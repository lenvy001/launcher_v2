"""
API Flask - Serve os apps via HTTP
Local com segurança, sem rede
"""

from flask import Flask, send_from_directory, jsonify, request
import os
import sys
from app import load_config, save_config, abrir_app, fechar_app, validar_app_id, get_todos_apps, log_acao, adicionar_app

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")

# ============================================
# ROTAS PARA SERVIR ARQUIVOS ESTÁTICOS
# ============================================

@app.route("/")
def home():
    """Retorna a página principal"""
    return send_from_directory(STATIC_DIR, "index.html")


# ============================================
# ROTAS PARA CONTROLAR APPS
# ============================================

@app.route("/api/apps", methods=["GET"])
def get_apps():
    """Retorna lista de todos os apps"""
    try:
        apps = get_todos_apps()
        return jsonify({
            "success": True,
            "apps": apps,
            "count": len(apps)
        })
    except Exception as e:
        log_acao("api_get", "error", str(e))
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/api/apps", methods=["POST"])
def add_app():
    """
    Adiciona um novo app
    
    JSON esperado:
    {
        "id": "spotify",
        "nome": "Spotify",
        "caminho": "C:\...",
        "processo": "spotify.exe"
    }
    """
    try:
        data = request.get_json(silent=True) or {}

        app_id = (data.get("id") or "").strip().lower()
        nome = (data.get("nome") or "").strip()
        caminho = (data.get("caminho") or "").strip() or None
        processo = (data.get("processo") or "").strip() or None

        if not app_id or not nome:
            return jsonify({
                "success": False,
                "message": "Campos obrigatorios: id, nome"
            }), 400

        if not validar_app_id(app_id):
            return jsonify({
                "success": False,
                "message": "ID invalido (apenas letras, numeros, -, _)"
            }), 400

        ok, mensagem, novo_app = adicionar_app(app_id, nome, caminho, processo)
        if not ok:
            return jsonify({
                "success": False,
                "message": mensagem
            }), 400

        return jsonify({
            "success": True,
            "message": mensagem,
            "app": novo_app
        }), 201
    except Exception as e:
        log_acao("adicionar", "error", str(e))
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/api/apps/<app_id>", methods=["DELETE"])
def delete_app(app_id):
    """Remove um app"""
    try:
        if not validar_app_id(app_id):
            return jsonify({
                "success": False,
                "message": "ID inválido"
            }), 400
        
        config = load_config()
        app = next((a for a in config['apps'] if a['id'] == app_id), None)
        
        if not app:
            return jsonify({
                "success": False,
                "message": f"App '{app_id}' não encontrado"
            }), 404
        
        config['apps'] = [a for a in config['apps'] if a['id'] != app_id]
        save_config(config)
        log_acao("deletar", app_id, "SUCESSO")
        
        return jsonify({
            "success": True,
            "message": f"App '{app['nome']}' removido"
        })
    except Exception as e:
        log_acao("deletar", app_id, str(e))
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/api/open/<app_id>", methods=["POST"])
def open_app(app_id):
    """Abre um app pelo ID"""
    try:
        if abrir_app(app_id):
            return jsonify({
                "success": True,
                "message": f"App {app_id} aberto"
            })
        else:
            return jsonify({
                "success": False,
                "message": f"Erro ao abrir {app_id}"
            }), 400
    except Exception as e:
        log_acao("abrir", app_id, str(e))
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/api/close/<app_id>", methods=["POST"])
def close_app(app_id):
    """Fecha um app pelo ID"""
    try:
        if fechar_app(app_id):
            return jsonify({
                "success": True,
                "message": f"App {app_id} fechado"
            })
        else:
            return jsonify({
                "success": False,
                "message": f"Erro ao fechar {app_id}"
            }), 400
    except Exception as e:
        log_acao("fechar", app_id, str(e))
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ============================================
# ERROR HANDLER
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Página não encontrada"""
    return jsonify({
        "success": False,
        "message": "Rota não encontrada"
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Erro no servidor"""
    return jsonify({
        "success": False,
        "message": "Erro no servidor"
    }), 500


# ============================================
# INICIALIZAÇÃO
# ============================================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
