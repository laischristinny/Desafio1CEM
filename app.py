import streamlit as st
import plotly.graph_objects as go
import math

st.set_page_config(layout="wide")
st.title("Dimensionamento de Transformador Monofásico (Método Martignoni)")

# ======= ENTRADAS =======
st.sidebar.header("Dados de entrada")
Vp = st.sidebar.number_input("Tensão Primária (Vp) em V", value=120)
Vs = st.sidebar.number_input("Tensão Secundária (Vs) em V", value=220)
S = st.sidebar.number_input("Potência (S) em VA", value=300)
frequencia = 50  # Hz

# ======= CÁLCULOS =======

# 1. Seção do núcleo (Sc em cm²)
Sc = 1.152 * math.sqrt(S)
Sc_approx = round(Sc, 2)

# 2. Número de espiras por volt (Ev)
Ev = 50 / Sc
Ev_approx = round(Ev, 2)

# 3. Número de espiras
Np = round(Ev * Vp)
Ns = round(Ev * Vs)

# 4. Correntes
Ip = round(S / Vp, 2)
Is = round(S / Vs, 2)

# 5. Bitola dos fios (usando densidade 2,5 A/mm²)
bitola_prim = round(Ip / 2.5, 2)
bitola_sec = round(Is / 2.5, 2)

# 6. Tipo e quantidade de lâminas (simplificação)
def tipo_lamina(Sc):
    if Sc <= 6.0:
        return "EI 66", 20
    elif Sc <= 9.0:
        return "EI 78", 25
    elif Sc <= 12.0:
        return "EI 96", 30
    else:
        return "EI 120", 40

lamina_tipo, lamina_qtd = tipo_lamina(Sc_approx)

# 7. Dimensões do núcleo
largura_perna = round(math.sqrt(Sc_approx), 2)
espessura_nucleo = round(largura_perna * 1.5, 2)
altura_nucleo = 10  # cm

# 8. Peso estimado do núcleo
volume_ferro_cm3 = Sc * altura_nucleo
peso_ferro_kg = round(volume_ferro_cm3 * 7.6 / 1000, 2)

# ======= RESULTADOS =======
st.subheader("Resultados do Dimensionamento:")

st.markdown(f"- **Seção do núcleo (Sc):** {Sc_approx} cm²")
st.markdown(f"- **Número de espiras primário (Np):** {Np}")
st.markdown(f"- **Número de espiras secundário (Ns):** {Ns}")
st.markdown(f"- **Corrente primária (Ip):** {Ip} A")
st.markdown(f"- **Corrente secundária (Is):** {Is} A")
st.markdown(f"- **Bitola do fio primário:** {bitola_prim} mm²")
st.markdown(f"- **Bitola do fio secundário:** {bitola_sec} mm²")
st.markdown(f"- **Tipo de lâmina:** {lamina_tipo}")
st.markdown(f"- **Quantidade de lâminas:** {lamina_qtd}")
st.markdown(f"- **Dimensões do núcleo (largura x espessura):** {largura_perna} cm x {espessura_nucleo} cm")
st.markdown(f"- **Peso estimado do núcleo:** {peso_ferro_kg} kg")

# ======= VISUALIZAÇÃO 3D =======
st.subheader("Visualização 3D do Núcleo e Bobinas")

def cubo(x0, y0, z0, dx, dy, dz, cor):
    X = [x0, x0+dx, x0+dx, x0, x0, x0+dx, x0+dx, x0]
    Y = [y0, y0, y0+dy, y0+dy, y0, y0+dy, y0+dy, y0]
    Z = [z0, z0, z0, z0, z0+dz, z0+dz, z0+dz, z0+dz]
    faces = [[0,1,2,3],[4,5,6,7],[0,1,5,4],
             [2,3,7,6],[1,2,6,5],[0,3,7,4]]
    return go.Mesh3d(x=X, y=Y, z=Z,
                     i=[f[0] for f in faces],
                     j=[f[1] for f in faces],
                     k=[f[2] for f in faces],
                     color=cor, opacity=1.0)

# Escala para visualização
escala = 0.5
lp = largura_perna * escala
ep = espessura_nucleo * escala
h = altura_nucleo * escala

nucleo1 = cubo(0, 0, 0, lp, ep, h, 'gray')
nucleo2 = cubo(3*lp, 0, 0, lp, ep, h, 'gray')
nucleo_top = cubo(0, 0, h - lp, 4*lp, ep, lp, 'gray')

bobina_p = cubo(0.1, 0.1, lp, lp*0.8, ep*0.8, lp, 'red')
bobina_s = cubo(3*lp+0.1, 0.1, lp*2, lp*0.8, ep*0.8, lp, 'blue')

fig = go.Figure(data=[nucleo1, nucleo2, nucleo_top, bobina_p, bobina_s])
fig.update_layout(scene=dict(
    xaxis_title="Largura",
    yaxis_title="Profundidade",
    zaxis_title="Altura",
    aspectratio=dict(x=2, y=1, z=2)
))
st.plotly_chart(fig, use_container_width=True)
