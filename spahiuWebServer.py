# -*- coding: utf-8 -*-
"""
Progetto di Programmazione di Reti a.a. 2020-21

Cognome e Nome: Spahiu Marsild
Matricola: 916048

Traccia 2: Python Web Server
"""

import sys
import signal
import http.server
import socketserver
import threading

#Gestire l'attesa senza busy waiting
waiting_refresh = threading.Event()

# Legge il numero di argomenti inseriti da linea di comando.
# Se è presente l'argomento 1, vuol dire che è stato inserito il valore della porta da utilizzare.
if sys.argv[1:]:
    try:
        port = int(sys.argv[1])
    except:
        print("Errore nell'inserimento della porta.")
        print("Porta inserita: " + sys.argv[1])
        print("Chiusura del programma.\n")
        sys.exit(0)
else: #Nel caso non venga specificato da linea di comando, viene utilizzato il valore di default.
    port = 8080
    
print('Porta inserita: {0}\n'.format(port))
print("Combinazione per interrompere da tastiera: Ctrl+C")

# classe che mantiene le funzioni di SimpleHTTPRequestHandler e implementa
# il metodo get nel caso in cui si voglia fare un refresh
class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        # Scrivo sul file AllRequestsGET le richieste dei client     
        with open("AllRequestsGET.txt", "a") as out:
            info = "GET request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n"
            out.write(str(info))
        if self.path == '/refresh':
            resfresh_contents()
            self.path = '/'
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
# ThreadingTCPServer per gestire più richieste
server = socketserver.ThreadingTCPServer(('127.0.0.1',port), ServerHandler)

# La composizione è la stessa per tutti i servizi:
# message = header_html + title + navigation_bar + end_page + footer_html
# la parte iniziale (header_html) è identica per tutti
header_html = """
<html>
    <head>
        <style>
            h1 {
                text-align: center;
                margin: 0;
                font-family: Monospace;
            }
            h2 {
                text-align: center;
                margin: 0;
                font-family: Monospace;
            }
            table {width:70%;}
            img {
                max-width:300;
                max-height:200px;
                width:auto;
            }
            td {width: 33%;}
            p {
                text-align:justify;
                font-family: Monospace;
                font-size: 20px;
            }
            td {
                padding: 20px;
                text-align: center;
            }
            .topnav {
  		        overflow: hidden;
  		        background-color: #F2F3F4;
  		    }
            .topnav a {
  		        float: left;
  		        color: #333;
  		        text-align: center;
  		        padding: 20px 16px;
  		        text-decoration: none;
  		        font-size: 17px;
  		    }        
  		    .topnav a:hover {
  		        background-color: #4CAF50;
  		        color: white;
  		    }        
  		    .topnav a.active {
  		        background-color: #ddd;
  		        color: black;
  		    }
        </style>
    </head>
    <body>
"""
# [message = header_html + title + navigation_bar + end_page + footer_html]
# la barra di navigazione (navigation_bar) è identica
navigation_bar = """
        <div class="topnav">
            <a class="active" href="http://127.0.0.1:{port}">Home</a>
            <a href="http://127.0.0.1:{port}/118.html">118</a>
            <a href="http://127.0.0.1:{port}/pronto-soccorso.html">Pronto soccorso</a>
            <a href="http://127.0.0.1:{port}/medici-famiglia.html">Medici e Pediatri di famiglia</a>
            <a href="http://127.0.0.1:{port}/guardia-medica.html">Guardia Medica (ex)</a>
            <a href="http://127.0.0.1:{port}/farmacie-turno.html">Farmacie di turno</a>
            <a href="http://127.0.0.1:{port}/FSE.html">FSE</a>
  		    <a href="http://127.0.0.1:{port}/refresh" style="float: right">Aggiorna contenuti</a>
            <a href="http://127.0.0.1:{port}/info.pdf" download="info.pdf" style="float: right">Download info</a>
            <a href="https://www.auslromagna.it/covid-19-aggiornamenti" style="float: right; font-family: Monospace; color: red;">COVID-19 &#129133</a>
  		</div>
        <table align="center">
""".format(port=port)

# [message = header_html + title + navigation_bar + end_page + footer_html]
# la parte finale (footer_html) è identica per tutti i giornali
footer_html= """
        </table>
    </body>
</html>
"""
# [message = header_html + title + navigation_bar + end_page + footer_html]
# Singole parti finali (end_page)

