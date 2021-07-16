# Progetto di Programmazione di Reti a.a. 2020-21

## TRACCIA
**Traccia 2: Python Web Server**

Si immagini di dover realizzare un Web Server in Python per
una azienda ospedaliera. I requisiti del Web Server sono i
seguenti:
* Il web server deve consentire l’accesso a più utenti in contemporanea
* La pagina iniziale deve consentire di visualizzare la lista dei servizi erogati dall’azienda ospedaliera e per ogni servizio avere un link di riferimento ad una pagina dedicata.
* L’interruzione da tastiera (o da console) dell’esecuzione del web server deve essere opportunamente gestita in modo da liberare la risorsa socket.
* Nella pagina principale dovrà anche essere presente un link per il download di un file pdf da parte del browser
* Come requisito facoltativo si chiede di autenticare gli utenti nella fase iniziale della connessione.

## ISTRUZIONI
Una volta clonato il progetto, posizionarsi all’interno della directory principale e lanciare da console (raccomandato l’utilizzo di Anaconda Powershell Prompt”) il seguente comando:

`python .\spahiuWebServer.py port`

dove 'port' specifica il valore della porta da utilizzare, ad esempio 80. Nel caso non venga specificato questo valore, viene utilizzato il valore 8080 di default (in maniera analoga, se si vuole avere il codice a portata di mano, si può utilizzare direttamente la console di Spyder ricordandosi di utilizzare `%run` invece che `python`). <br/>Successivamente, sempre da linea di comando, bisogna autenticarsi inserendo 'admin' sia come username che come password ed infine, dal proprio motore di ricerca preferito, è sufficiente recarsi all’indirizzo `http://localhost:port/index.html` (dove ‘port’ è il valore inserito in precedenza) per poter navigare nel Web Server.<br/>
Per chiudere il server da linea di comando bisogna premere contemporaneamente Ctrl + C (combinazione di chiusura), come viene riportato anche da console subito dopo l'autenticazione.

All’interno del Web-Server è inoltre presente (come richiesto dai requisiti della traccia al punto 4), in fondo alla barra di navigazione, un pulsante etichettato come “Download info” il quale, una volta premuto, farà partire il download di un file PDF “info.pdf” contenente un’introduzione al Web Server ed ai relativi servizi offerti.

## DOWNLOAD
La relazione finale si può trovare all'interno della cartella [report](https://github.com/marsild/ProgettoReti-2021/tree/main/report).

## LICENZA
[MIT License](https://github.com/marsild/ProgettoReti-2021/blob/main/LICENSE)

## AUTORE
**Cognome e Nome**: Spahiu Marsild

**Matricola**: 916048

**Email**: marsild.spahiu@studio.unibo.it
