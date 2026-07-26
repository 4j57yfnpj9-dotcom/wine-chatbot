import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page config
st.set_page_config(page_title="Wine Recommendation Chatbot", layout="centered")
st.title("🍷 Wine Recommendation Chatbot")

st.write("Tell me about your preferences, and I'll recommend the perfect wine!")

# Input form
with st.form("wine_form"):
    food_type = st.text_input("What food are you pairing with?", placeholder="e.g., grilled salmon, chocolate cake")
    budget = st.selectbox("Budget range:", ["Under $20", "$20-$50", "$50-$100", "$100+"])
    preferences = st.text_area("Any other preferences?", placeholder="e.g., dry, fruity, full-bodied")
    
    submit_button = st.form_submit_button("Get Recommendation")

if submit_button:
    if not food_type:
        st.error("Please tell me what food you're pairing with!")
    else:
        # Build the prompt
        prompt = f"""You are a wine expert. Based on the following preferences, recommend ONE specific wine.

Food pairing: {food_type}
Budget: {budget}
Additional preferences: {preferences if preferences else "None"}

Provide:
1. Wine name and region
2. Why it pairs well with the food
3. Tasting notes
4. Approximate price

Keep it concise and helpful."""

        try:
            with st.spinner("Finding the perfect wine..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=300
                )
            
            recommendation = response.choices[0].message.content
            st.success("Here's my recommendation:")
            st.write(recommendation)
        
        except Exception as e:
            st.error(f"Error getting recommendation: {e}")
