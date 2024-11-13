import pandas as pd
import sqlite3
import openpyxl

def atualizar_descricao(banco_dados=r'C:\Users\lsco\OneDrive - Intertechne Consultores SA\Documentos\APP - TCP\APP\TCP.db', 
                        arquivo_excel=r'C:\Users\lsco\OneDrive - Intertechne Consultores SA\Documentos\APP - TCP\APP\DataBase\SGM - INTERTECHNE.xlsx'):

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()

    # Verificar se a coluna 'Descricao' já existe na tabela 'Base_de_Familias'
    cursor.execute("PRAGMA table_info(Base_de_Familias)")
    colunas_existentes = [info[1] for info in cursor.fetchall()]
    if 'Descricao' not in colunas_existentes:
        cursor.execute("ALTER TABLE Base_de_Familias ADD COLUMN Descricao TEXT")
        print("Coluna 'Descricao' adicionada ao banco de dados.")
    
    # Carregar a planilha Excel e selecionar as colunas necessárias
    df_excel = pd.read_excel(arquivo_excel, usecols=["Pré Material", "Descrição Resumida Português"])
    df_excel.columns = ["Codigo_Pre_Mat", "Descricao"]  # Renomear as colunas para facilitar o uso

    # Remover linhas com valores nulos nas colunas essenciais
    df_excel.dropna(subset=["Codigo_Pre_Mat", "Descricao"], inplace=True)

    # Iterar sobre o DataFrame e atualizar o banco de dados
    for _, row in df_excel.iterrows():
        codigo = row["Codigo_Pre_Mat"]
        descricao = row["Descricao"]

        # Atualizar a coluna 'Descricao' no banco de dados onde Codigo_Pre_Mat coincide
        cursor.execute("""
            UPDATE Base_de_Familias
            SET Descricao = ?
            WHERE Codigo_Pre_Mat = ?
        """, (descricao, codigo))
        
        if cursor.rowcount > 0:
            print(f"Descricao atualizada para {codigo}: {descricao}")
    
    # Salvar e fechar a conexão
    conn.commit()
    conn.close()
    print("Atualização completa.")

# Chama função
atualizar_descricao()
