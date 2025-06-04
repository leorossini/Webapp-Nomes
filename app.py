import requestIBGE as ibge
import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(
    page_title="Frequência de Nomes no Brasil",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # dados
    st.subheader("Frequência de Nomes no Brasil")
    st.markdown("Fonte: Dados do IBGE (Beta por Leo Rossini)")
    nome = st.text_input("Digite um nome para análise:", key="nome_input")
    porProporcao = st.checkbox("Exibir proporção por 100 mil habitantes ao invés de Quantidade por UF", value=True, key="proporcao_checkbox")
    if nome:
        col1, col2 = st.columns(2)
        
        col1.text("Frequência por década:")
        dictFreqDecada = ibge.getFrequenciaNomesPorDecada(nome)
        if dictFreqDecada:
            dfDecada = pd.DataFrame.from_dict(dictFreqDecada, orient='index', columns=['Frequência'])
            dfDecada['Decada'] = dfDecada.index
            col1.line_chart(dfDecada, x="Decada", y='Frequência', y_label='Quantidade')

        col2.text("Frequência por UF:")
        dictFreqUFs = ibge.getFrequenciaNomesPorEstados(nome, porProporcao=porProporcao)
        if dictFreqUFs:
            df = pd.DataFrame.from_dict(dictFreqUFs, orient='index', columns=['Frequência'])
            df['UF'] = df.index.map(ibge.getIdUFs())
            dfShow = df[['UF', 'Frequência']].sort_values(by='UF')
            col2.bar_chart(dfShow, x='UF', y='Frequência',y_label='Quantidade', horizontal=True)
        if not dictFreqDecada:
            alert = st.warning("Nenhum dado encontrado para o nome informado.", icon="⚠️")
            time.sleep(10)
            alert.empty()
            

        


if __name__ == "__main__":
    main()