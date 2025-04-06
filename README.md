👩‍🍳 ChefPal: Smart AI Cooking Companion

ChefPal is a Streamlit-based multi-agent web application leveraging OpenAI's GPT-4o-mini model to provide personalized, nutritional recipe recommendations, step-by-step cooking guidance, and nutritional insights.

🚀 Features

Intelligent Ingredient Parsing: Extract detailed nutritional data and tags from raw ingredients.

Allergy and Diet Filtering: Automatically filters recipes according to allergies and dietary restrictions.

Customized Recipe Recommendations: Unique recipes tailored to individual taste preferences.

Interactive Cooking Assistant: Step-by-step cooking instructions and real-time voice assistance.

Nutritional Visualization: Clear nutritional breakdown presented through intuitive charts.

Multi-Agent System: Seamlessly integrates multiple AI agents to optimize recipe recommendation, filtering, and cooking assistance.

🔧 Technologies Used

Streamlit: Interactive UI framework.

React: Used for building the real-time voice-based cooking assistant.

OpenAI GPT-4o-mini: AI for natural language processing.

LangChain: Integration with language models.

Matplotlib: Nutritional data visualization.

🛠️ Setup Instructions

Step 1: Clone the Repository

git clone <repository_url>
cd <repository_directory>

Step 2: Install Dependencies

pip install streamlit langchain_openai openai matplotlib

Step 3: Configure API Key
Create a .env file:

OPENAI_API_KEY=your_api_key_here

Step 4: Run the Application

streamlit run your_script_name.py

The application opens automatically in your default browser.

🌐 Usage

Enter ingredients in the sidebar.

Specify allergies, dietary, and taste preferences.

Click Recommend Recipes.

Select recipes for detailed cooking instructions and nutritional insights.

Use the Live Cooking Assistant for hands-free cooking guidance.

🎙️ Live Cooking Assistant Integration

Real-time voice interface.

Run your local voice-assistant server at:

http://localhost:3000

🌟 Acknowledgments

OpenAI GPT models

Streamlit and LangChain communities
