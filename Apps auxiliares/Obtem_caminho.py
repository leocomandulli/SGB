import os
import sqlite3

def atualizar_caminho_arquivos(diretorio_base, banco_dados=r'C:\Users\lsco\OneDrive - Intertechne Consultores SA\Documentos\APP - TCP\APP\TCP.db'):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()

    # Obter os valores da coluna Codigo_Pre_Mat
    cursor.execute("SELECT Codigo_Pre_Mat FROM Base_de_Familias WHERE Codigo_Pre_Mat IS NOT NULL")
    codigos_pre_mat = cursor.fetchall()

    # Percorrer os valores de Codigo_Pre_Mat
    for (codigo,) in codigos_pre_mat:
        codigo_inicial = str(codigo)[:6]  # Obter os primeiros 6 dígitos do código

        # Variável para armazenar o caminho do arquivo encontrado
        caminho_arquivo_encontrado = None

        # Percorrer o diretório e subdiretórios em busca de arquivos .rfa
        for root, _, files in os.walk(diretorio_base):
            for file in files:
                # Verifica se o arquivo começa com os 6 primeiros dígitos e termina com '.rfa'
                if file.startswith(codigo_inicial) and file.endswith('.rfa'):
                    caminho_arquivo_encontrado = os.path.join(root, file)
                    break  # Parar a busca assim que o arquivo for encontrado
            if caminho_arquivo_encontrado:
                break  # Parar a busca nos diretórios se o arquivo foi encontrado

        # Atualizar o caminho no banco de dados se o arquivo foi encontrado
        if caminho_arquivo_encontrado:
            cursor.execute("""
                UPDATE Base_de_Familias
                SET File_Path = ?
                WHERE Codigo_Pre_Mat = ?
            """, (caminho_arquivo_encontrado, codigo))
            print(f"Caminho atualizado para {codigo}: {caminho_arquivo_encontrado}")
        else:
            print(f"Arquivo não encontrado para {codigo}")

    # Salvar e fechar a conexão
    conn.commit()
    conn.close()
    print("Atualização completa.")

# Exemplo de uso:
diretorio_base = r"C:\Users\lsco\DC\ACCDocs\INTERTECHNE CONSULTORES\0001-IT - AMBIENTE DE BIBLIOTECAS BIM\Project Files\DUAE\003 - Biblioteca\002 - Familias Revit\005 - Mecânica\V - Fixadores"
atualizar_caminho_arquivos(diretorio_base)

