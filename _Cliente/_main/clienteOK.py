######      Gui Reis     -      guisreis25@gmail.com      -   31920918   ######
######    Gian Gamberi   -   giangamberi@hotmail.com.br   -   31944043   ######

# -*- coding: utf-8 -*-

#### Bibliotecas necessárias
### Arquivos Globais ###
from socket import socket, AF_INET, SOCK_STREAM                                                 # Fazer uma conexão online
from datetime import datetime                                                                   # Horário real
from shutil import copyfile                                                                     # Copia um arquivo de um diretório (pasta) pra outro
from os.path import isdir, splitext, abspath                                                    # Informções de arquivo
from os.path import join as osJoin                                                              # Diferencia o join nativo de python
from os import mkdir, getcwd                                                                    # Criação de diretórios (pastas) e caminho absoluto

### Arquivos Locais ###
from guiChat import QMainWindow, InterfaceChat                                                  # Criação da interface gráfica
from threads import EnviaFileThread, EnviaTextThread, RecebeThread                              # Criação das threads


class Cliente(QMainWindow, InterfaceChat):
    """
    Classe responsável pelas ações e gerenciamento do cliente

    Aqui é a ligação da ação do usuário com a interface gráfica e também o envio 
    e recebimento de dados.
    """
    # Define alguns atributos da classe
    cliente = socket(AF_INET, SOCK_STREAM)                                                      # [Atributo] Cria uma conexão
    buffer:int = 4096                                                                           # [Atributo] Tamanho do buffer
    
    def __init__(self, usuario_:str, ip_:str, porta_:int) -> None:
        """[Método Especial] Construtor da classe:

        > Recebe o ip e a porta pra fazer a conexão, além do usuário pra mandar pro servidor
        mostrando quem está conectando.

        > Cria a interface gráfica

        > Cria uma thread para receber dados
        """
        super().__init__()                                                                      # Chama os construtores das classes pais

        self.ip:str = ip_                                                                       # [Atributo] Ip do server
        self.porta:int = porta_                                                                 # [Atributo] Porta do server
        
        self.pasta:str = f"{getcwd()}\\Chat-Gados"                                              # Caminho de onde vai receber o arquivo

        self.cliente.connect((self.ip, self.porta))                                             # Conecta com o server

        ## Esse parâmetro ("self") é da classe pai QMainWindow
        self.setupUi(self)                                                                      # (InterfaceChat) Gera a interface 
        
        self.cliente.sendall(usuario_.encode("UTF-8"))                                          # Envia o nome do usuário pro servidor

        self.recebe = RecebeThread(self.cliente, self.pasta)                                    # Cria uma thread para receber mensagens
        self.recebe.start()                                                                     # Inicia essa thread
        self.recebe.sigMensagem.connect(self.posta)                                             # Define a ação do sinal (Aqui é onde manda a mensagem)

        self.setEnterSignal(self.manda)                                                         # Define a ação dos botões Enters

    
    def __del__(self) -> None:
        """[Método Especial] Destrutor da classe: Fecha a conexão feita e deleta os atributos."""
        self.cliente.close()                                                                    # Fecha a conexão com o servidor
        self.cliente = self.ip = self.porta = self.recebe = None                                # Limpa os atributos
        del self.cliente, self.ip, self.porta, self.recebe                                      # Deleta os atributos

    def posta(self, msg_:str) -> None:
        """[Método] Posta a mensagem recebida na caixa de texto (saída)"""
        self.setTextChat(msg_)                                                                  # Aiciona a mensagem na caixa de texto
    
    def manda(self) -> None:
        """[Método] Manda a mensagem escrita na caixa de texto (entrada) pro servidor."""
        msg = self.getText()                                                                    # Pega o texto escrito

        # Se a mensagem for muito grande
        if len(msg) > 300:
            self.setTextStatusBar("Essa mensagem muito longa.", "Red")                          # Avisa o usuário pela barra de status
            return                                                                              # Sai da função
        
        # Se for um arquivo
        if ("file:///" in msg):
            try:
                # Criação do nome do arquivo
                tipoArquivo:str  = splitext(msg)[1]                                             # Pega o tipo de arquivo
                horaMomento:str = str(datetime.now().strftime("%X")).replace(":","-")           # Pega a hora que mandou a mensagem
                ip:str = self.ip.replace(".","")
                novoNomeArquivo:str = f"{horaMomento}-{ip}{tipoArquivo}"                        # Cria o nome do arquivo
                caminho:str = str(msg[8:])                                                      # Pega o caminho do arquivo inserido
                
                if (not isdir(self.pasta)): mkdir(self.pasta)                                   # Cria a pasta do chat
                
                rec:str = f"{self.pasta}\\Chat-Recebidos\\"                                     # Caminho da pasta de recebidos
                if (not isdir(rec)): mkdir(rec)                                                 # Se a pasta onde recebe arquivos não existir cria ela

                env:str = f"{self.pasta}\\Chat-Enviados\\"                                      # Caminho da pasta de enviados
                if (not isdir(env)): mkdir(env)                                                 # Se a pasta que guarda os arquivos enviados não existir cria ela
        
                copyfile(caminho, osJoin(abspath(env), novoNomeArquivo))                        # Copia o arquivo que quer enviar pra pasta
            except: 
                self.enviaTxt(msg)
                return
                
            self.tEnviar = EnviaFileThread(novoNomeArquivo, self.ip, self.porta, self.pasta)    # Cria uma thread para mandar o arquivo
            self.tEnviar.start()                                                                # Inicia essa thread
            self.clearAll()                                                                     # Limpa a caixa de texto (e barra de status)

            rec = env = tipoArquivo = horaMomento = ip = novoNomeArquivo = caminho = None       # Limpas as variáveis
            del tipoArquivo, horaMomento, ip, novoNomeArquivo, caminho, rec, env,               # Deleta as variáveis

        # Se for uma mensagem
        else: self.enviaTxt(msg)

        msg = None                                                                              # Limpas as variáveis
        del msg                                                                                 # Deleta as variáveis
            
    def enviaTxt(self, msg_:str) -> None:
        """[Método] Envia uma mensagem de texto pro servidor."""
        self.tEnviar = EnviaTextThread(self.cliente, msg_.encode("UTF-8"))                      # Cria uma thread para mandar o texto
        self.tEnviar.start()                                                                    # Inicia essa thread

        self.clearAll()                                                                         # Limpa a caixa de texto (e barra de status)