"""Web Scraping do site de avaliações de filmes Rotten Tomatoes"""

# aqui são importadas as bibliotecas que serão utilizadas para extrair os dados
import requests
from bs4 import BeautifulSoup
import pandas as pd

#Scraping da pagina principal
url = "https://www.rottentomatoes.com/browse/movies_in_theaters/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")


#listas com os dados extraidos
titulos = []



#Identificar os links de redirecionamento para cada filme da pagina
#Obs: precisamos dividir em duas partes pois o link de alguns filmes estava em um atributo diferente
links_filmes = []
filmes_elements = soup.find_all("a", class_="js-tile-link")
filmes_elements2 = soup.find_all("a", attrs={'data-track': 'scores'})



#Adicionando os links na lista
#Obs: esses links são apenas a terminação que é adicionada ao endereço principal da pagina
for element in filmes_elements:
    links_filmes.append(element['href'])
    
for element in filmes_elements2:
    links_filmes.append(element['href'])


    
# O filme_url contém o endereço da pagina principal mais a terminação que redireciona para um filme especifico
for link_filme in links_filmes:
    filme_url = "https://www.rottentomatoes.com" + link_filme
    filme_response = requests.get(filme_url)
    filme_soup = BeautifulSoup(filme_response.text, 'lxml')
    
    titulo = filme_soup.find("h1", class_="unset").find('span').text.strip()
    
    
    titulos.append(titulo)
    
    
print(titulos)

