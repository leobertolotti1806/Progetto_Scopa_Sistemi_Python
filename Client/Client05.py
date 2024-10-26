import socket
import threading
import tkinter 
from tkinter import *
from tkinter import font
from tkinter import ttk

import json

# DA OGGETTO A STRINGA
def stringifyObject(obj):
    try:
        stringa_json = json.dumps(obj)
        return stringa_json
    except (TypeError, ValueError) as e:
        print(f"Errore nella conversione dell'oggetto in stringa: {e}")
        return None

def parseObject(stringa):
    try:
        obj = json.loads(stringa)
        return obj
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Errore nella conversione della stringa in oggetto: {e}")
        return None

def riceviJson(qta = 1024):
    return parseObject(client.recv(qta).decode("utf-8"))

def inviaJSON(messaggio):
    client.send(stringifyObject(messaggio).encode())

#Host = "172.27.128.1" MAXWELL PC LEO
#Host = "192.168.178.24" PC LEO CASA
Host = "192.168.178.24"
Host = socket.gethostbyname(socket.gethostname())
Porta = 9999

Indirizzo = (Host, Porta)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
try:
    # Prova a connettersi al server
    client.connect(Indirizzo)
except socket.error as e:
    # Gestisce errori di connessione
    print(f"Errore di connessione al server: {e}")
    client.close()


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
        

    # Funzione per la Ricezione dei Messaggi dal SERVER
    def receive(self):
        while True:
            try:
                msgServer = client.recv(1024).decode("utf-8")
                msgServer = riceviJson(client)
                print(msgServer)
                    
            except:        
                print("Errore Generico !!!")
                client.close()
                break
            
    def sendMsgToServer(self):
        nome = self.txtNome.get()
        
        msg = {
            "nickname" : nome,
            "host": socket.gethostbyname(socket.gethostname())
        }

        inviaJSON(msg)

# Esegue la clsGrafica
grafica = clsGrafica()