import streamlit as st
import backend # import file with pegasus code

st.title("Protocol Use Case Landing Page")
st.write("""This web application is a proof of concept for the Non Interventional Protocol Use Case.
         The models used are not yet trained/fine-tuned on Pfizer specific data or use cases. 
         Navigation:
         "Document Processing" page is for the creation of a fine-tuning dataset using protocols.
         "Summary Generation" page is for usage of AI to supplement creation of protocols""")

