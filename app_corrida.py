import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Meu Strava Python", page_icon="🏃‍♂️")

st.title("🏃‍♂️ Meu Tracker de Corrida")

# Nome do arquivo
ARQUIVO_DADOS = "dados_corridas.csv"

# --- FUNÇÃO 1: CARREGAR DADOS ---
def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        # MUDANÇA: Adicionamos a coluna "Calorias"
        return pd.DataFrame(columns=["Data", "Distancia_KM", "Tempo_Minutos", "Pace", "Calorias"])
    else:
        return pd.read_csv(ARQUIVO_DADOS)

# --- FUNÇÃO 2: SALVAR NOVO TREINO ---
def salvar_treino(data, dist, tempo, pace, calorias):
    novo_dado = pd.DataFrame({
        "Data": [data],
        "Distancia_KM": [dist],
        "Tempo_Minutos": [tempo],
        "Pace": [pace],
        "Calorias": [calorias] # Nova coluna
    })
    
    df_atual = carregar_dados()
    df_novo = pd.concat([df_atual, novo_dado], ignore_index=True)
    df_novo.to_csv(ARQUIVO_DADOS, index=False)
    return df_novo

# --- SIDEBAR ---
with st.sidebar:
    st.header("Novo Treino")
    
    # NOVO: Input de Peso para calcular calorias
    peso = st.number_input("Seu Peso (kg)", value=70.0, step=0.5)
    
    data_treino = st.date_input("Data do Treino", datetime.now())
    distancia = st.number_input("Distância (km)", min_value=0.0, format="%.2f")
    
    col1, col2 = st.columns(2)
    horas = col1.number_input("Horas", min_value=0, step=1)
    minutos = col2.number_input("Minutos", min_value=0, max_value=59, step=1)
    
    if st.button("Salvar Treino 💾"):
        if distancia > 0:
            tempo_total = (horas * 60) + minutos
            pace = tempo_total / distancia
            
            # Cálculo Aproximado de Calorias (Fórmula: Peso * Distancia * 1.036)
            calorias = peso * distancia * 1.036
            
            salvar_treino(data_treino, distancia, tempo_total, pace, calorias)
            st.success(f"Treino salvo! Você queimou ~{calorias:.0f} kcal 🔥")
        else:
            st.error("A distância precisa ser maior que zero!")

# --- DASHBOARD ---
df = carregar_dados()

if not df.empty:
    df["Data"] = pd.to_datetime(df["Data"])
    df = df.sort_values("Data")
    
    # --- ÁREA DE MÉTRICAS (Novidade Visual!) ---
    # Vamos criar 3 cartões lado a lado com totais
    total_km = df["Distancia_KM"].sum()
    total_cal = df["Calorias"].sum()
    recorde_pace = df["Pace"].min()

    c1, c2, c3 = st.columns(3)
    c1.metric("Distância Total", f"{total_km:.1f} km")
    c2.metric("Calorias Queimadas", f"{total_cal:.0f} kcal", delta="🔥")
    c3.metric("Melhor Pace", f"{recorde_pace:.2f} min/km", delta="-Recorde!", delta_color="inverse")
    
    st.divider()

    # Tabela e Gráfico
    col_graf, col_tab = st.columns([2, 1]) # Gráfico maior que a tabela (proporção 2 pra 1)
    
    with col_graf:
        st.subheader("📈 Evolução")
        st.line_chart(df, x="Data", y="Pace")
    
    with col_tab:
        st.subheader("📋 Histórico")
        # Mostrando só colunas essenciais
        st.dataframe(df[["Data", "Distancia_KM", "Pace"]].style.format({"Distancia_KM": "{:.1f}", "Pace": "{:.2f}"}))

else:
    st.info("O banco de dados está vazio. Adicione seu primeiro treino na barra lateral!")