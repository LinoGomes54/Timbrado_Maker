import os, re, io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter


def gerar_pdf_timbrado(txt_path, timbrado_pdf, pasta_saida):
    """Gera SOMENTE o PDF final timbrado (nada de conteudo.pdf salvo)."""
    nome_base = os.path.splitext(os.path.basename(txt_path))[0]
    pdf_saida = os.path.join(pasta_saida, f"{nome_base}_timbrado.pdf")

    # === Carregar fontes ===
    try:
        pdfmetrics.registerFont(TTFont("Montserrat", os.path.join("fonts", "Montserrat-Regular.ttf")))
        pdfmetrics.registerFont(TTFont("Montserrat-Bold", os.path.join("fonts", "Montserrat-Bold.ttf")))
        FONT_NORMAL, FONT_BOLD = "Montserrat", "Montserrat-Bold"
    except:
        FONT_NORMAL, FONT_BOLD = "Helvetica", "Helvetica-Bold"

    # === Gerar conteúdo PDF em MEMÓRIA ===
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=3 * cm,
        rightMargin=2 * cm,
        topMargin=4 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle("normal", parent=styles["Normal"], fontName=FONT_NORMAL, fontSize=11, leading=16, alignment=TA_JUSTIFY)
    style_bold = ParagraphStyle("bold", parent=style_normal, fontName=FONT_BOLD)
    style_title = ParagraphStyle("title", parent=style_bold, fontSize=13, spaceAfter=10)

    elementos = []
    with open(txt_path, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            elementos.append(Spacer(1, 10))
            continue
        if linha.startswith("###"):
            texto = linha.replace("###", "").strip()
            elementos.append(Paragraph(texto, style_title))
            continue
        linha = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", linha)
        elementos.append(Paragraph(linha, style_normal))

    doc.build(elementos)
    buffer.seek(0)

    # === Mesclar com timbrado ===
    fundo_pdf = PdfReader(timbrado_pdf).pages[0]
    conteudo_pdf = PdfReader(buffer)
    writer = PdfWriter()

    for page in conteudo_pdf.pages:
        nova_pagina = PdfReader(timbrado_pdf).pages[0]
        nova_pagina.merge_page(page)
        writer.add_page(nova_pagina)

    os.makedirs(pasta_saida, exist_ok=True)
    with open(pdf_saida, "wb") as f_out:
        writer.write(f_out)

    buffer.close()
    return pdf_saida


def processar_txts_em_pasta():
    pasta_txts = "txt"
    timbrado = "timbrado/timbrado.pdf"
    pasta_saida = "pdf_atualizado"

    if not os.path.exists(pasta_txts):
        raise FileNotFoundError(f"Pasta de TXT não encontrada: {pasta_txts}")
    if not os.path.exists(timbrado):
        raise FileNotFoundError(f"Arquivo de timbrado não encontrado: {timbrado}")

    os.makedirs(pasta_saida, exist_ok=True)

    arquivos = [f for f in os.listdir(pasta_txts) if f.lower().endswith(".txt")]
    if not arquivos:
        print("Nenhum arquivo .txt encontrado.")
        return

    for arquivo in arquivos:
        caminho_txt = os.path.join(pasta_txts, arquivo)
        try:
            saida_pdf = gerar_pdf_timbrado(caminho_txt, timbrado, pasta_saida)
            print(f"✅ PDF final gerado: {saida_pdf}")
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo}: {e}")


if __name__ == "__main__":
    processar_txts_em_pasta()
