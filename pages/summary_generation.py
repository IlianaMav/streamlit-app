import streamlit as st
from transformers import AutoTokenizer, pipeline
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, AutoModelForCausalLM
import backend

# this is an access token for Eve's huggingface account, because Llama 2 is a gated model
# in order to get access to llama2, submit form to Meta and create a huggingface account
ACCESS_TOKEN = "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"

# changes session state var so that when page refreshes, pegasus isn't run again 
# this is because when the button is pressed, all of the code in this page is run again
# (except for session_state vars because of the cache)
def submitted():
    st.session_state.update(submit=True)


def main():
    if 'submit' not in st.session_state:
        st.session_state.submit = False

    st.title("Summary generation using GenAI")

    st.write(
        """This page is for usage of generative AI to supplement protocol creation. 
        The current supported use case is to generate the abstract of a protocol when given the rest of a written protocol. Upon further development, generative AI will supplement other aspects of the protocol creation as well.
        Toggle the buttons below for your preferred model, configurations, and current use case.""")

    st.write("Current configurations: ")
    col1, col2 = st.columns(2, gap="medium")
    with col1: 
        st.header("Use Case")
        abs_box = st.checkbox(label="make abstract")
    with col2: 
        st.header("AI Model")
        pegasus_box = st.checkbox(label="Pegasus")
        llama_box = st.checkbox(label="llama 2")
    docxfile = st.file_uploader("Upload protocol", type=['docx'])
    jsonfile = None
    if docxfile:
        jsonfile = backend.process_full_word_doc(docxfile)
        folders = backend.create_jsons(jsonfile)
    if abs_box and pegasus_box:
        if jsonfile:
            with st.spinner("Running pegasus..."):
                if not st.session_state.submit:
                    tokenizer, model = load_pegasus()
                    output_dict = backend.run_pegasus(jsonfile, tokenizer, model)
                    json_output = backend.create_jsons(output_dict)
                    zfile = backend.create_zip()
            with open("json_data.zip", 'rb') as file:
                st.download_button(
                    label="Download pegasus output as zip file",
                    data=file,
                    file_name="pegasus_output.zip",
                    on_click = submitted,
                )
    if abs_box and llama_box and not pegasus_box:
        if jsonfile:
            with st.spinner("Running llama2..."):
                if not st.session_state.submit:
                    tokenizer, model = load_llama2()
                    if tokenizer and model:
                        output_dict = backend.run_llama2(jsonfile, tokenizer, model)
                        st.write(tokenizer)

# prevent having to reload the model after every interaction with website
@st.cache_resource
def load_pegasus():
    with st.spinner("Loading pegasus model..."):
        model_id = "google/pegasus-xsum"
        tokenizer = PegasusTokenizer.from_pretrained(model_id)
        model = PegasusForConditionalGeneration.from_pretrained(model_id)
    return (tokenizer, model)

@st.cache_resource
def load_llama2():
    model_id = "meta-llama/Llama-2-13b-chat-hf"
    with st.spinner("Loading llama2 model..."):
        try:
            model = AutoModelForCausalLM.from_pretrained(model_id, use_auth_token=ACCESS_TOKEN)
            tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        except:
            st.write("Llama 2 requires GPU support to run. Use pegasus instead.")
            return (None, None)
    return (tokenizer, model)

main()
    