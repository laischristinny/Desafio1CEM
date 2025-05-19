import streamlit as st
import plotly.graph_objects as go
import math

# ======= CONFIGURAÇÃO INICIAL =======

st.set_page_config(layout="wide")
st.title("Dimensionamento de Transformador Monofásico")

# ======= ENTRADAS =======

st.sidebar.header("Dados de entrada")

tipo_transformador = st.sidebar.selectbox(
    "Tipo de Transformador",
    [
        "Transformador de um primário e um secundário",
        "Transformador de dois primários e um secundário ou um primário e dois secundários",
        "Transformador de dois primários e dois secundários"
    ]
)
V1_input = st.sidebar.text_input("Tensão Primária (V1) em V (use / para múltiplos)", value="120")
V2_input = st.sidebar.text_input("Tensão Secundária (V2) em V (use / para múltiplos)", value="220")

V1_list = [int(v.strip()) for v in V1_input.split("/") if v.strip().isdigit()]
V2_list = [int(v.strip()) for v in V2_input.split("/") if v.strip().isdigit()]
W2 = st.sidebar.number_input("Potência (W2) em VA", value=300)
f = st.sidebar.number_input("Frequência em Hz", value=50)
tipo_de_lamina = st.sidebar.selectbox("Tipo de Lâmina do Núcleo", ["Padronizada", "Comprida"])

# ======= CÁLCULOS =======

W1 = 1.1 * W2  # Potência primária
I1 = [round(W1 / v, 2) for v in V1_list] # Corrente primária
d = 3 if W2 <= 500 else 2.5 if W2 <= 1000 else 2 # Densidade da corrente
S1 = [round(i / d, 2) for i in I1] # Seção do condutor primário

I2 = [round(W2 / v, 2) for v in V2_list] # Corrente secundária
S2 = [round(i / d, 2) for i in I2] # Seção do condutor secundário

awg_table = [
    {"AWG": 25, "area_mm2": 0.162},
    {"AWG": 24, "area_mm2": 0.205},
    {"AWG": 23, "area_mm2": 0.258},
    {"AWG": 22, "area_mm2": 0.326},
    {"AWG": 21, "area_mm2": 0.410},
    {"AWG": 20, "area_mm2": 0.518},
    {"AWG": 19, "area_mm2": 0.653},
    {"AWG": 18, "area_mm2": 0.823},
    {"AWG": 17, "area_mm2": 1.04},
    {"AWG": 16, "area_mm2": 1.31},
    {"AWG": 15, "area_mm2": 1.65},
    {"AWG": 14, "area_mm2": 2.08},
    {"AWG": 13, "area_mm2": 2.62},
    {"AWG": 12, "area_mm2": 3.31},
    {"AWG": 11, "area_mm2": 4.17},
    {"AWG": 10, "area_mm2": 5.26},
    {"AWG": 9,  "area_mm2": 6.63},
    {"AWG": 8,  "area_mm2": 8.37},
    {"AWG": 7,  "area_mm2": 10.55},
    {"AWG": 6,  "area_mm2": 13.30},
    {"AWG": 5,  "area_mm2": 16.80},
    {"AWG": 4,  "area_mm2": 21.15},
    {"AWG": 3,  "area_mm2": 26.67},
    {"AWG": 2,  "area_mm2": 33.62},
    {"AWG": 1,  "area_mm2": 42.41},
    {"AWG": 0,  "area_mm2": 53.49},
]

def encontrar_awg_por_secao(secao_mm2):
    for fio in awg_table:
        if fio["area_mm2"] >= secao_mm2:
            return fio
    return None

fio_awg_s1_1 = encontrar_awg_por_secao(S1[0])
fio_awg_s2_1 = encontrar_awg_por_secao(S2[0])
if len(S1) >= 2:
    fio_awg_s1_2 = encontrar_awg_por_secao(S1[1])
if len(S2) >= 2:
    fio_awg_s2_2 = encontrar_awg_por_secao(S2[1])

fator_tipo = {
    "Transformador de um primário e um secundário": 1,
    "Transformador de dois primários e um secundário ou um primário e dois secundários": 1.25,
    "Transformador de dois primários e dois secundários": 1.5
}[tipo_transformador]

