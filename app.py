import os
import streamlit as st
import json
import re
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage

# API key setup
OPENAI_API_KEY = "your_api_key" 
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# --- Helpers ---
def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else "{}"

def parse_ingredients(ingredients: str) -> str:
    prompt = f"""
You are a nutrition parser.
Given a list of raw ingredients, return their cleaned names, tags (e.g., vegan, keto, protein-rich), quantity, nutrition (carbs, protein, fat), and estimated calories per 100g.

Ingredients: {ingredients}

Return the result in this JSON format:
{{
  "parsed_ingredients": [
    {{
      "name": "ingredient",
      "quantity": "100g",
      "tags": ["tag1"],
      "calories_per_100g": 0,
      "nutrition": {{
        "carbs": 0,
        "protein": 0,
        "fat": 0
      }}
    }}
  ]
}}
"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=OPENAI_API_KEY)
    return llm.invoke([SystemMessage(content=prompt)]).content

def filter_ingredients(parsed_json: str, allergies: str, restrictions: str) -> str:
    prompt = f"""
You are an allergy-aware ingredient checker.
Based on:
Parsed: {parsed_json}
Allergies: {allergies}
Restrictions: {restrictions}

Return safe ingredients in JSON:
{{"safe_ingredients": ["ingredient1", "ingredient2"]}}
"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=OPENAI_API_KEY)
    return llm.invoke([SystemMessage(content=prompt)]).content

def suggest_recipes(safe_json: str, taste: str) -> str:
    prompt = f"""
You are a creative recipe recommender.
Given these safe ingredients:
{safe_json}
And taste: {taste}
Suggest 3 recipes in JSON format:
{{
  "recipes": [
    {{"title": "Recipe 1", "description": "..." }},
    {{"title": "Recipe 2", "description": "..." }},
    {{"title": "Recipe 3", "description": "..." }}
  ]
}}
"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=OPENAI_API_KEY)
    return llm.invoke([SystemMessage(content=prompt)]).content

def generate_steps(recipe_title: str) -> str:
    prompt = f"""
You are a chef assistant.
Give a detailed, step-by-step cooking process for the recipe: "{recipe_title}"
Output as a numbered list.
"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=OPENAI_API_KEY)
    return llm.invoke([SystemMessage(content=prompt)]).content

def plot_nutrition_chart(parsed_ingredients):
    total_carbs = sum(item["nutrition"]["carbs"] for item in parsed_ingredients)
    total_protein = sum(item["nutrition"]["protein"] for item in parsed_ingredients)
    total_fat = sum(item["nutrition"]["fat"] for item in parsed_ingredients)

    labels = ['Carbs', 'Protein', 'Fat']
    sizes = [total_carbs, total_protein, total_fat]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

# --- Streamlit UI ---
st.set_page_config(page_title="ChefPal - Smart Recipe Assistant", layout="wide")
st.title("👩‍🍳 ChefPal: Your AI Cooking Companion")

# Sidebar
st.sidebar.header("🍽️ Customize Your Preferences")
ingredients = st.sidebar.text_area("🧂 Available Ingredients", placeholder="e.g., tomato, onion, rice, olive oil")
allergies = st.sidebar.text_input("🚫 Allergies", placeholder="e.g., peanuts, dairy")
diet = st.sidebar.selectbox("🥗 Dietary Preference", ["None", "Vegetarian", "Vegan", "Keto", "Gluten-Free"])
taste = st.sidebar.multiselect("🌶️ Taste Preferences", ["Spicy", "Sweet", "Savory", "Sour", "Umami"])

if st.sidebar.button("🍳 Recommend Recipes"):
    st.session_state["trigger_recommend"] = True
    st.session_state.pop("show_instructions", None)
else:
    st.session_state["trigger_recommend"] = False

# Tabs
# tab1,
tab2, tab3 = st.tabs(["📋 Recipe Recommendations", "🤖 Cooking Assistant"])

# --- Tab 2: Recipe Recommendations ---
with tab2:
    st.subheader("🍲 Recommended Recipes")

    if st.session_state.get("trigger_recommend"):
        if not ingredients:
            st.warning("Please enter ingredients to begin.")
            st.stop()

        # --- Parse Ingredients ---
        with st.spinner("Parsing ingredients..."):
            parsed_raw = parse_ingredients(ingredients)
            try:
                parsed = json.loads(extract_json(parsed_raw))
                st.session_state["parsed_ingredients_data"] = parsed["parsed_ingredients"]
                st.json(parsed)
                st.session_state["agent_status_parser"] = "done"
            except json.JSONDecodeError:
                st.error("Failed to parse ingredients.")
                st.stop()

        # --- Filter ---
        with st.spinner("Filtering by allergy/diet..."):
            filtered_raw = filter_ingredients(json.dumps(parsed), allergies, diet)
            try:
                filtered = json.loads(extract_json(filtered_raw))
                st.json(filtered)
                st.session_state["agent_status_filter"] = "done"
            except json.JSONDecodeError:
                st.error("Filtering failed.")
                st.stop()

        # --- Recommend Recipes ---
        with st.spinner("Generating recipes..."):
            recipe_raw = suggest_recipes(json.dumps(filtered), ', '.join(taste))
            try:
                recipes = json.loads(extract_json(recipe_raw))
                st.session_state["recipes_data"] = recipes
                st.session_state["recipe_titles"] = [r["title"] for r in recipes["recipes"]]
                st.session_state["agent_status_recommender"] = "done"
            except json.JSONDecodeError:
                st.error("Recipe generation failed.")
                st.stop()

    if "recipe_titles" in st.session_state:
        selected_title = st.selectbox("Choose a recipe to view instructions:", st.session_state["recipe_titles"])
        if st.button("Show Instructions"):
            st.session_state["show_instructions"] = True
            st.session_state["selected_recipe"] = selected_title

    if st.session_state.get("show_instructions"):
        recipe = next((r for r in st.session_state["recipes_data"]["recipes"]
                       if r["title"] == st.session_state["selected_recipe"]), None)
        if recipe:
            st.markdown(f"### 🍽️ {recipe['title']}")
            st.markdown(recipe["description"])

            with st.spinner("Generating instructions..."):
                steps = generate_steps(recipe["title"])
                st.markdown("### 🍳 Cooking Instructions:")
                st.markdown(steps)

            st.markdown("### 🥗 Nutritional Breakdown (per 100g):")
            plot_nutrition_chart(st.session_state["parsed_ingredients_data"])

        st.session_state["agent_status_instruction"] = "done"

# --- Tab 3: Cooking Assistant ---
with tab3:
    st.subheader("🧑‍🍳 Live Cooking Assistant")
    st.info("🎙️ Voice Assistant integrated below. Please allow microphone access when prompted.")

    st.markdown("""
        <iframe 
            src="http://localhost:3000" 
            width="100%" 
            height="600px" 
            style="border:none;" 
            allow="microphone"
        ></iframe>
        """, unsafe_allow_html=True)

