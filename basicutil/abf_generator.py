import numpy as np
import sys


np.set_printoptions(formatter={'float': '{:.6f}'.format})
fnameinput='input.inp'

#scelta generazione GEN-Xngen
#ngen=int(input("Scegliere generazione (2-4) GEN-X: "))

ngen=int(sys.argv[1])
#MAXXL_deMon=6


print('ABF generate con GEN-X'+str(ngen), file=sys.stderr)

exp=[]
exp1=[]
nfunct=[]
nfunct1=[]
minmaxl=[]



# LETTURA FILE INPUT
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
 LMAX.append(int(min(2*lmaxx[icent],6)))
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
print(ncent)
for icent in range (ncent):
  print(coord[icent][0],coord[icent][1],coord[icent][2])
  print(n_alpha[icent])
  #partendo dall'esponente più grande generato precedentemente 
  for set in range (n_alpha[icent]):              #loop su ogni esponente del set di base ausiliario
    L_set=0                                       #variabile per tenere traccia del momento angolare massimo per ogni esponente del set di base ausiliario
    for l in range (lmaxx[icent]+1):              #loop su ogni momento angolare del set di base principale
      L=min(2*l,6)                                #il momento angolare massimo per ogni l è 2*l, ma non può superare 6
      alphamin=2*minmaxl[icent][2*l+1]/beta       #calcola l'esponente minimo per generare funzioni di momento angolare l
      alphamax=2*minmaxl[icent][2*l]*beta         #calcola l'esponente massimo per generare funzioni di momento angolare l
      if round(alphamin, 10) < round(alpha[icent], 10) < round(alphamax, 10):          #se l'esponente è compreso tra il minimo e il massimo del set di base principale, allora genero funzioni di momento angolare l
        L_set=max(L,L_set)                        #aggiorna il momento angolare massimo per ogni esponente del set di base ausiliario
    print(f'{alpha[icent]:.6f}', L_set)   
    alpha[icent]=alpha[icent]/beta                #scalo l'esponente per generare il successivo


#print("Coppie di valori di zeta max/min per ogni momento angolare del set di base (a coppie con l crescente, in serie per atomi della molecola) ")
#print(minmaxl,"\n")
#print("Esponenti massimi e minimi overall")
#print(overmax,overmin,"\n")
#print("Momento angolare massimo per le funzioni del set di base ausiliario per ogni atomo")
#print(LMAX)

