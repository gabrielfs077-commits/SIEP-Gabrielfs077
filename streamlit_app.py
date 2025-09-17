import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Título do aplicativo
st.title('Análise de Overbooking e ROI - SIEP')
st.markdown('---')

# --- Análise de Overbooking ---
st.header('Análise de Overbooking (Questão 1)')

try:
    # Carrega os dados pré-calculados de overbooking
    df_overbooking = pd.read_csv('overbooking_data.csv')
    
    # Exibe a tabela de risco
    st.subheader('Tabela de Risco de Overbooking')
    st.dataframe(df_overbooking)
    
    # Exibe o gráfico de overbooking
    st.subheader('Gráfico de Probabilidade de Overbooking')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_overbooking['Passagens Vendidas'], df_overbooking['Probabilidade de Overbooking (%)'], marker='o')
    ax.axhline(y=7, color='red', linestyle='--', label='Limite de 7%')
    
    # Encontra o limite de venda seguro
    limite_venda = df_overbooking[df_overbooking['Probabilidade de Overbooking (%)'] <= 7]['Passagens Vendidas'].max()
    ax.axvline(x=limite_venda, color='green', linestyle='--', label=f'Limite seguro: {limite_venda}')
    
    ax.set_title('Probabilidade de Overbooking x Passagens Vendidas')
    ax.set_xlabel('Passagens Vendidas')
    ax.set_ylabel('Probabilidade de Overbooking (%)')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    
    # Comentário final da questão 1
    st.markdown(f'''
    - **Probabilidade de Overbooking (130 passagens):** {df_overbooking.loc[df_overbooking['Passagens Vendidas'] == 130, 'Probabilidade de Overbooking (%)'].iloc[0]:.2f}%
    - **Limite de Venda Seguro:** Para manter o risco abaixo de 7%, a empresa não deve vender mais que **{limite_venda}** passagens.
    ''')

except FileNotFoundError:
    st.error("Arquivo 'overbooking_data.csv' não encontrado. Certifique-se de que o pré-cálculo foi realizado e o arquivo está no local correto.")

st.markdown('---')

# --- Análise de ROI ---
st.header('Análise de ROI (Questão 2)')

try:
    # Carrega os dados pré-calculados do ROI
    cenarios = pd.read_csv('roi_data.csv')
    receitas_simuladas = np.load('receitas_simuladas.npy')
    
    # Exibe a tabela de cenários
    st.subheader('Cenários de ROI')
    st.dataframe(cenarios)

    # Exibe o gráfico de distribuição de receitas
    st.subheader('Distribuição das Receitas Simuladas')
    fig_receitas, ax_receitas = plt.subplots(figsize=(10, 6))
    ax_receitas.hist(receitas_simuladas, bins=30, color='lightblue', edgecolor='black')
    ax_receitas.axvline(x=60000, color='red', linestyle='--', label='Meta mínima R$60k')
    ax_receitas.axvline(x=80000, color='green', linestyle='--', label='Meta esperada R$80k')
    ax_receitas.set_title('Distribuição das Receitas Simuladas')
    ax_receitas.set_xlabel('Receita (R$)')
    ax_receitas.set_ylabel('Frequência')
    ax_receitas.legend()
    ax_receitas.grid(True)
    st.pyplot(fig_receitas)

    # Exibe o gráfico de distribuição dos ROIs
    st.subheader('Distribuição dos ROIs Simulados')
    investimento = 50000
    custo_operacional = 10000
    rois = ((receitas_simuladas - custo_operacional) / investimento) * 100
    
    fig_roi, ax_roi = plt.subplots(figsize=(10, 6))
    ax_roi.hist(rois, bins=30, color='lightgreen', edgecolor='black')
    ax_roi.axvline(x=0, color='red', linestyle='--', label='ROI = 0%')
    ax_roi.axvline(x=cenarios.loc[cenarios['Cenário'] == 'Realista', 'ROI (%)'].iloc[0], color='blue', linestyle='--', label='ROI esperado')
    ax_roi.set_title('Distribuição dos ROIs Simulados')
    ax_roi.set_xlabel('ROI (%)')
    ax_roi.set_ylabel('Frequência')
    ax_roi.legend()
    ax_roi.grid(True)
    st.pyplot(fig_roi)

    # Comentário final da questão 2
    st.markdown(f'''
    - **ROI Esperado:** {cenarios.loc[cenarios['Cenário'] == 'Realista', 'ROI (%)'].iloc[0]:.2f}%
    - **Chance de Receita abaixo de R$ 60.000:** {(np.mean(receitas_simuladas < 60000) * 100):.2f}%
    ''')

except FileNotFoundError:
    st.error("Arquivos de dados de ROI não encontrados. Certifique-se de que o pré-cálculo foi realizado e os arquivos estão no local correto.")

st.markdown('---')
st.markdown('**Comentários Finais da Tarefa:**')
st.markdown('''
- A análise de Overbooking sugere que a estratégia inicial de vender 130 passagens é arriscada, excedendo o limite de 7%. O sistema de informações deve ser ajustado para limitar as vendas a 129 passagens.
- A análise de ROI mostra que, embora o investimento seja promissor, há um risco considerável de a receita ficar abaixo do esperado. Recomenda-se um monitoramento contínuo para ajustar a estratégia dinamicamente.
''')
