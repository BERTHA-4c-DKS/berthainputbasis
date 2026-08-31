import numpy as np
import sys
import math

# Set file di input
np.set_printoptions(formatter={'float': '{:.6f}'.format})
fnameinput='input.inp'

# Se manca l'argomento o chiedi aiuto, stampa le istruzioni ed esce
if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
    sys.exit("Uso: python script.py X<numero> o Y<numero>\nEsempi: python script.py X2.0 o python script.py Y1.7\nConsigliato: X[2-4] e Y[1.5-2.5]")

# uniforma scelta
scelta = sys.argv[1].upper()

# massimo momento angolare per il set di base generato (numeri pari)
MAX_L=6

# inizializzazione lista variabili
exp=[]
exp1=[]
nfunct=[]
nfunct1=[]
minmaxl=[]

#=========================================================================
#                LETTURA FILE INPUT
#=========================================================================
with open(fnameinput,'r') as f:
  #print(f.read())
  f.readline()
  #lettura tipo di input
  intype=int(f.readline())
  f.readline()
  #lettura numeri di centri nel sistema
  ncent=int(f.readline())
  coord=np.empty((ncent,3), dtype=float)
  iznuc=np.empty(ncent, dtype=int)
  amass=np.empty(ncent, dtype=float)
  lmaxx=np.empty(ncent, dtype=int)
  icrge=np.empty(ncent, dtype=int)
  #loop su ogni atomo del sistema
  for icent in range (ncent):
    f.readline()
    #lettura coordinate del sistema
    vec=f.readline().split()
    coord[icent,0]=float(vec[0])
    coord[icent,1]=float(vec[1])
    coord[icent,2]=float(vec[2])
    f.readline()
    #lettura Z, N, MAXL AND CHARGE FOR EACH CENTRE
    info=f.readline().split(',')
    iznuc[icent]=int(info[0])
    amass[icent]=float(info[1])
    lmaxx[icent]=int(info[2])
    icrge[icent]=int(info[3])
    f.readline()
    #loop per lettura set di base
    for l in range (lmaxx[icent]+1):
      #lettura numero di funzioni di base per ogni l
      nff=int(f.readline().split()[0])
      nfunct1.append(nff)
      for n in range (nff):
        #lettura esponenti
        exp1.append(float(f.readline()))
    exp.append(exp1)
    nfunct.append(nfunct1)
    exp1=[]
    nfunct1=[]

