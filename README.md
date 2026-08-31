# Progetto-Robotica
Progetto di robotica.

> Richiesta:

>1 Modello:

Si modelli, in Godot, un multirotore e si scelgano a piacere i dati di massa e di attrito. Si consideri l’ambiente caratterizzato dalla presenza di 5 oggetti posizionati in modo random tra 20 possibili posizioni note.  
 >2 Controllo:

Usando la comunicazione via socket/DDS, si implementino in Python gli algoritmi di controllo del multirotore scegliendo a piacere i parametri di velocita, accelerazione e saturazione. In particolare si realizzino i controlli in velocita e posizione. Si tarino opportunamente i controllori e si producano i grafici per dimostrare la corretta taratura.  
 > 3 Path Planning:  

Si generi, all’avvio, un grafo prefissato che include le 20 possibili posizioni, piu’ una posizione di partenzascelta a piacere. 
    Si faccia effettuare al multirotore questa sequenza di azioni:    
          &nbsp;1. Decollo e posizionamento ad una z specifica;  
          &nbsp;2. Raggiungimento della posizione i-esima dove e’ posizionato uno dei 5 oggetti usando la navigazione lungo in grafo e l’algoritmo di percorso minimo;  
          &nbsp;3. Cattura dell’oggetto (la cattura va simulata rimuovendo l’oggetto dalla scena);  
          &nbsp;4. Trasporto dell’oggetto alla posizione di partenza;  
          &nbsp;5. Rilascio dell’oggetto a terra (simulato);  
          &nbsp;6. Restart dal punto 1.  
