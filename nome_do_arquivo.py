import streamlit as st
import PyPDF2
import os
from urllib.parse import quote

def extrair_descricao(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text = page.extract_text()
            for line in text.split("\n"):
                if "DESCRICAO:" in line:
                    return line.replace("DESCRICAO:", "").strip()
    except Exception as e:
        st.error(f"Erro ao processar o PDF: {e}")
    return None

st.title("Renomeador de Comprovantes Bancários")

uploaded_files = st.file_uploader("Envie os comprovantes em PDF", accept_multiple_files=True, type=["pdf"])

if uploaded_files:
    for i, uploaded_file in enumerate(uploaded_files):
        descricao = extrair_descricao(uploaded_file)
        if descricao:
            new_filename = f"Comprovante_{descricao.replace(' ', '_')}.pdf"
            file_bytes = uploaded_file.getvalue()
            st.download_button(
                label=f"Baixar {new_filename}",
                data=file_bytes,
                file_name=new_filename,
                mime="application/pdf",
                key=f"download_{i}_{uploaded_file.name}"
            )
            
            # Criar link do WhatsApp
            mensagem = f"Segue o comprovante: {new_filename}"
            whatsapp_url = f"https://wa.me/?text={quote(mensagem)}"
            st.markdown(f'[📤 Enviar pelo WhatsApp]({whatsapp_url})', unsafe_allow_html=True)
        else:
            st.warning(f"Não foi possível extrair a DESCRICAO do arquivo {uploaded_file.name}")

