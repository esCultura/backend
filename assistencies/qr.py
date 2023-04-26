import qrcode
import io
import base64


def genera_qr(text):
    file = qrcode.make(text)
    buf = io.BytesIO()
    file.save(buf)
    buf.seek(0)
    imatge_bytes = buf.read()
    return imatge_bytes


def genera_image_data_qr(text):
    imatge_bytes = genera_qr(text)
    encoded_image = base64.b64encode(imatge_bytes).decode('ascii')
    return "data:image/png;base64,"+encoded_image