if scelta.startswith("X"):

  # Mappa l'input al numero
  try:
      ngen = float(scelta[1:])
  except ValueError:
      # Se dopo la X c'è del testo o niente (es. "X", "Xabc"), dà errore
      sys.exit(f"Errore: input non valido. Dopo la 'X' deve esserci un numero (es. X2, X3). Hai inserito: '{scelta}'")


  print('ABF generate con GEN-X'+str(ngen), file=sys.stderr)


  minmaxl1=[]
  LMAX=[]
  alpha0=[]
  beta=6-ngen
  overmin=[]
  overmax=[]

  #loop per tutti i parametri su ogni centro
  for icent in range (ncent):
    nstart=0
    for val in nfunct[icent]:
      cap=nstart+val
      #trova max e min exponente per ogni momento angolare
      minmaxl1.append(max(exp[icent][nstart:cap]))
      minmaxl1.append(min(exp[icent][nstart:cap]))
      nstart=cap
    minmaxl.append(minmaxl1)
    minmaxl1=[]
    #calcola Lmax per l'atomo
    LMAX.append(int(min(2*lmaxx[icent],MAX_L)))
    #calcola l'esponente di partenza per ABF
    alpha0.append(2*minmaxl[icent][2*lmaxx[icent]+1])
    #ricava il minimo e il massimo esponente di tutto il set di base principale
    overmin.append(min(minmaxl[icent]))
    overmax.append(max(minmaxl[icent]))

  alpha_up=alpha0.copy()
  alpha_down=alpha0.copy()

  n_alpha=[]

  # loop generazione l'esponente più grande e più piccolo
  for icent in range (ncent):
    n_alpha_temp=1
    while alpha_up[icent]<2*overmax[icent]:
    #calcola l'esponente più grande del ABF e il numero di esponenti
        alpha_up[icent]=alpha_up[icent]*beta
        n_alpha_temp=n_alpha_temp+1

    while alpha_down[icent]>2*overmin[icent]:
    #calcola l'esponente più piccolo del ABF e il numero di esponenti
        alpha_down[icent]=alpha_down[icent]/beta
        n_alpha_temp=n_alpha_temp+1

    n_alpha.append(n_alpha_temp)


  alpha=alpha_up.copy()
  alpha_list=[]
  # loop per generare tutti gli esponenti del set di base ausiliario
  for icent in range(ncent):
    alpha_list.append([alpha[icent] / (beta ** i) for i in range(n_alpha[icent])])

  basi_atomi_pruned = []

  for icent in range (ncent):

        
        basis_raw = {}
        idx = 0 
        
        # Iteriamo sulla lista nfunct che contiene il numero di funzioni per ogni 'l'
        # Es: se nfunct[icent] = [3, 2], avremo 3 funzioni di tipo s (l=0) e 2 di tipo p (l=1)
        for l, num_funzioni in enumerate(nfunct[icent]):
            if num_funzioni > 0:
                # "Affettiamo" (slicing) la lista piatta exp per estrarre solo gli 
                # esponenti relativi al momento angolare corrente 'l'
                basis_raw[l] = exp[icent][idx : idx + num_funzioni]
            
            # Aggiorniamo l'indice per far ripartire il taglio successivo dal punto giusto
            idx += num_funzioni
        # ====================================================================
        #                        ASSEGNAZIONE L MAX
        # ====================================================================
        edge = {}
        
        # calcolo dei limiti degli esponenti dal set di base principale
        for L in sorted(basis_raw.keys()):
            exps_L = basis_raw.get(L, [])
            if not exps_L:
                continue
            # minimo e massimo per un L sono definiti 2*min e 2*max degli esponenti originali per quel L corretti per beta
            edge[L] = (2.0 * min(exps_L) / beta, 2.0 * max(exps_L) * beta)

        # ordiniamo tutti gli esponenti unici rimasti dopo la generazione del set ausiliario
        reduced = sorted(alpha_list[icent], reverse=False)

        assigned = {}
        
        # Assegnazion L basata sui limiti originali per ogni momento angolare L
        for L in sorted(basis_raw.keys()):
            if L not in edge:
                continue

            limite_min, limite_max = edge[L]
            
            # Estraiamo dall'insieme degli esponenti prunati quelli che ricadono all'interno dell'intervallo per il momento angolar L
            pero = [val for val in reduced if round(limite_min, 10) < round(val, 10) < round(limite_max, 10)]
            
            # Propagazione verso il basso
            # Se un esponente è valido per L, viene assegnato anche a tutti i canali sottostanti (da 0 fino a 2*L)
            for channel in range(2 * L + 1):
                existing = assigned.get(channel, [])
                # unione esponenti non duplicati e ordinamento crescente
                assigned[channel] = sorted(set(existing + pero), reverse=False)

        # salvataggio dati per atomo corrente
        basi_atomi_pruned.append(assigned)
        #print(f"Atomo {icent+1}/{ncent}", file=sys.stderr)
        #print(basi_atomi_pruned[icent], file=sys.stderr)        



  print(ncent)
  for icent in range (ncent):
    print(coord[icent][0],coord[icent][1],coord[icent][2])
    print(n_alpha[icent])
    #partendo dall'esponente più grande generato precedentemente 
    for set in range (n_alpha[icent]):              #loop su ogni esponente del set di base ausiliario
      L_set=0                                       #variabile per tenere traccia del momento angolare massimo per ogni esponente del set di base ausiliario
      for l in range (lmaxx[icent]+1):              #loop su ogni momento angolare del set di base principale
        L=min(2*l,MAX_L)                                #il momento angolare massimo per ogni l è 2*l, ma non può superare 6
        alphamin=2*minmaxl[icent][2*l+1]/beta       #calcola l'esponente minimo per generare funzioni di momento angolare l
        alphamax=2*minmaxl[icent][2*l]*beta         #calcola l'esponente massimo per generare funzioni di momento angolare l
        if round(alphamin, 10) < round(alpha[icent], 10) < round(alphamax, 10):          #se l'esponente è compreso tra il minimo e il massimo del set di base principale, allora genero funzioni di momento angolare l
          L_set=max(L,L_set)                        #aggiorna il momento angolare massimo per ogni esponente del set di base ausiliario
      print(f'{alpha[icent]:15.8E}', L_set)   
      alpha[icent]=alpha[icent]/beta                #scalo l'esponente per generare il successivo

    

  #print("Coppie di valori di zeta max/min per ogni momento angolare del set di base (a coppie con l crescente, in serie per atomi della molecola) ")
  #print(minmaxl,"\n")
  #print("Esponenti massimi e minimi overall")
  #print(overmax,overmin,"\n")
  #print("Momento angolare massimo per le funzioni del set di base ausiliario per ogni atomo")
  #print(LMAX)

