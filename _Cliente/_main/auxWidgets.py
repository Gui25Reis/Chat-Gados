######      Gui Reis     -      guisreis25@gmail.com      -   31920918   ######
######    Gian Gamberi   -   giangamberi@hotmail.com.br   -   31944043   ######

# -*- coding: utf-8 -*-

#### Bibliotecas necessárias:
### Arquivos Globais ###
# Interface Gráfica:
from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QLabel, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QKeyEvent


class AuxWidgets:
    """
    Classe responsável pela criação dos widgets usado na Interface Gráfica

        Nessa classe é criada as áreas personalizados que serão usados em toda a interface: \
    botão, etiquetas (labels), estradas de texto, áreas de vizualização de textos e agrupamentos.
    """
    def __init__(self) -> None: pass
        
    def __del__(self) -> None: pass

    def lbl(self, txt_:str, p1_:int, p2_:int, p3_:int, p4_:int, wid_:QWidget) -> QLabel:
        """[Método] Cria labels."""
        lb = QLabel(txt_, wid_)                                                 # Cria uma label
        lb.setGeometry(p1_, p2_, p3_, p4_)                                      # Define a posição
        lb.setFont(QFont('Arial', 10))                                          # Define a fonte
        return lb

    def bts(self, txt_:str, p1_:int, p2_:int, p3_:int, p4_:int, wid_:QWidget) -> QPushButton:
        """[Método] Cria botões."""
        bt = QPushButton(txt_, wid_)                                            # Cria o botão
        bt.setGeometry(p1_, p2_, p3_, p4_)                                      # Define a posição
        bt.setFont(QFont('Arial', 10))                                          # Define a fonte
        return bt

    def lineEdit(self, p1_:int, p2_:int, p3_:int, p4_:int, wid_:QWidget) -> QLineEdit:
        """[Método] Cria entrada de uma linha de texto."""
        le = QLineEdit(wid_)                                                    # Cria uma entrada de texto
        le.setGeometry(p1_, p2_, p3_, p4_)                                      # Define a posição
        le.setFont(QFont('Arial', 10))                                          # Define a fonte
        return le


class QChatEdit(QTextEdit):
    """
    Classe responsável pela criação da entrada de texto, definindo uma mesma ação
    para as teclas "return" e "enter"
    """
    returnPressed:pyqtSignal = pyqtSignal()                                     # [Atributo] Verifica quando o enter é pressionado

    def keyPressEvent(self, e:QKeyEvent) -> None:
        """[Método Sobre-carregado] Verifica os eventos do teclado"""
        if e.key() in [Qt.Key_Return, Qt.Key_Enter]:                            # Se a tecla "return" ou "enter" for apertado
            self.returnPressed.emit()                                           # Emite um sinal
        else:
            QTextEdit.keyPressEvent(self, e)                                    # Chama o método original
    
    #### POO-ENCAPSULAMENTOS ####

    def setReturnSignal(self, func_) -> None:
        """[Método Especial] Define o que acontece quando as teclas \"Return\" e \"Enter\" são pressionadas"""
        self.returnPressed.connect(func_)