# (end_page) home:
end_page_index = """
		<form action="http://127.0.0.1:{port}/home" method="post" style="text-align: center;">
        <hr>
          <img src='resources/hospital.jpg'
          style="float:left; left:0px; top:0px; width:180px; height:90px; border:none;" />
          <img src='resources/hospital.jpg'
          style="float:right; right:0px; top:0px; width:180px; height:90px; border:none;" />
		  <h1><strong>Servizi Ospedalieri</strong></h1><br>
          <h2>Servizi AUSL della Romagna</h1><br>
          <hr>
          <p>L'Azienda Unit&agrave Sanitaria Locale della Romagna (<a href="https://www.auslromagna.it/">AUSL Romagna</a>), istituita con Legge regionale n. 22 del 21 novembre 2013,
          &egrave l'ente strumentale attraverso il quale la Regione assicura i livelli essenziali ed uniformi di assistenza dell'ambito territoriale della Romagna.
          L'Azienda &egrave dotata di personalit&agrave giuridica pubblica e di autonomia imprenditoriale ai sensi delle disposizioni legislative nazionali e regionali di regolamentazione del Servizio Sanitario Regionale.<br><br>
          Attraverso la barra di navigazione sovrastante, oppure attraverso i collegamenti riportati qui di seguito, potrai accedere ai principali servizi offerti. &Egrave anche possibile scaricare l'elenco di questi ultimi da "Download info" nella barra di navigazione.</p>
          <a href="http://127.0.0.1:{port}/118.html"><h2>Passa al servizio 118</a></h2>
          <a href="http://127.0.0.1:{port}/pronto-soccorso.html"><h2>Passa al servizio Pronto Soccorso</a></h2>
          <a href="http://127.0.0.1:{port}/medici-famiglia.html"><h2>Passa al servizio Medici e Pediatri di famiglia</a></h2>
          <a href="http://127.0.0.1:{port}/guardia-medica.html"><h2>Passa al servizio Continuit&agrave Assistenziale (Guardia Medica)</a></h2>
          <a href="http://127.0.0.1:{port}/farmacie-turno.html"><h2>Passa al servizio Farmacie di turno</a></h2>
          <a href="http://127.0.0.1:{port}/FSE.html"><h2>Passa al servizio FSE</a></h2><br>
          <hr>
          <p style="text-align: center; font-size: 15px"> Per qualsiasi informazione, dubbio o segnalazione riguardante i Servizi Ospedalieri Spahiu <a href="mailto:marsild.spahiu@studio.unibo.it">contattaci qui</a>.</p><br>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

# (end_page) 118:
end_page_118= """
		<form action="http://127.0.0.1:{port}/118.html" method="post" style="text-align: center;">
        <hr>
          <img src='resources/118.png'
          style="float:left; left:0px; top:0px; width:180px; height:90px; border:none;" />
          <img src='resources/118.png'
          style="float:right; right:0px; top:0px; width:180px; height:90px; border:none;" />
          <h1><strong>118 Emilia-Romagna</strong></h1><br>
          <h2>118 Emilia-Romagna Pronto Soccorso Emergenza</h1><br>
          <hr>
          <a href="https://www.118er.it/istruzioni.asp"><h1>ISTRUZIONI - QUANDO CHIAMARE E COSA DIRE</a></h1><br>
          <p><strong>Chi &egrave il 118:</strong> Il 118 &egrave un servizio pubblico e gratuito di pronto intervento sanitario, attivo 24 ore su 24, coordinato da una centrale operativa che gestisce tutte le chiamate per necessit&agrave urgenti e di emergenza sanitaria.
          <a href="https://www.118er.it/118.asp"> [+]</a></p><br>
          <a href="https://www.118er.it/"><h2>Raggiungi il sito ufficiale del 118</a></h2><br>
          <hr>
          <p style="text-align: center; font-size: 15px">Torna alla <a href="http://127.0.0.1:{port}">home</a>.</p><br>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

