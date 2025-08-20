from flask import Flask, request, jsonify, render_template_string
import pymssql

app = Flask(__name__)

def get_connection():
    conn = pymssql.connect(
        server='basethepeppa.mssql.somee.com',
        user='bismar-ac_SQLLogin_1',
        password='uex7yg16hs',
        database='basethepeppa'
    )
    return conn

# Página principal con formulario
@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = ''
    if request.method == 'POST':
        lectura = request.form.get('lectura')
        if lectura:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Lecturas (lectura) VALUES (%s)", (lectura,))
                conn.commit()
                cursor.close()
                conn.close()
                mensaje = f"Lectura '{lectura}' insertada correctamente."
            except Exception as e:
                mensaje = f"Error: {str(e)}"
        else:
            mensaje = "Por favor, ingresa un valor de lectura."

    # HTML simple embebido
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Registro de Lecturas</title>
    </head>
    <body>
        <h1>Insertar Lectura</h1>
        <form method="post">
            <label for="lectura">Lectura:</label>
            <input type="text" id="lectura" name="lectura" required>
            <button type="submit">Enviar</button>
        </form>
        <p>{{ mensaje }}</p>
    </body>
    </html>
    '''
    return render_template_string(html, mensaje=mensaje)

# API para inserción vía JSON
@app.route('/insertar', methods=['POST'])
def insertar_lectura():
    try:
        data = request.json
        lectura = data.get('lectura')

        if lectura is None:
            return jsonify({"error": "Falta el campo lectura"}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Lecturas (lectura) VALUES (%s)", (lectura,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "OK", "lectura": lectura}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
