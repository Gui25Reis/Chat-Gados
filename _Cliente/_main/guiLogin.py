######      Gui Reis     -      guisreis25@gmail.com      -   31920918   ######
######    Gian Gamberi   -   giangamberi@hotmail.com.br   -   31944043   ######

# -*- coding: utf-8 -*-

#### Bibliotecas necessárias:
### Arquivos Globais ###
from PyQt5.QtWidgets import QMainWindow, QWidget, QStatusBar                    # Interface Gráfica:

### Arquivos Locais ###
from auxWidgets import AuxWidgets                                               # Widgets já pré criados:

class InterfaceLogin(AuxWidgets):
    """
    Classe responsável pela criação da interface gráfica da área de login e \
    toda configuração que é feita nela.
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
        janela_.resize(200, 145)                                            # Define a altura da jenela
        janela_.setFixedSize(200, 145)                                      # Deixa como tamanho fixado (não pode mexer nas dimensões da janela)
    
        janela_.setCentralWidget(self.root)                                 # Define como widget central
        janela_.setWindowTitle("LG Login Gados")                            # Título da janela

        self.statusbar = QStatusBar(janela_)                                # Cria uma barra de status
        janela_.setStatusBar(self.statusbar)                                # Add na janela

        ## Nome
        lblNome = self.lbl("NOME", 17, 10, 47, 20, self.root)               # Texto: "Nome"
        self.entNome = self.lineEdit(70, 10, 113, 20, self.root)            # Entrada de texto do nome 
        self.entNome.setMaxLength(10)

        ## Ip
        lblIp = self.lbl("IP", 17, 40, 47, 20, self.root)                   # Texto: "Ip"
        self.entIp = self.lineEdit(70, 40, 113, 20, self.root)              # Entrada de texto do ip
        self.entIp.setMaxLength(15)

        ## Porta
        lblPorta = self.lbl("PORTA", 17, 70, 47, 20, self.root)             # Texto: "Porta"
        self.entPorta = self.lineEdit(70, 70, 113, 20, self.root)           # Entrada de texto da porta
        self.entPorta.setMaxLength(5)

        self.bt = self.bts("Conectar", 109, 100, 75, 23, self.root)         # Botão conectar

        lblIp = lblNome = lblPorta = None
        del lblIp, lblNome, lblPorta                                        # Deleta os textos (não vão mais ser usados)
    
    def veri(self, t_:int) -> bool:
        """[Método] Verifica se as entradas inseridas são válidas"""
        # Se tiver algum campo vazio
        if (0 in [len(self.entNome.text()), len(self.entIp.text()), len(self.entPorta.text())]):
            self.setTextStatusBar("Não pode ter espaço em branco", t_)      # Mostra pro usuário o erro
            self.limpaAll()                                                 # Limpas as caixas de entradas
            return False

        # Se a porta não for numerica
        if (not self.entPorta.text().isnumeric()):
            self.setTextStatusBar("Porta inválida", t_)                     # Mostra pro usuário o erro
            return False
        
        # Se for um usuario do tipo arquivo não pode entrar
        if (self.entNome == "::file:"):
            self.setTextStatusBar("Nome de usuário inválido", t_)           # Mostra pro usuário o erro
            return False

        return True

    def limpaAll(self) -> None:
        """[Método] Limpa as caixas de entrada de texto"""
        self.entNome.clear()
        self.entIp.clear()
        self.entPorta.clear()

    #### POO-ENCAPSULAMENTOS ####
    
    def setTextStatusBar(self, s_:str, t_:int):
        """[Método Especial] Define o texto da barra de status."""
        self.statusbar.showMessage(s_, t_)
        self.statusbar.setStyleSheet("QStatusBar{background: red}")

    def getDadosConexao(self) -> tuple:
        """[Método Especial] Retorna os dados necessários para fazer uma conexão com o servidor."""
        return (self.entIp.text(), int(self.entPorta.text()))

    def getDados(self) -> list:
        """[Método Especial] Retorna os dados inseridos"""
        return [self.entNome.text(), self.entIp.text(), int(self.entPorta.text())]

    def setBtAction(self, func_) -> None:
        """[Método Especial] Define a ação do botão \"conectar\""""
        self.bt.clicked.connect(func_)                                     # Define a ação do botão enter da caixa de entrada