import json
import socket
import threading

def inviaJSON(client, messaggio):
    messaggio = stringifyObject(messaggio)
    client.send(messaggio.encode())

# DA OGGETTO A STRINGA
def stringifyObject(obj):
    try:
        # Converte l'oggetto in una stringa JSON
        stringa_json = json.dumps(obj)
        return stringa_json
    except (TypeError, ValueError) as e:
        print(f"Errore nella conversione dell'oggetto in stringa: {e}")
        return None

# DA STRINGA A OGGETTO
def parseObject(stringa):
    try:
        # Converte la stringa JSON in un oggetto Python
        obj = json.loads(stringa)
        return obj
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Errore nella conversione della stringa in oggetto: {e}")
        return None

Host = socket.gethostbyname(socket.gethostname())
Porta = 9999
Indirizzo = (Host, Porta)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(Indirizzo)

# Lista dei CLIENT
clients = []


def riceviJson(client, qta = 1024):
    return parseObject(client.recv(qta).decode("utf-8"))


# Avvio il SERVER
def avviaServer():
    print("[SERVER] avviato su " , Indirizzo)
    
    # Imposto il SERVER in ascolte delle eventuali Connessioni
    server.listen()
    
    while True:
        
        # Accetto la Connessione
        #  ==> restituiosco al CLIENT una Nuova Connessione ad cui viene associtao
        client, addr = server.accept()
        
        nome = riceviJson(client)

        print(nome)
        clients.append(client)

        # Avvio un Nuovo THREAD per la gestione del Singolo CLIENT
        thread = threading.Thread(target=messaggioInArrivo, args=(client, addr, nome))
        thread.start()
        
        print(f"Connessioni Attive {threading.active_count() - 1}")
        
        
# Metodo per Gestire i Messaggi in Arrivo dal CLIENT
def messaggioInArrivo(client, addr, nome):

    print(f"Si è connesso {nome['nickname']} : {nome['host']}")
    connesso = True
    
    while connesso:

        # Ricezione del Messaggio dal CLIENT
        msgClient = client.recv(1024)

        # Inoltro il Messaggio in Broadcast
        # messaggioBroadcast(msgClient)
        
    # Chiudo la Connessione
    client.close()


# Richiamo l' Avvio del SERVER
avviaServer()