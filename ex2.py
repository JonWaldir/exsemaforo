import multiprocessing
import time
import random
semaforo_tocha: None
posix : int = 0
semaforo_pedra = None
def init(sem_tocha,sem_pedra, posi):
    global semaforo_tocha
    global semaforo_pedra
    global posix
    semaforo_tocha = sem_tocha
    semaforo_pedra = sem_pedra
    posix = posi

def processamento(id):
    vel: int = 0
    chegada:int = 0
    global semaforo_tocha
    global semaforo_pedra
    while chegada < 20:
        velo = random.randint(2, 4)
        chegada += velo
        print(f'O corredor {id} esta {velo} em 50m/s distancia {chegada}')
        time.sleep(0.005)
    
        with semaforo_tocha:
            tocha(id, chegada)
            
    
        
        if chegada > 15:
            with semaforo_pedra:
                pedra(id, chegada)

def tocha(id, chegada):
    if chegada > 5 :
        print(f'O corredor {id} pegou a tocha')

    if chegada > 10 :
        print(f'O corredor {id} pegou a tocha')
        
    

def pedra(id, chegada):
    if chegada > 15:
        print(f"O corredor {id} pegou a tocha")

def main():
    i: int = 0
    proc : int= 0
    proc = 4
    sem_tocha = None
    sem_pedra = None
    posi = multiprocessing.Value('i' , 0)
    params = [0]*proc
    print("Começa a corrida no corredor (2km)")
    for i in range(4):
        params[i]= i
    with multiprocessing.Manager() as manager:
        sem_tocha = multiprocessing.Semaphore(2)
        sem_pedra = multiprocessing.Semaphore(1)
        with multiprocessing.Pool(processes=4, initializer=init, initargs=(sem_tocha, sem_pedra, posi)) as pool:
            pool.map(processamento, params)

if __name__ == "__main__":
    main()