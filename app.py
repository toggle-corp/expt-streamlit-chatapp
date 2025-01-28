import os
import time
import uuid
from dataclasses import dataclass

import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_local_storage import LocalStorage

from disclaimer import show_disclaimer

load_dotenv()

SERVER_IP = os.environ.get("SERVER_IP")
SERVER_PORT = os.environ.get("SERVER_PORT")


@dataclass
class ChatAgent:
    """
    Chat interface
    """

    path: str = "chat_message"

    def __post_init__(self):
        """
        Initialize the ChatAgent.
        """
        self.url = f"http://{SERVER_IP}:{SERVER_PORT}/{self.path}"
        self.ai_avatar = "https://togglecorp.com/favicon.png"
        if "user_id" not in st.session_state:
            st.session_state["user_id"] = str(uuid.uuid4())

    def stream_data(self, result):
        for word in result.split(" "):
            yield word + " "
            time.sleep(0.10)

    def send_request(self, query: str, timeout: int = 30):
        """
        Sends the post request to the server
        """

        payload = {"query": query, "user_id": st.session_state["user_id"]}
        try:
            response = requests.post(url=self.url, json=payload, timeout=timeout)
        except requests.Timeout:
            e = TimeoutError("Server is not responding")
            st.exception(e)
            return

        if response.status_code == 200:
            return response.json()
        else:
            st.write(f"Some errors occured while sending the request. http code: {response.status_code}")

    def display_messages(self):
        """
        Display messages in the chat interface.
        If no messages are present, adds a default AI message.
        """
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            st.session_state.chat_history.append({"ai": "I am a chabot with knowledge base. How can I help you?"})

        for item in st.session_state.chat_history:
            if "human" in item:
                with st.chat_message("human"):
                    st.markdown(item["human"])
            else:
                with st.chat_message("ai", avatar=self.ai_avatar):
                    st.markdown(item["ai"])

    def start_conversation(self):
        """
        Start a conversation in the chat interface.
        """
        self.display_messages()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query and len(user_query.split()) > 50:
            st.warning("No more than 50 words are allowed in a single query ")

        elif user_query:
            st.chat_message("human").write(user_query)
            st.session_state.chat_history.append({"human": user_query})
            response = self.send_request(query=user_query)
            if response:
                st.chat_message("ai", avatar=self.ai_avatar).write_stream(self.stream_data(response))
                st.session_state.chat_history.append({"ai": response})


def main():
    """
    main handler
    """
    st.set_page_config(page_title="AI Chatbot For Test")
    local_storage = LocalStorage()

    consent_status = local_storage.getItem("chatbot_consent_confirm")

    if consent_status != "true":
        show_disclaimer(local_storage=local_storage)

    else:
        chat_agent = ChatAgent()
        chat_agent.start_conversation()

    if consent_status == "true" and st.session_state.get("chatbot_consent_confirm") != "true":
        local_storage.setItem("chatbot_consent_confirm", "true")


if __name__ == "__main__":
    main()
