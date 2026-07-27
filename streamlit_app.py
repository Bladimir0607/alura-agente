"""
Alura Agente - Interfaz del agente inteligente para el torneo NBA2K
Desplegado en Streamlit Community Cloud.

Requiere:
- La carpeta 'faiss_index' (generada en el notebook de Colab) incluida en el repositorio.
- El secret GOOGLE_API_KEY configurado en Streamlit Cloud (Settings -> Secrets).

Ejecutar localmente:
    export GOOGLE_API_KEY="tu-api-key"
    streamlit run streamlit_app.py
"""

import os
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

st.set_page_config(page_title="Alura Agente - NBA2K Tournament", page_icon="🏀")

PROMPT_TEMPLATE = """Eres un asistente experto en el torneo NBA2K y en baloncesto/cultura general.

Sigue estas reglas para responder:
1. Si la pregunta es sobre el torneo NBA2K (reglas, equipos, formato, horarios, etc.), responde usando PRIORITARIAMENTE la información del siguiente contexto.
2. Si la pregunta NO está relacionada con el torneo (por ejemplo, historia de la NBA, jugadores como Michael Jordan, reglas generales de baloncesto, etc.), responde utilizando tu conocimiento general de forma clara y amable.
3. Si la pregunta ES sobre el torneo pero la respuesta específica NO está en el contexto, di claramente que no aparece en el reglamento (NO inventes fechas, premios ni reglas del torneo).

Contexto del torneo:
{context}

Pregunta: {question}

Respuesta:"""


def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)


@st.cache_resource(show_spinner="Cargando el agente...")
def build_qa_chain():
    api_key = os.environ.get("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("Falta configurar el secret GOOGLE_API_KEY en Streamlit Cloud (Settings -> Secrets).")
        st.stop()
    os.environ["GOOGLE_API_KEY"] = api_key

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True
    )
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.2)
    qa_prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | qa_prompt
        | llm
        | StrOutputParser()
    )


qa_chain = build_qa_chain()

st.title("🏀 Alura Agente — NBA2K Tournament")
st.write("Pregúntame sobre las reglas y equipos del torneo, o de baloncesto en general.")

question = st.text_input("Tu pregunta", placeholder="Ej: ¿Cuántos equipos participan en el torneo?")

if st.button("Preguntar") and question.strip():
    with st.spinner("Pensando..."):
        respuesta = qa_chain.invoke(question)
    st.markdown(f"**Respuesta:** {respuesta}")
