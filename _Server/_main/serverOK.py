######      Gui Reis     -      guisreis25@gmail.com      -   31920918   ######
######    Gian Gamberi   -   giangamberi@hotmail.com.br   -   31944043   ######

# -*- coding: utf-8 -*-

#### Bibliotecas necessárias
### Arquivos Globais ###
from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM                         # Fazer uma conexão online
from datetime import datetime                                                                       # Horário real
from time import sleep                                                                              # Delay
from requests import get                                                                            # Pega informações de api online
from threading import Thread                                                                        # Uso de threads
from os.path import isdir                                                                           # Verifica se existe repositório
from os import mkdir, getcwd                                                                        # Cria diretórios

### Arquivos Locais ###
from guiServer import QMainWindow, InterfaceServer                                                  # Interface Gráfica


class Server(QMainWindow, InterfaceServer):
    """Classe responsável pela criação e gerenciamento do servidor."""
    # Define alguns atributos da classe
    server = socket(AF_INET, SOCK_STREAM)                                                           # [Atributo] Cria uma conexão
    lock:bool = False                                                                               # [Atributo] Verifica quando uma thread esta sendo usada

    try: ipExterno:str = get('https://api.ipify.org').text                                          # [Atributo] Pega o ip externo (tem acesso á internet)
    except: ipExterno:str = "Local Host"                                                            # [Atributo] Pega o local host (sem internet)

    ipLocal:str = gethostbyname(gethostname())                                                      # [Atributo] Ip local
    connections_dict:dict = {}                                                                      # [Atributo] Dicionário com todas -> "usuario":conexão

    buffer:int = 4096                                                                               # [Atributo] Tamanho do buffer

    def __init__(self) -> None:
        """[Método Especial] Construtor da classe:

        > Define os ips: local e externo.

        > Cria a interface gráfica e faz as configurações iniciais.
        """
        super().__init__()                                                                          # Chama os construtores das classes pais

        ## Esse parâmetro ("self") é da classe pai QMainWindow
        self.setupUi(self)                                                                          # (InterfaceChat) Gera a interface 

        self.setTexts(self.ipExterno, self.ipLocal)                                                 # (InterfaceChat) Define os textos 
        self.setBtConectarAction(self.conectarAction)                                               # (InterfaceChat) Difine a ação do botão conectar

        if self.ipExterno == "Local Host":
            self.semInternet("Sem conexão com a internet")                                          # (InterfaceChat) Mostra que está sem internet
        else:
            txt = "Adicione a porta para ligar o servidor. (Verifique se a porta está aberta)"
            self.setTextStatusBar(txt, "Orange")                                                    # (InterfaceChat) Mensagem inicial
            txt = None                                                                              # Limpa a variável
            del txt                                                                                 # Deleta a variável
        
        self.pasta:str = f"{getcwd()}\\Chat-Gados"                                              # Caminho de onde vai receber o arquivo

    def __del__(self) -> None: 
        """[Método Especial] Destrutor da classe: Fecha a conexão feita."""
        self.server.close()                                                                         # Fecha a conexão do server
        self.server = self.connections_dict = None
        self.buffer = self.ipExterno = self.ipLocal = self.lock = None
        del self.server, self.connections_dict
        del self.buffer, self.ipExterno, self.ipLocal, self.lock

    def conectarAction(self) -> None:
        """[Método] Ação do botão conectar."""
        if (not self.veri()): return                                                                # (InterfaceLogin) Faz verificações dos dados inseridos
        try:
            self.server.bind(self.getDadosConexao())                                                # Tenta fazer a conexão
            self.ligaServer()                                                                       # (InterfaceLogin) Avisa ao usuário que conectou

        except:
            txt = "Falha ao ligar o servidor: verifique se está concectado a mesma rede do IP local e/ou se a porta está acessível."
            self.setTextStatusBar(txt, "Red")                                                       # (InterfaceLogin) Avisa ao usuário que deu erro
            txt = None                                                                              # Limpa a variável
            del txt                                                                                 # Deleta a variável

    def ligaServer(self) -> None:
        """[Método] Configurações pro servidor aceitar conexões."""
        self.serverLigado()                                                                         # Faz as configurações da interface pro server ativado
        self.server.listen(30)                                                                      # Define a quantidade máxima de clientes que vai receber

        aceitaCliente = Thread(target = self.aceitaCliente)                                         # Cria uma thread onde passa a aceitar conexões
        aceitaCliente.daemon = True
        aceitaCliente.start()                                                                       # Inicia a thread
        
    def aceitaCliente(self) -> None:
        """[Método] Aceita conexões."""
        while True:                                                                                 # Loop infinito
            cSock, address = self.server.accept()                                                   # Aceita conexão
            usuario:str = cSock.recv(self.buffer).decode("UTF-8")                                   # Recebe o nome do usuário

            # Se for um cliente pra entrega de arquivo
            if (usuario == "::file:"):
                self.setTextLog(f"ARQUIVO: {str(address[0])} na porta {str(address[1])} conectado!")# Mostra que eh um cliente de arquivo conectado

                clienteThread = Thread(target=self.recebe_arquivo, args=[cSock])                    # Cria uma thread pra receber o arquivo
                clienteThread.daemon = True
                clienteThread.start()                                                               # Inicia a thread

            # Se for um cliente normal
            elif (usuario != "Teste de Conexão"):
                contador = 2                                                                        # Número que vai ser adicionado no nome
                while (usuario in self.connections_dict.keys()):                                    # Caso já tenha um usuário com esse mesmo nome
                    usuario = f"{usuario}{contador}"                                                # Muda o usuário
                    contador += 1                                                                   # Aumenta o contador
                    
                self.connections_dict[usuario] = cSock                                              # Adiciona ele no dicionário

                self.setTextLog(f'{usuario.capitalize()} no ip {str(address[0])} na porta {str(address[1])} conectado!')    # Mostra o cliente conectado

                clienteThread = Thread(target=self.manda_recebe, args=[cSock, usuario])             # Cria uma thread pra mandar e receber o arquivo
                clienteThread.daemon = True
                clienteThread.start()                                                               # Inicia ela

                contador = None                                                                     # Limpa a variávei
                del contador                                                                        # Deleta a variávei

            cSock = address = usuario = None                                                        # Limpa as variáveis
            del cSock, address, usuario                                                             # Deleta as variáveis

    def recebe_arquivo(self, clientsocket_:socket) -> None:   
        """[Método] Recebe um arquivo."""
        try:
            self.setTextChat("*server*: >> Recebendo arquivo <<")
            nomeArquivo = clientsocket_.recv(4096).decode("UTF-8")                                  # Recebe o tipo de arquivo

            if (not isdir(self.pasta)): mkdir(self.pasta)                                           # Cria a pasta do chat

            pastaEnviados:str = f"{self.pasta}\\ServerArquivosRecebidos\\"                          # Caminho da pasta onde são colocados os arquivos que são enviados
            if (not isdir(pastaEnviados)): mkdir(pastaEnviados)                                     # Se a pasta não existir cria ela

            with open(f"{pastaEnviados}{nomeArquivo}", "wb") as f:                                  # Cria o arquivo
                while True:                                                                         # Loop: Enquanto tiver bytes para receber
                    bytes_read = clientsocket_.recv(4096)                                           # Recebe os bytes
                    if (not bytes_read): break                                                      # Break: Não tem mais bytes pra serem lidos 
                    f.write(bytes_read)                                                             # Escreve os bytes

            f.close()                                                                               # Fecha o arquivo usado
            clientsocket_.close()                                                                   # Fecha a conexão do cliente com o servidor

            clienteThread = Thread(target=self.enviaArqGeral, args=[nomeArquivo, pastaEnviados])    # Cria uma thread pra mandar e receber o arquivo
            clienteThread.daemon = True
            clienteThread.start()                                                                   # Inicia ela

            self.setTextLog("ARQUIVO: desconectado!")

            bytes_read = pastaEnviados = nomeArquivo = None                                         # Limpa as variáveis
            del bytes_read, pastaEnviados, nomeArquivo                                              # Deleta as variávies

        except:
            self.setTextLog("ARQUIVO: Houve um erro.")
            return

    def manda_arquivo(self, cliente_:socket, file_:str, path_:str) -> None:
        """[Método] Manda um arquivo."""
        try:
            cliente_.send("::file:".encode("UTF-8"))                                                # Envia uma mensagem (avisa que vai mandar um aqruivo)
            cliente_.send(f"{file_}".encode("UTF-8"))                                               # Envia o tipo de arquivo
            sleep(1)                                                                                # Delay: Tempo para o cliente conseguir processar os dados

            with open(f"{path_}{file_}", "rb") as f:                                                # Pega o arquivo
                while True:                                                                         # Loop: Enquanto tiver bytes para enviar
                    bytes_read = f.read(4096)                                                       # Le os bytes
                    if (not bytes_read): break
                    cliente_.sendall(bytes_read)                                                    # Envia os bytes
            cliente_.sendall("Break".encode("UTF-8"))                                               # Mensagem que quebra o loop do outro lado
            f.close()                                                                               # Fecha o arquivo usado    

            bytes_read = None                                                                       # Limpa as variáveis
            del bytes_read                                                                          # Deleta as variávies
        except: return
            
            
    def enviaArqGeral(self, file_:str, path_:str) -> None:
        """[Método] Cria thread para enviar arquivos para as cnexões."""
        self.lock = True                                                                            # Mostra que vai receber um arquivo
        threads:list = []                                                                           # Guarda as threads
        for connection in self.connections_dict.values():                                           # Loop: pega todas as conexões
            threads.append(Thread(target=self.manda_arquivo, args=[connection, file_, path_]))      # Thread que manda um arquivo e add ela na lista
            threads[-1].start()                                                                     # Inicia ela

        t:Thread = None                                                                             # Variável do loop
        for t in threads:                                                                           # Loop: pegas as threads
            while (t.is_alive()):                                                                   # Verifica se está ativa ainda
                pass
        self.lock = False                                                                           # Quando acabar de mandar mensagem, destrava
        threads = connection = None                                                                 # Limpa a variável
        del threads, connection                                                                     # Deleta ela

    def manda_recebe(self, clientsocket_:socket, user_:str) -> None:
        """[Método] Manda ou recebe um texto."""
        self.enviaTxtGeral(f'*server* {user_} entrou na conversa.')                                 # Cria a mensagem que vai ser enviada)                                                                  # Manda pra todos os usuários sobre a nova conexão
        msgEnviar:list = []
        while True:
            try:                                                                                    # Se tiver conexão
                data:bytes = clientsocket_.recv(self.buffer)                                        # Espera receber uma mensagem
                
                horaMomento:str = datetime.now().strftime("%X")                                     # Pega o horário que recebeu
                msg:str = f'{horaMomento[:5]} - {user_}: {data.decode("UTF-8")}'                    # Cria a formatação da mensagem

                if (self.lock):                                                                     # Se estiver travado (esta mandando arquivo)
                    msgEnviar.append(msg)                                                           # Adiciona a mensagem numa lista
                else:
                    if (msgEnviar):                                                                 # Se tiver mensagem pra ser mandada
                        msgEnviar.append(msg)                                                       # Adiciona a mensagem numa lista
                        for mensagem in msgEnviar:                                                  # Loop: pega todas as mensagens
                            self.enviaTxtGeral(mensagem)                                            # Envia
                        msgEnviar = []                                                              # Zera a lista
                    else:
                        self.enviaTxtGeral(msg)                                                     # Envia a mensagem normal
                    
            except:                                                                                 # Se não tiver conexão
                self.connections_dict.pop(user_, None)                                              # Tira do dicionário
                self.setTextLog(f"{user_} desconectado.")                                           # Mostra no log que foi desconectado

                self.enviaTxtGeral(f'*server* {user_} saiu do chat.')                               # Cria a mensagem que vai ser enviada
                clientsocket_.close()                                                               # Fecha a conexão como cliente
                break                                                                               # Quebra o loop
        msgEnviar = None
        del msgEnviar                                                                               # Tira a lista da memória

    def enviaTxtGeral(self, msg_:str) -> None:
        """[Método] Manda pra todos os usuários a mensagem de texto."""
        self.setTextChat(msg_)                                                                      # Mostra no chat do server
        for connection in self.connections_dict.values():                                           # Loop: pega todas as conexões
            connection.sendall(msg_.encode("UTF-8"))                                                # Manda a mensagem
        connection:socket = None                                                                    # Limpa a variável
        del connection                                                                              # Deleta a variável