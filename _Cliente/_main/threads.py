######      Gui Reis     -      guisreis25@gmail.com      -   31920918   ######
######    Gian Gamberi   -   giangamberi@hotmail.com.br   -   31944043   ######

# -*- coding: utf-8 -*-

#   Classes que vão ser usadas para criar threads para envio de mensagens ou arquivos 
# e receber mensagens ou arquivos 

#### Bibliotecas necessárias
### Arquivos Globais ###
from socket import socket, AF_INET, SOCK_STREAM                                                         # Fazer uma conexão online:
from PyQt5.QtCore import QThread, pyqtSignal                                                            # Interface gráfica (parte de thread)
from time import sleep                                                                                  # Delay

class EnviaTextThread(QThread):
    """Classe responsável por criar uma thread para enviar uma mensagem de texto."""
    def __init__(self, socket_:socket, msg_:str) -> None:
        """[Método Especial] Construtor da classe: Define o destino da mensagem e o texto dela."""
        self.sock = socket_                                                                             # [Atributo] Destino da mensagem
        self.msg = msg_                                                                                 # [Atributo] Mensagem
        super().__init__()                                                                              # Chama o construtor da classe pai (QThread)

    def run(self) -> None:
        """[Método Sobre-carregado] Re-define a função run() de QThread

        Aqui é onde envia as mensagens de texto.

        OBS: Essa função é chamada no construtor de QThread
        """
        try: self.sock.send(self.msg)                                                                   # Tenta: manda a mensagem 
        except: exit()                                                                                  # Erro: fecha a aplicação


class RecebeThread(QThread):
    """Classe responsável por criar uma thread para receber dados."""

    sigMensagem:pyqtSignal = pyqtSignal(str)                                                            # [Atributo] Responsável por mandar a mensagem
    
    def __init__(self, socket_:socket, path_:str) -> None:
        """[Método Especial] Construtor da classe: Define de onde vai receber os dados."""
        self.sock = socket_                                                                             # [Atributo] Destino da mensagem
        self.caminho = path_                                                                            # [Atributo] Caminho que esta a imagem
        super().__init__()                                                                              # Chama o construtor da classe pai (QThread)
    
    def __del__(self) -> None:
        """[Método Especial] Destrutor da classe: Deleta os atributos."""
        self.sock = self.caminho = None                                                                 # Limpa as variáveis
        del self.sock, self.caminho                                                                     # Deleta os atriutos

    def run(self) -> None:
        """[Método Sobre-carregado] Re-define a função run() de QThread

        Aqui é onde recebe os dados.

        OBS: Essa função é chamada no construtor de QThread
        """
        while True:
            try:
                texto = self.sock.recv(4096).decode("UTF-8")                                            # Recebe a mensagemdo servidor
                if (texto == "::file:"):                                                                # Se for um arquivo
                    self.sigMensagem.emit("*server*: >> Recebendo arquivo <<")                          # Mostra pro usuário que vai receber os arquivos
                    self.recebendoFile = RecebeFileThread(self.sock, self.caminho)                      # Cria uma thread pra receber os arquivos
                    self.recebendoFile.start()                                                          # Inicia essa thread
                    while (self.recebendoFile.isRunning()):                                             # Enquanto ela estiver rodando
                        pass                                                                            # Permanece nessa função
                    
                    sleep(1.5)                                                                          # Delay: Tempo para o servidor conseguir processar os dados
                    self.tEnviar = EnviaTextThread(self.sock, "Arquivo recebido".encode("UTF-8"))       # Cria uma thread para mandar o texto
                    self.tEnviar.start()                                                                # Inicia essa thread
                    self.sigMensagem.emit("Você recebeu um arquivo.")                                   # Mostra pro usuário que ele recebeu um arquivo
                else:
                    self.sigMensagem.emit(texto)

                texto = None                                                                            # Limpa a variável
                del texto                                                                               # Deleta a variável

            except:                                                                                     # Erro: não tem como receber
                self.sigMensagem.emit(">>> Você foi desconectado <<<")
                break


