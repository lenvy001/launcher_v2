"""
Menu Principal - Interface de linha de comando
Controla apps via JSON de forma interativa
"""

from app import abrir_app, fechar_app, listar_apps, get_app_por_numero, adicionar_app


def exibir_menu_principal():
    """Exibe o menu principal"""
    print("\n" + "="*50)
    print("     WEB APP LAUNCHER - GERENCIADOR DE APPS")
    print("="*50)
    print("  1. Abrir app")
    print("  2. Fechar app")
    print("  3. Listar apps")
    print("  4. Adicionar app")
    print("  5. Sair")
    print("="*50)


def menu_abrir():
    """Menu para abrir um app"""
    print("
=== ABRIR APP ===")
    listar_apps()

    try:
        numero = int(input("
  Escolha o numero do app (ou 0 para voltar): "))
        if numero == 0:
            return

        app_id = get_app_por_numero(numero)
        if app_id:
            abrir_app(app_id)
        else:
            print("  Opcao invalida!")
    except ValueError:
        print("  Digite um numero valido!")


def menu_fechar():
    """Menu para fechar um app"""
    print("
=== FECHAR APP ===")
    listar_apps()

    try:
        numero = int(input("
  Escolha o numero do app (ou 0 para voltar): "))
        if numero == 0:
            return

        app_id = get_app_por_numero(numero)
        if app_id:
            fechar_app(app_id)
        else:
            print("  Opcao invalida!")
    except ValueError:
        print("  Digite um numero valido!")


def menu_adicionar():
    """Menu para adicionar um app"""
    print("
=== ADICIONAR APP ===")
    app_id = input("  ID do app (ex: spotify): ").strip().lower()
    nome = input("  Nome do app (ex: Spotify): ").strip()

    if not app_id or not nome:
        print("  ID e Nome sao obrigatorios!")
        return

    ok, mensagem, _ = adicionar_app(app_id, nome)
    if ok:
        print(f"  {mensagem}")
    else:
        print(f"  Erro: {mensagem}")


def main():
    """Loop principal do programa"""
    while True:
        exibir_menu_principal()
        opcao = input("
  Escolha uma opcao (1-5): ").strip()

        if opcao == '1':
            menu_abrir()
        elif opcao == '2':
            menu_fechar()
        elif opcao == '3':
            listar_apps()
        elif opcao == '4':
            menu_adicionar()
        elif opcao == '5':
            print("
  Ate logo!")
            break
        else:
            print("  Opcao invalida! Tente novamente.")

        input("
  Pressione ENTER para continuar...")


if __name__ == "__main__":
    main()
