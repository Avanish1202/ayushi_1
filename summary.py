import streamlit as st
from transformers import pipeline

@st.cache(allow_output_mutation=True)
def load_summarizer():
    model = pipeline("summarization", device=-1)  # Use CPU
    return model

def generate_chunks(inp_str):
    max_chunk = 500
    inp_str = inp_str.replace('.', '.<eos>')
    inp_str = inp_str.replace('?', '?<eos>')
    inp_str = inp_str.replace('!', '!<eos>')
    
    sentences = inp_str.split('<eos>')
    current_chunk = 0 
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.(chunks[chunk_id])
    return chunks

summarizer = load_summarizer()
st.title("Summarize Text")
sentence = st.text_area('Please paste your article:', height=200)
button = st.button("Summarize")

max_len = st.sidebar.slider('Select max length', 50, 500, step=10, value=150)
min_len = st.sidebar.slider('Select min length', 10, 450, step=10, value=50)
do_sample = st.sidebar.checkbox("Do sample", value=False)

if button and sentence:
    with st.spinner("Generating Summary..."):
        chunks = generate_chunks(sentence)
        res = summarizer(chunks, max_length=max_len, min_length=min_len, do_sample=do_sample)
        summary = ' '.join([summ['summary_text'] for summ in res])
        st.write(summary)
