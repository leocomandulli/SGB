import sqlite3
import win32com.client as win32
import time

def atualizar_e_processar_dados():
    # Abrir o Excel com o win32com
    excel = win32.Dispatch('Excel.Application')
    excel.Visible = False  # Para rodar em background

    # 1. Entrar no arquivo Excel
    excel_path = r'G:\DepMec\PRODUÇÃO\Rotinas Dynamo\DataBase\Controle_Biblioteca.xlsx'
    wb = excel.Workbooks.Open(excel_path)
    print("Planilha Excel aberta")

    # 2. Atualizar a entrada de dados
    wb.RefreshAll()
    excel.CalculateFull()  # Recalcula todas as fórmulas na planilha
    print("Dados atualizados no Excel")

    # 3. Extrair todos os dados, preenchendo valores nulos com "Não definido"
    ws = wb.Sheets['Famílias inseridas']
    max_row = ws.UsedRange.Rows.Count

    dados_planilha = [(ws.Cells(row, 1).Value if ws.Cells(row, 1).Value is not None else "Não definido",  # Código_Pre_Mat
                   ws.Cells(row, 2).Value if ws.Cells(row, 2).Value is not None else "Não definido",  # Elaborador
                   ws.Cells(row, 3).Value if ws.Cells(row, 3).Value is not None else "Não definido")  # Status_Biblioteca
                  for row in range(2, max_row + 1)]

    print(f"Extraído {len(dados_planilha)} registros da planilha")

    # 4. Conectar ao banco de dados SQLite "TCP"
    sqlite_path = 'TCP.db'
    con = sqlite3.connect(sqlite_path)
    cur = con.cursor()

    # Criação da tabela (caso não exista)
    cur.execute('''CREATE TABLE IF NOT EXISTS Base_de_Familias (
                    Codigo_Pre_Mat TEXT PRIMARY KEY,
                    Elaborador TEXT,
                    Status_Biblioteca TEXT)''')

    # 5. Aplicar os dados em uma tabela do SQLite
    for codigo_pre_mat, elaborador, status_biblioteca in dados_planilha:
        cur.execute('''INSERT OR IGNORE INTO Base_de_Familias (Codigo_Pre_Mat, Elaborador, Status_Biblioteca) 
                        VALUES (?, ?, ?)''', (codigo_pre_mat, elaborador, status_biblioteca))

    # 6. Salvar o arquivo SQLite
    con.commit()
    con.close()
    print("Dados atualizados no SQLite")

    # 7. Salvar o arquivo Excel novamente após atualizar
    wb.Save()
    wb.Close()
    excel.Quit()
    print("Arquivo Excel salvo e fechado")

# Repetição a cada 2 horas
while True:
    atualizar_e_processar_dados()
    print("Processo completo. Aguardando 2 horas para a próxima execução.")
    time.sleep(2 * 60 * 60)  # Esperar 2 horas (2h * 60min/h * 60s/min)
