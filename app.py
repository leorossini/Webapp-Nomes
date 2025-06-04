import requestIBGE as ibge
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Frequência de Nomes no Brasil",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # dados
    st.title("Frequência de Nomes no Brasil")
    st.text("Fonte: Dados do IBGE")
    st.text("Beta por Leo Rossini")
    nome = st.text_input("Digite um nome para análise:", key="nome_input")
    if nome:
        col1, col2 = st.columns(2)
        
        col1.text("Frequência por década:")
        dictFreqDecada = ibge.getFrequenciaNomesPorDecada(nome)
        if dictFreqDecada:
            dfDecada = pd.DataFrame.from_dict(dictFreqDecada, orient='index', columns=['Frequência'])
            dfDecada['Decada'] = dfDecada.index
            col1.line_chart(dfDecada, x="Decada", y='Frequência', y_label='Quantidade')

        col2.text("Frequência por UF:")
        dictFreqUFs = ibge.getFrequenciaNomesPorEstados(nome, porProporcao=False)
        df = pd.DataFrame.from_dict(dictFreqUFs, orient='index', columns=['Frequência'])
        df['UF'] = df.index.map(ibge.getIdUFs())
        dfShow = df[['UF', 'Frequência']].sort_values(by='UF')
        col2.bar_chart(dfShow, x='UF', y='Frequência',y_label='Quantidade', horizontal=True)
        
        


if __name__ == "__main__":
    main()