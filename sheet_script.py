from openpyxl import Workbook
from web_scraping import lista, declarar_listas
from main import trope
import openpyxl.styles

#incializando os excel
wb = Workbook()
ws = wb.active
ws.title = "Tabela de Filmes"

i = 0
n = 0

#nomes na primeira linha da tabela
names =[
    "Filme",
    "Data de Lançamento",
    "Gênero",
    "Diretor",
    "Bilheteria(Gross USD)",
    "Consensu dos Críticos",
    "Consensu da Audiência",
    "Reviews dos Críticos",
    "Reviews da Audiência"
]

#inserção dos dados dos scripts para o excel sheet
for n in range(len(declarar_listas())):
    while i < (len(lista[0])):
        if n == 4 or n == 9 or n == 10 or n == 11:
            ws.cell(row=i+3, column=n+2)
        else:
            ws.cell(row=i+3, column=n+2, value=lista[n][i])
        i += 1
    i = 0
    n += 1

#deletando colunas vazias
ws.delete_cols(11,3)
ws.delete_cols(6,1)

#inserção dos nomes para a primeira linha
i = 0
while i < len(names):
    ws.cell(row=2, column=i+2, value=names[i])
    i += 1

#criação da coluna 5
ws.insert_cols(5, 1)
#inserção do nome "Trope" para a primeira linha da coluna 5
ws.cell(row=2, column=5, value="Trope")

#inserção de dados dos tropes para a coluna 5
i = 0
while i < len(trope):
    ws.cell(row=i+3, column=5, value=(trope[i].replace("trope", "")))
    i += 1

#salvando a tabela no excel
wb.save("rotten_tomatos.xlsx")