elif scelta.startswith("Y"):
    # Mappa l'input al numero
    try:
        THRESHOLD = float(scelta[1:])
    except ValueError:
        # Se dopo la Y c'è del testo o niente (es. "Y", "Xabc"), dà errore
        sys.exit(f"Errore: input non valido. Dopo la 'Y' deve esserci un numero (es. Y2.0, Y1.7). Hai inserito: '{scelta}'")

    print('ABF generate con GEN-Y'+str(THRESHOLD), file=sys.stderr)

    # Ordine per il pruning: False => partenza dal più piccolo, True => dal più grande.
    MINMAX = False

    # applica il threshold a tutti gli L
    config_soglie = {level: THRESHOLD for level in range(MAX_L + 1)}

    print(f"Avvio algoritmo di clustering con soglia {THRESHOLD}...",file=sys.stderr)

    # Variabile per immagazzinare il risultato finale
    basi_atomi_pruned = []

    # Loop principale per applicare l'algoritmo su ogni atomo
    for icent in range(ncent):
        basis_raw = {}
        idx = 0 
        
        # Iteriamo sulla lista nfunct che contiene il numero di funzioni per ogni 'l'
        # Es: se nfunct[icent] = [3, 2], avremo 3 funzioni di tipo s (l=0) e 2 di tipo p (l=1)
        for l, num_funzioni in enumerate(nfunct[icent]):
            if num_funzioni > 0:
                # "Affettiamo" (slicing) la lista piatta exp per estrarre solo gli 
                # esponenti relativi al momento angolare corrente 'l'
                basis_raw[l] = exp[icent][idx : idx + num_funzioni]
            
            # Aggiorniamo l'indice per far ripartire il taglio successivo dal punto giusto
            idx += num_funzioni

        # ====================================================================
        #                     GENERAZIONE BASE PRODOTTO 
        # ====================================================================
        prodotto_raw = {}
        
        # loop per calcolare tutti i prodotti (mu * nu) eseguito su tutti gli l
        for l_mu, exps_mu in basis_raw.items():
            for l_nu, exps_nu in basis_raw.items():
                # Calcolo dei limiti per il canale di Clebsch-Gordan
                l_sum = l_mu + l_nu
                l_diff = abs(l_mu - l_nu)

                # Generazione dei canali di momento angolare L del prodotto
                for L in range(l_diff, l_sum + 1):
                    if L not in prodotto_raw:
                        prodotto_raw[L] = set() # set() per evitare duplicati esatti

                    # Calcolo del fattore di scala basato sulle funzioni Gamma
                    # F = [ Gamma(l_sum + 1.5)*Gamma(L + 2.0) / (Gamma(L + 1.5)*Gamma(l_sum + 2.0)) ]^2
                    num = math.gamma(l_sum + 1.5) * math.gamma(L + 2.0)
                    den = math.gamma(L + 1.5) * math.gamma(l_sum + 2.0)
                    fattore_scala = (num / den) ** 2

                    # Doppio ciclo per combinare tutti gli esponenti dei due set
                    for a_mu in exps_mu:
                        for a_nu in exps_nu:
                            # L'esponente del prodotto Gaussiano per fattore di scala
                            alpha_effettivo = (a_mu + a_nu) * fattore_scala
                            
                            # arrotondamento e aggiunta prodotti al momento angolare L
                            prodotto_raw[L].add(round(alpha_effettivo, 10))

        # ====================================================================
        #                     PRUNING A SOGLIA A CASCATA
        # ====================================================================
        # Prendiamo tutti i canali L generati e li ordiniamo in modo decrescente
        # per attuare un pruning top-down (dal momento angolare più alto al più basso)
        L_ordinati = sorted(prodotto_raw.keys(), reverse=True)
        basis_pruned = {}
        esponenti_ereditati = []
        
        # Filtriamo per tenere solo i canali L pari 
        L_ordinati = list(filter(lambda x: x % 2 == 0, L_ordinati))

        for l in L_ordinati:
            # Ordiniamo gli esponenti grezzi del livello 'l'.
            # MINMAX definisce la direzione: False = dal più piccolo al più grande.
            raw_l = sorted(list(prodotto_raw[l]), reverse=MINMAX)
            if not raw_l:
                continue

            # Otteniamo il valore di soglia per questo specifico 'l' oppure il default 2.0
            ratio_soglia = config_soglie.get(l, 2.0)
            
            # La distanza da superare per non collassare è il logaritmo naturale della soglia:
            # $\Delta = \ln(ratio\_soglia)$
            distanza_log_soglia = math.log(ratio_soglia)
            
            # Inizializziamo i centri scelti ereditando quelli del livello 'l' superiore
            scelti = list(esponenti_ereditati)

            # Scansioniamo ogni esponente generato dal prodotto completo del set di base
            for val in raw_l:
                if not scelti:
                    # Se non ci sono ancora centri, il primo esponente fonda il primo centro
                    scelti.append(val)
                else:
                    # Calcoliamo la distanza logaritmica minima tra l'esponente analizzato 'val'
                    # e tutti i centri 'c' già consolidati in 'scelti'
                    dist_min = min([abs(math.log(val) - math.log(c)) for c in scelti])
                    
                    # Se l'esponente è abbastanza lontano da tutti i centri esistenti, 
                    # non collassa e diventa esso stesso un nuovo centro indipendente
                    if dist_min > distanza_log_soglia:
                        scelti.append(val)

            # ordine esponenti collassati per il canale 'l'
            scelti = sorted(scelti, reverse=MINMAX)
            basis_pruned[l] = scelti
            
            # passa il set prunato/contratto come base di partenza per il livello sottostante (l-2)
            esponenti_ereditati = scelti

        # ====================================================================
        #                        ASSEGNAZIONE L MAX
        # ====================================================================
        edge = {}
        
        # calcolo dei limiti degli esponenti dal set di base principale
        for L in sorted(basis_raw.keys()):
            exps_L = basis_raw.get(L, [])
            if not exps_L:
                continue
            # minimo e massimo per un L sono definiti 2*min e 2*max degli esponenti originali per quel L
            edge[L] = (2.0 * min(exps_L), 2.0 * max(exps_L))

        # Raccogliamo e ordiniamo tutti gli esponenti unici rimasti dopo la riduzione 
        insieme_unici = {float(val) for exps in basis_pruned.values() for val in exps}
        reduced = sorted(insieme_unici, reverse=False)

        assigned = {}
        
        # Assegnazion L basata sui limiti originali per ogni momento angolare L
        for L in sorted(basis_raw.keys()):
            if L not in edge:
                continue

            limite_min, limite_max = edge[L]
            
            # Estraiamo dall'insieme degli esponenti prunati quelli che ricadono all'interno dell'intervallo per il momento angolar L
            pero = [val for val in reduced if round(limite_min, 10) <= round(val, 10) <= round(limite_max, 10)]

            # Propagazione verso il basso
            # Se un esponente è valido per L, viene assegnato anche a tutti i canali sottostanti (da 0 fino a 2*L)
            for channel in range(2 * L + 1):
                existing = assigned.get(channel, [])
                # unione esponenti non duplicati e ordinamento crescente
                assigned[channel] = sorted(set(existing + pero), reverse=False)

        # salvataggio dati per atomo corrente
        basi_atomi_pruned.append(assigned)
        #print(f"Atomo {icent+1}/{ncent}", file=sys.stderr)
        #print(basi_atomi_pruned[icent], file=sys.stderr)        
        #for L in sorted(basi_atomi_pruned[icent].keys(), reverse=True):
        #    print(f"  L={L}: {basi_atomi_pruned[icent][L]}", file=sys.stderr)



    # ====================================================================
    #            STAMPA SET GENERATO NEL FORMATO fitt2.inp
    # ====================================================================

    # stampa numero atomi sistema
    print(ncent)
    for icent in range(ncent):
        # stampa coordinate
        print(coord[icent][0], coord[icent][1], coord[icent][2])
        # stampa esponenti unici con L associato
        esponenti_unici = {}
        for L in sorted(basi_atomi_pruned[icent].keys()):
            for val in basi_atomi_pruned[icent].get(L, []):
                if val not in esponenti_unici or int(L) > esponenti_unici[val]:
                    esponenti_unici[val] = int(L)
                    
        entries = sorted(esponenti_unici.items(), key=lambda item: item[0], reverse=True)
        
        # stampa numero di esponenti e esponenti con L
        print(len(entries))
        for val, L in entries:
            print(f"{val:15.8E} {L}")

        

