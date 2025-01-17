import requests
from requests.exceptions import SSLError
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Caminho para o certificado digital A1 (.pem)
CERT_PATH = r"C:\Users\Rodrigo\Documents\certificado\T2R_TRANSPORTES.pem"

# URL do WSDL do serviço da SEFAZ
url = "https://mdfe.svrs.rs.gov.br/ws/MDFeConsNaoEnc/MDFeConsNaoEnc.asmx"

# Cabeçalhos HTTP
headers = {
    "Content-Type": "application/soap+xml; charset=utf-8"
}

# Corpo da mensagem SOAP com namespace corrigido
body = f"""
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Header>
    <mdfeCabecMsg xmlns="http://www.portalfiscal.inf.br/mdfe/wsdl/MDFeConsNaoEnc">
      <cUF>31</cUF>
      <versaoDados>3.00</versaoDados>
      <CNPJ>22664479000101</CNPJ>
    </mdfeCabecMsg>
  </soap12:Header>
  <soap12:Body>
    <mdfeConsNaoEnc xmlns="http://www.portalfiscal.inf.br/mdfe/wsdl/MDFeConsNaoEnc">
      <mdfeDadosMsg xmlns="http://www.portalfiscal.inf.br/mdfe/wsdl/MDFeConsNaoEnc">
        <tpAmb>1</tpAmb>
        <xServ>CONSULTAR NÃO
ENCERRADOS</xServ>
        <cUF>31</cUF>
      </mdfeDadosMsg>
    </mdfeConsNaoEnc>
  </soap12:Body>
</soap12:Envelope>
"""

# Função para gerar o PDF
def gerar_pdf(dados, nome_arquivo="consulta_mdfe.pdf"):
    pdf = canvas.Canvas(nome_arquivo, pagesize=A4)
    width, height = A4
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 100, "Resultado da Consulta MDFe")
    pdf.setFont("Helvetica", 12)
    text = pdf.beginText(100, height - 140)
    text.textLines(dados)
    pdf.drawText(text)
    pdf.save()
    print(f"PDF gerado com sucesso: {nome_arquivo}")

# Enviar a requisição SOAP e capturar a resposta
try:
    response = requests.post(url, headers=headers, data=body, cert=CERT_PATH, verify=True)
    response.raise_for_status()  # Verifica se houve um erro HTTP
    print(response.text)
    gerar_pdf(response.text)
except SSLError as ssl_error:
    print(f"Erro de SSL: {ssl_error}")
except Exception as e:
    print(f"Erro ao consultar: {e}")
