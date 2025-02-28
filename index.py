
from flask import Flask, render_template,redirect,url_for,request,flash,jsonify
from flask_mysqldb import MySQL
from datetime import date
app = Flask(__name__)

# Configuración de los parámetros para conectarse a MySQL
app.config['MYSQL_HOST'] = 'boq3eoaobhvxboc3lwbe-mysql.services.clever-cloud.com'  
app.config['MYSQL_USER'] = 'uwhsry1gc568d68q' 
app.config['MYSQL_PASSWORD'] = 'IAlNkLmyOO8jYdDzndy7' 
app.config['MYSQL_DB'] = 'boq3eoaobhvxboc3lwbe'
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id,titulo,descripcion,estado,fecha FROM primeraprueba')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', contacts=data)

@app.route('/registrar_actividad', methods=['POST'])
def registrar_actividad():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        estado = request.form.get('estado', '').strip() 
        fecha = date.today()
        # Validaciones
        if not titulo or not descripcion:
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for('index'))

        if not estado or estado not in ['1', '0']:  # Validar que sea una opción válida
            flash("Selecciona una opción válida en el campo 'Estado'.", "error")
            return redirect(url_for('index'))
        print(titulo)
        print(descripcion)
        print(estado)
        print(fecha)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO primeraprueba (titulo, descripcion, estado, fecha) VALUES (%s, %s, %s, %s)', (titulo, descripcion, estado,fecha))
        mysql.connection.commit()
        flash("Actividad registrada con éxito.", "success")
        return redirect(url_for('index'))

@app.route('/editar_actividad/<int:id>')
def editar_actividad(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM primeraprueba WHERE id = %s', (id,))
    actividad = cur.fetchone()
    cur.close()
    
    if actividad:
        return jsonify({
            "id": actividad[0],
            "titulo": actividad[1],
            "descripcion": actividad[2],
            "estado": actividad[3]
        })  # Retorna los datos en JSON sin redireccionar
    else:
        return jsonify({"error": "Actividad no encontrada"}), 404

@app.route('/actualizar_actividad', methods=['POST'])
def actualizar_actividad():
    id = request.form.get('id')
    titulo = request.form.get('titulo', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    estado = request.form.get('estado', '').strip()
    
    if not id or not titulo or not descripcion or estado not in ['1', '0']:
        return jsonify({"error": "Todos los campos son obligatorios."}), 400

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE primeraprueba 
        SET titulo = %s, descripcion = %s, estado = %s 
        WHERE id = %s
    """, (titulo, descripcion, estado, id))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({"message": "Actividad actualizada con éxito."})    

@app.route('/eliminar_actividad/<id>')
def eliminar_actividad(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM primeraprueba WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Contact deleted')
    return redirect(url_for('index'))

# Bloque principal que ejecuta la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
