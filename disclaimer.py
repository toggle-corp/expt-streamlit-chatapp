import streamlit as st


@st.dialog("Disclaimer and Terms of Use", width="large")
def show_disclaimer(local_storage):
    """Show disclaimer message"""
    text = """

        The information provided by this chatbot is for informational purposes only.
        The chatbot does not store any user-related personal data, ensuring complete anonymity. 
        However queries are stored in its backend for analysis and improvement purposes. 
        Users are advised not to input sensitive, confidential, or personally identifiable information into this platform.
        <br><br>
        
        By using this chatbot, you acknowledge and agree to these terms.

    """
    st.html(text)

    if st.button("Accept", use_container_width=True):
        local_storage.setItem("chatbot_consent_confirm", "true")
        st.rerun()
