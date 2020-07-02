Installare tutte le dipendenze:
pip install -r requirements.txt7
pip install --upgrade google-cloud-storage

Se da come errore 'Error: pg_config executable not found.' allora bisogna:
sudo apt-get install libpq-dev
pip install psycopg2

Per poter usare Tint è necessario avere installato java:
apt-get install default-jdk

La prima volta di ogni sessione il programma farà partire il server Tint su 'http://localhost:8012/tint', per questo la
prima volta si vedono molti più log

Per poter usare le API di google bisogna avere il file 'client_secret.json' e specificare il percorso per trovarlo in
captionDownload = CaptionDownload('YoutubeAPI/client_secret.json')

Il programma può scaricare i sottotitoli da un video di youtube, per farlo è necessario specificare l'id del video in
main.py alla voce 'videoID', se nessun id è stato specificato il programma userà il file specificato in 'captionFileName'.
Questo è stato fatto per poter testare più volte il programma con configurazioni diverse senza dover scaricare ogni volta i sottotitoli.

Si possono specificare i tag grammaticali di intesse specificandoli in 'posTag', ponendolo uguale a 'posTag = ['']' userà
tutti i tag possibili.
Non è necessario specificare postTag nelle funzioni, se verrà omesso userà tutti i tag come default.
La lista completa dei tag utilizzabili la si può trovare a 'http://medialab.di.unipi.it/wiki/POS_and_morphology'
Si possono usare tag diversi per le diverse funzioni, basta specificarli separatamente

Tutti i file generati verranno salvati nella cartella Outputs, sono tutti nel formato csv e come separatore si è usato
il punto e virgola ;
I sottotitoli scaricati originariamente da youtube sono in formato originale vtt, vengono "puliti" e viene quindi generato
il file caption.txt che ha un indentazione comoda per il programma.

Tutti i file generati vengono sostituiti nel caso esistessero già, se la cartella Output non ci fosse viene generata automaticamente
Per ogni funzione si può specificare il nome del file che deve generare, ogni volta si utilizza la funzione 'generateFile()'
se non si passano argomenti darà un nome preimpostato al file, altrimenti il nome specificato.
Esempio:
tokenizer.generateFile() genera come impostazione predefinita 'token.csv'
tokenizer.generateFile('test') genera 'test.csv' con lo stesso contenuto