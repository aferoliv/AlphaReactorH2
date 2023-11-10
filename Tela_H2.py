from pathlib import Path
import pandas as pd
# biblioteca sistema operacional
import os
# biblioteca interface com usuário
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec   # atualiza os gráficos na mesma janela
import array as array
# biblioteca criada para esse projeto
import LeituraUSB





## Classe da Interface com Usuário
class Tela(ttk.Frame):
    def __init__(self, master):
        #
        # ttk.Frame.__init__(self, master)
        self.Yaxis = array.array('f')
        self.inicio_coleta=0
        self.master = master
        self.title = "AlphaH2 Reactor - V.0"
        #
        # define tamanho da janela_
        #
        self.master.geometry('600x150')
        #
        # Botões e Texto no MasterFrame
        #
        self.caixa1 = tk.Frame(master, borderwidth=2, relief='raised')
        self.caixa1.grid(column=1, row=2)
        self.texto1 = tk.Label(self.caixa1, text='---------AlphaH2 Reactor V1.0-----------')
        self.texto1.grid(column=0, row=1)
        self.texto2 = tk.Label(self.caixa1, text='Nome do arquivo ')  # a ser criado - sem extensão')
        self.texto2.grid(column=0, row=3)
        self.texto3 = tk.Label(self.caixa1,text='')  #
        self.texto3.grid(column=0, row=7)

        self.nome = tk.Entry(self.caixa1)
        self.nome.grid(column=1, row=3)
        self.botaoSair = tk.Button(self.caixa1, text='     Sair    ', command=master.destroy)
        self.botaoSair.grid(column=3, row=6)
        self.botaoLeitura = tk.Button(self.caixa1, text='  Obter Dados   ', command=self.leitura)
        self.botaoLeitura.grid(column=1, row=6)
        self.botaoDiretorio = tk.Button(self.caixa1, text=' Selecionar Diretório  ', command=self.diretorio)
        self.botaoDiretorio.grid(column=2, row=6)
        #
        self.master.mainloop()
        #

    def diretorio(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        global folder_path
        filename = filedialog.askdirectory()
        folder_path.set(filename)
        # definir folder_path como diretorio ativo
        sourcePath = folder_path.get()
        os.chdir(sourcePath)  # Provide the path here
        #print(filename)

    def popup_showinfo(self):
        #
        #  Tratamento de Erro:
        #print('chegou em popup_showinfo')
        showinfo("ATENÇÃO", "Definir o nome do arquivo para armazenar o espectro!!")

    def desligando(self,arduino,Raw_list,saida_dado):
        development = 1
        print("-----coleta finalizada-----")
        arduino.close()
        #
        # tratar e salvar dados
        #
        nome_arquivo = self.nome.get()
        #
        # Salvar arquivo raw em .txt
        #
        arquivo = open(f"{nome_arquivo}-raw.txt", 'w')
        arquivo.writelines(Raw_list)
        #
        # Salvar arquivo com dados tratados em .xlsx
        #
        df = pd.DataFrame(saida_dado)
        df.rename(columns={0: 'tempo', 1: 'temperatura', 2: 'pressao', 3: 'H2'}, inplace=True)
        df.to_excel(f"{nome_arquivo}.xlsx")

        arquivo.close()
        Tela.texto1 = tk.Label(self.caixa1, text='-------COLETA REALIZADA---------')
        Tela.texto1.grid(column=2, row=4)

    def leitura(self):
        #
        nome_arquivo = self.nome.get()
        nome_completo=nome_arquivo+'.xlsx'
        #print(Path.cwd())
        if (Path(nome_completo).exists() and nome_arquivo != ''):
            showinfo("ATENÇÃO", "Esse nome já existe!!")
            #print("EPA")
        #
        # avalia erros associados ao nome do arquivo
        if (nome_arquivo == ''):
            #print("sem nome do arquivo")
            showinfo("ATENÇÃO", "Definir o nome do arquivo para armazenar o espectro!!")
            # self.popup_showinfo()
            return
        #print(nome_arquivo)
        inicio_coleta=1

        LeituraUSB.LeituraRS.leitura(self, nome_arquivo)







if __name__ == '__main__':
    window = tk.Tk()
    folder_path = tk.StringVar()
    app = Tela(window)
