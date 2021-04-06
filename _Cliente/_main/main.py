######      Gui Reis     -      guisreis25@gmail.com      -   31920918   ######
######    Gian Gamberi   -   giangamberi@hotmail.com.br   -   31944043   ######

# -*- coding: utf-8 -*-

#### Bibliotecas necessárias
### Arquivos globais ###
from sys import argv
from sys import exit as sair                    # Fechar a aplicação
from PyQt5.QtWidgets import QApplication        # Interface Gráfica

### Arquivo local ###
from login import Login                         # Ações de login

def main() -> None:
    """Função de inicialização."""
    app = QApplication(argv)
    win = Login()

    win.show()
    sair(app.exec_())

## Chamada da função main
if __name__ == "__main__":
    main()

## Criação do executável
## pyinstaller.exe --onefile --windowed --noconsole --name='Chat Gados' main.py --version-file _versao.txt
## pyinstaller.exe --onefile --windowed --noconsole --name='Chat Gados' --icon=images/Icone-Chat.ico main.py --version-file _versao.txt