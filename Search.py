import os
import sqlite3
import pandas as pd
import streamlit as st
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

    # Carrega o extrato_biblioteca do session state para a página
    extrato_biblioteca = st.session_state['extrato_biblioteca']

    # Interface
    st.title("Buscador de famílias")

    # Elemento de busca das famílias
    search_query = st.text_input("Digite a família que procura:")

    # Faz a busca no banco de dados
    if search_query:
        # Filtra a tabela com base na busca
        filtered_data = extrato_biblioteca.apply(
            lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1
        )

        # Obtém as linhas correspondentes
        results = extrato_biblioteca[filtered_data]
        
        if not results.empty:
            familia_procurada = results.iloc[0]['Codigo_Pre_Mat']
            elaborador = results.iloc[0]['Elaborador']
            status_biblioteca = results.iloc[0]['Status_Biblioteca']
            ultima_atualizacao = results.iloc[0]['Ultima_Atualizacao']
            File_Path = results.iloc[0]['File_Path']

            # Verifica se File_Path não é None antes de construir o caminho
            if File_Path:
                Caminho_Arquivo = os.path.abspath(File_Path)
            else:
                Caminho_Arquivo = None

            # Exibir as informações
            st.subheader("Família encontrada")

            # Configura colunas para exibir a imagem e o texto lado a lado
            col1, col2 = st.columns([1, 2])  # Ajusta o tamanho das colunas, se necessário

            with col1:
                imagem = exibir_imagem(search_query)
                if imagem:
                    st.image(imagem, caption=f"Imagem de {familia_procurada}", use_column_width=True)
                else:
                    st.write("Imagem não encontrada")

            with col2:
                st.write(f"Família procurada: {familia_procurada}")
                st.write(f"Elaborador: {elaborador}")
                st.write(f"Status na biblioteca: {status_biblioteca}")
                st.write(f"Última atualização: {ultima_atualizacao}")

                if Caminho_Arquivo:
                    with open(Caminho_Arquivo, "rb") as file:
                        st.download_button(
                            label="Baixar arquivo",
                            data=file,
                            file_name=os.path.basename(Caminho_Arquivo)
                        )
                else:
                    st.write("Arquivo não disponível para download")

        else:
            st.subheader("Nenhum resultado encontrado.")
