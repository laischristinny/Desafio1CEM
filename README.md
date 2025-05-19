# 🔌 Dimensionamento de Transformador Monofásico com Visualização 3D

Este projeto em [Streamlit](https://streamlit.io/) permite realizar o **dimensionamento completo de um transformador monofásico**, a partir de parâmetros elétricos básicos. Também fornece uma **visualização 3D interativa do núcleo com as espiras** usando a biblioteca Plotly.

## 📑 Tabela AWG utilizada
- https://en.wikipedia.org/wiki/American_wire_gauge

## ✨ Funcionalidades

- Cálculo de número de espiras para primário e secundário.
- Dimensionamento da seção do fio com base na corrente e tabela AWG.
- Seleção do tipo e número da lâmina do núcleo.
- Cálculo de peso do cobre e do núcleo.
- Verificação de executabilidade do projeto (critério Sj/Scu ≥ 3).
- Visualização 3D do transformador com núcleo e espiras (Plotly).

## 🖥️ Tecnologias utilizadas

- [Streamlit](https://streamlit.io/) – Para a interface interativa.
- [Plotly](https://plotly.com/python/) – Para visualização 3D.
- Python 3.9+

## 🚀 Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/nome-do-repo.git
cd nome-do-repo
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute o aplicativo
```bash
streamlit run app.py
```
