import streamlit as st
import plotly.graph_objects as go
import math

st.set_page_config(layout="wide")
st.title("Dimensionamento de Transformador Monofásico")

# ======= ENTRADAS =======
st.sidebar.header("Dados de entrada")
V1 = st.sidebar.number_input("Tensão Primária (V1) em V", value=120)
V2 = st.sidebar.number_input("Tensão Secundária (V2) em V", value=220)
W2 = st.sidebar.number_input("Potência (W2) em VA", value=300)
f = st.sidebar.number_input("Frequência em Hz", value=50)
tipo_transformador = st.sidebar.selectbox(
    "Tipo de Transformador",
    [
        "Transformador de um primário e um secundário",
        "Transformador de dois primários e um secundário ou um primário e dois secundários",
        "Transformador de dois primários e dois secundários"
    ]
)
tipo_de_lamina = st.sidebar.selectbox("Tipo de Lâmina do Núcleo", ["Padronizada", "Comprida"])

# ======= CÁLCULOS =======

W1 = 1.1 * W2 # Potência primária
I1, I2 = round(W1 / V1, 1), round(W2 / V2, 1) # Corrente primária e secundária

d = 3 if W2 <= 500 else 2.5 if W2 <= 1000 else 2 # Densidade da corrente
S1, S2 = round(I1 / d, 1), round(I2 / d, 1)  # Seção do condutor primário e secundário

fator_tipo = {
    "Transformador de um primário e um secundário": 1,
    "Transformador de dois primários e um secundário ou um primário e dois secundários": 1.25,
    "Transformador de dois primários e dois secundários": 1.5
}[tipo_transformador]

coef = 7.5 if tipo_de_lamina == "Padronizada" else 6
Sm = round(coef * math.sqrt((fator_tipo * W2) / f), 1) # Seção magnética do núcleo

Sg = round(Sm * 1.1, 1) # Seção geométrica do núcleo
a = math.ceil(math.sqrt(Sg))  # Largura da coluna central  do transformador
b = round(Sg / a, 1)  # Comprimento do pacote laminado

# Funções para seleção de lâminas
def selecionar_lamina(a, tipo):
    laminas_padronizadas = [
        {"numero": 0, "a_cm": 1.5, "secao_mm2": 168, "peso_kgcm": 0.095},
        {"numero": 1, "a_cm": 2, "secao_mm2": 300, "peso_kgcm": 0.170},
        {"numero": 2, "a_cm": 2.5, "secao_mm2": 468, "peso_kgcm": 0.273},
        {"numero": 3, "a_cm": 3, "secao_mm2": 675, "peso_kgcm": 0.380},
        {"numero": 4, "a_cm": 3.5, "secao_mm2": 900, "peso_kgcm": 0.516},
        {"numero": 5, "a_cm": 4, "secao_mm2": 1200, "peso_kgcm": 0.674},
        {"numero": 6, "a_cm": 5, "secao_mm2": 1880, "peso_kgcm": 1.053}
    ]
    laminas_compridas = [
        {"numero": 5, "a_cm": 4, "secao_mm2": 2400, "peso_kgcm": 1.000},
        {"numero": 6, "a_cm": 5, "secao_mm2": 3750, "peso_kgcm": 1.580}
    ]
    laminas = laminas_padronizadas if tipo == "Padronizada" else laminas_compridas
    for lamina in laminas:
        if a <= lamina["a_cm"]:
            return lamina
    return laminas[-1]

numero_lamina = selecionar_lamina(a, tipo_de_lamina)

# Dimensões efetivas do nucleo central

SgEfetivo, SmEfetivo = a * b, (a * b) / 1.1
EspVolt = round((1e8 / (4.44 * 11300 * f)) / SmEfetivo, 2)
N1, N2 = math.ceil(EspVolt * V1), math.ceil(EspVolt * V2 * 1.1) # Espiras

Scu = N1 * S1 + N2 * S2 # Seção do cobre enrolado
Sj = numero_lamina["secao_mm2"]
executavel = Sj / Scu

Pfe = numero_lamina["peso_kgcm"] * b # Peso do ferro
lm = (2 * a) + (2 * b) + (0.5 * a * 3.14) # Comprimento da espira média do cobre
Pcu = (Scu / 100 * lm * 9) / 1000 # Peso do cobre

