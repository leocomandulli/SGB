import sqlite3
import pandas as pd
import streamlit as st
import base64
import os
from PIL import Image


def app():
    # Função para buscar e exibir uma imagem correspondente
    def exibir_imagem(nome_familia):
        # Caminho do arquivo de imagem
        caminho_imagem = f"images/{nome_familia}.png"
        
        # Verifica se a imagem existe
        if os.path.exists(caminho_imagem):
            # Carrega e exibe a imagem
            imagem = Image.open(caminho_imagem)
            return imagem
        else:
            return None

    def gerar_botao_download(file_path):
        # Verifica se o file_path é válido e o arquivo existe
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, "rb") as file:
                    file_data = file.read()
                    b64 = base64.b64encode(file_data).decode()  # Codifica o arquivo em base64
                return f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">Download</a>'
            except PermissionError:
                # Mensagem amigável para problemas de permissão
                return "Sem permissão"
        else:
            # Mensagem caso o arquivo não exista
            return "Arquivo insdisponível"
    # ----- Tabela de Últimos Registros -----

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('TCP.db')

    # Carregar dados da tabela 'Extrato_Dynamo'
    query = "SELECT Codigo_Pre_Mat, Data_de_execucao, File_Path FROM Extrato_Dynamo WHERE Codigo_Pre_Mat IS NOT NULL"
    df_extrato = pd.read_sql_query(query, conn)

    # Fechar a conexão após carregar os dados
    conn.close()

     # Remover registros onde Codigo_Pre_Mat é 'none' ou None
    df_extrato = df_extrato[(df_extrato['Codigo_Pre_Mat'].notna()) & (df_extrato['Codigo_Pre_Mat'] != "None")]


    # Remover registros duplicados, mantendo apenas o último inserido
    df_extrato = df_extrato.drop_duplicates(subset='Codigo_Pre_Mat', keep='last')

    # Ordenar pelo campo 'Data_de_execucao' em ordem decrescente e selecionar os 5 últimos registros
    df_ultimos_registros = df_extrato.sort_values(by='Data_de_execucao', ascending=True).head(5)

    # ----- Exibição dos Últimos Registros em Três Colunas -----

    st.subheader("Últimos Registros da Tabela Extrato_Dynamo:")

    # Configuração das colunas para exibir as informações
    for _, row in df_ultimos_registros.iterrows():
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])

        # Exibir imagem correspondente na coluna 1
        with col1:
            imagem = exibir_imagem(row['Codigo_Pre_Mat'])
            if imagem:
                st.image(imagem, caption=f"Imagem de {row['Codigo_Pre_Mat']}", use_column_width=True)
            else:
                st.write("Imagem não encontrada")
        
        # Exibir Código SGM na coluna 2
        with col2:
            st.write("")
            st.write("**Código SGM:**")
            st.write(row['Codigo_Pre_Mat'])

        # Exibir Data de Execução na coluna 3
        with col3:
            st.write("")
            st.write("**Data de Execução:**")
            st.write(row['Data_de_execucao'])

        # Botão de Download para o File_Path na coluna 4
        with col4:
        # Exibe o botão de download somente se o arquivo estiver disponível
            st.markdown(gerar_botao_download(row['File_Path']), unsafe_allow_html=True)
        # Linha divisória entre registros
        st.markdown("---")