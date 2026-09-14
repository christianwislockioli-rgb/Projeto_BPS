import pandas as pd
import glob
import os
import sys

print("Iniciando o processamento dos dados do BPS...")

caminho_dados = 'dados_brutos/*.csv'
arquivos = glob.glob(caminho_dados)

# TRAVA 1: Verifica se os arquivos realmente existem na pasta
if not arquivos:
    print("\nERRO CRÍTICO: Nenhum arquivo .csv encontrado na pasta 'dados_brutos/'. Verifique o caminho.")
    sys.exit()

lista_dataframes = []

for arquivo in arquivos:
    print(f"Lendo arquivo: {arquivo}")
    try:
        df = pd.read_csv(arquivo, sep=';', encoding='utf-8', low_memory=False)
        print(" -> Sucesso: Arquivo lido em padrão UTF-8")
    except UnicodeDecodeError:
        print(" -> Tentando fallback para padrão Latin-1...")
        df = pd.read_csv(arquivo, sep=';', encoding='latin1', low_memory=False)
        print(" -> Sucesso: Arquivo lido em padrão Latin-1")
    except Exception as e:
        print(f" -> Erro inesperado ao ler o arquivo {arquivo}: {e}")
        continue
        
    nome_arquivo = os.path.basename(arquivo)
    ano = ''.join(filter(str.isdigit, nome_arquivo))
    if ano:
        df['Ano_Arquivo'] = ano
        
    lista_dataframes.append(df)

print("\nConcatenando as bases de todos os anos...")
df_consolidado = pd.concat(lista_dataframes, ignore_index=True)

print("Tratando nulos e corrigindo tipos de dados...")
colunas_numericas = ['co_pdm', 'co_classe', 'co_grupo', 'co_catmat']
for col in colunas_numericas:
    if col in df_consolidado.columns:
        df_consolidado[col] = pd.to_numeric(df_consolidado[col], errors='coerce')

# TRAVA 2: Sintaxe atualizada para evitar o Pandas4Warning
cols_texto = df_consolidado.select_dtypes(include=['object', 'string']).columns
df_consolidado[cols_texto] = df_consolidado[cols_texto].fillna('Não Informado')

nome_saida = 'BPS_20_26_ChristianWislocki.csv'
print(f"Exportando arquivo final: {nome_saida}...")

# TRAVA 3: Previne quebra de código se o arquivo estiver aberto em outro programa
try:
    df_consolidado.to_csv(nome_saida, sep=';', index=False, encoding='utf-8-sig')
    print(f"\nSucesso absoluto! Base limpa com {df_consolidado.shape[0]} linhas gerada.")
except PermissionError:
    print(f"\nERRO DE PERMISSÃO: Feche o arquivo '{nome_saida}' no Power BI/Excel e rode o script novamente!")