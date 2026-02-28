import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Voetbal AI", layout="wide")

st.title("⚽ Voetbal AI")

API_KEY = st.secrets["API_KEY"]

BASE_URL = "https://v3.football.api-sports.io/"
headers = {"x-apisports-key": API_KEY}

TOP_LEAGUES = [39, 140, 135, 78, 61, 88]

def get_fixtures(date):
    return requests.get(
        BASE_URL + "fixtures",
        headers=headers,
        params={"date": date}
    ).json()

dates = [
    datetime.now().strftime("%Y-%m-%d"),
    (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
]

rows = []

for d in dates:
    data = get_fixtures(d)

    for m in data.get("response", []):
        if m["league"]["id"] not in TOP_LEAGUES:
            continue

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        rows.append({
            "Datum": d,
            "Wedstrijd": f"{home} vs {away}"
        })

if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("Geen wedstrijden gevonden.")
