
![Recriando o jogo da cobrinha com JavaScript](cartoon-ai-robot-character-scene.jpg)
# Automação de Renovação de Empréstimos - Biblioteca IFTM

Este projeto tem como objetivo automatizar o processo de login, consulta e renovação de empréstimos de livros na biblioteca do Instituto Federal do Triângulo Mineiro (IFTM), utilizando Python. A automação é feita por meio da API da biblioteca, permitindo realizar as operações sem a necessidade de interação manual.

## Funcionalidades

- **Login no Sistema:** Realiza o login na plataforma da biblioteca usando as credenciais armazenadas em variáveis de ambiente.
- **Consulta de Empréstimos:** Consulta a lista de livros atualmente emprestados pelo usuário.
- **Renovação de Empréstimos:** Renova os empréstimos de livros de acordo com os dados de empréstimos em aberto.

## Requisitos

Antes de rodar o projeto, é necessário instalar as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt

```
Além disso, o projeto utiliza o módulo python-dotenv para carregar variáveis de ambiente de um arquivo .env. Certifique-se de que este arquivo está presente na raiz do projeto, contendo suas credenciais de login.

## Estrutura do Projeto
A estrutura do projeto é a seguinte:

```bash
automacao-renovacao-livros/
    .venv/                   # Ambiente virtual do Python
    .env                     # Arquivo com as variáveis de ambiente (credenciais de login)
    src/                     # Código-fonte
        main_class.py        # Lógica de automação (login, consulta e renovação)
    requirements.txt         # Dependências do projeto
    main.py                  # Arquivo principal que executa o script
    executar_script.bat      # Script de inicialização para o Agendador de Tarefas
```
## Como Usar
1. Configuração das Credenciais
No arquivo .env, adicione as suas credenciais de login da biblioteca:
```bash
identificacao=SEU_LOGIN

psw=SUA_SENHA
```

2. Instalação das Dependências
Instale as dependências necessárias para rodar o projeto:

```bash
pip install -r requirements.txt
```
3. Rodando o Script Manualmente
Para rodar o script manualmente, execute o seguinte comando no terminal:

```bash
python main.py
```
4. __Automatizando a Execução com o Agendador de Tarefas__
Se você deseja automatizar a execução do script ao iniciar o sistema ou em horários específicos, use o Agendador de Tarefas do Windows.

Crie um arquivo __.bat__ (por exemplo, executar_script.bat) com o seguinte conteúdo:
```bash
@echo off
cd C:\Users\raque\OneDrive - IFTM\Documentos\Projetos\automacao-renovacao-livros
call .venv\Scripts\activate
python main.py
```
Este arquivo irá ativar o ambiente virtual e rodar o script Python. Configure o Agendador de Tarefas para rodar o arquivo .bat conforme desejado.

5. Visualizando os Logs
O script usa o módulo logging para registrar logs de execução, como sucessos e erros. Os logs podem ser visualizados no arquivo app de logs.

## Principais Componentes do Código
### Classe Renovacao: 
Implementa a lógica para realizar o login, consultar empréstimos em aberto e renovar livros. Está localizada em src/utils/renovacao.py.

Métodos principais:
- __login()__: Realiza o login utilizando credenciais armazenadas no .env.
- __consultar_livros()__: Obtém a lista de livros emprestados.
- __renovar(livros)__: Renova os empréstimos.
### Classe MainClass
Gerencia o processo completo de renovação de empréstimos, utilizando a classe Renovacao. Está localizada em src/main_class.py.

Métodos principais:
- __init()__: Inicializa a classe e cria uma instância de Renovacao.
- __renovar_emprestimo()__: Orquestra as operações de login, consulta e renovação, verificando a necessidade de renovação com base na data atual.
```python
class Renovacao:
    def __init__(self) -> None:
        load_dotenv()  # Carrega variáveis de ambiente
        self.url = 'https://biblioteca.iftm.edu.br'
        self.session = requests.Session()

    def login(self):
        url = self.url + "/Login/Login"
        payload = json.dumps({
            "identificacao": os.getenv('identificacao'),
            "senha": os.getenv('psw')
        })
        response = self.session.post(url, headers={'Content-Type': 'application/json'}, data=payload)
        return response

    def consultar_livros(self):
        url = self.url + "/emprestimo/ListarCirculacoesEmAberto"
        response = self.session.post(url, data={})
        return response

    def renovar(self, livros):
        url = self.url + "/emprestimo/ListarCirculacoesEmAberto"
        payload = livros['Result']
        response = self.session.post(url, data=payload)
        return response
```
## Requisitos de Sistema
- Python 3.x
- Windows (para uso do Agendador de Tarefas)
- Bibliotecas: requests, python-dotenv
- Licença: Este projeto está licenciado sob a MIT License.

Se você tiver alguma dúvida ou sugestão, sinta-se à vontade para contribuir com o projeto!


---

### **Explicações do README:**
- **Instalação e uso:** Como configurar e executar o script manualmente ou automatizá-lo com o Agendador de Tarefas.
- **Estrutura do projeto:** Descrição da estrutura de pastas e arquivos.
- **Funcionalidades:** Detalhamento das funcionalidades do script, como login, consulta e renovação.
- **Exemplo de código:** Apresentação da classe `Renovacao` e seus métodos para entender a lógica de automação.

Se precisar de ajustes ou detalhes adicionais, posso modificar o README! 😊





