import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

# Título do seu Aplicativo do TCA
st.set_page_config(page_title="Simulador de Apostas - TCA", layout="wide")
st.title("🎰 Simulador de Estatística: Apostas vs Matemática")

# BARRA LATERAL (Onde as pessoas mudam os dados)
st.sidebar.header("Configurações da Simulação")
pessoas_dia = st.sidebar.number_input("Pessoas por dia", value=50)
dias = st.sidebar.number_input("Total de dias", value=30)
total_pessoas = pessoas_dia * dias

st.sidebar.markdown(f"**Total de Apostadores: {total_pessoas}**")

rodadas = st.sidebar.slider("Rodadas por pessoa", 1, 50, 10)
saldo_ini = st.sidebar.number_input("Saldo Inicial (R$)", value=200)
valor_ap = st.sidebar.number_input("Valor da Aposta (R$)", value=20)

# Chance da Casa (51.4%) e do Jogador (48.6%)
chance_casa = st.sidebar.slider("Vantagem da Casa (%)", 50.1, 60.0, 51.4)
chance_jog = (100 - chance_casa) / 100

if st.sidebar.button("📊 RODAR SIMULAÇÃO"):
    saldos = []
    for _ in range(total_pessoas):
        s = saldo_ini
        for _ in range(rodadas):
            if s >= valor_ap:
                if random.random() < chance_jog:
                    s += valor_ap
                else:
                    s -= valor_ap
        saldos.append(s)
    
    # Resultados
    df = pd.DataFrame(saldos, columns=['Final'])
    lucro_casa = (total_pessoas * saldo_ini) - df['Final'].sum()
    perderam = len(df[df['Final'] < saldo_ini])

    col1, col2 = st.columns(2)
    col1.metric("Pessoas com Prejuízo", f"{perderam} de {total_pessoas}")
    col2.metric("Lucro Total da Casa", f"R$ {lucro_casa:,.2f}")

    # Gráfico
    st.subheader("Gráfico Estatístico (Distribuição)")
    fig, ax = plt.subplots()
    df['Final'].hist(bins=15, ax=ax, color='red', edgecolor='white')
    ax.axvline(saldo_ini, color='black', linestyle='--')
    plt.xlabel("Saldo Final (R$)")
    plt.ylabel("Nº de Pessoas")
    st.pyplot(fig)
