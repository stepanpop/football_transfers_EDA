import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv("fotbal_prestupy_2000_2019.csv")
    data = data[data['Věk'] != 0]
    return data

df = load_data()

# 1. Základní statistiky
st.title("Fotbalové přestupy 2000-2018 EDA :bar_chart:")
st.header("1. Základní statistiky")
st.write("Shrnutí statistik datasetu:")
st.write(df.describe())

# 2. Interactive Visualization: Transfers per Season and per Nová Liga
st.header("2. Transfery podle sezóny a příjmajících klubů")
top_leagues = df["Nová  Liga"].value_counts().head(5).index
filtered_df = df[df["Nová  Liga"].isin(top_leagues)]
selected_season = st.selectbox("Zvol sezónu", sorted(filtered_df["Sezóna"].unique()))
selected_league = st.selectbox("Zvol příjmající klub", sorted(filtered_df["Nová  Liga"].unique()))
filtered_data = filtered_df[(filtered_df["Sezóna"] == selected_season) & (filtered_df["Nová  Liga"] == selected_league)]

st.write(f"Transfery za {selected_season} v {selected_league}:")
st.bar_chart(filtered_data["Přestupová částka"])

# 3. Kolik útratí jednotlivé ligy za přestupy?
st.header("Kolik útratí jednotlivé ligy za přestupy?")
selected_year = st.slider("Zvol rok", min_value=int(df["Sezóna"].str[:4].min()), max_value=int(df["Sezóna"].str[:4].max()), value=int(df["Sezóna"].str[:4].min()))
yearly_df = df[df["Sezóna"].str[:4] == str(selected_year)]
liga_spending = yearly_df.groupby("Nová  Liga")["Přestupová částka"].sum().reset_index()
top_liga_spending = liga_spending.sort_values(by="Přestupová částka", ascending=False).head(5)
st.write(f"Celková útrata za transfery v  top 5 ligách za rok {selected_year}:")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="Nová  Liga", y="Přestupová částka", data=top_liga_spending, palette="viridis")
ax.set_title(f"Celková útrata za transfery v  top 5 ligách za rok {selected_year}", fontsize=15)
ax.set_xlabel("Liga")
ax.set_ylabel("Celkové transferové poplatky")
st.pyplot(fig)
# 4. Visualization: Which League Pays the Most?
st.header("4. Jaká liga platí nejvíce za přestupy?")
view_all_stats = st.checkbox("Zobrazit všechny statistiky za 2000-2018")
if view_all_stats:
    yearly_df_4 = df
else:
    selected_year_4 = st.slider("Zvol sezónu", min_value=int(df["Sezóna"].str[:4].min()), max_value=int(df["Sezóna"].str[:4].max()), value=int(df["Sezóna"].str[:4].min()), key="slider_4")
    yearly_df_4 = df[df["Sezóna"].str[:4] == str(selected_year_4)]

liga_spending_4 = yearly_df_4.groupby("Nová  Liga")["Přestupová částka"].sum().reset_index()
top_liga_spending_4 = liga_spending_4.sort_values(by="Přestupová částka", ascending=False).head(5)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="Přestupová částka", y="Nová  Liga", data=top_liga_spending_4)
if view_all_stats:
    ax.set_title("Jaká liga platí nejvíce za transfery v letech 2000-2018?", fontsize=15)
else:
    ax.set_title(f"Jaká liga platí nejvíce za transfery v roce {selected_year_4}?", fontsize=15)
ax.set_xlabel("Transferové poplatky")
ax.set_ylabel("Liga")
st.pyplot(fig)

# 5. Biggest Liga_příjmy
st.header("5. Jaká liga má největší příjem z transferů?")
income_by_league = df.groupby("Původní liga")["Přestupová částka"].sum().reset_index()
view_all_income_stats = st.checkbox("Zobraz statistiku za 2000-2018")
if view_all_income_stats:
    top_income_by_league = income_by_league.sort_values(by="Přestupová částka", ascending=False).head(5)
    title = "Liga_příjmy: Největš příjmy z trasnferů za 2000-2018"
else:
    selected_income_year = st.slider("Zvol sezónu", min_value=int(df["Sezóna"].str[:4].min()), max_value=int(df["Sezóna"].str[:4].max()), value=int(df["Sezóna"].str[:4].min()), key="slider_income")
    income_by_league_yearly = df[df["Sezóna"].str[:4] == str(selected_income_year)].groupby("Původní liga")["Přestupová částka"].sum().reset_index()
    top_income_by_league = income_by_league_yearly.sort_values(by="Přestupová částka", ascending=False).head(5)
    title = f"Liga_příjmy: Největší příjem z transferů {selected_income_year}"

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="Přestupová částka", y="Původní liga", data=top_income_by_league)
ax.set_title(title)
ax.set_xlabel("Transferové poplatky")
ax.set_ylabel("Původní liga")
st.pyplot(fig)

