import unittest 
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

import requests
from src.utils.renovacao import Renovacao
from src.main_class import MainClass


class TestRenovacao(unittest.TestCase):

    def setUp(self):
        """
        Configura os objetos necessários para os testes.
        """
        self.renovacao = Renovacao()
        self.main_class = MainClass()
        
    @patch('src.utils.renovacao.requests.Session.post')
    def test_login_sucesso(self, mock_post):
        """
        Testa o login com sucesso.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"resultado": True, "temAviso": False}
        mock_post.return_value = mock_response
        
        response = self.renovacao.login()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['resultado'])
        
    @patch('src.utils.renovacao.requests.Session.post')
    def test_login_erro(self, mock_post):
        """
        Testa o login com erro (credenciais inválidas ou problema no servidor).
        """
        # Configuração do mock para simular erro no login
        mock_post.side_effect = Exception("Erro de login")

        response = self.renovacao.login()
        
        self.assertIsNone(response)  # Login deve retornar None em caso de erro
    
    @patch('src.utils.renovacao.requests.Session.post')
    def test_consultar_livros(self, mock_post):
        """
        Testa a consulta de livros emprestados com sucesso.
        """
        # Configuração do mock para simular resposta de consulta
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
    "Result": {
        "Data": [
            {
                "Codigo": 349533,
                "CodigoRegistro": 835,
                "Titulo": "Introdução ao teste de software",
                "NumeroChamada": "",
                "CodigoBarras": 2517,
                "CodigoExemplar": 2517,
                "Tombo": "05204649",
                "Biblioteca": "Biblioteca Udi Centro",
                "DataEmprestimo": "2024-11-12T00:00:00",
                "DataDevolucaoPrevista": "2024-11-19T00:00:00",
                "DataDevolucao": None,
                "TipoEmprestimoCategoria": 3
            },
            {
                "Codigo": 349534,
                "CodigoRegistro": 20424,
                "Titulo": "Programação em Python 3 : uma introdução completa à linguagem Python",
                "NumeroChamada": "005.132 S955p",
                "CodigoBarras": 53265,
                "CodigoExemplar": 53265,
                "Tombo": "05207450",
                "Biblioteca": "Biblioteca Udi Centro",
                "DataEmprestimo": "2024-11-12T00:00:00",
                "DataDevolucaoPrevista": "2024-11-19T00:00:00",
                "DataDevolucao": None,
                "TipoEmprestimoCategoria": 3
            },
            {
                "Codigo": 349537,
                "CodigoRegistro": 827,
                "Titulo": "Estruturas de dados usando C",
                "NumeroChamada": "005.134 T292e",
                "CodigoBarras": 2455,
                "CodigoExemplar": 2455,
                "Tombo": "05200353",
                "Biblioteca": "Biblioteca Udi Centro",
                "DataEmprestimo": "2024-11-13T00:00:00",
                "DataDevolucaoPrevista": "2024-11-21T00:00:00",
                "DataDevolucao": None,
                "TipoEmprestimoCategoria": 3
            }
        ],
        "Total": 3,
        "AggregateResults": None,
        "Errors": None
    },
    "Page": None,
    "Index": None
}
        mock_post.return_value = mock_response

        response = self.renovacao.consultar_livros()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Result", response.json())
        
    @patch('src.utils.renovacao.requests.Session.post')
    def test_consulta_livros_sem_resultados(self, mock_post):
        """
        Testa o comportamento do sistema quando a API retorna uma lista vazia de livros.

        Cenário:
        - A resposta da API não contém nenhum livro emprestado.

        Verificação:
        - O sistema deve logar que não há livros para renovar.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Result": {
                "Data": [],
                "Total": 0
            }
        }
        mock_post.return_value = mock_response

        main_class = MainClass()
        with self.assertLogs(level='INFO') as log:
            main_class.renovar_emprestimo()
            self.assertIn("Não há livros para serem renovados.", log.output)

    @patch('src.utils.renovacao.requests.Session.post')
    def test_consulta_livros_com_erro(self, mock_post):
        """
        Testa o comportamento do sistema quando a API retorna um erro de autorização.

        Cenário:
        - A API retorna uma mensagem de erro indicando que o usuário não está autorizado.

        Verificação:
        - O sistema deve capturar o erro, logar a mensagem de erro e interromper o processo de renovação.
        """
        # Simula uma resposta de erro de autenticação
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized")
        mock_post.return_value = mock_response

        main_class = MainClass()
        with self.assertLogs(level='ERROR') as log:
            main_class.renovar_emprestimo()  # Isso irá chamar o método consultar_livros e pegar o erro
            self.assertIn("Erro HTTP ao consultar livros", log.output)
            self.assertIn("401 Unauthorized", log.output)  # Verifica se o erro de autorização foi logado

    @patch('src.utils.renovacao.requests.Session.post')
    def test_renovar_emprestimo(self, mock_post):
        """
        Testa o processo de renovação de empréstimos.
        """
        # Configuração do mock para simular resposta de renovação
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        livros_mock = {
            "Result": {
                "Data": [
                    {"DataDevolucaoPrevista": "2024-11-15T23:59:59"}
                ]
            }
        }

        response = self.renovacao.renovar(livros_mock)

        self.assertEqual(response, mock_response.text)
    
    @patch('src.main_class.Renovacao.consultar_livros')
    @patch('src.main_class.Renovacao.login')
    @patch('src.main_class.Renovacao.renovar')
    def test_main_class_renovar_emprestimo(self, mock_renovar, mock_login, mock_consultar_livros):
        """
        Testa o método renovar_emprestimo da MainClass.
        """
        # Mock para o login
        mock_login.return_value = None

        # Mock para consultar livros
        livros_mock = {
            "Result": {
                "Data": [
                    {"DataDevolucaoPrevista": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')}
                ]
            }
        }
        mock_response = MagicMock()
        mock_response.json.return_value = livros_mock
        mock_consultar_livros.return_value = mock_response

        # Mock para renovar
        mock_renovar.return_value = "Renovação realizada com sucesso."

        # Executa o método
        self.main_class.renovar_emprestimo()

        # Asserções
        mock_login.assert_called_once()
        mock_consultar_livros.assert_called_once()
        mock_renovar.assert_called_once_with(livros_mock)

if __name__ == "__main__":
    unittest.main()