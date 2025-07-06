#%%
from ftplib import FTP
import os
from tqdm import tqdm
import subprocess

#Baixar arquivo via FTP
def baixar_arquivo_ftp(host, caminho_ftp, arquivo, destino_local):
    ftp = FTP(host)
    ftp.login()
    ftp.cwd(caminho_ftp)

    os.makedirs(destino_local, exist_ok=True)
    local_path = os.path.join(destino_local, arquivo)

    # Obter o tamanho do arquivo
    tamanho_total = ftp.size(arquivo)
    print(f"⬇️ Baixando {arquivo} ({tamanho_total / (1024**2):.2f} MB)...")

    with open(local_path, 'wb') as f, tqdm(
        total=tamanho_total,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        desc=f"Baixando {arquivo}",
        ncols=80
    ) as barra:
        def atualizar_barra(chunk):
            f.write(chunk)
            barra.update(len(chunk))

        ftp.retrbinary(f'RETR {arquivo}', callback=atualizar_barra)

    ftp.quit()
    print(f"✔️ Arquivo baixado: {arquivo}")
    return local_path

#Extrair com 7-Zip via subprocess
def extrair_arquivo(arquivo_7z, destino, caminho_7z_exe=r"C:\Program Files\7-Zip\7z.exe"):
    nome_arquivo = os.path.basename(arquivo_7z)
    nome_subpasta = os.path.splitext(nome_arquivo)[0]
    pasta_destino = os.path.join(destino, nome_subpasta)

    os.makedirs(pasta_destino, exist_ok=True)
    print(f"Extraindo {nome_arquivo} com 7-Zip...")

    comando = [caminho_7z_exe, 'x', arquivo_7z, f'-o{pasta_destino}', '-y']
    processo = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if processo.returncode != 0:
        print("❌ Erro ao extrair o arquivo:")
        print(processo.stderr)
    else:
        print(f"📦 Arquivo extraído para: {pasta_destino}")

#Configurações

host = 'ftp.mtps.gov.br'
caminho = '/pdet/microdados/RAIS/2010' 
arquivo = 'MG2010.7z'        
destino = r'C:\Users\Eduardo\Desktop\hr-analytics-sql\data\raw' 
caminho_7z_exe = r"C:\Program Files\7-Zip\7z.exe"

#Execução
caminho_baixado = baixar_arquivo_ftp(host, caminho, arquivo, destino)
extrair_arquivo(caminho_baixado, destino,caminho_7z_exe)

#%%
