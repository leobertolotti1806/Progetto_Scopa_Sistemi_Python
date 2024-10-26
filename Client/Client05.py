# Esercizio 5 - Chat Multipla

import socket
import threading

import tkinter 
from tkinter import *
from tkinter import font
from tkinter import ttk

import json

# Funzione per convertire un oggetto in una stringa
def oggetto_a_stringa(obj):
    try:
        # Converte l'oggetto in una stringa JSON
        stringa_json = json.dumps(obj)
        return stringa_json
    except (TypeError, ValueError) as e:
        print(f"Errore nella conversione dell'oggetto in stringa: {e}")
        return None

# Funzione per convertire una stringa in un oggetto
def stringa_a_oggetto(stringa):
    try:
        # Converte la stringa JSON in un oggetto Python
        obj = json.loads(stringa)
        return obj
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Errore nella conversione della stringa in oggetto: {e}")
        return None

Host = "172.27.128.1"
Porta = 9999

Indirizzo = (Host, Porta)
Codifica = "utf-8"

qta1024 = 1024
qta2048 = 2048

# Creo il mio Nuovo Socket CLIENT
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(Indirizzo)

# Gestisco la GUI Client
class clsGrafica:
    # Costruttore
    def __init__(self):
        
        self.Form = Tk()
        self.Form.withdraw()
        
        # Imposto il Nome del Client
        self.FormNome = Toplevel()
        
        # Imposto il Titolo 
        self.FormNome.title("Chat Multipla")
        self.FormNome.resizable(width=False, height=False)
        self.FormNome.configure(width=400, height=300)
        
        # Imposto LABEL
        self.label1 = Label(self.FormNome,
                            text="Inserisci il tuo Nome",
                            justify=CENTER,
                            font="Helvetica 14 bold")
        self.label1.place(relheight=0.15, relx=0.2,rely=0.07)
        
        # Imposto LABEL - NOME
        self.lblNome = Label(self.FormNome,
                            text="Nome: ",
                            font="Helvetica 12")
        self.lblNome.place(relheight=0.2, relx=0.1,rely=0.2)
        
        # Imposto INPUT - NOME
        self.txtNome = Entry(self.FormNome, font="Helvetica 12")
        self.txtNome.place(relwidth=0.4, relheight=0.12, relx=0.35,rely=0.2)            
        self.txtNome.focus()
        
        # Inposto il BOTTONE
        self.btnConferma = Button(self.FormNome,
                                  text="Conferma",
                                  font="Helvetica 14",
                                  command=lambda: self.sendMessaggio(self.txtNome.get()))
        self.btnConferma.place(relx=0.4, rely=0.55)
        self.Form.mainloop()
        

    # Funzione per Inviare il Messaggio Tramite un Traed
    def sendMessaggio(self, msg):
        treadRcv = threading.Thread(target=self.receive)
        treadRcv.start()
    
        treadSnd = threading.Thread(target=self.sendMsgToServer)
        treadSnd.start()
        
    def inviaJSON(self, client, messaggio):
        messaggio = oggetto_a_stringa(messaggio)
        
        client.send(messaggio.encode())
        

    # Funzione per la Ricezione dei Messaggi dal SERVER
    def receive(self):
        while True:
            try:
                msgServer = client.recv(qta1024).decode(Codifica)
                print(msgServer)
                    
            except:        
                print("Errore Generico !!!")
                client.close()
                break
            
    def sendMsgToServer(self):
        nome = self.txtNome.get()
        
        msg = {
            "nome" : nome,
            "cod": 1
        }
        self.inviaJSON(client, msg)

# Esegue la clsGrafica
grafica = clsGrafica()