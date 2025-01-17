import streamlit as st
import PyPDF2
from urllib.parse import quote

# Função para extrair a descrição do PDF
def extrair_descricao(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text = page.extract_text()
            st.write(f"Texto extraído: {text}")  # Log para verificar o texto extraído (para depuração)
            for line in text.split("\n"):
                if "DESCRICAO:" in line:
                    return line.replace("DESCRICAO:", "").strip()
    except Exception as e:
        st.error(f"Erro ao processar o PDF: {e}")
    return None

# Título da aplicação
st.title("Renomeador de Comprovantes Bancários")

# Fazer o upload de múltiplos arquivos
uploaded_files = st.file_uploader("Envie os comprovantes em PDF", accept_multiple_files=True, type=["pdf"])

# Verificar se os arquivos foram enviados
if uploaded_files:
    for i, uploaded_file in enumerate(uploaded_files):
        st.write(f"Arquivo {i+1}: {uploaded_file.name}")  # Log para verificar se o arquivo foi carregado

        # Tentar extrair a descrição
        descricao = extrair_descricao(uploaded_file)

        # Se a descrição for encontrada, proceder com o renomeio e download
        if descricao:
            new_filename = f"Comprovante_{descricao.replace(' ', '_')}.pdf"
            file_bytes = uploaded_file.getvalue()

            # Exibir o botão de download
            st.download_button(
                label=f"Baixar {new_filename}",
                data=file_bytes,
                file_name=new_filename,
                mime="application/pdf",
                key=f"download_{i}_{uploaded_file.name}"
            )
            
            # Criar link para o WhatsApp
            mensagem = f"Segue o comprovante: {new_filename}"
            whatsapp_url = f"https://wa.me/?text={quote(mensagem)}"
            st.markdown(f'[📤 Enviar pelo WhatsApp]({whatsapp_url})', unsafe_allow_html=True)
        
        else:
            st.warning(f"Não foi possível extrair a DESCRICAO do arquivo {uploaded_file.name}")

# Mensagem caso nenhum arquivo tenha sido enviado
else:
    st.info("Por favor, envie um ou mais arquivos PDF para renomear.")
