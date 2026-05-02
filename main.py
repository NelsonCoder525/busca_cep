import streamlit as st
import pandas as pd
import requests



@st.cache_data
def busca_cep(uf, cidade, logradouro):
   
    try:
        uf = uf.upper()
        
        link = f"https://viacep.com.br/ws/{uf}/{cidade}/{logradouro}/json/"
        requisicao = requests.get(link)
        dic_requisicao = requisicao.json()
        for item in dic_requisicao:
            item["cep"] = item["cep"].replace("-", "")
        tabela = pd.DataFrame(dic_requisicao)
        tabela = tabela[["cep", "logradouro", "complemento", "bairro", "localidade", "uf"]]
        return tabela
    except Exception as erro:
        return f"Erro: {erro}"
    
st.set_page_config(layout="wide")
    
st.markdown("<h1 style='text-align: center; font-size: 62px;'>BUSCA DE CEP POR LOGRADOURO DO NELSÃO</h1>", unsafe_allow_html=True)


coluna_esquerda, coluna_meio, coluna_direita = st.columns([1, 2.5, 1])
coluna_direita.image("imagens/meme.gif", width=300)


container = coluna_esquerda.container(border=True)

coluna_container_esquerda, coluna_container_direita = container.columns([1, 1])
    
uf = coluna_container_esquerda.text_input("Digite o Estado (UF)", key="estado", width=200)
cidade = coluna_container_direita.text_input("Digite o Município", key="municipio", width=200)
logradouro = coluna_container_esquerda.text_input("Digite o Logradouro", key="logradouro", width=500)

botao_pesquisar = coluna_container_esquerda.button("Pesquisar")

if botao_pesquisar:
    try: 
        resultado = busca_cep(uf, cidade, logradouro)
        coluna_meio.table(resultado)
    except:
        st.error("Ocorreu um erro ao buscar os dados. Verifique os campos e tente novamente.")