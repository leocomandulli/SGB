import sqlite3

# Caminho do banco de dados SQLite
caminho_db = "TCP.db"

# Conectar ao banco de dados
con = sqlite3.connect(caminho_db)
cur = con.cursor()

# Função para atualizar a tabela Base_de_Familias
def atualizar_base_de_familias():
    try:
        # Obter todos os Codigo_Pre_Mat da tabela Extrato_Dynamo
        cur.execute('SELECT Codigo_Pre_Mat, Data_de_execucao, File_Path, Tempo_de_execucao FROM Extrato_Dynamo')
        resultados = cur.fetchall()  # Retorna uma lista de tuplas

        # Iterar sobre os resultados e atualizar a tabela Base_de_Familias
        for codigo_pre_mat, data_execucao, file_path, tempo_execucao in resultados:
            # Verificar se o Codigo_Pre_Mat está na tabela Base_de_Familias
            cur.execute('SELECT rowid FROM Base_de_Familias WHERE Codigo_Pre_Mat = ?', (codigo_pre_mat,))
            row = cur.fetchone()

            if row:
                # Se houver correspondência, atualizar as colunas
                rowid = row[0]
                cur.execute(''' 
                UPDATE Base_de_Familias 
                SET Elaborador = ?, Status_Biblioteca = ?, Ultima_atualizacao = ?, File_Path = ?, Tempo_TCP = ?
                WHERE rowid = ?
                ''', ('TCP', 'Atualizado', data_execucao, file_path, tempo_execucao, rowid))

                print(f"Atualizado: Codigo_Pre_Mat = {codigo_pre_mat}, rowid = {rowid}")
            else:
                # Se não houver correspondência, inserir um novo registro
                cur.execute('''
                INSERT INTO Base_de_Familias (Codigo_Pre_Mat, Elaborador, Status_Biblioteca, Ultima_atualizacao, File_Path) 
                VALUES (?, ?, ?, ?, ?)
                ''', (codigo_pre_mat, 'TCP', 'Atualizado', data_execucao, file_path))

                print(f"Inserido novo registro: Codigo_Pre_Mat = {codigo_pre_mat}")

        # Confirmar as alterações
        con.commit()

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")

# Chamar a função para realizar a atualização
atualizar_base_de_familias()

# Fechar a conexão com o banco de dados
con.close()