# (end_page) pronto soccorso:
end_page_pronto_soccorso= """
		<form action="http://127.0.0.1:{port}/pronto-soccorso" method="post" style="text-align: center;">
          <hr>
          <img src='resources/pronto_soccorso.png'
          style="float:left; left:0px; top:0px; width:90px; height:90px; border:none;" />
          <img src='resources/pronto_soccorso.png'
          style="float:right; right:0px; top:0px; width:90px; height:90px; border:none;" />
          <h1><strong>Pronto Soccorso</strong></h1><br>
          <h2>Pronto Soccorso e pronto intervento</h1><br>
          <hr>
          <a href="https://www.auslromagna.it/luoghi/pronto-soccorso"><h1>MAPPA DEI PUNTI DI PRONTO SOCCORSO E PRONTO INTERVENTO</a></h1><br>
          <p>Il servizio di Pronto Soccorso &egrave rivolto a persone che hanno di bisogno di cure urgenti.
          Per situazioni non urgenti &egrave opportuno rivolgersi direttamente al proprio <a href="http://127.0.0.1:{port}/medici-famiglia.html"> medico di famiglia</a> od al <a href="http://127.0.0.1:{port}/guardia-medica.html"> servizio sostitutivo di guardia medica</a>.</p><br>
          <a href="https://www.auslromagna.it/servizi/pronto-soccorso"><h2>Raggiungi il sito ufficiale del Pronto Soccorso</a></h2><br>
		  <hr>
          <p style="text-align: center; font-size: 15px">Torna alla <a href="http://127.0.0.1:{port}">home</a>.</p><br>
        </form>
		<br>
    </body>
</html>
""".format(port=port)

# (end_page) medici_famiglia:
end_page_medici_famiglia= """
		<form action="http://127.0.0.1:{port}/medici-famiglia.html" method="post" style="text-align: center;">
        <hr>
          <img src='resources/famiglia.jpg'
          style="float:left; left:0px; top:0px; width:150px; height:90px; border:none;" />
          <img src='resources/famiglia.jpg'
          style="float:right; right:0px; top:0px; width:150px; height:90px; border:none;" />
          <h1><strong>Medici e Pediatri di famiglia</strong></h1><br>
          <h2>Medici e Pediatri di famiglia in Romagna</h1><br>
          <hr>
          <p>Medico e pediatra di famiglia sono il primo riferimento per problemi di salute, per avere confronti e counselling. Alla base di ogni rapporto di collaborazione tra il medico e la famiglia ci deve essere naturalmente fiducia reciproca. La scelta del medico avviene contemporaneamente all'iscrizione al Servizio sanitario nazionale.</p><br>
          <a href="https://www.auslromagna.it/servizi/medici-famiglia"><h2>Raggiungi il sito ufficiale riguardante Medici e Pediatri di famiglia</a></h2><br>
		  <hr>
          <p style="text-align: center; font-size: 15px">Torna alla <a href="http://127.0.0.1:{port}">home</a>.</p><br>
        </form>
		<br>
    </body>
</html>
""".format(port=port)

# (end_page) guardia_medica:
end_page_guardia_medica= """
		<form action="http://127.0.0.1:{port}/guardia-medica.html" method="post" style="text-align: center;">
        <hr>
          <img src='resources/guardia-medica.jpg'
          style="float:left; left:0px; top:0px; width:90px; height:90px; border:none;" />
          <img src='resources/guardia-medica.jpg'
          style="float:right; right:0px; top:0px; width:90px; height:90px; border:none;" />
          <h1><strong>Continuit&agrave assistenziale</strong></h1><br>
          <h2>Servizio di Continuit&agrave assistenziale (ex Guardia medica)</h1><br>
          <hr>
          <a href="https://www.auslromagna.it/servizi/guardia-medica/mappa-ambulatori-continuita-assistenziale"><h1>MAPPA DEGLI AMBULATORI DI CONTINUIT&Agrave ASSISTENZIALE</a></h1><br>
          <p>&Egrave il servizio che, in assenza del medico di famiglia, garantisce l'assistenza medica di base per situazioni che rivestono carattere di non differibilit&agrave, cio&egrave per quei problemi sanitari per i quali non si pu&ograve aspettare fino all'apertura dell'ambulatorio del proprio medico curante o pediatra di libera scelta.<br><br>
          <strong>NUMERO TELEFONICO COMPETENTE</strong>: <br>
          <strong>Comprensorio di Forl&igrave</strong>: 800533118 
          <strong>Comprensorio di Cesena</strong>: 800050909 
          <strong>Comprensorio di Ravenna</strong>: 800244244 
          <strong>Comprensorio di Rimini</strong>: 0541787461
          </p><br>
          <a href="https://www.auslromagna.it/servizi/guardia-medica"><h2>Raggiungi il sito ufficiale del servizio di Continuit&agrave assistenziale</a></h2><br>
	      <hr>
          <p style="text-align: center; font-size: 15px">Torna alla <a href="http://127.0.0.1:{port}">home</a>.</p><br>	
        </form>
		<br>
    </body>
</html>
""".format(port=port)

