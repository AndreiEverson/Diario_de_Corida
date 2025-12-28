import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração inicial
st.set_page_config(page_title="Meu Tracker", page_icon="🏃‍♂️", layout="centered")

# --- FUNÇÕES (iguais a antes) ---
ARQUIVO_DADOS = "dados_corridas.csv"

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return pd.DataFrame(columns=["Data", "Distancia_KM", "Tempo_Minutos", "Pace", "Calorias"])
    else:
        return pd.read_csv(ARQUIVO_DADOS)

def salvar_treino(data, dist, tempo, pace, calorias):
    novo_dado = pd.DataFrame({
        "Data": [data],
        "Distancia_KM": [dist],
        "Tempo_Minutos": [tempo],
        "Pace": [pace],
        "Calorias": [calorias]
    })
    df_atual = carregar_dados()
    df_novo = pd.concat([df_atual, novo_dado], ignore_index=True)
    df_novo.to_csv(ARQUIVO_DADOS, index=False)
    return df_novo

# --- TÍTULO DO APP ---
st.title("🏃‍♂️ Tracker de Corrida")

# --- CRIAÇÃO DAS ABAS (O Pulo do Gato 🐱) ---
# Criamos duas abas: uma para ver os gráficos, outra para adicionar
aba1, aba2 = st.tabs(["📊 Dashboard", "➕ Novo Treino"])

# --- CONTEÚDO DA ABA 1: DASHBOARD ---
with aba1:
    df = carregar_dados()
    
    if not df.empty:
        df["Data"] = pd.to_datetime(df["Data"])
        df = df.sort_values("Data")
        
        # Métricas no topo
        total_km = df["Distancia_KM"].sum()
        total_cal = df["Calorias"].sum()
        
        c1, c2 = st.columns(2)
        c1.metric("Km Total", f"{total_km:.1f} km")
        c2.metric("Kcal", f"{total_cal:.0f}", delta="🔥")
        
        st.divider()
        
        st.subheader("Evolução do Pace")
        st.line_chart(df, x="Data", y="Pace")
        
        st.subheader("Histórico Recente")
        # Mostra os ultimos 5 treinos, do mais novo pro mais velho
        st.dataframe(
            df.sort_values("Data", ascending=False).head(5)[["Data", "Distancia_KM", "Pace"]],
            use_container_width=True
        )
    else:
        st.info("Nenhum dado ainda. Vá na aba 'Novo Treino'!")

# --- CONTEÚDO DA ABA 2: ADICIONAR TREINO ---
with aba2:
    st.header("Registrar Corrida")
    
    # Colocamos num formulário para ficar organizado
    with st.form("form_treino"):
        peso = st.number_input("Seu Peso (kg)", value=70.0, step=0.5)
        data_treino = st.date_input("Data", datetime.now())
        distancia = st.number_input("Distância (km)", min_value=0.0, step=0.1, format="%.2f")
        
        c_hora, c_min = st.columns(2)
        horas = c_hora.number_input("Horas", min_value=0, step=1)
        minutos = c_min.number_input("Minutos", min_value=0, max_value=59, step=1)
        
        # Botão de submissão que ocupa a largura toda
        enviado = st.form_submit_button("💾 SALVAR TREINO", use_container_width=True)
        
        if enviado:
            if distancia > 0:
                tempo_total = (horas * 60) + minutos
                pace = tempo_total / distancia
                calorias = peso * distancia * 1.036
                
                salvar_treino(data_treino, distancia, tempo_total, pace, calorias)
                st.success("✅ Treino Registrado! Volte para a aba Dashboard.")
                # Dica: st.rerun() força a atualização da página para mostrar os dados novos
                st.rerun() 
            else:
                st.error("A distância precisa ser maior que zero!")