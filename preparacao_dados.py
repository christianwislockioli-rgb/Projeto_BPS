import pandas as pd
import numpy as np
import glob
import os
import sys

print("Iniciando o processamento dos dados do BPS...")

caminho_dados = 'dados_brutos/*.csv'
arquivos = glob.glob(caminho_dados)

if not arquivos:
    print("\nERRO CRÍTICO: Nenhum arquivo .csv encontrado na pasta 'dados_brutos/'. Verifique o caminho.")
    sys.exit()

lista_dataframes = []

for arquivo in arquivos:
    print(f"Lendo arquivo: {arquivo}")
    try:
        df = pd.read_csv(arquivo, sep=';', encoding='utf-8', low_memory=False, decimal=',', thousands='.')
        print(" -> Sucesso: Arquivo lido em padrão UTF-8")
    except UnicodeDecodeError:
        print(" -> Tentando fallback para padrão Latin-1...")
        df = pd.read_csv(arquivo, sep=';', encoding='latin1', low_memory=False, decimal=',', thousands='.')
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

print("Tratando nulos, 'NULL' literal e corrigindo tipos de dados...")

# Trata strings literais de nulo
df_consolidado.replace(['NULL', 'null', 'None'], np.nan, inplace=True)

# 1. Tratamento de identificadores numéricos/códigos
colunas_codigos = ['co_pdm', 'co_classe', 'co_grupo', 'co_catmat']
for col in colunas_codigos:
    if col in df_consolidado.columns:
        df_consolidado[col] = pd.to_numeric(df_consolidado[col], errors='coerce')

# 2. Tratamento das colunas financeiras e quantitativas
colunas_valor = [col for col in df_consolidado.columns if col.startswith('vl_') or 'valor' in col.lower()]
for col in colunas_valor:
    if col in df_consolidado.columns:
        if df_consolidado[col].dtype == 'object':
            df_consolidado[col] = (
                df_consolidado[col]
                .astype(str)
                .str.strip()
                .str.replace(r'\.(?=\d{3}(,|$))', '', regex=True)
                .str.replace(',', '.', regex=False)
            )
        df_consolidado[col] = pd.to_numeric(df_consolidado[col], errors='coerce')

# 3. Tratamento de nulos por regra de negócio vs descritivos
colunas_data = ['dt_compra', 'dt_insercao']
colunas_nulas_regra = ['nu_ata', 'vl_capacidade', 'registro_anvisa']

cols_texto = df_consolidado.select_dtypes(include=['object', 'string']).columns
cols_texto = [col for col in cols_texto if col not in colunas_data and col not in colunas_nulas_regra]

df_consolidado[cols_texto] = df_consolidado[cols_texto].fillna('Não Informado')

# 4. Limpeza de erros grotescos de digitação no BPS (> 100M ou negativos)
if 'vl_preco_total' in df_consolidado.columns:
    condicao_valida = (
        (df_consolidado['vl_preco_total'] > 0) & 
        (df_consolidado['vl_preco_total'] < 100_000_000)
    ) | (df_consolidado['vl_preco_total'].isna())
    df_consolidado = df_consolidado[condicao_valida]

nome_saida = 'BPS_20_26_ChristianWislocki.csv'
print(f"Exportando arquivo final: {nome_saida}...")

try:
    df_consolidado.to_csv(nome_saida, sep=';', index=False, encoding='utf-8-sig', decimal=',')
    print(f"\nSucesso! Base tratada com {df_consolidado.shape[0]} linhas gerada.")
except PermissionError:
    print(f"\nERRO DE PERMISSÃO: Feche o arquivo '{nome_saida}' no Power BI/Excel e execute novamente.")