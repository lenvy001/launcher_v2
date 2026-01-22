# Launcher V2

## O que é?

Um gerenciador de aplicativos. Basicamente, você cria uma lista de programas que quer abrir, e o Launcher V2 deixa você:

- Abrir programas de forma fácil
- Fechar programas que estão rodando
- Ver qual apps estão disponíveis
- Adicionar novos apps à lista

## O que ele faz?

Tem duas formas de usar:

1. **Interface Web** - você acessa pelo navegador
2. **Menu de comando** - você digita números para escolher

Dentro do arquivo `config.json` fica salva a lista de programas que você quer gerenciar.

## Como usar

### Para rodar a interface Web
```
cd src
python serve.py
```
Depois acesse: http://localhost:5000

**Na web você pode:**
- Ver todos os apps cadastrados
- Clicar em "Abrir" para rodar um app
- Clicar em "Fechar" para matar o app
- Clicar em "Adicionar App" para registrar novos programas

### Para rodar o menu de comando
```
cd src
python main.py
```
**No menu você digita:**
- 1 = Abrir um app
- 2 = Fechar um app
- 3 = Ver lista de apps
- 4 = Adicionar novo app
- 5 = Sair

## Como funciona (por trás)

1. **Config.json** - é um arquivo que guarda a lista de programas. Tem:
   - `id` - nome curto do app (ex: "brave", "spotify")
   - `nome` - nome legível (ex: "Navegador Brave")
   - `caminho` - onde o programa está instalado (ex: "C:\Program Files\...")
   - `processo` - nome do processo (ex: "brave.exe")

2. **Abrir** - o programa encontra o caminho no config.json e executa o arquivo

3. **Fechar** - o programa usa o nome do processo e mata ele (taskkill no Windows)

4. **Registrar novo** - você digita os dados e é salvo no config.json

## O que você precisa

- Python 3.7 ou mais novo
- Flask

Para instalar Flask:
```
pip install flask
```

## Pastas importantes

- `src/` - código Python
- `static/` - páginas Web (HTML, CSS, JS)
- `docs/` - documentação

## Observações

Esse é um projeto simples para aprender. Use apenas localmente.
