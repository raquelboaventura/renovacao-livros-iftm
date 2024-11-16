import json
import logging
import os
import requests

class Renovacao:
    """
    Classe para automatizar o processo de login, consulta e renovação de empréstimos
    de livros na biblioteca do IFTM.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe Renovacao.
        """
        self.url = 'https://biblioteca.iftm.edu.br'
        self.session = requests.Session()
        logging.info("Classe Renovacao inicializada com sucesso.")

    def login(self):
        """
        Realiza o login no sistema da biblioteca.

        Envia uma requisição POST para a URL de login, utilizando as credenciais
        (identificação e senha) que estão armazenadas nas variáveis de ambiente
        'identificacao' e 'psw'. Retorna a resposta da requisição.

        Returns:
            response (requests.Response): Resposta da requisição de login.
        """
        url = self.url + "/Login/Login"
        payload = json.dumps({
            "identificacao": os.getenv('identificacao'),
            "senha": os.getenv('psw')
        })
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            logging.info(f"Enviando requisição de login para {url}.")
            response = self.session.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Garante que exceções sejam levantadas para códigos de status >= 400

            logging.info("Login realizado com sucesso.")
            return response
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP no login: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Erro de requisição no login: {req_err}")
        except Exception as err:
            logging.error(f"Erro inesperado no login: {err}")

        return None

    def consultar_livros(self):
        """
        Consulta a lista de livros atualmente emprestados pelo usuário.

        Envia uma requisição POST para a URL que lista os empréstimos em aberto.
        Retorna a resposta da requisição com as informações dos livros.

        Returns:
            response (requests.Response): Resposta da requisição com dados dos livros emprestados.
        """
        url = self.url + "/emprestimo/ListarCirculacoesEmAberto"
        payload = {}
        headers = {}

        try:
            logging.info(f"Enviando requisição para consultar livros emprestados para {url}.")
            response = self.session.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Garante que exceções sejam levantadas para códigos de status >= 400

            logging.info("Consulta de livros realizada com sucesso.")
            return response
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP ao consultar livros: {http_err}")
            return None  # Retorna None caso haja erro
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Erro de requisição ao consultar livros: {req_err}")
            return None
        except Exception as err:
            logging.error(f"Erro inesperado ao consultar livros: {err}")
            return None

    def renovar(self, livros):
        """
        Renova o empréstimo dos livros especificados.

        Envia uma requisição POST para renovar os empréstimos de livros informados no
        parâmetro `livros`, utilizando a URL de renovação.

        Args:
            livros (dict): Dados dos livros que serão renovados, formatados para envio como payload.

        Returns:
            response (requests.Response): Resposta da requisição de renovação dos livros.
        """
        url = self.url + "emprestimo/ListarCirculacoesEmAberto"
        payload = livros['Result']
        headers = {}

        try:
            logging.info(f"Enviando requisição para renovar os empréstimos dos livros para {url}.")
            response = self.session.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Garante que exceções sejam levantadas para códigos de status >= 400

            logging.info("Renovação de empréstimos realizada com sucesso.")
            return response.text
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP ao renovar empréstimos: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Erro de requisição ao renovar empréstimos: {req_err}")
        except Exception as err:
            logging.error(f"Erro inesperado ao renovar empréstimos: {err}")

        return None