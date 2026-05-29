import multiprocessing
import time
import random

sem_pista = None
travas_equipes = None

def init_treino(pista, equipes):
    global sem_pista
    global travas_equipes
    sem_pista = pista
    travas_equipes = equipes

def aguarda_nos_boxes(numero_carro, equipe):
    print(f"[BOXES] Carro {numero_carro} da equipe {equipe} aguardando liberação...")
    time.sleep(random.uniform(0.1, 0.3))

def dar_volta(numero_carro, equipe, volta):
    tempo_volta = random.uniform(71.5, 84.0)
    time.sleep(0.5)
    print(f"⏱️ [VOLTA] Carro {numero_carro} ({equipe}) -> Completou a Volta {volta} em {tempo_volta:.2f}s")

def corre_treino(numero_carro, equipe):
    print(f"[PISTA] O Carro {numero_carro} da equipe {equipe} ENTROU na pista!")
    for volta in range(1, 4):
        dar_volta(numero_carro, equipe, volta)
    print(f"🏁 [RETORNO] O Carro {numero_carro} da equipe {equipe} concluiu o treino e SAIU da pista.")

def processamento_carro(numero_carro, equipe):
    global sem_pista
    global travas_equipes
    
    aguarda_nos_boxes(numero_carro, equipe)

    with travas_equipes[equipe]:
        with sem_pista:
            corre_treino(numero_carro, equipe)

def main():
    escuderias = [
        'Ferrari', 'McLaren', 'Red Bull', 'Mercedes', 
        'Aston Martin', 'Alpine', 'Sauber'
    ]

    with multiprocessing.Manager() as manager:
        pista_compartilhada = manager.Semaphore(5)
        equipes_compartilhadas = manager.dict()
        
        for equipe in escuderias:
            equipes_compartilhadas[equipe] = manager.Semaphore(1)
            
        params = []
        for equipe in escuderias:
            for numero_carro in range(1, 3):
                params.append((numero_carro, equipe))
        
        random.shuffle(params)
        
        print("SINAL VERDE: INÍCIO DO TREINO ORGANIZADO DE F1")
        
        with multiprocessing.Pool(
            processes=14, 
            initializer=init_treino, 
            initargs=(pista_compartilhada, equipes_compartilhadas)
        ) as pool:
            pool.starmap(processamento_carro, params)

if __name__ == "__main__":
    main()
