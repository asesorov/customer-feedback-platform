import streamlit as st
import json
from src.llm.agent import Agent

# Load the JSON data
with open('E:\\customer-feedback-platform\\src\\data\\reviews_data_vladimir_pyaterochka.json', 'r', encoding='utf-8') as f:
    shop_data_vladimir_pyaterochka = json.load(f)

# Extract addresses from the keys (URLs)
addresses = [data["address"] for data in shop_data_vladimir_pyaterochka.values()]

# Create a Streamlit app
st.title('Address Review Analyzer')

# Create a dropdown to select an address
selected_address = st.selectbox('Select an address:', addresses)

# Create a button to trigger the analysis
if st.button('Analyze'):
    # Get the key (URL) associated with the selected address
    selected_url = None
    for url, data in shop_data_vladimir_pyaterochka.items():
        if data["address"] == selected_address:
            selected_url = url
            break

    # Get the reviews for the selected address
    reviews = shop_data_vladimir_pyaterochka.get(selected_url, {}).get("reviews_list", [])

    # Prepare the reviews for analysis
    review_text = ""
    for review in reviews:
        review_text += f"Рейтинг: {review['rating']}\nОтзыв: {review['text']}\nДата: {review['date']}\n\n"

    # Analyze the reviews using the agent
    model_path = "D:\\llama.cpp\\models\\7b\\ggml-model-q4_1.bin"
    overall_sys_prompt = 'Ты — русскоязычный автоматический анализатор отзывов. Ты получаешь на вход несколько отзывов. Проанализируй текст отзывов и выделите ключевые проблемы в этих отзывах. Ответ дай коротким списком. Обобщи.'
    review_filials_agent = Agent(model_path, overall_sys_prompt)
    request = 'Отзывы для анализа:\n' + review_text
    result = review_filials_agent.interact(request)

    # Display the analysis result
    st.subheader('Analysis Result:')
    st.write(result)
