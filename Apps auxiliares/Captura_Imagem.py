'''
ESSA APLICAÇÃO SOLICITA UM DIRETÓRIO E A PARTIR DELE, EXECUTA ESSAS AÇÕES:
    1. ABRE A FAMÍLIA;
    2. APLICA O MODO SOMBREADO;
    3. APLICA DETALHE ALTO;
    4. COLOCA NA VISTA 3D;
    5. TIRA UM PRINT;
    6. ARMAZENA A IMAGEM COM O CÓDIGO PRE_MAT NA PASTA DE IMAGENS.
'''
import os
import pyautogui
import win32gui
import win32con
import time
import sqlite3
from PIL import Image
import tkinter as tk
from tkinter import filedialog  # Importando filedialog para selecionar diretórios


# Função para abrir um arquivo Revit que já está em execução
def abrir_arquivo_revit(caminho_arquivo):
    caminho_arquivo = os.path.normpath(caminho_arquivo)  # Normaliza o caminho
    try:
        os.startfile(caminho_arquivo)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.hotkey('s', 'o', 'm')
        time.sleep(1)
        pyautogui.hotkey('d', 'd')
        time.sleep(1)
        pyautogui.hotkey('i', 'n')
        time.sleep(1)
        pyautogui.hotkey('3', 'd')
        time.sleep(1.5) 

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}. Verifique o caminho.")

# Função para fechar o arquivo Revit
def fechar_arquivo_revit():
    print("Fechando o arquivo Revit...")
    pyautogui.hotkey('ctrl', 'w')  # Atalho para fechar o arquivo no Revit
    pyautogui.press('right')
    pyautogui.press('enter')
    time.sleep(2)  # Aguardar o fechamento do arquivo

# Função para trazer a janela do Revit para frente
def bring_revit_to_front():
    def enum_windows(hwnd, windows):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd):
            windows.append(hwnd)

    windows = []
    win32gui.EnumWindows(enum_windows, windows)
    
    for hwnd in windows:
        window_text = win32gui.GetWindowText(hwnd)
        if "Revit" in window_text:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restaura a janela se minimizada
            win32gui.SetForegroundWindow(hwnd)  # Traz a janela para frente
            break

# Função para selecionar o diretório do Revit
def selecionar_diretorio():
    root = tk.Tk()
    root.withdraw()  # Ocultar a janela principal
    diretorio_revit = filedialog.askdirectory(title="Selecione o diretório do Revit")
    return diretorio_revit

# Caminhos para diretórios
diretorio_revit = selecionar_diretorio()  # Obtenha o diretório do usuário
diretorio_imagens = r"C:\Users\lsco\OneDrive - Intertechne Consultores SA\Documentos\APP - TCP\APP\Images"
caminho_banco = r"C:\Users\lsco\OneDrive - Intertechne Consultores SA\Documentos\APP - TCP\APP\TCP.db"  # Substitua pelo caminho correto para seu banco de dados

# Função para atualizar o banco de dados com o caminho da imagem
def atualizar_banco(nome_arquivo, caminho_imagem):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(caminho_banco)
        cursor = conn.cursor()
        
        # Atualizar a coluna 'Imagem' na tabela 'Base_de_Familias' onde 'Codigo_Pre_Mat' é igual ao nome_arquivo
        cursor.execute("""
            UPDATE Base_de_Familias
            SET Imagem = ?
            WHERE Codigo_Pre_Mat = ?
        """, (caminho_imagem, nome_arquivo))
        
        # Confirmar as mudanças
        conn.commit()
        print(f"Atualizado: {nome_arquivo} com o caminho da imagem: {caminho_imagem}")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar o banco de dados: {e}")
    finally:
        # Fechar a conexão
        if conn:
            conn.close()

