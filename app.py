import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

CHROMA_PATH = "chromaDB"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    st.title("Langchain RAG")
    
    # Create a text input box
    query_text = st.text_input("Enter your text here:")

    # Create a button
    button_clicked = st.button("Response")
    
    # Display text when button is clicked
    if button_clicked:
        # Prepare the DB.
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

        # Search the DB.
        results = db.similarity_search_with_relevance_scores(query_text, k=3)
        if len(results) == 0 or results[0][1] < 0.7:
            st.write("Unable to find matching results.")
            return

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        model = ChatOpenAI()
        response_text = model.invoke(prompt)

        sources = [doc.metadata.get("source", None) for doc, _score in results]
        st.write("Response:", response_text)
        st.write("Sources:", sources)

if __name__ == "__main__":
    main()
