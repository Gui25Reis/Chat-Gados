######      Gui Reis     -      guisreis25@gmail.com      -   31920918   ######
######    Gian Gamberi   -   giangamberi@hotmail.com.br   -   31944043   ######

# -*- coding: utf-8 -*-

#### Bibliotecas necessárias
### Arquivos Globais ###
from socket import socket, error, AF_INET, SOCK_STREAM                              # Fazer uma conexão online:

### Arquivos Locais ###
from guiLogin import QMainWindow, InterfaceLogin                                    # Interface gráfica do login:
from clienteOK import Cliente                                                       # Ações do cliente:


class Login(QMainWindow, InterfaceLogin):
    """
    Classe responsável pelas ações e gerenciamento do login

    > Aqui é a ligação da ação do usuário, inserindo os dados de login, com a interface gráfica.
    
    > Verifica e tenta fazer uma conexão com o servidor, qualquer erro de conexão local é mostrado
    para o usuário.
    """
    # Define alguns atributos da classe
    cliente = socket(AF_INET, SOCK_STREAM)                                          # [Atributo] Cria uma conexão
    tempo:int = 3500                                                                # [Atributo] Tempo da mensagem de status

    def __init__(self) -> None:
        """[Método Especial] Construtor da classe

        Criação da interface gráfica.
        """
        super().__init__()                                                          # Chama os construtores das classes pais

        ## Esse parâmetro ("self") é da classe pai QMainWindow
        self.setupUi(self)                                                          # (InterfaceLogin) Gera a interface

        self.setBtAction(self.actBt)                                                # (InterfaceLogin) Define a ação do botão conectar

    
    def __del__(self) -> None:
        """[Método Especial] Destrutor da classe

        Fecha a conexão criada para teste de conexão.
        """
        self.cliente.close()                                                        # Fecha a conxão com o server
        self.cliente = self.tempo = None                                            # Limpa as variáveis
        del self.cliente, self.tempo                                                # Deleta as variáveis


    def actBt(self) -> None:
        """[Método] Ação do botão conectar"""
        if (not self.veri(self.tempo)): return                                      # (InterfaceLogin) Faz verificações dos dados inseridos

        self.setTextStatusBar("Conectando ao servidor..", self.tempo)               # (InterfaceLogin) Avisa ao usuário sobre a tentativa de conexão com o servidor
        try:
            self.cliente.connect(self.getDadosConexao())                            # Tenta fazer a conexão
            self.cliente.send("Teste de Conexão".encode("UTF-8"))                   # Manda pro server que é um teste
            self.cliente.close()                                                    # Fecha a conexão
        
            self.setTextStatusBar("Servidor conectado!", self.tempo)                # (InterfaceLogin) Avisa ao usuário que conectou

            dados = self.getDados()                                                 # (InterfaceLogin) Pega os dados inseridos
            self.win = Cliente(dados[0], dados[1], dados[2])                        # Cria a janela do chat
            self.hide()                                                             # Esconde a janela do login
            self.win.show()                                                         # Mostra a janela do chat

            dados = None                                                            # Limpa a variável
            del dados                                                               # Deleta a variável

        except error as e:
            self.error(str(e).split()[1][:5])                                       # Pega o código de erro
            self.limpaAll()                                                         # (InterfaceLogin) Limpa as entradas

    
    def error(self, e_:str) -> None: 
        """
        [Método] Mostra, pela barra de status, o erro pro usuário (de acordo com o código de erro WinError)
        """

        if e_ == "10061":
            self.setTextStatusBar("IP ou PORTA inválidos.", self.tempo)

        elif e_ == "10060":
            self.setTextStatusBar("Servidor está offline.", self.tempo)

        elif e_ == "11001":
            self.setTextStatusBar("Ip inexistente", self.tempo)
            
        else:
            self.setTextStatusBar(f"Erro: WinError {e_}.", self.tempo)