import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec   # atualiza os gráficos na mesma janela
from drawnow import * #
from array import array #
import Tela_H2

Yaxistemp = array('f')
Yaxispres = array('f')
YaxisH2=array('f')

def makeFig():
    gs = gridspec.GridSpec(3, 3)  # gridspec 3x3
    # Plot 1
    plt.subplot(gs[0, :])  # posicao do subplot
    #plt.ylim([-30, 50])  # valor min e max de y
    plt.title('Pressão')  # titulo
    plt.grid(True)
    plt.ylabel('Pressão')  # etiquetas do eixo y
    plt.plot(Yaxispres, 'ro-', label='pressão') #plot de temperature
    plt.legend(loc='upper left')
    # plot da legenda
    plt2 = plt.twinx()
    # cria um Segundo eixo y
    #plt.ylim(-30, 50)
    # define os limites do Segundo eixo y
    plt2.plot(Yaxispres, 'b^-', label='---')
    # desenha os val. De tempF2
    plt2.set_ylabel('----')  # Etiqueta do
    # Segundo eixo
    plt2.ticklabel_format(useOffset=False)  # impede
    # a escala do eixo X
    plt2.legend(loc='upper right')
    # Plot 2
    plt.subplot(gs[1, :])
    #plt.ylim([0, 100])
    plt.title('gás hidrogênio')
    plt.grid(True)
    plt.ylabel('H2 /ppmv -1 %')
    plt.plot(YaxisH2, 'ro-', label='H2')
    plt.legend(loc='upper left')
    plt2 = plt.twinx()
    #plt.ylim(0, 100)
    plt2.plot(YaxisH2, 'b^-', label='-----2 %')
    plt2.set_ylabel('----')
    plt2.ticklabel_format(useOffset=False)
    plt2.legend(loc='upper right')
    # Plot 3
    plt.subplot(gs[-1, 0])
    #plt.ylim([0, 100])
    plt.title('Temperatura')
    plt.grid(True)
    plt.ylabel('T /°C')
    plt.plot(Yaxistemp, 'ro-', label='temperatura')
    plt.legend(loc='upper left')
    # Plot 4
    plt.subplot(gs[-1, -1])
    #plt.ylim([0, 2000])
    plt.title('-----')
    plt.grid(True)
    plt.ylabel('-----')
    plt.plot(YaxisH2, 'ro-', label='-----')
    plt.legend(loc='upper left')



class LeituraRS:
    def __init__(self):

        self.leitura()


    def leitura(self, nome):

        development = 0
        coleta_ativa=0

        # coleta de dados via USB
        if (development == 0):

            # cria a instância arduino para coleta dos dados via USB
            arduino = serial.Serial()
            # arquivo com.txt contem a porta a ser usada (texto sem aspas)
            porta = open('com.txt', 'r', encoding="utf8")
            Nporta = porta.readline()
            print(Nporta)
            #
            # configura a porta serial
            arduino.port = Nporta
            arduino.baudrate = 9600
            arduino.timeout = 10
            arduino.open()

            if arduino.isOpen():
                try:
                    print("1a linha: ",arduino.readline())
                except Exception:
                    print("error open serial port: ")
                    exit()

            Raw_list=[]
            saida_dado= []
            espera=1
            epa=0
            while (espera == 1):
                dado = str(arduino.readline())
                # identifica a mensagem para iniciar
                if (dado.find("Pressione")!=-1):       # 2: posição 1a ocorrência raw:"b'Pressione bot\xc3\xa3o para iniciar\r\n' 2"
                    print('PRESSIONE O BOTÃO PARA INICIAR A COLETA')
                    if (epa==0):
                        Tela_H2.showinfo("ATENÇÃO", "PRESSIONE O BOTÃO PARA INICIAR A COLETA")
                        epa=1
                    #Tela_H2.Tela.texto1 = Tela_H2.tk.Label(self.caixa1, text='PRESSIONE ALGUMA TECLA PARA INICIAR A COLETA')
                    #Tela_H2.Tela.texto1.grid(column=0, row=8)
                    #Tela_H2.Tela.texto3 = Tela_H2.tk.Label(self.caixa1, text='PRESSIONE ALGUMA TECLA PARA INICIAR A COLETA')  #
                    #Tela_H2.Tela.texto3.grid(column=0, row=7)

                elif dado.find("alimenta")==11:    #b'bomba de alimenta\xc3\xa7\xc3\xa3o ligada\r\n' -1
                     coleta_ativa=1
                     fora = str(arduino.readline())  #lê uma linha que não tem nada.
                     Tela_H2.Tela.texto3 = Tela_H2.tk.Label(self.caixa1, text='Iniciando a leitura de dados')  #
                     Tela_H2.Tela.texto3.grid(column=1, row=7)
                     espera = 0

            tempo_inicio = time.time()

            while (coleta_ativa==1):
                dado = str(arduino.readline())
                if dado.find("Desligando") == 2:
                    self.desligando(arduino,Raw_list,saida_dado)

                # converte a string em uma lista, usando o separador \t
                Lista_Dado=dado.split('\\t')
                #verificar a necessidade do \n (new line)
                Raw_list.append(dado)

                excluido="b'"
                temperatura = float(Lista_Dado[0].replace(excluido,""))
                pressao=float(Lista_Dado[1])
                #remove \\r\\n' do sensor H2
                excluido="\\r\\n'"
                H2=float(Lista_Dado[3].replace(excluido,""))
                    #
                tempo= time.time()-tempo_inicio
                saida_dado.append([tempo,temperatura, pressao, H2])

                #
                Yaxistemp.append(temperatura)
                Yaxispres.append(pressao)
                YaxisH2.append(H2)
                plt.ion()
                cnt = 0
                #
                drawnow(makeFig)
                plt.pause(.000005)
                cnt = cnt + 1
                if (cnt > 50):
                    df.pop(0)
                #
                #
                #


                Tela_H2.Tela.texto1 = Tela_H2.tk.Label(self.caixa1, text=dado)
                Tela_H2.Tela.texto1.grid(column=0, row=8)
