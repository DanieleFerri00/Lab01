from domanda import Domanda
import random

def leggi_domande(nome_file):
    domande=[]
    with open(nome_file, "r", encoding="utf-8") as file:
        righe=file.readlines()
        righe= [riga.strip() for riga in righe]

        indice=0
        while indice< len(righe):
            testo=righe[indice]
            livello=int(righe[indice+1])
            corretta=righe[indice+2]
            errate=[
                righe[indice+3],
                righe[indice+4],
                righe[indice+5]
            ]
            domanda=Domanda(testo,livello, corretta, errate)
            domande.append(domanda)
            indice+=7
    return domande

def raggruppa_per_livello(domande):
    livelli={}

    for domanda in domande:

        if domanda.livello not in livelli:
            livelli[domanda.livello]=[]

        livelli[domanda.livello].append(domanda)

    return livelli


def scegli_domanda(livelli,livello):

    return random.choice(livelli[livello])


def mostra_domanda(domanda):
    risposte=[domanda.risposta_corretta]+domanda.risposte_errate
    random.shuffle(risposte)
    print()
    print(f"\nLivello {domanda.livello}) {domanda.testo}")
    for i, risposta in enumerate(risposte, start=1):
        print(f"{i}. {risposta}")

    indice_corretto=risposte.index(domanda.risposta_corretta)

    return indice_corretto


def stampa_punteggio(punteggio):
    if punteggio == 1:
        print("Hai totalizzato 1 punto!")
    else:
        print(f"Hai totalizzato {punteggio} punti!")


def gioca(domande_per_livello):
    livello=0
    punteggio=0

    while True:
        domanda = scegli_domanda(domande_per_livello, livello)
        indice_corretto = mostra_domanda(domanda)
        risposta = int(input("Inserisci la risposta: "))
        if risposta == indice_corretto + 1:
            print("Risposta corretta!")
            punteggio += 1
            livello += 1
            if livello not in domande_per_livello:
                print("Hai completato tutti i livelli!")
                break
        else:
            print("Risposta sbagliata!")
            print(f"La risposta corretta era: {domanda.risposta_corretta}")
            break
    stampa_punteggio(punteggio)
    nickname = input("Inserisci il tuo nickname: ")
    salva_punteggio("punti.txt", nickname, punteggio)

def salva_punteggio(nome_file,nickname,punteggio):
    classifica=[]
    with open(nome_file, "r", encoding="utf-8") as file:
        for riga in file:
            parti=riga.split()
            nome = parti[0]
            punti = int(parti[1])
            classifica.append((nome,punti))
    classifica.append((nickname,punteggio))
    classifica.sort(key=lambda x: x[1], reverse=True)
    with open(nome_file, "w", encoding="utf-8") as file:
        for nome, punti in classifica:
            file.write(f"{nome} {punti}\n")


domande = leggi_domande("domande.txt")

livelli = raggruppa_per_livello(domande)

gioca(livelli)
