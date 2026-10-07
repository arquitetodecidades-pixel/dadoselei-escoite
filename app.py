import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mapa Eleitoral de Conceição do Coité", layout="wide")
st.title("Mapa Eleitoral de Conceição do Coité")
st.info("Protótipo inicial. Substitua data/resultados.csv pelos dados oficiais tratados do TSE.")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/resultados.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["ano","lat","lon","local","secao","vencedor_prefeito","candidato_prefeito","votos_prefeito","candidato_vereador","votos_vereador"])

df=load_data()
anos=sorted(df["ano"].dropna().unique().tolist()) if not df.empty else [2012,2016,2020,2024]
ano=st.sidebar.selectbox("Eleição municipal", anos)
if not df.empty:
    d=df[df.ano==ano].copy()
else: d=df

m=folium.Map(location=[-11.56,-39.28], zoom_start=11, tiles="OpenStreetMap")
colors={}
for _,r in d.iterrows():
    winner=str(r.get("vencedor_prefeito","Sem dados"))
    if winner not in colors: colors[winner]=["#1f77b4","#d62728","#2ca02c","#ff7f0e","#9467bd"][len(colors)%5]
    html=f"<b>{r.get('local','')}</b><br>Seção: {r.get('secao','')}<br>Prefeito vencedor: {winner}<br>Votos prefeito: {r.get('candidato_prefeito','')} — {r.get('votos_prefeito','')}<br>Vereador: {r.get('candidato_vereador','')} — {r.get('votos_vereador','')}"
    folium.CircleMarker([r.lat,r.lon], radius=8, color=colors[winner], fill=True, fill_color=colors[winner], fill_opacity=.8, tooltip=f"Seção {r.get('secao','')}", popup=folium.Popup(html,max_width=320)).add_to(m)
st_folium(m,width=None,height=650)
st.subheader(f"Legenda — {ano}")
for k,v in colors.items(): st.markdown(f"<span style='color:{v};font-size:24px'>●</span> {k}", unsafe_allow_html=True)
