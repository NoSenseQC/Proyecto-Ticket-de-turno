from flask import Flask, render_template, request, redirect, url_for, send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
import random
import os  # IMPORTANTE para Render

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('Login.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    if username.strip() == '' or password.strip() == '':
        return redirect(url_for('login'))

    if username == 'admin' and password == 'password':
        return redirect(url_for('admin_menu'))
    else:
        return redirect(url_for('login'))

@app.route('/admin_menu')
def admin_menu():
    return render_template('AdminMenu.html')

@app.route('/admin_consulta')
def admin_consulta():
    return render_template('AdminConsulta.html')

@app.route('/admin_catalogos')
def admin_catalogos():
    return render_template('AdminCatalogos.html')

@app.route('/User_Registrar', methods=['GET', 'POST'])
def user_registrar():
    if request.method == 'POST':
        curp = request.form['curp']
        nombre = request.form['nombre']
        paterno = request.form['paterno']
        materno = request.form['materno']
        telefono = request.form['telefono']
        celular = request.form['celular']
        correo = request.form['correo']
        nivel = request.form['nivel']
        municipio = request.form['municipio']
        asunto = request.form['asunto']

        numero_turno = random.randint(1000, 9999)

        pdf_buffer = generar_pdf(curp, nombre, paterno, materno, numero_turno)
        generar_qr(curp)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name='solicitud.pdf',
            mimetype='application/pdf'
        )

    return render_template('UserRegistrar.html')

def generar_pdf(curp, nombre, paterno, materno, numero_turno):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Solicitud de Registro")
    c.drawString(100, 730, f"Nombre: {nombre} {paterno} {materno}")
    c.drawString(100, 710, f"CURP: {curp}")
    c.drawString(100, 690, f"Turno Asignado: {numero_turno}")
    c.save()

    buffer.seek(0)
    return buffer

def generar_qr(curp):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(curp)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("static/qrcode.png")


#  CONFIGURACIÓN PARA RENDER 
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)