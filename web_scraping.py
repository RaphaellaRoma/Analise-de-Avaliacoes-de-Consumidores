#importando as bibliotecas necessárias
import requests
from bs4 import BeautifulSoup
import re

#scraping de paginas
def scraping(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    return soup

#inicializando as variavies do tipo lista
def declarar_listas():
    titulos = []
    lancamentos = []
    generos = []
    diretores = []
    sinopses = []
    bilheterias = []
    tomatometer_scores = []
    audience_scores = []
    number_scores = []
    critics_consensus = []
    audience_consensus = []
    links_filmes = []
    audience_reviews = []
    
    lista = titulos, lancamentos, generos, diretores,\
        sinopses, bilheterias, tomatometer_scores,\
        audience_scores, number_scores, critics_consensus,\
        audience_consensus, links_filmes, audience_reviews
        
    return lista

#encontrando a terminação dos links
def encontrar_link():
    links_filmes = lista[11]
    filmes_elements = soup.find_all("a", class_="js-tile-link") + soup.find_all("a", attrs={'data-track': 'scores'})

    for element in filmes_elements:
        links_filmes.append(element['href']) 
        
    return links_filmes

#limpando os dados do scraping e separando-os em cada uma de suas listas
#1° -> Critics/Audience Scores, Consensus e Reviews
def separar_critics_audience(filme_arg, string, strain, element_arg, posicao):
    info = lista[posicao]
    element = filme_soup.find(f"{filme_arg}", attrs={f"{string}" : f"{strain}"})
    if element and len(element_arg) >= 1:
        text = element.find(f"{element_arg}")
        if text:
            info = text.text.strip()
            if not info:
                info = ""
    elif element:
        info = element.text.strip()
        
        temp = re.findall(r'\d+', info)
        temp = ''.join(temp[0:])
        
        info = temp
        if not info:
            info = ""
    else: 
        info = "empty" 
    return info
#2° -> Sinopse e Titulo
def separar_sinopse_titulo(filme_arg, class_, element_arg, posicao):
    info = lista[posicao]
    element = filme_soup.find(f"{filme_arg}", attrs=f"{class_}")
    if element:
        if posicao == 4:
            text = element.find_all(f"{element_arg}")
            if len(text) > 1:
                info = text[1].text.strip()
        else:
            text = element.find(f"{element_arg}")
            if text:
                info = text.text.strip() 
    return info
#1° ->Lancamento, Bilheteria, Genero e Diretor
def separar_lan_bil_gen_dir():
    lancamento = None
    genero = None
    diretor = None
    bilheteria = None
    dt_elements = filme_soup.find_all('dt')
    dd_elements = filme_soup.find_all('dd')
    
    for dt, dd in zip(dt_elements, dd_elements):
        if dt.find('rt-text'):
            dt_text = dt.find('rt-text').text.strip()
        else:
            dt_text = ''
        
        if dd.find('rt-text'):
            dd_text = dd.find('rt-text').text.strip()
            if dd.find('rt-link'):
                dd_text = dd.find('rt-link').text.strip()
        else:
            dd_text = ''
            
        if dd.find('rt-link'):
            dd_links = dd.find_all('rt-link') 
        else:
            dd_links = []
            
        for link in dd_links:
            dd_texts = [link.text.strip()]
        
        match dt_text:
            case 'Release Date (Theaters)': lancamento = dd_text
            case 'Box Office (Gross USA)': bilheteria = dd_text
            case 'Genre':
                if dd_texts:
                    genero = ', '.join(dd_texts) 
                else:
                    genero = None
            case 'Director':
                if dd_texts:
                    diretor = ', '.join(dd_texts) 
                else:
                    diretor = None
    
    info = [lancamento, bilheteria, genero, diretor]
    return info

#Trancrevendo os dados para confirmação (opcional)
def escrever_filmes(lista):
    i = 0
    while i < len(lista[0]):  
        print(f"Título: {lista[0][i]}")
        print(f"Data de lançamento: {lista[1][i]}")
        print(f"Gênero: {lista[2][i]}")
        print(f"Diretor: {lista[3][i]}")
        print(f"Sinopse: {lista[4][i]}")
        print(f"Bilheteria (bruto EUA): {lista[5][i]}")
        print("-" * 20)
        print(f"Avaliação de críticos: {lista[6][i]}")
        print(f"Avaliação do público: {lista[7][i]}")
        print(f"Número de avaliações de críticos: {lista[8][i]}")
        print(f"Número de avaliações de críticos: {lista[12][i]}")
        print(f"Consenso dos críticos: {lista[9][i]}")
        print(f"Consenso do público: {lista[10][i]}")
        print("-" * 20)
        print(" ")
        i += 1

#gerando as funções
def call_main():
    global soup, lista, filme_soup
    url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular"
    (soup) = scraping(url)
    lista = declarar_listas()
    for link_filme in encontrar_link():
        filme_url = "https://www.rottentomatoes.com" + link_filme
        filme_soup = scraping(filme_url)

        titulo = None
        sinopse = None
        critics_consensu = None
        audience_consensu = None
        tomatometer_score = None
        audience_score = None
        number_score = None
        audience_review = None

        #chamamando cada tipo de informação separados
        titulo = separar_sinopse_titulo("h1", "unset", "span", 0)
        lancamento = separar_lan_bil_gen_dir()[0]
        bilheteria = separar_lan_bil_gen_dir()[1]
        genero = separar_lan_bil_gen_dir()[2]
        diretor =separar_lan_bil_gen_dir()[3]
        sinopse = separar_sinopse_titulo("div", "synopsis-wrap", "rt-text", 4)
        tomatometer_score = separar_critics_audience("rt-button", "slot", "criticsScore", "rt-text", 6)
        audience_score = separar_critics_audience("rt-button", "slot", "audienceScore", "rt-text", 7)
        number_score = separar_critics_audience("rt-link", "slot", "criticsReviews", "", 8)
        critics_consensu = separar_critics_audience("div", "id", "critics-consensus", "p", 9)
        audience_consensu = separar_critics_audience("div", "id", "audience-consensus", "p", 10)
        audience_review = separar_critics_audience("rt-link", "slot", "audienceReviews", "", 12)
        
        # Armazenando nas listas 
        lista[0].append(titulo)
        lista[1].append(lancamento)
        lista[2].append(genero) 
        lista[3].append(diretor)
        lista[4].append(sinopse)
        lista[5].append(bilheteria)
        lista[6].append(tomatometer_score)
        lista[7].append(audience_score)
        lista[8].append(number_score)
        lista[9].append(critics_consensu)
        lista[10].append(audience_consensu)
        lista[12].append(audience_review)

    #escrever_filmes(lista)

#chamando a main
call_main()