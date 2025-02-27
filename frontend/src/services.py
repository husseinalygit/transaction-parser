import requests
import streamlit as st
from .config import NER_SERVICE_URL, CLASSIFICATION_SERVICE_URL, CHAT_URL   

def extract_ner(message):
    """Calls the NER extraction web service."""
    req_body = {"message": message}
    response = requests.post(NER_SERVICE_URL, json=req_body)
    try:
        return response.json()['response_json']
    except Exception as e:
        st.error(f"Error parsing response: {e}")
        return None

def classify_transaction(transaction):
    """Calls the classification service with the given transaction."""
    req_body = {"transaction": transaction}
    response = requests.post(CLASSIFICATION_SERVICE_URL, json=req_body)
    try:
        return response.json()['response_json']
    except Exception as e:
        st.error(f"Error parsing classification response: {e}")
        return None

def chat_request(query):
    """Send a chat request to the API and return the response"""
    try:
        response = requests.post(
            CHAT_URL,
            json={"query": query}
        )
        if response.status_code == 200:
            return response.json()['response']
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Failed to send chat request: {str(e)}")
        return None 