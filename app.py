---

### **app.py**

```python
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.title("Real-Time COVID-19 Dashboard")
st.markdown("Live data visualization of COVID-19 cases by country")

# API URL
url = "https://disease.sh/v3/covid-19/countries"

@st.cache_data
def load_data():
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)
    return df

df = load_data()
countries = df['country'].tolist()
country = st.selectbox("Select a country", countries)

# Filter for selected country
selected = df[df['country'] == country].iloc[0]
st.metric("Total Cases", f"{selected['cases']:,}")
st.metric("Deaths", f"{selected['deaths']:,}")
st.metric("Recovered", f"{selected['recovered']:,}")

# Plotting
st.subheader("COVID-19 Stats by Country")
fig = px.bar(x=['Active', 'Recovered', 'Deaths'],
             y=[selected['active'], selected['recovered'], selected['deaths']],
             labels={'x': 'Category', 'y': 'Count'},
             color=['Active', 'Recovered', 'Deaths'])

st.plotly_chart(fig)
