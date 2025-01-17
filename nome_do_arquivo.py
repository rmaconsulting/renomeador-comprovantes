import streamlit as st
import PyPDF2
from urllib.parse import quote
from io import BytesIO

# Função para extrair a descrição do PDF
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

# Função para gerar um PDF a partir de um arquivo carregado
def gerar_pdf_individual(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    writer = PyPDF2.PdfWriter()
    
    # Adiciona todas as páginas do arquivo ao writer
    for page in reader.pages:
        writer.add_page(page)
    
    output_pdf = BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)
    
    return output_pdf

# Função para limpar a sessão e simular um F5 (atualizar a página)
def limpar_arquivos():
    if 'uploaded_files' in st.session_state:
        del st.session_state.uploaded_files

# Título da aplicação
st.title("Renomeador de Comprovantes Bancários")

# Botão para limpar os arquivos carregados
if st.button('Limpar registros'):
    limpar_arquivos()  # Limpa os arquivos carregados e simula o F5

# Fazer o upload de múltiplos arquivos
uploaded_files = st.file_uploader("Envie os comprovantes em PDF", accept_multiple_files=True, type=["pdf"])

# Adicionando novos arquivos à sessão (caso tenham sido carregados)
if uploaded_files:
    st.session_state.uploaded_files = uploaded_files  # Atualiza os arquivos na sessão
    uploaded_files = uploaded_files

# Exibir contagem de arquivos convertidos
if uploaded_files:
    st.subheader(f"Total de arquivos convertidos: {len(uploaded_files)}")

# Processa os arquivos se houverem arquivos carregados
if uploaded_files:
    for i, uploaded_file in enumerate(uploaded_files):
        st.write(f"Arquivo {i+1}: {uploaded_file.name}")  # Exibir o nome do arquivo carregado

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

    # Adicionar o botão para baixar todos os arquivos como PDFs individuais
    if st.button("Baixar todos os arquivos convertidos"):
        for i, uploaded_file in enumerate(uploaded_files):
            descricao = extrair_descricao(uploaded_file)
            if descricao:
                new_filename = f"Comprovante_{descricao.replace(' ', '_')}.pdf"
                pdf_individual = gerar_pdf_individual(uploaded_file)
                st.download_button(
                    label=f"Baixar {new_filename}",
                    data=pdf_individual,
                    file_name=new_filename,
                    mime="application/pdf",
                    key=f"download_{i}_{new_filename}"
                )

# Mensagem caso nenhum arquivo tenha sido enviado
else:
    st.info("Por favor, envie um ou mais arquivos PDF para renomear.")
