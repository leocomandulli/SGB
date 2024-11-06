import sqlite3
import pandas as pd
import streamlit as st
import sqlite3
import os

def app():
    # ----- Leitura do banco de Dados -----
    def load_data():
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('TCP.db')
        cursor = conn.cursor()

        # Carregar dados da tabela 'Base_de_Familias'
        query = "SELECT * FROM Base_de_Familias"
        df = pd.read_sql_query(query, conn)

        # Fechar a conexão após carregar os dados
        conn.close()
        return df

    # Adiciona a leitura do banco ao session_state
    extrato_biblioteca = load_data()
    st.session_state["extrato_biblioteca"] = extrato_biblioteca

    # Puxa as informações do db do sessiin state
    extrato_biblioteca = st.session_state['extrato_biblioteca']

    # Selecionar o status da biblioteca
    st.title("Famílias presentes na biblioteca:")



    # ----- Botão de filtragem -----
    # Inicializando o estado de visibilidade - Filtro oculto
    if 'mostrar' not in st.session_state:
        st.session_state.mostrar = False
    # Função para alternar a visibilidade
    def toggle_visibilidade():
        st.session_state.mostrar = not st.session_state.mostrar
    # Botão que altera o texto dependendo do estado
    botao_filtro = "Ocultar Filtro" if st.session_state.mostrar else "Mostrar Filtro"
    if st.button(botao_filtro):
        toggle_visibilidade()



    # ----- Colorir o fundo de acordo com o status -----
    # Função para aplicar cores de acordo com o status
    def colorir_status(status):
        if status == 'OK':
            return 'background-color: green; color: white'
        elif status == 'Pendente':
            return 'background-color: yellow'
        elif status == 'Erro':
            return 'background-color: red'


    # ----- Tatamento de dados para a tabela -----
    # Renomear colunas para a tabela
    df_renomeado = extrato_biblioteca.rename(columns={'Status_Biblioteca': 'Status da Biblioteca', 'Codigo_Pre_Mat': 'Código SGM'})
    # Selecionar apenas as colunas renomeadas
    df_renomeado = df_renomeado[['Código SGM', 'Status da Biblioteca']]
    # Aplicar a função de cor na coluna 'Status da Biblioteca'
    df_colored = df_renomeado.style.applymap(colorir_status, subset=['Status da Biblioteca'])

    
    # ----- Tabela de Status -----
    # Seção com extrato da biblioteca - varia pelo botão de filtro
    st.subheader("Extrato da biblioteca:")
    if st.session_state.mostrar:
        # Exibir o filtro
        status_unicos = df_renomeado['Status da Biblioteca'].unique()
        status_selecionado = st.multiselect("Filtrar por Status na biblioteca:", status_unicos, default=status_unicos)
        df_filtrado = df_renomeado[df_renomeado['Status da Biblioteca'].isin(status_selecionado)]
        st.write(f"Total de famílias no filtro selecionado: {len(df_filtrado)}")
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        # Exibir tabela sem filtro
        st.write(f"Total de famílias: {len(df_renomeado)}")
        st.dataframe(df_colored, use_container_width=True)

    st.markdown("---")



    # ----- Definição da tabela de contagem -----
    #Tabela lateral com contagem dos status
    contagem = df_renomeado['Status da Biblioteca'].value_counts()
    contagem.name = "Qtd. de famílias:"
    print(contagem)
    # Armazenar no session_state para usar em outras páginas
    st.session_state['contagem_familias'] = contagem

    # ----- Resmuo de status -----
    st.subheader("Resumo de status:")
    contagem_familias = st.session_state['contagem_familias']
    st.dataframe(contagem_familias, use_container_width=True)