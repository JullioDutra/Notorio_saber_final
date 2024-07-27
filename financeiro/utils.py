import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def gerar_qr_code_pix(chave_pix, nome_recipiente, cidade, valor, identificador):
    # Constrói o conteúdo do código QR para o Pix
    qr_code_data = f"{chave_pix}|{nome_recipiente}|{cidade}|{valor}|{identificador}"

    # Cria a instância do QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_code_data)
    qr.make(fit=True)

    # Gera a imagem do QR code
    img = qr.make_image(fill='black', back_color='white')

    # Salva a imagem em um objeto de arquivo
    qr_code_io = BytesIO()
    img.save(qr_code_io, format='PNG')
    qr_code_content = ContentFile(qr_code_io.getvalue(), 'qrcode.png')

    return qr_code_content