else:
    sys.exit(f"Errore: l'opzione '{scelta}' non è valida. Usa opzioni che iniziano per X o Y.\nPer aiuto: python script.py -h")




def plot_basis(basi_atomi):
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    for icent in range(ncent):
        #print(f"Atomo {icent+1}/{ncent}", file=sys.stderr)
        #print(basi_atomi[icent], file=sys.stderr)
        #for L in basi_atomi[icent].keys():
        #    print(f"L={L} : {basi_atomi[icent][L]}", file=sys.stderr)
        n_subplot=len(basi_atomi[icent].keys())
        fig, axes = plt.subplots(nrows=n_subplot, sharex=True, figsize=(12, 2.5 * n_subplot))
        if n_subplot == 1:
            axes = [axes]
        fig.subplots_adjust(hspace=0.08)
        livelli_ordinati = sorted(list(basi_atomi[icent].keys()), reverse=True)
        for ax, L in zip(axes, livelli_ordinati):
            esponenti = basi_atomi[icent][L]

            if not esponenti:
                continue # Se un livello è vuoto, salta al prossimo

            # Calcolo il logaritmo naturale per l'asse X
            exp_log = np.log(esponenti)

            # Disegno le linee verticali per ogni esponente
            ax.vlines(x=exp_log, ymin=1.0, ymax=2.0, 
                      color='navy', linewidth=1.5, alpha=0.8)

            # Aggiungo il numero di esponenti a destra del grafico
            ax.text(1.02, 0.5, f"n={len(esponenti)}", transform=ax.transAxes,
                    color='navy', va='center', fontsize=10, fontweight='bold')

            # Formattazione asse Y
            ax.set_ylabel(f"$L={L}$", fontsize=14, rotation=0, labelpad=25, va='center')
            ax.set_yticks([]) 
            ax.set_ylim(0, 3.0)
            ax.grid(True, axis='x', linestyle=':', alpha=0.6)

        # Asse X
        axes[-1].set_xlabel(r"$\ln(\alpha)$", fontsize=12, fontweight='bold')

        # Salvataggio plot per ogni atomo
        fig.suptitle(f"Auxiliary basis set {scelta} - Atom {icent+1}", fontsize=14, fontweight='bold', y=1.02)
        nome_file = f'atomo_{icent+1}_GEN{scelta}_plot.png'
        fig.savefig(nome_file, bbox_inches='tight', dpi=300)
        
        # chiusura figura 
        plt.close(fig)


plot_basis(basi_atomi_pruned)
