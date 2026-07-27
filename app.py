import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

load_dotenv()

# ===== WINE RECOMMENDATION PROMPT =====
WINE_RECOMMENDATION_PROMPT = """You are a sommelier and wine expert with deep knowledge of wines from around the world.

Your task: Based on the user's preferences below, recommend ONE specific wine that will delight them.

USER PREFERENCES:
• Food pairing: {food_type}
• Budget: {budget}
• Other preferences: {preferences}

RECOMMENDATION REQUIREMENTS:
1. Wine name and region (be specific: "2019 Cloudy Bay Sauvignon Blanc, Marlborough, New Zealand")
2. Why it pairs perfectly with their food (2-3 sentences connecting flavor to food)
3. Tasting notes (what they'll taste: acidity, fruit, tannins, etc.)
4. Approximate price range
5. Where to buy it (generic: "wine shop, grocery store, online retailers")

TONE: Authoritative, knowledgeable, enthusiastic about wine.
LENGTH: Keep under 200 words. Be helpful and specific."""

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
        # Handle empty preferences
        preferences_text = preferences if preferences else "None specified"
        
        # Use the prompt template
        prompt = WINE_RECOMMENDATION_PROMPT.format(
            food_type=food_type,
            budget=budget,
            preferences=preferences_text
        )
        
        try:
            with st.spinner("Finding the perfect wine..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=300
                )
                recommendation = response.choices[0].message.content
                st.success("Here's my recommendation:")
                st.write(recommendation)
        except Exception as e:
            st.error(f"Error getting recommendation: {e}")
