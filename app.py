import os
from dataclasses import dataclass

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

    def __post_init__(self):
        """
        Initialize the ChatAgent.
        """
        self.url = f"http://{SERVER_IP}:{SERVER_PORT}/{self.path}"

    def send_request(self, query: str, timeout: int = 30):
        """
        Sends the post request to the server
        """
        payload = {"query": query}
        try:
            response = requests.post(url=self.url, json=payload, timeout=timeout)
        except requests.Timeout as e:
            st.write("Timeout occured. Server is not responding.")
            raise Exception(e)
        if response.status_code == 200:
            return response.json()
        else:
            st.write(f"Some errors occured while sending the request. http code: {response.status_code}")

    def start_conversation(self):
        """
        Start a conversation in the chat interface.
        """
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            st.chat_message("human").write(user_query)
            response = self.send_request(query=user_query)

            st.chat_message("ai").write(response)


def main():
    """
    main handler
    """
    st.set_page_config(page_title="AI Chatbot For Test")

    chat_agent = ChatAgent()
    chat_agent.start_conversation()


if __name__ == "__main__":
    main()