class EnviaFileThread(QThread):
    """Classe responsável por criar uma thread para enviar arquivos."""
    def __init__(self, arq_:str, ip_:str, porta_:int, path_:str):
        """[Método Especial] Construtor da classe: Faz uma nova conexão com o servidor para mandar o arquivo."""
        self.cliente = socket(AF_INET, SOCK_STREAM)                                                     # [Atributo] Cria uma conexão
        self.cliente.connect((ip_, porta_))                                                             # Conecta com o servidor (destino da mensagem)

        self.cliente.send("::file:".encode("UTF-8"))                                                    # Envia uma mensagem (avisa que vai mandar um aqruivo)

        self.arq:str = arq_                                                                             # [Atributo] Nome do arquivo
        self.caminho:str = f"{path_}\\Chat-Enviados\\{self.arq}"                                        # [Atributo] Caminho que esta a imagem

        super().__init__()                                                                              # Chama o construtor da classe pai (QThread)
    
    def __del__(self) -> None:
        """[Método Especial] Destrutor da classe: Deleta os atributos."""
        self.cliente = self.arq = self.caminho = None                                                   # Limpa as variáveis
        del self.cliente, self.arq, self.caminho                                                        # Deleta os atriutos

    def run(self):      
        """[Método Sobre-carregado] Re-define a função run() de QThread

        Aqui é onde envia os dados do arquivo.

        OBS: Essa função é chamada no construtor de QThread
        """ 
        self.cliente.send(f"{self.arq}".encode("UTF-8"))                                                # Envia o tipo de arquivo

        sleep(1)                                                                                        # Delay: Tempo para o servidor conseguir processar os dados
        with open(self.caminho, "rb") as f:                                                             # Pega o arquivo
            while (True):                                                                               # Loop: Enquanto tiver bytes para enviar
                bytes_read = f.read(4096)                                                               # Le os bytes
                if (not bytes_read): break                                                              # Break: Não tem mais bytes pra serem lidos 
                self.cliente.sendall(bytes_read)                                                        # Envia os bytes

        f.close()                                                                                       # Fecha o arquivo usado
        self.cliente.close()                                                                            # Fecha a conexão com o servidor

        bytes_read = None                                                                               # Limpa variável
        del bytes_read                                                                                  # Deleta ela


class RecebeFileThread(QThread):
    """Classe responsável por criar uma thread para receber arquivos."""
    def __init__(self,socket_:socket, path_:str):
        """[Método Especial] Construtor da classe: Define de onde vai receber os dados e recebe o nome do arquivo."""
        self.nomeArquivo:str = socket_.recv(4096).decode("UTF-8")                                       # [Atributo] Nome do arquivo
        self.socket:socket = socket_                                                                    # [Atributo] Destino da mensagem
        self.caminho:str = f"{path_}\\Chat-Recebidos\\{self.nomeArquivo}"                               # [Atributo] Caminho que esta a imagem
        super().__init__()                                                                              # Chama o construtor da classe pai (QThread)

    def __del__(self) -> None:
        """[Método Especial] Destrutor da classe: Deleta os atributos."""
        self.nomeArquivo = self.socket = self.caminho = None                                            # Limpa as variáveis
        del self.nomeArquivo, self.socket, self.caminho                                                 # Deleta os atriutos
    
    def run(self):                                  
        """[Método Sobre-carregado] Re-define a função run() de QThread

        Aqui é onde recebe os dados do arquivo.

        OBS: Essa função é chamada no construtor de QThread
        """ 
        with open(self.caminho, "wb") as f:                                                             # Abre o arquivo
            while (True):                                                                               # Loop: Enquanto tiver bytes para receber
                bytes_read = self.socket.recv(4096)                                                     # Recebe os bytes
                try: 
                    bytes_read.decode("UTF-8")                                                          # Tenta decodifica a mensagem
                    break
                except: f.write(bytes_read)                                                             # Escreve os bytes
        f.close()                                                                                       # Fecha o arquivo usado

        bytes_read = None                                                                               # Limpa variável
        del bytes_read                                                                                  # Deleta ela