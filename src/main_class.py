from datetime import datetime
import logging
import dotenv
from src.utils.renovacao import Renovacao

logging.basicConfig(
    level=logging.DEBUG,                  # Define o nível mínimo dos logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato da mensagem de log
    datefmt="%Y-%m-%d %H:%M:%S",         # Formato da data/hora
    filename="app.log",                   # Arquivo onde os logs serão salvos
    filemode="a"                          # Modo de abertura do arquivo (w = sobrescreve, a = anexa)
)

class MainClass:
    """
    Classe principal para gerenciar o processo de renovação de empréstimos de livros,
    utilizando a classe Renovacao para realizar as operações.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe MainClass e cria uma instância da classe Renovacao.
        """
        self.renovacao = Renovacao()

    def renovar_emprestimo(self):
        """
        Executa o processo completo de renovação de empréstimos de livros.

        Este método realiza o login no sistema, consulta a lista de livros emprestados
        em aberto e renova esses empréstimos. Os métodos utilizados para cada etapa
        pertencem à instância da classe Renovacao.
        """
        try:
            dotenv.load_dotenv()
            # Realiza login no sistema de biblioteca
            self.renovacao.login()
            # Consulta a lista de livros emprestados em aberto
            livros = self.renovacao.consultar_livros().json()
            if len(livros['Result']['Data']) > 0:
                logging.info("Há livros para serem renovados.")
                datas_convertidas = [
                datetime.strptime(livro['DataDevolucaoPrevista'], '%Y-%m-%dT%H:%M:%S')
                for livro in livros['Result']['Data']
                ]
                # Verificando se todas as datas de devolução são maiores ou iguais a data atual
                if any(data <= datetime.now() for data in datas_convertidas):
                    logging.info("A data atual é maior ou igual a todas as datas de devolução.")
                    # Renova o empréstimo dos livros consultados
                    self.renovacao.renovar(livros)
                else:
                    logging.info("A data atual não é maior ou igual a todas as datas de devolução."
                               "Não é necessário renovar.")
            else:
                logging.info("Não há livros para serem renovados.")
        except Exception as e:
            logging.error(f"Erro ao renovar empréstimo: {e}")