# (end_page) farmacie_turno:
end_page_farmacie_turno= """
		<form action="http://127.0.0.1:{port}/farmacie-turno.html" method="post" style="text-align: center;">
        <hr>
          <img src='resources/farmacia.png'
          style="float:left; left:0px; top:0px; width:90px; height:90px; border:none;" />
          <img src='resources/farmacia.png'
          style="float:right; right:0px; top:0px; width:90px; height:90px; border:none;" />
          <h1><strong>Farmacie di turno</strong></h1><br>
          <h2>Farmacie di turno in Romagna</h1><br>
          <hr>
          <p>La Guardia Farmaceutica (Farmacia di Turno) &egrave un servizio che ogni farmacia aperta al pubblico deve fornire in base a una specifica Legge Regionale (n. 33 del 30 dicembre 2009).
          Tale servizio ha due caratteristiche fondamentali: la presenza e l'accessibilit&agrave su tutto il territorio e la disponibilit&agrave 24 ore su 24 per 365 giorni all'anno.
          Il servizio viene svolto da un farmacista nella farmacia di turno ed assicura la distribuzione dei farmaci durante gli orari di chiusura delle farmacie.
          Le farmacie di turno svolgono il servizio di norma fino alle ore 20.00 a battenti aperti e successivamente a battenti chiusi fino all'ora di apertura antimeridiana.</p><br>
          <a href="https://www.auslromagna.it/servizi/farmacie"><h2>Trova la farmacia di turno pi&ugrave vicina a te</a></h2><br>
		  <hr>
          <p style="text-align: center; font-size: 15px">Torna alla <a href="http://127.0.0.1:{port}">home</a>.</p><br>
        </form>
		<br>
    </body>
</html>
""".format(port=port)

# (end_page) FSE:
end_page_FSE= """
		<form action="http://127.0.0.1:{port}/FSE.html" method="post" style="text-align: center;">
        <hr>
          <img src='resources/fse.png'
          style="float:left; left:0px; top:0px; width:90px; height:90px; border:none;" />
          <img src='resources/fse.png'
          style="float:right; right:0px; top:0px; width:90px; height:90px; border:none;" />
          <h1><strong>FSE</strong></h1><br>
          <h2>Fascicolo Sanitario Elettronico</h1><br>
          <hr>
          <p>Il <a href="https://www.auslromagna.it/servizi-on-line/fse-fascicolo-sanitario-elettronico">Fascicolo Sanitario Elettronico (FSE)</a> consente l'archiviazione e la consultazione da pc e da smartphone dei propri dati e documenti di tipo sanitario e socio-sanitario, in forma riservata e protetta.
          Tramite il Fascicolo Sanitario Elettronico &egrave anche possibile ricevere i referti delle prestazioni sanitarie, evitando di recarsi agli sportelli per il ritiro del documento cartaceo.
          Inoltre, il cittadino pu&ograve arricchire il proprio FSE con dati e documenti medici in suo possesso - ad esempio appunti sulle cure, agenda degli appuntamenti sanitari, referti di strutture non convenzionate o rilasciati da altri specialisti - ed ha accesso ad ulteriori servizi online.
          Possono attivare il FSE tutte le persone maggiorenni iscritte al Servizio Sanitario Nazionale, che possono farlo anche per i figli minori.</p><br>
          <a href="https://support.fascicolo-sanitario.it/"><h2>Come attivare FSE</a></h2><br>
          <a href="https://www.fascicolo-sanitario.it/fse/;jsessionid=90F1C30D12B671EF7203450B71876F41?0"><h2>Accedi al tuo FSE</a></h2><br>
		  <hr>
          <p style="text-align: center; font-size: 15px">Torna alla <a href="http://127.0.0.1:{port}">home</a>.</p><br>
        </form>
		<br>
    </body>
</html>
""".format(port=port)

#metodo lanciato per la creazione delle pagine servizi
def create_page_servizio(title,file_html, end_page):
    f = open(file_html,'w', encoding="utf-8")
    try:
        message = header_html + title + navigation_bar + end_page + footer_html
    except:
        pass
    f.write(message)
    f.close()
    
#definisco il font da utilizzare nel titolo della pagina
intro_page = "<hr><h1 style='font-family: Trebuchet MS;'>";

#definisco il titolo di ciascuna scheda
bar_title_index = "<title>Servizi Ospedalieri</title>" + intro_page;
bar_title_118 = "<title>Servizi Ospedalieri - 118</title>" + intro_page;
bar_title_pronto_soccorso = "<title>Servizi Ospedalieri - Pronto Soccorso</title>" + intro_page;
bar_title_medici_famiglia = "<title>Servizi Ospedalieri - Medici e Pediatri di famiglia</title>" + intro_page;
bar_title_guardia_medica = "<title>Servizi Ospedalieri - Continuit&agrave assitenziale</title>" + intro_page;
bar_title_farmacie_turno = "<title>Servizi Ospedalieri - Farmacie di turno</title>" + intro_page;
bar_title_FSE = "<title>Servizi Ospedalieri - FSE</title>" + intro_page;


