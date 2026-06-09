import multiprocessing
import time
import random

# Suas estruturas de variáveis globais
posix: int = 0
semaforo_tocha = None
semaforo_pedra = None
tocha_pega = None
pedra_pega = None

def init(sem_t, sem_p, t_flag, p_flag, posi):
    global semaforo_tocha
    global semaforo_pedra
    global tocha_pega
    global pedra_pega
    global posix
    
    semaforo_tocha = sem_t
    semaforo_pedra = sem_p
    tocha_pega = t_flag
    pedra_pega = p_flag
    posix = posi

def processamento(id):
    global semaforo_tocha
    global semaforo_pedra
    global tocha_pega
    global pedra_pega
    global posix

    chegada: int = 0
    pegou_item = False 

    while chegada < 2000:
        velo = random.randint(2, 4)
        if pegou_item:
            velo += 2
        
        chegada += velo
        time.sleep(0.05)
        print(f'Cavaleiro {id} esta a {velo}m/50ms - Distância: {chegada}m')

        # Lógica de pegar a tocha
        if chegada >= 500 and not pegou_item and tocha_pega.value == 0:
            with semaforo_tocha:
                if tocha_pega.value == 0:
                    tocha_pega.value = 1
                    pegou_item = True
                    print(f'*** O cavaleiro {id} pegou a TOCHA! ***')

        # Lógica de pegar a pedra
        if chegada >= 1500 and not pegou_item and pedra_pega.value == 0:
            with semaforo_pedra:
                if pedra_pega.value == 0:
                    pedra_pega.value = 1
                    pegou_item = True
                    print(f'*** O cavaleiro {id} pegou a PEDRA! ***')

    # Escolha da porta (1 é saída, outras 3 são monstros)
    porta = random.randint(1, 4)
    if porta == 1:
        print(f"-> Cavaleiro {id} escolheu a porta {porta}: ENCONTROU A SAÍDA!")
    else:
        print(f"-> Cavaleiro {id} escolheu a porta {porta}: FOI DEVORADO POR UM MONSTRO!")

def main():
    i: int = 0
    proc: int = 4
    params = [0] * proc
    posi = multiprocessing.Value('i', 0)
    
    print("Começa a corrida dos cavaleiros (2km)")
    for i in range(proc):
        params[i] = i + 1
        
    with multiprocessing.Manager() as manager:
        sem_tocha = manager.Semaphore(1)
        sem_pedra = manager.Semaphore(1)
        tocha_pega = manager.Value('i', 0)
        pedra_pega = manager.Value('i', 0)
        
        with multiprocessing.Pool(processes=proc, initializer=init, initargs=(sem_tocha, sem_pedra, tocha_pega, pedra_pega, posi)) as pool:
            pool.map(processamento, params)

if __name__ == "__main__":
    main()
