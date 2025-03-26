import streamlit as st
import requests

# Get IBM API key from Streamlit Secrets
ibm_api_key = st.secrets["IBM_API_KEY"]

# Function to get bearer token from IBM
def get_bearer_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = f"apikey={api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        st.error("❌ Failed to retrieve Bearer Token.")
        st.write("Status Code:", response.status_code)
        st.json(response.json())
        return None

# Function to call watsonx.ai with prompt
def call_watsonx_api(token, user_input):
    endpoint_url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    prompt = f"""### Instruction:
Suggest 3 to-do list tasks based on the user's message.

### Input:
{user_input}

### Response:"""

    payload = {
        "model_id": "granite-13b-chat",
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy"
        }
    }

    response = requests.post(endpoint_url, headers=headers, json=payload)
    return response

# Streamlit UI
st.set_page_config(page_title="Smart To-Do List", page_icon="📝")
st.title("📝 Smart To-Do List (AI-Powered by IBM Watsonx.ai)")
st.write("Type a sentence about your day, and AI will suggest tasks for you!")

user_input = st.text_input("🗣️ What’s on your mind today?")

if st.button("💡 Suggest Tasks"):
    if user_input:
        with st.spinner("Talking to AI..."):
            token = get_bearer_token(ibm_api_key)
            if token:
                response = call_watsonx_api(token, user_input)
                if response.status_code == 200:
                    result = response.json()
                    output = result["results"][0]["generated_text"]
                    st.success("✅ AI Suggested Tasks:")
                    for line in output.strip().split("\n"):
                        if line.strip():
                            st.write(f"✅ {line}")
                else:
                    st.error("❌ AI API call failed.")
                    st.write("📡 Status Code:", response.status_code)
                    try:
                        st.json(response.json())
                    except Exception as e:
                        st.write("⚠️ Could not decode JSON.")
                        st.text(response.text)
                        st.write("⚠️ Error:", str(e))
    else:
        st.warning("Please enter something before generating tasks.")
