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

# --- Análise de ROI com Interatividade ---
st.header('Análise de ROI (Questão 2)')
st.markdown('Ajuste os parâmetros abaixo para simular diferentes cenários de ROI:')

# Widgets de entrada para o usuário
col1, col2 = st.columns(2)
with col1:
    receita_esperada_user = st.number_input('Receita Esperada (R$)', min_value=50000, max_value=150000, value=80000, step=1000)
with col2:
    custo_operacional_user = st.number_input('Custo Operacional (R$)', min_value=5000, max_value=50000, value=10000, step=500)

investimento = 50000

# Recalcula o ROI baseado nas entradas do usuário
lucro_simulado = receita_esperada_user - custo_operacional_user
roi_simulado = (lucro_simulado / investimento) * 100

st.subheader('Resultados da Simulação de ROI')
st.markdown(f"**Investimento:** R$ {investimento:,.2f}")
st.markdown(f"**Lucro Calculado:** R$ {lucro_simulado:,.2f}")
st.markdown(f"**ROI Calculado:** **{roi_simulado:.2f}%**")

# Exibe o gráfico de distribuição de ROIs e cenários fixos
try:
    cenarios = pd.read_csv('roi_data.csv')
    receitas_simuladas = np.load('receitas_simuladas.npy')
    
    st.subheader('Distribuição dos ROIs Simulados (Cenários Fixos)')
    rois_simulacao = ((receitas_simuladas - custo_operacional_user) / investimento) * 100
    
    fig_roi, ax_roi = plt.subplots(figsize=(10, 6))
    ax_roi.hist(rois_simulacao, bins=30, color='lightgreen', edgecolor='black')
    ax_roi.axvline(x=0, color='red', linestyle='--', label='ROI = 0%')
    ax_roi.axvline(x=roi_simulado, color='blue', linestyle='--', label=f'ROI (Usuário) = {roi_simulado:.2f}%')
    ax_roi.set_title('Distribuição dos ROIs Simulados')
    ax_roi.set_xlabel('ROI (%)')
    ax_roi.set_ylabel('Frequência')
    ax_roi.legend()
    ax_roi.grid(True)
    st.pyplot(fig_roi)

    # Comentário final da questão 2
    st.markdown(f'''
    - **Comentário:** O ROI esperado de **{cenarios.loc[cenarios['Cenário'] == 'Realista', 'ROI (%)'].iloc[0]:.2f}%** sugere um investimento viável.
    - **Nota:** A interatividade acima demonstra como alterações nos valores de receita e custo afetam o ROI, proporcionando uma ferramenta de análise dinâmica.
    ''')

except FileNotFoundError:
    st.error("Arquivos de dados de ROI não encontrados. Certifique-se de que o pré-cálculo foi realizado e os arquivos estão no local correto.")

st.markdown('---')
st.markdown('**Comentários Finais da Tarefa:**')
st.markdown('''
- A análise de Overbooking sugere que a estratégia inicial de vender 130 passagens é arriscada, excedendo o limite de 7%. O sistema de informações deve ser ajustado para limitar as vendas a 129 passagens.
- A análise de ROI mostra que, embora o investimento seja promissor, há um risco considerável de a receita ficar abaixo do esperado. Recomenda-se um monitoramento contínuo para ajustar a estratégia dinamicamente.
''')
