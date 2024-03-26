import streamlit as st
from langchain.llms import OpenAI
from google.oauth2 import service_account
from google.cloud import bigquery
import json
import pandas_gbq
import pandas as pd
credentials = service_account.Credentials.from_service_account_info(
    st.secrets[""]
)


#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/Dell/OneDrive - BrainAI/Cognify/mvp/gcp_service_account.json"


with open("C:/Users/Dell/OneDrive - BrainAI/Cognify/mvp/gcp_service_account.json") as source:
    info = json.load(source)


credentials = service_account.Credentials.from_service_account_info(info)
sql = "SELECT * FROM `brainai-382204.cognify.menningersynth`"
df = pd.read_gbq(sql, dialect="standard", credentials=credentials)  

st.title("🦜🔗 Langchain Quickstart App")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(llm(input_text))


with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your GuilleFP1! OpenAI API key to continue.")
    elif submitted:
        generate_response(text)
    st.dataframe(df)
