# Esercizio 5 - Chat Multipla
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

import socket
import threading

Host = socket.gethostbyname(socket.gethostname())
Porta = 9999

Indirizzo = (Host, Porta)
Codifica = "utf-8"

qta1024 = 1024
qta2048 = 2048

# Lista dei CLIENT
clients, nomes = [], []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Assegno l'Indirizzo del SERVER al Socket
server.bind(Indirizzo)

def riceviJson(conn):
    obj = conn.recv(qta1024).decode(Codifica)
    return stringa_a_oggetto(obj)
    
    

# Avvio il SERVER
def avviaServer():
    print("[SERVER] avviato su " , Indirizzo)
    
    # Imposto il SERVER in ascolte delle eventuali Connessioni
    server.listen()
    
    while True:
        
        # Accetto la Connessione
        #  ==> restituiosco al CLIENT una Nuova Connessione ad cui viene associtao
        conn, addr = server.accept()
        
        # Recupero la "Quantità" di Bytes inviata dal Cliente
        nome = riceviJson(conn)
        """ nome = conn.recv(qta1024).decode(Codifica)
        nome = stringa_a_oggetto(nome) """
        print(nome)
        nomes.append(nome)
        clients.append(conn)
        
        print(f"Nome : {nome}")
        
        # Invio un Messaggio in Broadcast per il Nuovo CLIENT
        messaggioBroadcast(f"{nome} si è aggiunto alla CHAT !!!".encode(Codifica))
        
        conn.send("Connessione alla Chat evvenuta con Successo !!!".encode(Codifica))
        
        # Avvio un Nuovo THREAD per la gestione del Singolo CLIENT
        thread = threading.Thread(target=messaggioInArrivo, args=(conn, addr))
        thread.start()
        
        print(f"Connessioni Attive [{threading.activeCount()-1}]")
        
        
# Metodo per Gestire i Messaggi in Arrivo dal CLIENT
def messaggioInArrivo(conn, addr):

    print(f"Nuova Connessione {addr}")
    connesso = True
    
    while connesso:
        # Ricezione del Messaggio dal CLIENT
        msgClient = conn.recv(qta1024)
        print(msgClient)
        # Inoltro il Messaggio in Broadcast
        messaggioBroadcast(msgClient)
        
    # Chiudo la Connessione
    conn.Close()
        
# Metodo Invio Messaggio in Broadcast
def messaggioBroadcast(msgBytes):
    for client in clients:
        client.send(msgBytes)

# Richiamo l' Avvio del SERVER
avviaServer()