import logging
from src.main_class import MainClass

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main():
    main = MainClass()
    main.renovar_emprestimo()
    
if __name__ == '__main__':
    main()