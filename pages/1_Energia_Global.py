# ==============================
# app.py
# ==============================

import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------
# Configuração da página
# ------------------------------
st.set_page_config(
    page_title="Consumo de Energia no Mundo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption/data"
    }
)

st.title("⚡ Consumo de Energia Elétrica no Mundo")

# ------------------------------
# Carregamento de dados
# ------------------------------
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data("World_Energy_Consumption.csv")

# ------------------------------
# Seleção de colunas relevantes
# ------------------------------
cols_elec = [
    'biofuel_electricity', 'hydro_electricity', 'nuclear_electricity',
    'solar_electricity', 'wind_electricity', 'other_renewable_electricity',
    'coal_electricity', 'gas_electricity', 'oil_electricity'
]

df['total'] = df[cols_elec].sum(axis=1)
df = df[df['total'] > 0]

# Percentuais
for col in cols_elec:
    df[f'{col.split("_")[0]}_perc'] = 100 * df[col] / df['total']

cols_renov = ['biofuel_perc', 'hydro_perc', 'solar_perc', 'wind_perc']
cols_nao_renov = ['nuclear_perc', 'coal_perc', 'gas_perc', 'oil_perc']

df['renewable'] = df[cols_renov].sum(axis=1)
df['not_renewable'] = df[cols_nao_renov].sum(axis=1)

# ------------------------------
# Sidebar – filtros
# ------------------------------
st.sidebar.header("Filtros")

anos = sorted(df['year'].dropna().unique())
ano_sel = st.sidebar.multiselect(
    "Ano",
    anos,
    default=[2020, 2021]
)

paises = sorted(df['country'].dropna().unique())
pais_sel = st.sidebar.multiselect(
    "País",
    paises,
    default=["World"]
)

df_filt = df[
    (df['year'].isin(ano_sel)) &
    (df['country'].isin(pais_sel))
]

# ------------------------------
# Métricas
# ------------------------------
st.subheader("Indicadores Gerais")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Consumo Total Médio (TWh)",
    f"{df_filt['total'].mean():.1f}"
)

c2.metric(
    "% Renovável Médio",
    f"{df_filt['renewable'].mean():.1f}%"
)

c3.metric(
    "% Não Renovável Médio",
    f"{df_filt['not_renewable'].mean():.1f}%"
)

# ------------------------------
# Gráfico 1 – Renovável vs Não Renovável
# ------------------------------
df_long = df_filt.melt(
    id_vars=["country", "year"],
    value_vars=["renewable", "not_renewable"],
    var_name="tipo",
    value_name="percentual"
)

fig1 = px.line(
    df_long,
    x="year",
    y="percentual",
    color="country",          # cores diferentes por país
    line_dash="tipo",         # sólido vs tracejado (renovável / não)
    markers=True,
    labels={
        "percentual": "%",
        "year": "Ano",
        "country": "País",
        "tipo": "Fonte"
    },
    title="Participação Renovável vs Não Renovável por País"
)

st.plotly_chart(fig1, use_container_width=True)


# ------------------------------
# Gráfico 2 – Composição da matriz elétrica
# ------------------------------
cols_stack = cols_renov + cols_nao_renov
df_stack = df_filt.groupby("year")[cols_stack].mean().reset_index()

fig2 = px.bar(
    df_stack,
    x="year",
    y=cols_stack,
    title="Composição Percentual da Eletricidade",
    labels={"value": "%", "variable": "Fonte"},
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------------------
# Ranking – países mais dependentes de fóssil
# ------------------------------
st.subheader("Países mais dependentes de fontes não renováveis")

df_rank = (
    df_filt
    .groupby("country")[['renewable', 'not_renewable', 'total']]
    .mean()
    .sort_values(by='not_renewable', ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    df_rank,
    x="country",
    y="not_renewable",
    title="Top 10 – Dependência Não Renovável (%)",
    labels={"not_renewable": "%", "country": "País"}
)

st.plotly_chart(fig3, use_container_width=True)

# ------------------------------
# Tabela final
# ------------------------------
with st.expander("📄 Ver dados filtrados"):
    st.dataframe(
        df_filt[['country', 'year', 'renewable', 'not_renewable', 'total']]
        .sort_values(by='total', ascending=False)
    )
