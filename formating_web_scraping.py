#importando as bibliotecas necessárias
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    
    lista = titulos, lancamentos, generos, diretores,\
        sinopses, bilheterias, tomatometer_scores,\
        audience_scores, number_scores, critics_consensus,\
        audience_consensus, links_filmes
        
    return lista

#funcao para econtrar a terminação dos links
def encontrar_link():
    links_filmes = lista[11]
    filmes_elements = soup.find_all("a", class_="js-tile-link") + soup.find_all("a", attrs={'data-track': 'scores'})

    for element in filmes_elements:
        links_filmes.append(element['href']) 
        
    return links_filmes

#main
url = "https://www.rottentomatoes.com/browse/movies_in_theaters/"
soup = scraping(url)
lista = declarar_listas()

# O filme_url contém o endereço da pagina principal mais a terminação que redireciona para um filme especifico
for link_filme in encontrar_link():
    filme_url = "https://www.rottentomatoes.com" + link_filme
    filme_soup = scraping(filme_url)
    
    # Encontrando o nome do filme
    titulo = filme_soup.find("h1", class_="unset").find('span').text.strip()
    
    # A sinopse está dentro de <rt-text> que está dentro de uma div que contém dois <rt-text>, mas so queremos o segundo
    sinopse_element = filme_soup.find("div", class_="synopsis-wrap")
    if sinopse_element:
        sinopse_rt_texts = sinopse_element.find_all('rt-text')
        if len(sinopse_rt_texts) > 1:
            sinopse = sinopse_rt_texts[1].text.strip()
    
    # Encontrando informações básicas do filme que são fornecidas em uma lista, ou seja, as informações estão em um mesmo tipo de elemento dt e dd
    # precisamos então diferencia-las pelo texto
    lancamento = None
    genero = None
    diretor = None
    bilheteria = None
    critics_consensu = None
    audience_consensu = None
    
    dt_elements = filme_soup.find_all('dt')
    dd_elements = filme_soup.find_all('dd')
    
    # Buscando a informação dt em dd
    for dt, dd in zip(dt_elements, dd_elements):
        dt_text = dt.find('rt-text').text.strip() if dt.find('rt-text') else ''
        dd_text = (dd.find('rt-text').text.strip() if dd.find('rt-text') else '') or \
                  (dd.find('rt-link').text.strip() if dd.find('rt-link') else '')
        
        # Diferenciando as informações pelo texto que está dentro do elemento dt e armazenando-as
        if 'Release Date (Theaters)' in dt_text:
            lancamento = dd_text
        elif 'Box Office (Gross USA)' in dt_text:
            bilheteria = dd_text
            
    # Mesmo processo do for anterior, porém aqui existem mais de uma informação por dd que estão separadas por links, por isso criamos uma lista 
    for dt, dd in zip(dt_elements, dd_elements):
        dt_text = dt.find('rt-text').text.strip() if dt.find('rt-text') else ''
        dd_links = dd.find_all('rt-link') if dd.find('rt-link') else []
        dd_texts = [link.text.strip() for link in dd_links]
        
        # Novamente fazendo a diferenciação
        if 'Genre' in dt_text:
            genero = ', '.join(dd_texts) if dd_texts else None
        elif 'Director' in dt_text:
            diretor = ', '.join(dd_texts) if dd_texts else None
    
    # Porcentagem de avaliações dos críticos usando a mesma lógica feita para pegar a sinopse
    tomatometer_score_element = filme_soup.find('rt-button', attrs={'slot': 'criticsScore'})
    if tomatometer_score_element:
        tomatometer_score_text = tomatometer_score_element.find('rt-text')
        if tomatometer_score_text:
            tomatometer_score = tomatometer_score_text.text.strip()
            
    # Número de avaliações dos críticos usando a mesma lógica feita para pegar a sinopse
    number_score_text = filme_soup.find('rt-link', attrs={'slot': 'criticsReviews'})
    if number_score_text:
        number_score = number_score_text.text.strip()
            
    # Porcentagem de avaliações do público usando a mesma lógica feita para pegar a sinopse
    audience_score_element = filme_soup.find('rt-button', attrs={'slot': 'audienceScore'})
    if audience_score_element:
        audience_score_text = audience_score_element.find('rt-text')
        if audience_score_text:
            audience_score = audience_score_text.text.strip()
    
    # Consenso dos críticos usando a mesma lógica feita para pegar a sinopse
    critics_consensu_element = filme_soup.find('div', attrs={'id': 'critics-consensus'})
    if critics_consensu_element:
        critics_consensu_text = critics_consensu_element.find('p')
        if critics_consensu_text:
            critics_consensu = critics_consensu_text.text.strip()
            
    # Consenso do público usando a mesma lógica feita para pegar a sinopse
    audience_consensu_element = filme_soup.find('div', attrs={'id': 'audience-consensus'})
    if audience_consensu_element:
        audience_consensu_text = audience_consensu_element.find('p')
        if audience_consensu_text:
            audience_consensu = audience_consensu_text.text.strip()
    
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


listas = declarar_listas()    
def escrever_filmes(lista, listas):
    i = 0
    while i < len(listas):  
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
        print(f"Consenso dos críticos: {lista[9][i]}")
        print(f"Consenso do público: {lista[10][i]}")
        print("-" * 20)
        print(" ")
        i += 1

escrever_filmes(lista, listas)