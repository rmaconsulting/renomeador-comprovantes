import tabula
import pandas as pd

# Extrai as tabelas do PDF e as coloca em uma lista de DataFrames
dfs = tabula.read_pdf("Descarga pagas - Outubro 2024.pdf", pages='all')

# Escreve o primeiro DataFrame em um arquivo Excel
dfs[0].to_excel("meu_excel.xlsx", index=False)