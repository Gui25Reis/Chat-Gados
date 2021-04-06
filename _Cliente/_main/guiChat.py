######      Gui Reis     -      guisreis25@gmail.com      -   31920918   ######
######    Gian Gamberi   -   giangamberi@hotmail.com.br   -   31944043   ######

# -*- coding: utf-8 -*-

#### Bibliotecas necessárias:
### Arquivos Globais ###
from PyQt5.QtWidgets import QMainWindow, QWidget, QTextEdit, QStatusBar             # Interface Gráfica:
from PyQt5.QtGui import QFont

### Arquivos Locais ###
from auxWidgets import QChatEdit                                                    # Entrada de texto personalizada:

class InterfaceChat:
    """
    Classe responsável pela criação da interface gráfica do chat e \
    qualquer configuração que é feita nela.
    """
    
    def __init__(self) -> None:
        """[Método Especial] Construtor da classe: Cria os atributos da classe."""
        self.root = QWidget()                                                       # [Atributo] Widget central: onde vai ser colocado os objetos
    
    def __del__(self) -> None: 
        """[Método Especial] Destrutor da classe: Deleta os atributos."""
        self.root = None
        del self.root                                                               # Deleta o atributo

    def setupUi(self, janela_:QMainWindow) -> None:
        """[Método] Criação da interface"""
        janela_.resize(390, 385)                                                # Define a altura da jenela
        janela_.setFixedSize(390, 385)                                          # Deixa como tamanho fixado (não pode mexer nas dimensões da janela)
    
        janela_.setCentralWidget(self.root)                                     # Define como widget central
        janela_.setWindowTitle("Chat Gados")                                    # Título da janela
        janela_.setStyleSheet("QMainWindow{background: rgb(0, 139, 139);}")     # Cor de fundo

        self.statusbar = QStatusBar(janela_)                                    # Cria uma barra de status
        janela_.setStatusBar(self.statusbar)                                    # Add na janela

        self.entrada = QChatEdit(self.root)                                     # Cria a caixa de entrada de texto
        self.entrada.setGeometry(20, 300, 350, 60)                              # Define a posição
        self.entrada.setFont(QFont('Consolas', 11))                             # Define a fonte
        self.entrada.setStyleSheet("QTextEdit{background: rgb(235, 230, 215);}")# Define a cor de fundo
        self.entrada.setFocus()                                                 # Deixa focado na hora de inicializar
    
        self.saida = QTextEdit(self.root)                                       # Cria a caixa de entrada de texto
        self.saida.setGeometry(20, 20, 350, 280)                                # Define a posição
        self.saida.setFont(QFont('Consolas', 11))                               # Define a fonte
        self.saida.setStyleSheet("QTextEdit{background: rgb(235, 230, 215);}")  # Define a cor de fundo
        self.saida.setReadOnly(True)                                            # Deixa apenas pra leitura (não pode editar)
    
    
    def clearAll(self) -> None:
        """[Método] Limpa os textos da caixa de entrada e da barra de status"""
        self.entrada.clear()                                                    # Tira o texto da caixa de entrada
        self.setTextStatusBar("", "rgb(0, 139, 139);")                          # Tira o texto da status bar

    #### POO-ENCAPSULAMENTOS ####
    
    def getText(self) -> str:
        """[Método Especial] Retorna o texto da caixa de entrada"""
        return self.entrada.toPlainText()
    
    def setTextStatusBar(self, s_:str, cor_:str) -> None:
        """[Método Especial] Define o texto da barra de status"""
        self.statusbar.showMessage(s_)                                          # Mostra a mensagem pro usuário
        self.statusbar.setStyleSheet(f"QStatusBar{{background: {cor_}}}")       # Define a cor
    
    def setTextChat(self, s_:str) -> None:
        """[Método Especial] Adiciona texto no chat (caixa de saída de texto)"""
        self.saida.append(s_)                                                   # Adiciona o texto na caixa de saída
    
    def setEnterSignal(self, func_) -> None:
        """[Método Especial] Define a conexão (ação) dos botões \"return\" e \"enter\""""
        self.entrada.setReturnSignal(func_)                                     # Define a ação do botão enter da caixa de entrada