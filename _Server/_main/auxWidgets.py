######      Gui Reis     -      guisreis25@gmail.com      -   31920918   ######
######    Gian Gamberi   -   giangamberi@hotmail.com.br   -   31944043   ######

# -*- coding: utf-8 -*-

#### Bibliotecas necessárias:
### Arquivos Globais ###
# Interface Gráfica:
from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QLabel, QGroupBox, QTextEdit
from PyQt5.QtGui import QFont


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
    
    def txtEdit(self, p1_:int, p2_:int, p3_:int, p4_:int, wid_:QWidget) -> QTextEdit:
        """[Método] Cria a área de entrada de texto grandes e/ou vizualização de texto."""
        le = QTextEdit(wid_)                                                    # Cria uma entrada de texto
        le.setGeometry(p1_, p2_, p3_, p4_)                                      # Define a posição
        le.setFont(QFont('Consolas', 11))                                       # Define a fonte
        le.setReadOnly(True)                                                    # Não poode editar o conteúdo
        return le
    
    def gBox(self, n_:str, p1_:int, p2_:int, p3_:int, p4_:int, wid_:QWidget) -> QGroupBox:
        """[Método] Cria os grupos de áreas (Group Box)."""
        gb = QGroupBox(n_, wid_)                                                # Cria o Gruop Box 
        gb.setGeometry(p1_, p2_, p3_, p4_)                                      # Define as proporções
        gb.setFont(QFont('Arial', 12))                                          # Define a fonte
        gb.setStyleSheet("QGroupBox {border: 1px solid brown;}")                # Define a borda
        return gb