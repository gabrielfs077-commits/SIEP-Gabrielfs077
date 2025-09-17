import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# Título do aplicativo
st.title('Análise de Overbooking e ROI - SIEP')
st.markdown('---')

# --- Análise de Overbooking Interativa ---
st.header('Análise de Overbooking')
st.markdown('Ajuste os parâmetros abaixo para simular diferentes cenários de Overbooking:')

# Widgets de entrada para o usuário (Questão 1)
col1, col2 = st.columns(2)
with col1:
    capacidade_user = st.number_input('Capacidade do Avião', min_value=100, max_value=200, value=120, step=1)
with col2:
    p_comparecimento_user = st.number_input('Probabilidade de Comparecimento (%)', min_value=0.0, max_value=100.0, value=88.0, step=0.1) / 100

# Parâmetros de cálculo
max_vendidos = int(capacidade_user * 1.2)  # Aumenta o limite de vendas para a simulação
valores_vendidos = list(range(capacidade_user, max_vendidos + 1))
probs_user = [1 - binom.cdf(capacidade_user, n, p_comparecimento_user) for n in valores_vendidos]

df_overbooking_user = pd.DataFrame({
    'Passagens Vendidas': valores_vendidos,
    'Probabilidade de Overbooking (%)': np.array(probs_user) * 100
})

# Encontra o limite de venda seguro com a nova probabilidade
try:
    limite_venda_user = df_overbooking_user[df_overbooking_user['Probabilidade de Overbooking (%)'] <= 7]['Passagens Vendidas'].max()
    if np.isnan(limite_venda_user):
        limite_venda_user = "N/A (Risco sempre alto)"
except:
    limite_venda_user = "N/A (Risco sempre alto)"

# Exibe o gráfico de overbooking
st.subheader('Gráfico de Probabilidade de Overbooking')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_overbooking_user['Passagens Vendidas'], df_overbooking_user['Probabilidade de Overbooking (%)'], marker='o')
ax.axhline(y=7, color='red', linestyle='--', label='Limite de 7%')

if isinstance(limite_venda_user, int):
    ax.axvline(x=limite_venda_user, color='green', linestyle='--', label=f'Limite seguro: {limite_venda_user}')
else:
    ax.axvline(x=capacidade_user, color='orange', linestyle='--', label='Limite de Venda: Capacidade')

ax.set_title('Probabilidade de Overbooking x Passagens Vendidas')
ax.set_xlabel('Passagens Vendidas')
ax.set_ylabel('Probabilidade de Overbooking (%)')
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.markdown(f'''
- **Limite de Venda Seguro:** Para manter o risco abaixo de 7%, a empresa não deve vender mais que **{limite_venda_user}** passagens.
- **Análise:** Aumentar a probabilidade de comparecimento reduz o número de passagens extras que podem ser vendidas com segurança.
''')

st.markdown('---')

# --- Análise de ROI com Interatividade ---
st.header('Análise de ROI')
st.markdown('Ajuste os parâmetros abaixo para simular diferentes cenários de ROI:')

# Widgets de entrada para o usuário (Questão 2)
col3, col4 = st.columns(2)
with col3:
    receita_esperada_user = st.number_input('Receita Esperada (R$)', min_value=50000, max_value=150000, value=80000, step=1000)
with col4:
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
st.markdown('---')
st.header('Análise e Comentários Finais da Tarefa')

st.markdown('''
A interatividade deste dashboard não serve apenas para visualizar os resultados, mas para transformá-lo em uma ferramenta dinâmica de análise e tomada de decisão. As alterações nos parâmetros revelam insights importantes e ajudam a quantificar os riscos e oportunidades de forma mais precisa.
''')

st.subheader('Importância da Interatividade na Análise de Overbooking')
st.markdown('''
A capacidade de ajustar a **Probabilidade de Comparecimento** e a **Capacidade do Avião** diretamente no dashboard demonstra o valor de um sistema de informação ágil.

* **Entendendo o Risco Dinâmico:** Um aumento na probabilidade de comparecimento de 88% para 90%, por exemplo, aumenta drasticamente o risco de overbooking para um mesmo número de passagens vendidas. A ferramenta permite que a gerência entenda essa sensibilidade e defina um limite de vendas mais conservador em situações de alta probabilidade de comparecimento (como em feriados).
* **Tomada de Decisão Baseada em Dados:** Em vez de depender de uma regra fixa, a equipe pode usar a ferramenta para estabelecer limites de vendas personalizados. Se a equipe de marketing realizar uma campanha para melhorar o comparecimento, o dashboard pode ser usado para simular o novo cenário e ajustar a estratégia de overbooking de forma proativa.
''')

st.subheader('Importância da Interatividade na Análise de ROI')
st.markdown('''
A interatividade na análise de **Retorno sobre o Investimento (ROI)** é crucial para a viabilidade financeira de um projeto. Os campos para **Receita Esperada** e **Custo Operacional** permitem que a gestão explore o impacto de diferentes variáveis em tempo real.

* **Análise de Sensibilidade:** Ao alterar a receita esperada, a equipe pode simular o impacto de um desempenho de vendas superior ou inferior ao previsto. Isso ajuda a entender qual é o "ponto de equilíbrio" do projeto e como a receita mínima afeta o ROI.
* **Negociação e Otimização de Custos:** A ferramenta se torna um recurso valioso em negociações. Se os custos operacionais forem mais altos do que o esperado, a gerência pode usar o dashboard para determinar se o investimento ainda vale a pena ou se é preciso renegociar com fornecedores.
* **Planejamento de Cenários:** O dashboard possibilita um planejamento mais robusto e realista, permitindo que a empresa se prepare para cenários otimistas e pessimistas. Ele serve como uma prova visual de que o projeto é viável, mas que também requer um monitoramento contínuo.
''')
