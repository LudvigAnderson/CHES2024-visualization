import streamlit as st
import plotly.express as px
import pandas as pd
import json


df = pd.read_csv("CHES_2024_final_v2.csv") # the data for each party
with open("codebook.json", "r", encoding="utf-8") as cb, open("country_names.json", "r", encoding="utf-8") as cn:
    codebook = json.load(cb) # the codebook with information about each question
    country_names = json.load(cn) # {"NOR" : "Norway", ...}
    country_names_reverse = {v : k for k, v in country_names.items()}

# I got these color suggestions simply from asking ChatGPT:
family_color_map = {
    "radrt" : "#003366",
    "con" : "#1E3A8A",
    "lib" : "#00BFFF",
    "cd" : "#dea302",
    "soc" : "#FF0000",
    "radleft" : "#800000",
    "green" : "#008000",
    "reg" : "#8A2BE2",
    "nofamily" : "#808080",
    "confess" : "#8B4513",
    "agrarian/centre" : "#556B2F"
}

# Add a sidebar filter
country = st.sidebar.selectbox("Choose country", country_names.values())
#x_axis = "lrecon" # change to selection
x_axis = st.sidebar.selectbox("X-axis question", codebook.keys())
y_axis = st.sidebar.selectbox("Y-axis question", codebook.keys())
#y_axis = "lrgen" # change to selection

filtered_df = df[df['country'] == country_names_reverse[country]]

# Create an interactive scatter plot
fig = px.scatter(
    filtered_df,
    x=x_axis,
    y=y_axis,
    size="seatperc",
    color="family",
    hover_name="party",
    color_discrete_map=family_color_map
)

fig.update_layout(
    xaxis = dict(range=codebook[x_axis]["range"]),
    yaxis = dict(range=codebook[y_axis]["range"]),
    showlegend = False,
    dragmode = False
)

config = {
    'displayModeBar': True,  # or False to hide it entirely
    'modeBarButtonsToRemove': [
        'zoom2d', 'pan2d', 'select2d', 'lasso2d',
        'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
    ],
    'scrollZoom': False,
    'displaylogo': True  # optional: remove Plotly logo
}

# Display the plot
st.plotly_chart(fig, use_container_width=True, config=config)

st.write("### Question descriptions:")
for axis in [x_axis, y_axis]:
    st.write(f"**{axis}:** {codebook[axis]['description']}")
    st.write(codebook[axis]["values"])