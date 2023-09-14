import streamlit as st
from zipfile import ZipFile
import backend
import os

st.title("Document Processing")
st.write(
    """This page is for processing protocol docx file into JSON files. 
    The current intended use case is to create a dataset of protocols for fine-tuning the AIs for future protocol generation. 
    A folder of many documents can be entered for processing as well.""")

# multiple files can be uploaded if all selected at once
file = st.file_uploader("Upload protocol(s)", type=['docx'], accept_multiple_files=True)
results = []
if file:
    for f in file:
        results.append(backend.process_full_word_doc(f))
    jsonfiles = backend.create_jsons(results)
    zfile = backend.create_zip()
    with open("json_data.zip", 'rb') as file:
        st.download_button(
                label="Download JSON file(s) as zipfile",
                data=file,
                file_name = 'output.zip'
            )
    backend.delete_zip()