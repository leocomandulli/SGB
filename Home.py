import streamlit as st
import sqlite3
import pandas as pd

def app():
    texto_sobre = '''
        # Sobre o TCP e o SGB    
    
        
        ## Template para criação de parâmetros (TCP)

        O **TCP** iniciou como uma rotina no **Dynamo** para a criação de famílias mecânicas, mas evoluiu para um sistema integrado ao **Revit**, **SGM** e a este painel interativo, denominado **SGB (Sistema de Gerenciamento de Bibliotecas)**.

        ### Funcionalidades do TCP

        Dentro do **Revit**, o TCP tem a capacidade de:

        - Criar, excluir ou modificar parâmetros de uma família, seja ela existente ou nova, com base em informações extraídas do **SGM**, como:
            - Descrição (em português, inglês e espanhol)
            - Dimensões
            - Peso
            - Fabricante
            - Derivar parâmetros adicionais, como **Diâmetro Nominal**, **Comprimento** e **Altura**, a partir dessa mesma base de dados.
            - Identificar se a família deve ser do tipo ou instanciada, aplicando as padronizações necessárias para atender aos critérios estabelecidos pela mecânica do **DUAE**.

        Após essas operações, o **TCP** gera um **relatório** para atualizar a base de dados, garantindo que tenhamos as informações mais recentes sobre as famílias. Em seguida, a aplicação salva o arquivo editado no diretório adequado e com o nome conforme o **padrão estabelecido**.

        ## Sistema de Gerenciamento de Bibliotecas (SGB)
        ### Funcionalidades do SGB

        Posteriormente, surgiu o **SGB**, uma ferramenta que:

        - Transmite informações e relatórios sobre a biblioteca.
        - Acessa arquivos sem a necessidade de navegar manualmente pelos diretórios.

        ##### Biblioteca

        A partir deste painel, é possível:

        - Verificar se uma família está **padronizada** e inclusa na biblioteca.
        - **Filtrar** as listagens entre os seguintes status: 
            - Ok
            - Erro
            - Pendente
            - Atualizado
        - Obter um **resumo quantitativo** desses parâmetros.

        ##### Busca de Família

        É possível procurar um material pelo **código SGM**, obtendo as seguintes informações:
        - **Elaborador**
        - **Status**
        - **Última atualização**
        - **Imagem da família**
        - **Link para download do arquivo**

        ##### Últimos Registros

        Visualize as **últimas famílias** inseridas ou reformuladas na biblioteca, com as seguintes informações:
        - Imagem
        - Data de atualização
        - Link para download

        ##### Dashboard (em construção)

        Ainda em construção, o **Dashboard** permitirá:
        - Acompanhar o uso da ferramenta nos últimos meses.
        - Analisar a **economia de tempo** gerada pelo sistema em comparação com a criação manual de famílias (estimada entre **15 a 20 minutos por família**).

        ## Automatizações

        Além dessas funcionalidades, o **SGB** automatiza várias tarefas, como:
        - Atualização de **planilhas de controle**
        - Envio de **mensagens**
        - Armazenamento de **dados de uso** em um banco de dados.
        '''
    st.markdown(texto_sobre)


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



