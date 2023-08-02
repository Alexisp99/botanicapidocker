import streamlit as st
import requests
import json

# set page layout
st.set_page_config(
    page_title="Botanic - Iris Prediction",
    layout="wide",
    initial_sidebar_state="expanded",
)

# define columns
col1, col2 = st.columns(2)

# title and subtitle
with col1:
    st.title('Botanic')

with col2:
    st.subheader('Iris Species Prediction')
    st.markdown('Please input the features of the iris flower below to predict its species.')

# API setup
url = "https://elidockerapp.azurewebsites.net/getpredict"
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

# input sliders in the left column
with col1:
    st.subheader('Features')
    sepal_length = st.slider('Sepal Length (cm)', min_value=4.0, max_value=8.0, value=5.0, step=0.1)
    sepal_width = st.slider('Sepal Width (cm)', min_value=2.0, max_value=4.5, value=3.0, step=0.1)
    petal_length = st.slider('Petal Length (cm)', min_value=1.0, max_value=7.0, value=4.0, step=0.1)
    petal_width = st.slider('Petal Width (cm)', min_value=0.1, max_value=2.5, value=1.0, step=0.1)

# send GET request
data = {"sepal_length": sepal_length,"sepal_width": sepal_width,"petal_length": petal_length,"petal_width": petal_width}
response = requests.get(url, headers=headers, params = data)

# Parse the JSON response
probabilities = json.loads(response.text)

# show the result in the right column
with col2:
    st.subheader('Prediction')
    st.markdown('The prediction is:')
    st.write(probabilities["prediction"].capitalize(), int(probabilities["probability"] * 100))

    
    # st.write(f"{probabilities["prediction"].capitalize()}: ")
    # st.progress(int(probability * 100))

st.markdown("---")
