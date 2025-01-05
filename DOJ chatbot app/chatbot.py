import streamlit as st
from transformers import pipeline, GPT2Tokenizer, GPT2LMHeadModel

# Load fine-tuned model and tokenizer
model_path = "/content/drive/MyDrive/Colab Notebooks/SIH- DOJ CHATBOT/Trained LLM model"  # Path to your fine-tuned model
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Generate a pipeline for text generation
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, pad_token_id=tokenizer.eos_token_id)

def generate_response(query):
    input_text = f"<|startoftext|> {query} |bot|"
    output = generator(input_text, max_length=100, num_return_sequences=1)
    response = output[0]['generated_text'].split("|bot|")[1].split("<|endoftext|>")[0].strip()
    return response

# App Layout
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    # Login Page with Streamlit's native inputs
    if st.session_state.logged_in:
        # Chatbot Page
        st.title("Saul GoodBOT 🤖👨🏻‍⚖")
        st.write("Ask me anything my G!!! 💪😤")

        # Display the ongoing conversation
        for message in st.session_state.conversation:
            if message["role"] == "user":
                # User message
                st.markdown(f'''
                    <div style="border: 2px solid #D7CCC8; border-radius: 10px; padding: 10px; background-color: #D7CCC8; color: #000000; max-width: 80%; text-align: right; margin: 5px;">
                        <strong>You:</strong> {message["text"]}
                    </div>
                ''', unsafe_allow_html=True)
            else:
                # Bot response
                st.markdown(f'''
                    <div style="border: 2px solid #6D4C41; border-radius: 10px; padding: 10px; background-color: #6D4C41; max-width: 80%; text-align: left; margin: 5px;">
                        <strong>Bot:</strong> {message["text"]}
                    </div>
                ''', unsafe_allow_html=True)

        # Input field for user's query
        user_input = st.text_input("Your Query:", key="input_box", help="Type your message here")

        if st.button("Send"):
            if user_input.strip():
                # Add user input to the conversation
                st.session_state.conversation.append({"role": "user", "text": user_input})
                response = generate_response(user_input)
                # Add bot response to the conversation
                st.session_state.conversation.append({"role": "bot", "text": response})

        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.conversation = []  # Reset conversation on logout
            st.experimental_rerun()

    else:
        # Login Page without custom color
        st.title("Saul GoodBOT 🤖 👨🏻‍⚖ ")
        st.text(" 😮🫵 Do you know that you have rights? The Constitution says you do. 😌☝️ Well you are at right place cause it'Saul goodman!")
        st.text(" ")
        st.text("Fill your accuont details real quick! 📝")

        # Adjusted input fields for username and password using Streamlit's native input
        with st.form(key="login_form"):
            username = st.text_input("Username", key="username_input", max_chars=30)
            password = st.text_input("Password", type="password", key="password_input", max_chars=30)
            submit_button = st.form_submit_button("Login")

        if submit_button:
            if username.strip() and password.strip():  # Ensure both fields are not empty
                st.session_state.logged_in = True
                st.experimental_rerun()  # Refresh after logging in
            else:
                st.error("Please enter both username and password!")

if __name__ == "__main__":
    main()