coef = 7.5 if tipo_de_lamina == "Padronizada" else 6
Sm = round(coef * math.sqrt((fator_tipo * W2) / f), 1) # Seção magnética do núcleo
Sg = round(Sm * 1.1, 1)  # Seção geométrica do núcleo

a = math.ceil(math.sqrt(Sg)) # Largura da coluna central  do transformador
b = round(Sg / a)  # Comprimento do pacote laminado

# Função para seleção de lâminas
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
SgEfetivo = a * b
SmEfetivo = round(SgEfetivo / 1.1, 2)

if f == 50:
    EspVolt = round(40 / SmEfetivo, 2)
elif f == 60:
    EspVolt = round(33.5 / SmEfetivo, 2)
else:
    EspVolt = round((1e8 / (4.44 * 11300 * f)) / SmEfetivo, 2)

N1 = math.ceil(EspVolt * V1_list[0])  # Espiras do primário
N2 = math.ceil(EspVolt * V2_list[0] * 1.1) # Espiras do secundário

if len(S1) >= 2 and len(S2) >= 2:
    Scu = N1 * fio_awg_s1_1['area_mm2'] + N1 * fio_awg_s1_2['area_mm2'] + N2 * fio_awg_s2_1['area_mm2'] + N2 * fio_awg_s2_2['area_mm2']
elif len(S1) >= 2:
    Scu = N1 * fio_awg_s1_1['area_mm2'] + N1 * fio_awg_s1_2['area_mm2'] + N2 * fio_awg_s2_1['area_mm2']
elif len(S2) >= 2:
    Scu = N1 * fio_awg_s1_1['area_mm2'] + N2 * fio_awg_s2_1['area_mm2'] + N2 * fio_awg_s2_2['area_mm2']
else:
    Scu = N1 * fio_awg_s1_1['area_mm2'] + N2 * fio_awg_s2_1['area_mm2']

Sj = numero_lamina["secao_mm2"] # Seção da janela
executavel = Sj / Scu

Pfe = numero_lamina["peso_kgcm"] * b # Peso do ferro
lm = (2 * a) + (2 * b) + (0.5 * a * math.pi)  # Comprimento da espira média do cobre
Pcu = (Scu / 100 * lm * 9) / 1000 # Peso do cobre

# ======= RESULTADOS =======

st.header("Resultados do Dimensionamento")

st.subheader("Número de Espiras")
st.write(f"Primário: {N1} espiras")
st.write(f"Secundário: {N2} espiras")

st.subheader("Bitola dos Cabos")
st.write(f"Tipo de fio AWG para S1 Primário 1: {fio_awg_s1_1['AWG']}, cuja seção é  {fio_awg_s1_1['area_mm2']}")
st.write(f"Tipo de fio AWG para S2 Secundário 1: {fio_awg_s2_1['AWG']}, cuja seção é  {fio_awg_s2_1['area_mm2']}")
if len(S1) >= 2:
    st.write(f"Tipo de fio AWG para S1 Primário 2: {fio_awg_s1_2['AWG']}, cuja seção é  {fio_awg_s1_2['area_mm2']}")
if len(S2) >= 2:
    st.write(f"Tipo de fio AWG para S2 Secundário 2: {fio_awg_s2_2['AWG']}, cuja seção é  {fio_awg_s2_2['area_mm2']}")

for i, (v, s) in enumerate(zip(V1_list, S1)):
    st.write(f"Primário {i+1} ({v} V): {s:.2f} mm²")
for i, (v, s) in enumerate(zip(V2_list, S2)):
    st.write(f"Secundário {i+1} ({v} V): {s:.2f} mm²")

st.subheader("Lâmina do Núcleo")
st.write(f"Tipo de lâmina selecionada: Nº {numero_lamina['numero']} com seção {numero_lamina['secao_mm2']} mm²")
st.write(f"Quantidade de lâminas aproximada (baseado no comprimento b): {b} unidades")

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
    st.warning("Transformador não executável.")

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

n_espiras_primario = min(N1 // 10, 10)
blocos += adicionar_espiras(espessura + largura_coluna, 0, 0, espessura, altura_coluna, largura_coluna, n_espiras_primario, 'blue')

n_espiras_secundario = min(N2 // 10, 10)
blocos += adicionar_espiras(espessura + largura_coluna, 0, 50, espessura, altura_coluna, largura_coluna, n_espiras_secundario, 'red')

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
