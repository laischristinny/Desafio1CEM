import streamlit as st
import plotly.graph_objects as go
import math

# Funções de cálculo baseadas no livro do Martignoni

def calcular_secao_nucleo(potencia_va):
    return math.sqrt(potencia_va)

def calcular_espiras_por_volt(frequencia, secao_cm2):
    return 45 / (frequencia * secao_cm2)

def calcular_espiras(espiras_por_volt, tensao):
    return espiras_por_volt * tensao

def calcular_corrente(potencia_va, tensao):
    return potencia_va / tensao

# Interface Streamlit
st.title("Dimensionamento de Transformador Monofásico (Método Martignoni)")

st.sidebar.header("Dados de Entrada")
vp = st.sidebar.number_input("Tensão Primária (Vp)", value=120)
vs = st.sidebar.number_input("Tensão Secundária (Vs)", value=220)
potencia_va = st.sidebar.number_input("Potência (VA)", value=300)
frequencia = st.sidebar.number_input("Frequência (Hz)", value=50)

if st.sidebar.button("Calcular"):
    secao_cm2 = calcular_secao_nucleo(potencia_va)
    espiras_por_volt = calcular_espiras_por_volt(frequencia, secao_cm2)
    np = calcular_espiras(espiras_por_volt, vp)
    ns = calcular_espiras(espiras_por_volt, vs)
    ip = calcular_corrente(potencia_va, vp)
    is_ = calcular_corrente(potencia_va, vs)

    st.subheader("Resultados do Dimensionamento")
    st.write(f"Seção do núcleo (cm²): {secao_cm2:.2f}")
    st.write(f"Número de espiras primário (Np): {np:.0f}")
    st.write(f"Número de espiras secundário (Ns): {ns:.0f}")
    st.write(f"Corrente no primário (Ip): {ip:.2f} A")
    st.write(f"Corrente no secundário (Is): {is_:.2f} A")

    # Visualização 3D do núcleo
    st.subheader("Visualização 3D do Núcleo (Aproximada)")
    core_width = secao_cm2 / 2
    core_height = secao_cm2
    core_depth = 3

    fig = go.Figure(data=[
        go.Mesh3d(
            x=[0, core_width, core_width, 0, 0, core_width, core_width, 0],
            y=[0, 0, core_depth, core_depth, 0, 0, core_depth, core_depth],
            z=[0, 0, 0, 0, core_height, core_height, core_height, core_height],
            color='gray',
            opacity=0.5
        )
    ])
    fig.update_layout(scene=dict(
        xaxis_title='Largura',
        yaxis_title='Profundidade',
        zaxis_title='Altura'
    ))
    st.plotly_chart(fig)