# Função para atualizar o banco de dados com a pasta inserida
def atualizar_banco_imagens(diretorio_revit):
    try:
                # Extrair apenas o nome da pasta após a última barra invertida
        nome_pasta = os.path.basename(diretorio_revit)
        # Conectar ao banco de dados
        conn = sqlite3.connect(caminho_banco)
        cursor = conn.cursor()
        
        # Criar a tabela Controle_Imagens se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Controle_Imagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Pastas_executadas TEXT
            )
        """)
        
        # Atualizar a coluna 'Imagem' na tabela 'Base_de_Familias' onde 'Codigo_Pre_Mat' é igual ao nome_arquivo
        cursor.execute("""
            INSERT INTO Controle_Imagens (Pastas_executadas)
            VALUES (?)
        """, (nome_pasta,))
        
        # Confirmar as mudanças
        conn.commit()
        print(f"Pasta {nome_pasta} adicionada ao controle. ")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar o banco de dados de imagem: {e}")
    finally:
        # Fechar a conexão
        if conn:
            conn.close()


# Função para capturar e salvar imagens dos arquivos Revit
def capturar_imagem_revit():
    # Verifica se há subpastas no diretório Revit
    has_subfolders = False
    for root, dirs, files in os.walk(diretorio_revit):
        if dirs:  # Se houver subpastas
            has_subfolders = True
            break

    if has_subfolders:
        # Itera sobre cada subpasta e executa a função
        for root, dirs, files in os.walk(diretorio_revit):
            for arquivo in files:
                caminho_arquivo = os.path.join(root, arquivo)
                nome_arquivo = arquivo[:6]  # Pegar os primeiros 6 caracteres do nome do arquivo

                print(f"Abrindo o arquivo {arquivo} em {root}...")
                abrir_arquivo_revit(caminho_arquivo)
                bring_revit_to_front()  # Traz a janela do Revit para frente
                time.sleep(2)  # Aguarda o Revit carregar o arquivo
                
                # Captura da tela
                screenshot = pyautogui.screenshot()

                # Define a área de recorte (ajuste conforme necessário para a área de modelagem)
                area_recorte = (450, 200, 1400, 940)  # Ajuste conforme a posição e o tamanho desejado

                # Recortar a imagem
                imagem_recortada = screenshot.crop(area_recorte)

                # Caminho para salvar a imagem com os 6 primeiros caracteres do arquivo
                caminho_imagem = os.path.join(diretorio_imagens, f"{nome_arquivo}.png")

                # Salvar a imagem recortada
                imagem_recortada.save(caminho_imagem)
                print(f"Imagem salva como: {caminho_imagem}")

                fechar_arquivo_revit()
                print(f"Fechando o arquivo {arquivo}...")

                # Atualizar o banco de dados com o caminho da imagem
                atualizar_banco(nome_arquivo, caminho_imagem)
                
                time.sleep(2)  # Tempo de espera para o próximo arquivo

    else:
        # Se não houver subpastas, executa a função diretamente no diretório
        for arquivo in os.listdir(diretorio_revit):
            caminho_arquivo = os.path.join(diretorio_revit, arquivo)
            nome_arquivo = arquivo[:6]  # Pegar os primeiros 6 caracteres do nome do arquivo

            print(f"Abrindo o arquivo {arquivo} em {diretorio_revit}...")
            abrir_arquivo_revit(caminho_arquivo)
            bring_revit_to_front()  # Traz a janela do Revit para frente
            time.sleep(2)  # Aguarda o Revit carregar o arquivo
            
            # Captura da tela
            screenshot = pyautogui.screenshot()

            # Define a área de recorte (ajuste conforme necessário para a área de modelagem)
            area_recorte = (450, 200, 1400, 940)  # Ajuste conforme a posição e o tamanho desejado

            # Recortar a imagem
            imagem_recortada = screenshot.crop(area_recorte)

            # Caminho para salvar a imagem com os 6 primeiros caracteres do arquivo
            caminho_imagem = os.path.join(diretorio_imagens, f"{nome_arquivo}.png")

            # Salvar a imagem recortada
            imagem_recortada.save(caminho_imagem)
            print(f"Imagem salva como: {caminho_imagem}")

            fechar_arquivo_revit()
            print(f"Fechando o arquivo {arquivo}...")

            # Atualizar o banco de dados com o caminho da imagem
            atualizar_banco(nome_arquivo, caminho_imagem)
            
            time.sleep(2)  # Tempo de espera para o próximo arquivo

    atualizar_banco_imagens(diretorio_revit)
    print("Pasta finalizada com sucesso")

# Chamar a função para executar a captura de imagens
if __name__ == "__main__":
    capturar_imagem_revit()
