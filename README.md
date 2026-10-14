\# Highway Code RAG Chatbot (Greek)



A Retrieval-Augmented Generation (RAG) chatbot that answers questions in Greek

about the Greek Highway Code (Κ.Ο.Κ., 2007 edition), citing the pages its answers come from.



> The 2007 edition has since been amended. Answers are for demonstration only and are not legal advice.



\## How it works

1\. \*\*Ingestion\*\* (`ingest.py`): extracts text from the PDF, cleans it, splits it into overlapping chunks and embeds them with `intfloat/multilingual-e5-small`. Vectors are stored in a local Chroma database.

2\. \*\*Retrieval\*\* (`ask.py`): embeds the question and fetches the 8 most similar chunks.

3\. \*\*Generation\*\*: sends the chunks and the question to Google Gemini, which is instructed to answer only from the provided excerpts and to cite page numbers. If the answer is not in the excerpts, it says so.

4\. \*\*UI\*\* (`app.py`): a Streamlit app that shows the answer and the source passages.



\## Data cleaning

The source PDF mixes Latin letters that look like Greek ones (e.g. Latin `o` and `P`), which broke

semantic search. `ingest.py` normalizes these look-alike characters inside Greek words before embedding.



\## Run it

```bash

pip install -r requirements.txt

\# put your own copy of the Highway Code PDF in docs/

python ingest.py

\# set your key (PowerShell): $env:GEMINI\_API\_KEY = "your-key"

python -m streamlit run app.py

```

Get a free Gemini API key at https://aistudio.google.com/apikey. Never commit your key.



\## Tech stack

Python, pypdf, sentence-transformers, ChromaDB, Google Gemini API, Streamlit.



The generation step is a single function (`answer` in `ask.py`), so another LLM provider

(Claude, OpenAI, Ollama) can be swapped in easily.



\## Author

\[Ilias Anagnostou]

