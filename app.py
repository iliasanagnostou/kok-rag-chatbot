import streamlit as st
from ask import answer

st.set_page_config(page_title="ΚΟΚ Chatbot", page_icon="🚦")
st.title("🚦 Chatbot για τον Κώδικα Οδικής Κυκλοφορίας")
st.caption("Βασίζεται στην έκδοση του 2007 και δεν αποτελεί νομική συμβουλή.")

question = st.text_input("Κάνε μια ερώτηση:")
if question:
    with st.spinner("Αναζήτηση..."):
        text, hits = answer(question)
    st.markdown(text)
    with st.expander("Αποσπάσματα που χρησιμοποιήθηκαν"):
        for doc, meta in hits:
            st.markdown(f"**Σελίδα {meta['page']}**")
            st.text(doc)