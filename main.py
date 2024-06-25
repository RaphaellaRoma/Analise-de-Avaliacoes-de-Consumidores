from trope_prompt import gerar_trope
from web_scraping import lista

def most_frequent():
    n = 0
    i = 0
    tropes = []
    main_tropes = []
    
    while n < len(lista[0]):
        while i < 5:
            trope = gerar_trope(lista[4][n], lista[9][n], lista[10][n])
            tropes.append(trope)
            if i == 4:
                main_trope = max(set(tropes), key = tropes.count)
                main_tropes.append(main_trope)
            i += 1
    
        i = 0
        tropes.clear()
        n += 1 
    return main_tropes

def escrever_tropes(lista, trope):
    i = 0
    while i < len(lista[0]):  
        print(f"Filme: {lista[0][i]}")
        print(f"Trope: {trope[i]}")
        print("-" * 20)
        print(" ")
        i += 1
        
trope = most_frequent()
#escrever_tropes(lista, trope)