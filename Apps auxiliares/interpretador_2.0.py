import json
import sqlite3
import os
import time

# Caminho do banco de dados SQLite
caminho_db = "C:/Users/lsco/OneDrive - Intertechne Consultores SA/Documentos/APP - TCP/APP/TCP.db"
# Caminho para o arquivo JSON
caminho_json = "G:/DepMec/PRODUÇÃO/Rotinas Dynamo/DataBase/transfer.json"

# Conectar ao banco de dados (ou criar um novo)
con = sqlite3.connect(caminho_db)
cur = con.cursor()

# Criar tabela se não existir
cur.execute('''
CREATE TABLE IF NOT EXISTS Extrato_Dynamo (
    Tipo TEXT,
    Fonte_de_dados TEXT,
    Modo_de_entrada TEXT,
    Data_de_execucao TEXT,
    Codigo_Pre_Mat TEXT,
    Tempo_de_execucao TEXT,
    Descricao_Ingles TEXT,
    Descricao_Portugues TEXT,
    Descricao_Espanhol TEXT,
    Fabricante TEXT,
    If_de_dimensoes TEXT,
    If_de_SGM TEXT,
    If_de_peso TEXT,
    Peso_Tipo TEXT,
    Alt_Tipo TEXT,
    SGM_Tipo TEXT,
    Comp_Tipo TEXT,
    Dim_Tipo TEXT,
    DN_Tipo TEXT,
    File_Path TEXT,
    UNIQUE(Codigo_Pre_Mat, Data_de_execucao)  -- Adicionando restrição de unicidade
)
''')

# Função para verificar se o registro já existe
def registro_existe(codigo_pre_mat, data_execucao):
    cur.execute('SELECT 1 FROM Extrato_Dynamo WHERE Codigo_Pre_Mat = ? AND Data_de_execucao = ?', (codigo_pre_mat, data_execucao))
    return cur.fetchone() is not None

# Função principal para processar o JSON e inserir novos dados
def processar_json():
    try:
        # Carregar os dados do JSON
        with open(caminho_json, 'r') as arquivo_json:
            dados_json = json.load(arquivo_json)

        # Verificar se os dados carregados são uma lista
        if not isinstance(dados_json, list):
            raise ValueError("Os dados carregados do JSON não são uma lista.")

        # Iterar sobre os dados JSON para combinar e verificar se são novos
        for entrada in dados_json:
            codigo_pre_mat = entrada.get("Codigo_Pre_Mat")
            data_execucao = entrada.get("Data_de_execucao")

            # Verificar se o registro já existe no banco
            if codigo_pre_mat and data_execucao and not registro_existe(codigo_pre_mat, data_execucao):
                # Inserir dados na tabela
                cur.execute('''
                INSERT OR IGNORE INTO Extrato_Dynamo (
                    Tipo, Fonte_de_dados, Modo_de_entrada, Data_de_execucao, Codigo_Pre_Mat, Tempo_de_execucao,
                    Descricao_Ingles, Descricao_Portugues, Descricao_Espanhol, Fabricante,
                    If_de_dimensoes, If_de_SGM, If_de_peso, Peso_Tipo, Alt_Tipo, SGM_Tipo,
                    Comp_Tipo, Dim_Tipo, DN_Tipo, File_Path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    entrada.get("Tipo"),
                    entrada.get("Fonte_de_dados"),
                    entrada.get("Modo_de_entrada"),
                    entrada.get("Data_de_execucao"),
                    entrada.get("Codigo_Pre_Mat"),
                    entrada.get("Tempo_de_execucao"),
                    entrada.get("Descricao_Ingles"),
                    entrada.get("Descricao_Portugues"),
                    entrada.get("Descricao_Espanhol"),
                    entrada.get("Fabricante"),
                    entrada.get("If_de_dimensoes"),
                    entrada.get("If_de_SGM"),
                    entrada.get("If_de_peso"),
                    entrada.get("Peso_Tipo"),
                    entrada.get("Alt_Tipo"),
                    entrada.get("SGM_Tipo"),
                    entrada.get("Comp_Tipo"),
                    entrada.get("Dim_Tipo"),
                    entrada.get("DN_Tipo"),
                    entrada.get("File Path")  
                ))
                # Exibir os dados inseridos
                print(f"Dados inseridos: Codigo_Pre_Mat = {codigo_pre_mat}, Data_de_execucao = {data_execucao}")
            else:
                print(f"Registro já existe: Codigo_Pre_Mat = {codigo_pre_mat}, Data_de_execucao = {data_execucao}")

        # Confirmar a transação
        con.commit()

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_json}")
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON. Verifique o formato do arquivo.")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")

# Loop que verifica o JSON a cada 5 segundos
try:
    ultimo_modificado = 0
    while True:
        # Verificar a última modificação do arquivo
        modificado = os.path.getmtime(caminho_json)

        # Se o arquivo foi modificado desde a última verificação
        if modificado != ultimo_modificado:
            print("Alteração detectada no arquivo JSON. Processando...")
            processar_json()
            ultimo_modificado = modificado  # Atualizar o timestamp da última modificação

        # Esperar 5 segundos antes de verificar novamente
        time.sleep(5)

except KeyboardInterrupt:
    print("Execução interrompida pelo usuário.")
finally:
    # Fechar a conexão com o banco de dados
    con.close()
