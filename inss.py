import pandas as pd

# Carregar a planilha em um DataFrame
arquivo = r"C:\Users\Rodrigo\Desktop\base.xlsx"  # Ajuste o caminho para sua planilha
df = pd.read_excel(arquivo)

# Verificar se a coluna 'tit' existe
if 'tit' not in df.columns:
    raise ValueError("A coluna 'tit' não foi encontrada na planilha.")

# Encontrar valores duplicados na coluna 'tit'
duplicados = df['tit'][df['tit'].duplicated(keep=False)]

# Agrupar e contar as duplicatas
duplicados_contagem = duplicados.value_counts()

# Exibir os resultados no console
if duplicados_contagem.empty:
    print("Não foram encontrados valores duplicados na coluna 'tit'.")
else:
    print("Valores duplicados encontrados na coluna 'tit':")
    print(duplicados_contagem)

# Salvar os resultados em um arquivo, se necessário
saida_arquivo = r"C:\Users\Rodrigo\Desktop\titulos_duplicados.xlsx"
duplicados_contagem.to_frame(name='Frequência').reset_index().rename(columns={'index': 'Valor'}).to_excel(saida_arquivo, index=False)
print(f"Resultados salvos em: {saida_arquivo}")
