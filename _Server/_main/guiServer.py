######      Gui Reis     -      guisreis25@gmail.com      -   31920918   ######
######    Gian Gamberi   -   giangamberi@hotmail.com.br   -   31944043   ######

# -*- coding: utf-8 -*-

#### Bibliotecas necessárias:
### Arquivos Globais ###
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QTextBrowser                   # Interface Gráfica.
from PyQt5.QtCore import Qt

### Arquivos Locais ###
from auxWidgets import AuxWidgets, QWidget, QFont                                   # Configurações da interface gráfica pré-criadas.


class InterfaceServer(AuxWidgets):
    """
    Classe responsável pela criação da interface gráfica do servidor e \
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
        janela_.resize(780, 490)                                                    # Define a altura da jenela
        janela_.setFixedSize(780, 490)                                              # Deixa como tamanho fixado (não pode mexer nas dimensões da janela)
    
        janela_.setCentralWidget(self.root)                                         # Define como widget central
        janela_.setWindowTitle("Server Gados")                                      # Título da janela

        self.statusbar = QStatusBar(janela_)                                        # Cria uma barra de status
        janela_.setStatusBar(self.statusbar)                                        # Add na janela

        ## Configuração
        self.gBoxConfig = self.gBox("Configuração", 10, 15, 371, 101, self.root)    # Cria a área de configuração

        lblIpLocal = self.lbl("IP Local", 12, 30, 61, 20, self.gBoxConfig)          # Texto: "Ip"
        self.entIpLocal = self.lineEdit(78, 30, 111, 20, self.gBoxConfig)           # Entrada de texto do ip
        self.entIpLocal.setMaxLength(15)                                            # Define o máximo de caracter aceito

        lblPorta = self.lbl("Porta", 206, 30, 41, 20, self.gBoxConfig)              # Texto: "Porta"
        self.entPorta = self.lineEdit(250, 30, 111, 20, self.gBoxConfig)            # Entrada de texto da porta
        self.entPorta.setMaxLength(5)                                               # Define o máximo de caracter aceito
        self.entPorta.setFocus()                                                    # Deixa focado

        self.btConectar = self.bts("Conectar", 286, 66, 75, 23, self.gBoxConfig)    # Botão conectar

        ## Ip externo
        lbl = self.lbl("Server-IP", 440, 21, 107, 49, self.root)                    # Texto: "Server-IP"
        lbl.setFont(QFont('MS Shell Dlg 2', 18, 50))                                # Define a fonte

        self.lblIp = self.lbl("", 560, 21, 179, 49, self.root)                      # Cria a label com texto vazio
        self.lblIp.setFont(QFont('MS Shell Dlg 2', 18, 50))                         # Define a fonte
        self.lblIp.setAlignment(Qt.AlignCenter)                                     # Define o alinhamento
        self.lblIp.setTextInteractionFlags(Qt.TextSelectableByMouse)                # Permite selecionar o texto com o mouse

        # Usada pra função copiar e colar
        self.txt = QTextBrowser()                                                   # Cria uma área de texto (mas não coloca ela na interface)
        self.btCopiar = self.bts("Copiar", 550, 83, 75, 23, self.root)              # Botão copiar
        self.btCopiar.clicked.connect(self.btCopiar_action)                         # Definea ação do botão

        ## Log
        self.gBoxLog = self.gBox("Log", 10, 138, 371, 321, self.root)               # Cria a área de log
        self.txtLog = self.txtEdit(10, 30, 351, 281, self.gBoxLog)                  # Cria a área de vizualização de texto
        self.txtLog.setReadOnly(True)                                               # Deixa apenas pra leitura (não pode editar)

        ## Chat
        self.gBoxChat = self.gBox("Chat", 400, 138, 371, 321, self.root)            # Cria a área de log
        self.txtChat = self.txtEdit(10, 30, 351, 281, self.gBoxChat)                # Cria a área de vizualização de texto
        self.txtChat.setReadOnly(True)                                              # Deixa apenas pra leitura (não pode editar)

        lbl = lblPorta = lblIpLocal = None
        del lbl, lblPorta, lblIpLocal                                               # Deleta os textos (não vão mais ser usados)

    def btCopiar_action(self):
        """[Método] Ação do botão \"copiar\"."""
        self.txt.selectAll()                                                        # Seleciona o texto
        self.txt.copy()                                                             # Copia o texto

    def serverLigado(self):
        """[Método] Alterações na interface quando o servidor está ligado."""
        self.gBoxConfig.setEnabled(False)                                           # Desativa a área de configuração
        self.setTextStatusBar("Servidor ligado.", "Green")                          # Mostra que o servidor está ligado

    def semInternet(self, s_:str) -> None:
        """[Método] Mostra para o usuário que está sem conexão com a internet."""
        self.setTextStatusBar(s_, "Orange")
    
    def veri(self) -> bool:
        """[Método] Verifica se a porta é válida."""
        if (len(self.entPorta.text()) == 0) or (not self.entPorta.text().isnumeric()):
            self.setTextStatusBar("Porta inválida.", "Red")
            return False
        return True

    #### POO-ENCAPSULAMENTOS ####

    def setTexts(self, externo_:str, local_:str):
        """[Método Especial] Define o texto da label que vai ser copiado."""
        self.txt.setText(externo_)
        self.lblIp.setText(externo_)
        self.entIpLocal.setText(local_)
    
    def setTextStatusBar(self, s_:str, cor_:str):
        """[Método Especial] Define o texto da barra de status."""
        self.statusbar.showMessage(s_)
        self.statusbar.setStyleSheet(f"QStatusBar{{background: {cor_}}}")
        
    def setTextLog(self, s_:str) -> None:
        """[Método Especial] Adiciona texto na área de log."""
        self.txtLog.append(s_)

    def setTextChat(self, s_:str) -> None:
        """[Método Especial] Adiciona texto na área de chat."""
        self.txtChat.append(s_)

    def setBtConectarAction(self, func_) -> None:
        """[Método Especial] Define a ação do botão \"conectar\"."""
        self.btConectar.clicked.connect(func_)                                     # Define a ação do botão enter da caixa de entrada
    
    def getDadosConexao(self) -> tuple:
        """[Método Especial] Retorna os dados necessários para fazer uma conexão com o servidor."""
        return (self.entIpLocal.text(), int(self.entPorta.text()))