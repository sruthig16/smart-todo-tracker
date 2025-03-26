import streamlit as st
import requests

# 🔐 Get your IBM API Key from Streamlit Secrets
ibm_api_key = st.secrets["IBM_API_KEY"]

# Step 1: Get Bearer Token from IBM
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
        st.error("Failed to retrieve Bearer Token.")
        st.write("Status Code:", response.status_code)
        st.json(response.json())
        return None

# Step 2: Call watsonx.ai Text Generation API
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
        "model_id": "granite-13b-chat",  # You can change to mpt-7b-instruct2 if needed
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy"
        }
    }

    response = requests.post(endpoint_url, headers=headers, json=payload)
    return response

# 🎯 Streamlit UI starts here
st.set_page_config(page_title="Smart To-Do List", page_icon="📝")
st.title("📝 Smart To-Do List (AI-Powered by IBM Watsonx.ai)")
st.write("Type a sentence about your day, and AI will suggest tasks for you!")

user_input = st.text_input("🗣️ What’s on your mind today?")

if st.button("💡 Suggest Tasks"):
    if user_input:
        with st.spinner("Talking to IBM watsonx.ai..."):
            token = get_bearer_token(ibm_api_key)
            if token:
                response = call_watsonx_api(token, user_input)
                if response.status_code == 200:
                    result = response.json()
                    generated = result["results"][0]["generated_text"]
                    st.success("✅ AI Suggested Tasks:")
                    for line in generated.strip().split("\n"):
                        if line.strip():
                            st.write(f"✅ {line}")
                else:
                    st.error("❌ AI API call failed.")
                    st.write("Status Code:", response.status_code)
                    st.json(response.json())
    else:
        st.warning("Please enter something before clicking.")
