import streamlit as st
import sqlite3
import pandas as pd

def app():

    st.header("Sobre o TCP")
    texto_sobre = '''
    O TCP começou como uma rotina no Dynamo para a criação de famílias mecânicas, mas evoluiu para um sistema que integra o Revit, SGM e este painel interativo.

    No Revit, o TCP é capaz de criar, excluir ou modificar parâmetros de uma família, seja ela existente ou nova, com base em informações como Descrição (em português, inglês e espanhol), Dimensões, Peso e Fabricante, todas extraídas do SGM. Além disso, o sistema permite a obtenção de parâmetros derivados, como Diâmetro Nominal, Comprimento e Altura, a partir da mesma fonte de dados. Ele também identifica se a família deve ser de tipo ou instanciada e aplica todas as padronizações necessárias para atender ao padrão estabelecido pela mecânica.

    A partir deste painel, é possível:
    - Verificar se uma família está padronizada e incluída na biblioteca;
    - Visualizar as últimas famílias inseridas ou reformuladas na biblioteca;
    - Acompanhar o uso da ferramenta nos últimos meses;
    - Analisar a economia de tempo gerada pelo sistema em comparação com a criação manual de famílias (estimada entre 15 a 20 minutos por família).

    Além dessas funcionalidades, o TCP automatiza várias tarefas, como a atualização de planilhas de controle, envio de mensagens e armazenamento de dados de uso em um banco de dados.'''
    st.markdown(texto_sobre)

    # Verificar se a contagem de famílias está no session_state

    contagem_familias = st.session_state['contagem_familias']


    st.dataframe(contagem_familias, use_container_width=True)


