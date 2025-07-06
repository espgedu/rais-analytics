#%% 
import pandas as pd 

colunas = ['Sexo Trabalhador', 'Raça Cor', 'Tipo Defic','Tempo Emprego', 'Faixa Remun Média (SM)',
           'Escolaridade após 2005','Vl Remun Dezembro Nom']

caminho_txt = r"C:\Users\Eduardo\Desktop\hr-analytics-sql\data\raw\RAIS_VINC_PUB_SP\RAIS_VINC_PUB_SP.txt"
caminho_saida = r"C:\Users\Eduardo\Desktop\hr-analytics-sql\data\processed\RAIS_SP_2024_tratada.csv"
chunksize = 100_000  

sexo_map = {'1': 'Masculino', '2': 'Feminino'}

raca_map = {
    '1': 'Indígena', '2': 'Branca', '4': 'Parda',
    '6': 'Amarela', '8': 'Preta', '9': 'Não Informado'
}
defic_map = {
    '0': 'Sem deficiência', '1': 'Def. Física', '2': 'Def. Auditiva',
    '3': 'Def. Visual', '4': 'Def. Intelectual', '5': 'Reabilitado',
    '6': 'Def. Múltipla', '9': 'Não Informado'
}

escolaridade_map = {
    '1': 'Analfabeto', '2': 'Até a quinta incompleta série',
    '3': 'Quinta série do fundamental', '4':'6ª a 9ª série do Ensino Fundamental completo',
    '5': 'Ensino Fundamental completo', '6': 'Ensino Médio incompleto', '7':' Ensino Médio completo',
    '8': 'Superior incompleto', '9': 'Superior completo', '10': 'Pós-graduação'
}

def normalizar_colunas(df):
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.normalize('NFKD')
        .str.encode('ascii', errors='ignore')
        .str.decode('utf-8')
        .str.replace(' ', '_')
        .str.replace('(', '', regex=False)
        .str.replace(')', '', regex=False)
    )
    return df

chunks = []

for i, chunk in enumerate(pd.read_csv(
    caminho_txt,
    sep=';',
    encoding='latin1',
    usecols=colunas,
    chunksize=chunksize,
    low_memory=False)):
    
    chunk = normalizar_colunas(chunk)
    
    chunk['tempo_emprego'] = (
        chunk['tempo_emprego']
        .astype(str)
        .str.strip()
        .str.replace(',', '.', regex=False)
    )
    chunk['vl_remun_dezembro_nom'] = (
        chunk['vl_remun_dezembro_nom']
        .astype(str)
        .str.strip()
        .str.replace(r'\s+', '', regex=True)  # Remove espaços internos
        .str.replace(',', '.', regex=False)
    )

    chunk['tempo_emprego'] = pd.to_numeric(chunk['tempo_emprego'], errors='coerce')
    chunk['vl_remun_dezembro_nom'] = pd.to_numeric(chunk['vl_remun_dezembro_nom'], errors='coerce')


    chunk = chunk[chunk['vl_remun_dezembro_nom'].notnull()]
    chunk = chunk[chunk['vl_remun_dezembro_nom'] > 0]
    chunk = chunk[chunk['vl_remun_dezembro_nom'] < 100_000]
    chunk = chunk[chunk['faixa_remun_media_sm'].notnull()]

    
    chunk['sexo_trabalhador'] = chunk['sexo_trabalhador'].astype(str).map(sexo_map)
    chunk['raca_cor'] = chunk['raca_cor'].astype(str).map(raca_map)
    chunk['tipo_defic'] = chunk['tipo_defic'].astype(str).map(defic_map)
    chunk['escolaridade_apos_2005'] = chunk['escolaridade_apos_2005'].astype(str).map(escolaridade_map)

    chunks.append(chunk)
    print(f" Chunk {i + 1} processado...")

df = pd.concat(chunks, ignore_index=True)
print("Todos os chunks foram concatenados.")

df.to_csv(caminho_saida, index=False, encoding='utf-8')
print(f"Arquivo salvo com sucesso: {caminho_saida}")


# %%