# ======= RESULTADOS =======
st.header("Resultados do Dimensionamento")

st.subheader("Número de Espiras")
st.write(f"Espiras do Enrolamento Primário (Np): {N1}")
st.write(f"Espiras do Enrolamento Secundário (Ns): {N2}")

st.subheader("Bitola dos Cabos")
st.write(f"Seção do cabo primário (S1): {S1:.2f} mm²")
st.write(f"Seção do cabo secundário (S2): {S2:.2f} mm²")

st.subheader("Lâmina do Núcleo")
if numero_lamina:
    st.write(f"Tipo de lâmina selecionada: Nº {numero_lamina['numero']} com seção {numero_lamina['secao_mm2']} mm²")
    st.write(f"Quantidade de lâminas aproximada (baseado no comprimento b): {b} unidades")
else:
    st.write("Nenhuma lâmina padronizada adequada encontrada para as dimensões calculadas.")

st.subheader("Dimensões do Transformador")
st.write(f"Largura da coluna central (a): {a} cm")
st.write(f"Comprimento do pacote laminado (b): {b} cm")
st.write(f"Seção geométrica efetiva do núcleo (SgEfetivo): {SgEfetivo:.2f} cm²")
st.write(f"Seção magnética efetiva do núcleo (SmEfetivo): {SmEfetivo:.2f} cm²")

st.subheader("Peso do Transformador")
st.write(f"Peso do núcleo de ferro (Pfe): {Pfe:.2f} kg")
st.write(f"Peso estimado do cobre (Pcu): {Pcu:.2f} kg")

if executavel >= 3:
    st.success("Transformador é executável conforme critério de relação Sj/Scu >= 3.")
else:
    st.warning("Transformador não executável. É preciso recalcular com um núcleo maior.")

# ======= VISUALIZAÇÃO 3D =======
st.subheader("Visualização 3D do Núcleo com Espiras")

escala = 10
largura_coluna, altura_coluna = a * escala, b * escala
espessura = 2 * escala

def bloco(x, y, z, dx, dy, dz, color='gray', opacity=0.8):
    return go.Mesh3d(
        x=[x, x+dx, x+dx, x, x, x+dx, x+dx, x],
        y=[y, y, y+dy, y+dy, y, y, y+dy, y+dy],
        z=[z, z, z, z, z+dz, z+dz, z+dz, z+dz],
        color=color,
        opacity=opacity
    )

blocos = [
    bloco(0, 0, 0, espessura, altura_coluna, largura_coluna),
    bloco(espessura + largura_coluna, 0, 0, espessura, altura_coluna, largura_coluna),
    bloco((espessura + largura_coluna) * 2, 0, 0, espessura, altura_coluna, largura_coluna)
]

def adicionar_espiras(x_ini, y_ini, z_ini, espessura, altura, largura, n_espiras, cor):
    espiras = []
    esp_faixa = 0.6 * escala
    for i in range(n_espiras):
        desloc = i * (esp_faixa / 2)
        espiras.append(bloco(
            x_ini - desloc,
            y_ini,
            z_ini - desloc,
            espessura + 2 * desloc,
            altura,
            largura + 2 * desloc,
            color=cor,
            opacity=0.6
        ))
    return espiras

n_espiras_visuais_primario = min(N1 // 10, 10)
n_espiras_visuais_secundario = min(N2 // 10, 10)

x_central, y_central, z_central = espessura + largura_coluna, 0, 0

blocos += adicionar_espiras(x_central, y_central, z_central, espessura, altura_coluna, largura_coluna, n_espiras_visuais_primario, 'blue')
blocos += adicionar_espiras(x_central, y_central, z_central, espessura, altura_coluna, largura_coluna, n_espiras_visuais_secundario, 'red')

fig = go.Figure(data=blocos)
fig.update_layout(
    scene=dict(
        xaxis=dict(title='X', visible=False),
        yaxis=dict(title='Altura', visible=False),
        zaxis=dict(title='Profundidade', visible=False),
        aspectmode='data'
    ),
    margin=dict(r=10, l=10, b=10, t=10)
)

st.plotly_chart(fig, use_container_width=True)
