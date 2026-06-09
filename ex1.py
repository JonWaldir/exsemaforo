import multiprocessing
import time
import random

posix : int  = 0
semaforo = None
semaforo_decola = None

def init( s , posi, sem_decola):
    global posix
    global semaforo
    global semaforo_decola
    semaforo_decola = sem_decola
    posix = posi
    semaforo = s

def initDecola(sem_decola):
    global semaforo_decola
    semaforo_decola = sem_decola

def aeronaves(id):
    global semaforo
    global posix
    global semaforo_decola
    
    #aguarda(id)
    time.sleep(1)
    with semaforo: 
        time.sleep(2)
        aguarda(id)
        time.sleep(2)
        with semaforo_decola:
            time.sleep(1)
            decola(id)

def aguarda(id):
    global posix
    posix.value +=1
    print(f"O aviao {id} que esta em {posix.value}° esta aguardando na area de decolagem")
    
    time.sleep(2)
    #with semaforo_decola:
     #   time.sleep(1)
      #  decola(id)

def decola(id):
    fase_manobra: int = 0
    fase_taxiar: int = 0
    fase_decolagem: int = 0
    fase_afastamento: int = 0

    fase_manobra = random.randint(300,700)
    fase_taxiar  = random.randint(500,1000)
    fase_decolagem = random.randint(600,800)
    fase_afastamento = random.randint(300 , 800)
    
    print(f"O aviao {id} esta decolando")
    
    direcao: int = 0
    direcao = random.randint(1,2)
    time.sleep(0.3)
    if (direcao == 1):
        print(f"O aviao {id} esta indo a direcao Sul")
    else:
        print(f"O aviao {id} esta indo a direcao Norte")
    time.sleep(0.5)
    
    # FASE 1
    print(f"{id} esta manobrando ")
    time.sleep(fase_manobra/1000.0)     
    # FASE 2
    print(f"{id} esta taxiando")
    time.sleep(fase_taxiar/1000.0) #

    # FASE 3 (C
    print(f"{id} esta decolando")
    time.sleep(fase_decolagem/1000.0) #

    # FASE 4
    print(f"{id} esta afastando-se ")
    time.sleep(fase_afastamento/1000.0) #
    

def main():
    i: int = 0
    proc: int = 0
    sem_aguarda = None
    proc = 12
    params = [0]*proc
    posi = multiprocessing.Value('i' , 0)
    sem_decola = None
    print("começara a decolagem")
    
    for i in range(12):
        params[i] = i
        
    with multiprocessing.Manager()as manager:
        
        sem_aguarda = manager.Semaphore(2) 
        sem_decola = manager.Semaphore(1)
        
        with multiprocessing.Pool(processes= 12, initializer=init, initargs=(sem_aguarda, posi,sem_decola)) as pool:
            pool.map(aeronaves, params)

    #with multiprocessing()as manager:
     #   sem_decola = manager.Semaphore(1)
      #  with multiprocessing.Pool(processes=3, initializer=initDecola,  initargs=(sem_decola)) as pool:
       #      poo.map(aeronaves, params)

if __name__ == "__main__":
    main()
