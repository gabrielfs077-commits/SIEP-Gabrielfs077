import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
import pandas as pd

# Definindo a configuração da página
st.set_page_config(
    page_title="Aérea Confiável - Análise de Overbooking e ROI",
    layout="wide",
)

# Título principal e cabeçalho
st.title("Sistema de Análise de Decisão da Aérea Confiável")
st.markdown("Bem-vindo ao sistema de análise de overbooking e ROI. Utilize os controles na barra lateral para simular diferentes cenários.")

# =========================================================
# Barra Lateral com Controles Interativos
# =========================================================

st.sidebar.header("Controles de Simulação")

# Controle para o número de passagens vendidas (Módulo 1)
st.sidebar.subheader("Análise de Overbooking")
capacidade = 120
p_comparecimento = 0.88
vendas_max = 140
vendidos_slider = st.sidebar.slider(
    "Número de Passagens Vendidas",
    min_value=120,
    max_value=vendas_max,
    value=130,
    step=1
)

st.sidebar.markdown("---")

# Controles para o cenário de ROI (Módulo 2)
st.sidebar.subheader("Análise de ROI")
investimento_input = st.sidebar.number_input(
    "Custo de Investimento Inicial (R$)",
    min_value=10000,
    max_value=100000,
    value=50000,
    step=5000
)

receita_esperada_input = st.sidebar.number_input(
    "Aumento de Receita Esperada (R$)",
    min_value=20000,
    max_value=120000,
    value=80000,
    step=5000
)

custo_operacional = 10000

# =========================================================
# Abas para Organização do Conteúdo Principal
# =========================================================

tab1, tab2, tab3 = st.tabs(["Análise de Overbooking", "Análise de ROI", "Conclusão"])

with tab1:
    st.header("Análise de Overbooking")
    st.markdown("Use o slider na barra lateral para ver como a probabilidade de overbooking muda com o número de passagens vendidas.")

    # Cálculo da probabilidade de overbooking
    prob_overbooking_atual = 1 - binom.cdf(capacidade, vendidos_slider, p_comparecimento)
    st.metric(
        label=f"Probabilidade de Overbooking com {vendidos_slider} passagens",
        value=f"{prob_overbooking_atual:.2%}"
    )

    # Gráfico da probabilidade de overbooking
    st.subheader("Gráfico de Risco de Overbooking")
    valores_vendidos = list(range(capacidade, vendas_max + 1))
    probs_overbooking = [1 - binom.cdf(capacidade, n, p_comparecimento) for n in valores_vendidos]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(valores_vendidos, np.array(probs_overbooking) * 100, marker='o', label='Risco de Overbooking')
    ax.axhline(y=7, color='red', linestyle='--', label='Limite de 7% (meta da gestão)')
    ax.set_title("Probabilidade de Overbooking vs. Passagens Vendidas")
    ax.set_xlabel("Passagens Vendidas")
    ax.set_ylabel("Probabilidade de Overbooking (%)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Identificando o limite de risco
    limite_venda = next((n for n, p in zip(valores_vendidos, probs_overbooking) if p <= 0.07), None)
    st.success(f"Para manter o risco de overbooking abaixo de 7%, a empresa deve vender no máximo **{limite_venda}** passagens.")

with tab2:
    st.header("Análise de ROI do Novo Sistema de TI")
    st.markdown("Ajuste os valores para o investimento e a receita esperada na barra lateral para simular o ROI do novo sistema.")

    # Cálculo do ROI
    lucro_esperado = receita_esperada_input - custo_operacional
    roi_esperado = (lucro_esperado / investimento_input) * 100
    st.metric(label="ROI Esperado", value=f"{roi_esperado:.2f}%")

    # Simulação de cenários
    st.subheader("Simulação de Cenários de ROI")
    st.markdown("A simulação mostra a distribuição do ROI final considerando a incerteza da receita.")
    n_simulacoes = 5000
    prob_sucesso = 0.7

    resultados_simulacao = np.random.binomial(1, prob_sucesso, n_simulacoes)
    receitas_simuladas = np.where(
        resultados_simulacao == 1,
        np.random.normal(receita_esperada_input, 5000, n_simulacoes),
        np.random.normal(receita_esperada_input * 0.75, 7000, n_simulacoes)
    )

    rois_simulados = ((receitas_simuladas - custo_operacional) / investimento_input) * 100

    # Gráfico da distribuição dos ROIs simulados
    fig_roi, ax_roi = plt.subplots(figsize=(10, 6))
    ax_roi.hist(rois_simulados, bins=30, color='lightgreen', edgecolor='black')
    ax_roi.axvline(x=0, color='red', linestyle='--', label='ROI = 0%')
    ax_roi.axvline(x=roi_esperado, color='blue', linestyle='--', label=f'ROI Esperado: {roi_esperado:.2f}%')
    ax_roi.set_title("Distribuição dos ROIs Simulados")
    ax_roi.set_xlabel("ROI (%)")
    ax_roi.set_ylabel("Frequência")
    ax_roi.legend()
    ax_roi.grid(True)
    st.pyplot(fig_roi)

    # Cenários de ROI para Tabela
    cenarios_df = pd.DataFrame({
        "Cenário": ["Otimista", "Realista", "Pessimista"],
        "Receita (R$)": [receitas_simuladas.max(), receita_esperada_input, receitas_simuladas.min()],
        "ROI (%)": [
            ((receitas_simuladas.max() - custo_operacional) / investimento_input) * 100,
            roi_esperado,
            ((receitas_simuladas.min() - custo_operacional) / investimento_input) * 100
        ]
    })
    st.subheader("Tabela de Cenários")
    st.dataframe(cenarios_df.set_index("Cenário"))

with tab3:
    st.header("Conclusão e Recomendações")
    st.markdown("""
A adoção de um sistema como o que você analisou permite à Aérea Confiável tomar decisões baseadas em dados, indo além de simples suposições.

**1. Sobre Overbooking:**
* O gráfico interativo mostra claramente que vender mais passagens aumenta drasticamente o risco.
* A empresa deve usar o limite seguro de 129 passagens como uma diretriz do sistema de vendas, em vez de um número fixo de 130.

**2. Sobre ROI:**
* O ROI esperado é positivo, mas a simulação mostra que há um risco real de o sistema não gerar o retorno esperado.
* Recomenda-se um plano de implementação por fases e um monitoramento contínuo dos resultados.

Em resumo, o sistema é uma ferramenta poderosa, mas deve ser usado com cautela, combinando a análise técnica com um olhar atento sobre os riscos financeiros e de imagem.
""")
