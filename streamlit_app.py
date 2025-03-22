import streamlit as st
from openai import OpenAI
import streamlit as st
import json

def run():

    st.title("💬 SafeHarbor AI")
    st.write(
        "Welcome to **SafeHarbor AI**, your trusted companion in the fight against financial fraud and investment scams! In today's fast-paced digital world, staying vigilant against deceptive schemes is more important than ever. FraudShield AI leverages cutting-edge artificial intelligence to empower individuals with the knowledge and tools to protect their finances and make informed decisions."
    )




# Show title and description.




if __name__ == "__main__":
    run()


# Custom CSS for the buttons
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# Initialize session variables if they do not exist
default_values = {'current_index': 0, 'current_question': 0, 'score': 0, 'selected_option': None, 'answer_submitted': False}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# Load quiz data
with open('content/quiz_data.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

def restart_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

def submit_answer():
    # Check if an option has been selected
    if st.session_state.selected_option is not None:
        # Mark the answer as submitted
        st.session_state.answer_submitted = True
        # Check if the selected option is correct
        if st.session_state.selected_option == quiz_data[st.session_state.current_index]['answer']:
            st.session_state.score += 10
    else:
        # If no option selected, show a message and do not mark as submitted
        st.warning("Please select an option before submitting.")

def next_question():
    st.session_state.current_index += 1
    st.session_state.selected_option = None
    st.session_state.answer_submitted = False

# Title and description
st.title("Financial Education")

# Progress bar
progress_bar_value = (st.session_state.current_index + 1) / len(quiz_data)
st.metric(label="Score", value=f"{st.session_state.score} / {len(quiz_data) * 10}")
st.progress(progress_bar_value)

# Display the question and answer options
question_item = quiz_data[st.session_state.current_index]
st.subheader(f"Question {st.session_state.current_index + 1}")
st.title(f"{question_item['question']}")
st.write(question_item['information'])

# Display the video if the question contains a "video" key
if "video" in question_item:
    st.video(question_item["video"])  # Assuming the value of "video" is a URL or local video path

st.markdown(""" ___""")

# Answer selection
options = question_item['options']
correct_answer = question_item['answer']

if st.session_state.answer_submitted:
    for i, option in enumerate(options):
        label = option
        if option == correct_answer:
            st.success(f"{label} (Correct answer)")
        elif option == st.session_state.selected_option:
            st.error(f"{label} (Incorrect answer)")
        else:
            st.write(label)
else:
    for i, option in enumerate(options):
        if st.button(option, key=i, use_container_width=True):
            st.session_state.selected_option = option

st.markdown(""" ___""")

# Submission button and response logic
if st.session_state.answer_submitted:
    if st.session_state.current_index < len(quiz_data) - 1:
        st.button('Next', on_click=next_question)
    else:
        st.write(f"Quiz completed! Your score is: {st.session_state.score} / {len(quiz_data) * 10}")
        if st.button('Restart', on_click=restart_quiz):
            pass
else:
    if st.session_state.current_index < len(quiz_data):
        st.button('Submit', on_click=submit_answer)




# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)
    #client = OpenAI(
    #    base_url="wss://spark-api.xf-yun.com/v1.1/chat",
    #    api_key="46909103&MTU1YWQ5MGFkNzhkYTBmM2NjNzMyYTBj&e8583878e386f949c0776808a7160823", 
    #)


    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )


