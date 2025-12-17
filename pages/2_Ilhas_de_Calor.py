import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("🌡️ Ilhas de Calor Urbanas")
st.subheader("Modelo simplificado de resfriamento térmico")

st.markdown("""
Esta simulação compara o **resfriamento térmico** de duas superfícies:

- 🧱 **Concreto** (alta inércia térmica)
- 🌱 **Grama** (resfriamento mais eficiente)

O modelo é simplificado e considera um coeficiente efetivo de perda de energia na forma de calor.
""")

# ------------------------------
# Sidebar – parâmetros do modelo
# ------------------------------
st.sidebar.header("Parâmetros do Modelo")

T0 = st.sidebar.slider(
    "Temperatura inicial da superfície (°C)",
    min_value=25.0,
    max_value=70.0,
    value=50.0,
    step=1.0
)

T_amb = st.sidebar.slider(
    "Temperatura ambiente (°C)",
    min_value=15.0,
    max_value=35.0,
    value=25.0,
    step=1.0
)

tempo_total = st.sidebar.slider(
    "Tempo total (min)",
    min_value=30,
    max_value=300,
    value=180,
    step=10
)

# Coeficientes efetivos (didáticos)
k_concreto = st.sidebar.slider(
    "Coeficiente térmico – Concreto",
    min_value=0.001,
    max_value=0.02,
    value=0.005,
    step=0.001
)

k_grama = st.sidebar.slider(
    "Coeficiente térmico – Grama",
    min_value=0.005,
    max_value=0.05,
    value=0.02,
    step=0.001
)

# ------------------------------
# Simulação
# ------------------------------
dt = 1  # minuto
t = np.arange(0, tempo_total + dt, dt)

T_concreto = T_amb + (T0 - T_amb) * np.exp(-k_concreto * t)
T_grama = T_amb + (T0 - T_amb) * np.exp(-k_grama * t)

df_sim = pd.DataFrame({
    "Tempo (min)": t,
    "Concreto (°C)": T_concreto,
    "Grama (°C)": T_grama
})

# ------------------------------
# Gráfico
# ------------------------------
fig = px.line(
    df_sim,
    x="Tempo (min)",
    y=["Concreto (°C)", "Grama (°C)"],
    markers=False,
    labels={"value": "Temperatura (°C)"},
    title="Resfriamento de Superfícies – Modelo Simplificado"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Métricas finais
# ------------------------------
col1, col2 = st.columns(2)

col1.metric(
    "Temperatura final – Concreto",
    f"{T_concreto[-1]:.1f} °C"
)

col2.metric(
    "Temperatura final – Grama",
    f"{T_grama[-1]:.1f} °C"
)

# ------------------------------
# Discussão didática
# ------------------------------

with st.expander("📘 Discussão do Modelo"):
    st.markdown("""
**O que o modelo mostra:**
- Superfícies com maior coeficiente térmico perdem energia na forma de calor mais rapidamente
- O concreto permanece com maior temperatura por mais tempo → ilha de calor

**Limitações do modelo:**
- Não considera radiação solar contínua
- Não diferencia condução, convecção e evaporação

**Extensões possíveis:**
- Adicionar fluxo solar
- Modelo de condução 1D
- Comparar asfalto, telhado, água
""")


st.markdown("### 📐 Modelo Matemático")

st.latex(r"""
\frac{dT}{dt} = -k \, (T - T_{\text{amb}})
""")

st.markdown("""
A solução analítica da equação diferencial é:

""")

st.latex(r"""
T(t) = T_{\text{amb}} + (T_0 - T_{\text{amb}})e^{-kt}
""")
