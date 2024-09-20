from openai import OpenAI
import streamlit as st
import time
import os

# Set OpenAI API key (remember to add your API key)
api_key = os.environ.get('OPENAI_API_KEY')
# Check if the API key is missing or invalid
if api_key is None:
    raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key)

# GPT-3.5/4 model parameters
temperature = 0.85
frequency_penalty = 1.0
presence_penalty = 1.0
timeout_duration = 1.5  # Timer set for 10 seconds

# Function to generate opinionated text
def generate_gpt4_continuation(prompt, stance):
    if stance == 'positive':
        engineered_prompt = f"Is social media good for society? Explain why social media is good for society: {prompt}"
    else:
        engineered_prompt = f"Is social media good for society? Explain why social media is bad for society: {prompt}"


    response = client.chat.completions.create(
        model="gpt-4",  # Use "gpt-4" if you have access gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are an AI assistant that writes persuasive opinions based on a specified stance."},
            {"role": "user", "content": engineered_prompt}
        ],
        temperature=temperature,
        max_tokens=300,
        frequency_penalty=frequency_penalty,  # Apply repetition penalty
        presence_penalty=presence_penalty 
    )
    
    # Return the response
    # return response['choices'][0]['message']['content'].strip()
    return response.choices[0].message.content.strip()

# Streamlit app setup
st.title("Interactive Opinionated Auto-Completer - NLP Class Group 2")
st.write("Start typing your text about social media. The system will autocomplete after 10 seconds of inactivity.")

# Create a text input area (textarea serves as a simple text editor)
if 'user_text' not in st.session_state:
    st.session_state.user_text = ""  # Initial text

if 'last_typed' not in st.session_state:
    st.session_state.last_typed = time.time()  # Track the last time user typed

if 'autocomplete_triggered' not in st.session_state:
    st.session_state.autocomplete_triggered = False  # Track whether autocomplete was already triggered

# Text area for user input
user_input = st.text_area("Your text:", value=st.session_state.user_text, height=200)

# Select stance for biased continuation
stance = st.selectbox("Select the opinion stance for continuation:", ['positive', 'negative'])

# Detect if user has typed something new
if user_input != st.session_state.user_text:
    # User typed something new: reset the timer and set autocomplete_triggered to False
    st.session_state.last_typed = time.time()
    st.session_state.autocomplete_triggered = False  # Allow autocomplete again since user typed
    st.session_state.user_text = user_input  # Update the stored user_text

# Check if 10 seconds have passed without user input and autocomplete hasn't been triggered yet
if time.time() - st.session_state.last_typed > timeout_duration and not st.session_state.autocomplete_triggered:
    continuation = generate_gpt4_continuation(st.session_state.user_text, stance)
    st.session_state.user_text += "\n\n" + continuation  # Append the GPT-3 continuation
    st.session_state.autocomplete_triggered = True  # Ensure we won't re-trigger autocomplete
    st.rerun()  # Rerun to display the updated text

# Display the current content in the text editor
st.write("### Completed text:")
st.write(st.session_state.user_text)

