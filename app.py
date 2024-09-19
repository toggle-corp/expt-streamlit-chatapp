import os
import uuid
from dataclasses import dataclass, field

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

SERVER_IP = os.environ.get("SERVER_IP")
SERVER_PORT = os.environ.get("SERVER_PORT")


@dataclass
class ChatAgent:
    """
    Chat interface
    """

    path: str = "chat_message"
    user_id: str = field(init=False)

    def __post_init__(self):
        """
        Initialize the ChatAgent.
        """
        self.url = f"http://{SERVER_IP}:{SERVER_PORT}/{self.path}"
        self.user_id = str(uuid.uuid4())

    def send_request(self, query: str, timeout: int = 30):
        """
        Sends the post request to the server
        """
        payload = {"query": query, "user_id": self.user_id}
        try:
            response = requests.post(url=self.url, json=payload, timeout=timeout)
        except requests.Timeout as e:
            st.write("Timeout occured. Server is not responding.")
            raise Exception(e)
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
                with st.chat_message("ai"):
                    st.markdown(item["ai"])

    def start_conversation(self):
        """
        Start a conversation in the chat interface.
        """
        self.display_messages()
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            st.chat_message("human").write(user_query)
            st.session_state.chat_history.append({"human": user_query})
            response = self.send_request(query=user_query)

            st.chat_message("ai").write(response)
            st.session_state.chat_history.append({"ai": response})


def main():
    """
    main handler
    """
    st.set_page_config(page_title="AI Chatbot For Test")

    chat_agent = ChatAgent()
    chat_agent.start_conversation()


if __name__ == "__main__":
    main()
