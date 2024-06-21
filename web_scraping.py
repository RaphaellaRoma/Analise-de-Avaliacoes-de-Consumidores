"""Web Scraping do site de avaliações de filmes Rotten Tomatoes"""

# aqui são importadas as bibliotecas que serão utilizadas para extrair os dados
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Scraping da pagina principal
url = "https://www.rottentomatoes.com/browse/movies_in_theaters/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")

# Listas com os dados extraidos
titulos = []
lancamentos = []
generos = []
diretores = []
sinopses = []
bilheterias = []

# Identificar os links de redirecionamento para cada filme da pagina
# Obs: precisamos dividir em duas partes pois o link de alguns filmes estava em um atributo diferente
links_filmes = []
filmes_elements = soup.find_all("a", class_="js-tile-link")
filmes_elements2 = soup.find_all("a", attrs={'data-track': 'scores'})

# Adicionando os links na lista
# Obs: esses links são apenas a terminação que é adicionada ao endereço principal da pagina
for element in filmes_elements:
    links_filmes.append(element['href'])
    
for element in filmes_elements2:
    links_filmes.append(element['href'])
    
# O filme_url contém o endereço da pagina principal mais a terminação que redireciona para um filme especifico
for link_filme in links_filmes:
    filme_url = "https://www.rottentomatoes.com" + link_filme
    filme_response = requests.get(filme_url)
    filme_soup = BeautifulSoup(filme_response.text, 'lxml')
    
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
    
    # Armazenando nas listas 
    titulos.append(titulo)
    sinopses.append(sinopse)
    lancamentos.append(lancamento)
    generos.append(genero) 
    diretores.append(diretor)
    bilheterias.append(bilheteria)

# Mostrar os resultados
for titulo, sinopse, lancamento, genero, diretor, bilheteria in zip(titulos, sinopses, lancamentos, generos, diretores, bilheterias):
    print(f"Título: {titulo}")
    print(f"Data de lançamento: {lancamento}")
    print(f"Gênero: {genero}")
    print(f"Diretor: {diretor}")
    print(f"Sinopse: {sinopse}")
    print(f"Bilheteria (bruto EUA): {bilheteria}")
    print("-" * 20)
    print(" ")






