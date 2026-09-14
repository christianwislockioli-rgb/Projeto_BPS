import pandas as pd
import glob
import os

print("Iniciando o processamento dos dados do BPS...")

# Caminho onde os arquivos CSV originais estão salvos
caminho_dados = 'dados_brutos/*.csv'
arquivos = glob.glob(caminho_dados)

lista_dataframes = []

for arquivo in arquivos:
    print(f"Lendo arquivo: {arquivo}")
    
    # ESTRATÉGIA DE ENCODING AUTOMÁTICO:
    # Tenta ler em UTF-8 primeiro (corrige o "SÃ“DICA", "PregÃ£o", etc.)
    try:
        df = pd.read_csv(arquivo, sep=';', encoding='utf-8', low_memory=False)
        print(" -> Sucesso: Arquivo lido em padrão UTF-8")
    except UnicodeDecodeError:
        # Se der erro de decoding, é porque o arquivo é antigo e usa Latin-1
        print(" -> Tentando fallback para padrão Latin-1...")
        df = pd.read_csv(arquivo, sep=';', encoding='latin1', low_memory=False)
        print(" -> Sucesso: Arquivo lido em padrão Latin-1")
    except Exception as e:
        print(f" -> Erro inesperado ao ler o arquivo {arquivo}: {e}")
        continue
        
    # Extrair o ano do nome do arquivo para garantir a identificação temporal
    nome_arquivo = os.path.basename(arquivo)
    ano = ''.join(filter(str.isdigit, nome_arquivo))
    if ano:
        df['Ano_Arquivo'] = ano
        
    lista_dataframes.append(df)

# Concatenando tudo em um único DataFrame
print("\nConcatenando as bases de todos os anos...")
df_consolidado = pd.concat(lista_dataframes, ignore_index=True)

# Limpeza básica exigida pelo edital (padronização de nulos)
df_consolidado = df_consolidado.fillna('Não Informado') 

# Exportando o arquivo final com encoding utf-8-sig (garante que o Excel/Power BI leiam os acentos perfeitos)
nome_saida = 'BPS_20_26_ChristianWislocki.csv'
print(f"Exportando arquivo final: {nome_saida}...")
df_consolidado.to_csv(nome_saida, sep=';', index=False, encoding='utf-8-sig')

print(f"Sucesso absoluto! Base limpa com {df_consolidado.shape[0]} linhas gerada.")