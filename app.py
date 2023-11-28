import streamlit as st
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from sidebar import *

st.set_page_config(page_title="Your Email GPT assistant")
st.title('Email Assistant')

sbar()
# receive inputs from user
email = st.text_area(
    "Enter your email"
)
username = st.text_input("Enter your name")
more_info = st.text_input("Anything else you want to add?")

def draft_email(user_email, name, additional_info):
    """
    Describe what this function does
    Args:
    user_email: (str)
    name: (str)

    Returns:

    """
    try:
        API_KEY = st.session_state['OPENAI_API_KEY']
    except Exception as e:
        response = st.error("Invalid [OpenAI API key](https://beta.openai.com/account/api-keys) or not found")
        return response
    
    draft_template = """
        You are a helpful assistant that drafts an email reply based on an a new email.

        Keep your reply short and straight to the point and mimic the style of the email.

        Do not assume anything and do not create fake informations.
        
        Start your reply by saying: "Hi {name}, here's a draft for your reply:". And then proceed with the reply on a new line.

        Make sure to sign of with {signature}.
        """

    signature = f"Best regards, \n\{name}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(draft_template)


    human_prompt = """Here's the email to reply to {user_email}
                Also, consider comments from the user when generating your email: {additional_info}
        """
    
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    with get_openai_callback() as cb:

        llm = ChatOpenAI(openai_api_key=API_KEY, model_name="gpt-3.5-turbo", temperature=0.01)
        chain = LLMChain(llm=llm, prompt=chat_prompt)
        response = chain.run(user_email=user_email, signature=signature, name=name, additional_info=additional_info)
    
    cost = cb.total_cost # retrieve from get_openai_callback
    return response, cost

submit_button = st.button(label="Draft")

if submit_button:
    with st.spinner("Working hard.."):
        try:
            response, cost = draft_email(email, username, more_info)
            st.text_area("Your draft email", response, height=600)
            st.write(f"Total Cost (USD): ${cost}")
        except Exception as e:
            st.write("Did you enter your own gpt api key?")




    