# creazione della pagina specifica del 118
def create_page_118():
    create_page_servizio(bar_title_118 + "118 Emilia-Romagna</h1><hr>"  , '118.html', end_page_118 )
    
# creazione della pagina specifica del pronto soccorso
def create_page_pronto_soccorso():
    create_page_servizio(bar_title_pronto_soccorso + "Pronto Soccorso</h1><hr>"  , 'pronto-soccorso.html', end_page_pronto_soccorso )
    
# creazione della pagina specifica dei medici di famiglia
def create_page_medici_famiglia():
    create_page_servizio(bar_title_medici_famiglia + "Medici e Pediatri di famiglia</h1><hr>"  , 'medici-famiglia.html', end_page_medici_famiglia )
    
# creazione della pagina specifica della guardia medica
def create_page_guardia_medica():
    create_page_servizio(bar_title_medici_famiglia + "Continuit&agrave assitenziale</h1><hr>"  , 'guardia-medica.html', end_page_guardia_medica )
    
# creazione della pagina specifica delle farmacie di turno
def create_page_farmacie_turno():
    create_page_servizio(bar_title_farmacie_turno + "Farmacie di turno</h1><hr>"  , 'farmacie-turno.html', end_page_farmacie_turno )

# creazione della pagina specifica del FSE
def create_page_FSE():
    create_page_servizio(bar_title_FSE + "FSE - Fascicolo Sanitario Elettronico</h1><hr>", 'FSE.html', end_page_FSE )
    
# creazione della pagina index.html (iniziale)
# contenente pagina principale del Azienda ospedaliera
def create_index_page():
    create_page_servizio(bar_title_index + "Servizi Ospedalieri Spahiu</h1><hr>", 'index.html', end_page_index )
    
# creo tutti i file utili per navigare.
def resfresh_contents():
    print("Aggiornamento contenuti...\n")
    create_index_page()
    create_page_118()
    create_page_pronto_soccorso()
    create_page_medici_famiglia()
    create_page_guardia_medica()
    create_page_farmacie_turno()
    create_page_FSE()
    print("Aggiornamento terminato.\n")
   
# lancio un thread che ogni 300 secondi (5 minuti) aggiorna i contenuti delle pagine     
def launch_thread_resfresh():
    t_refresh = threading.Thread(target=resfresh_contents())
    t_refresh.daemon = True
    t_refresh.start()
    
# definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
    print('Combinazione di interruzione (Ctrl+C) premuta: uscita dal server http.')
    try:
        if(server):
            server.server_close()
    finally:
        # fermo il thread del refresh senza busy waiting
        waiting_refresh.set()
        sys.exit(0)
      
# metodo che viene chiamato al "lancio" del server
def main():
    cond = True #variabile utilizzata come controllo del while. Finchè è true, continua a richiedere username e password
    while cond:
        try:
            username = input("Inserire l'username: ") #richiesto l'username da tastiera
            password = input("Inserire la password: ") #richiesta la password
        except: #Try ed Except nel caso, ad esempio, venisse premuto Ctrl + C durante l'inserimento delle credenziali
            print("\nErrore nell'inserimento delle credenziali.")
            print("Chiusura del programma.")
            server.server_close() #Per evitare errori al prossimo avvio
            sys.exit(0)
        if username != 'admin' or password != 'admin':
            print("\nUsername e/o password incorretta. Ritenta")
        else:
            cond = False #username e password inserite correttamente, variabile impostata a False per uscire dal while
    print("\nAccesso eseguito correttamente.\n")
    # lancio un thread che aggiorna ricorrentemente i contenuti
    launch_thread_resfresh()
    #Assicura che da tastiera usando la combinazione
    #di tasti Ctrl-C termini in modo pulito tutti i thread generati
    server.daemon_threads = True 
    #il Server acconsente al riutilizzo del socket anche se ancora non è stato
    #rilasciato quello precedente, andandolo a sovrascrivere
    server.allow_reuse_address = True  
    #interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
    signal.signal(signal.SIGINT, signal_handler)
    # cancella i dati get ogni volta che il server viene attivato
    f = open('AllRequestsGET.txt','w', encoding="utf-8")
    f.close()
    # entra nel loop infinito
    try:
        while True:
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

if __name__ == "__main__":
    main()
