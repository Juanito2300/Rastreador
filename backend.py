from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import or_

app = Flask(__name__)
CORS(app)

# Guardamos las ubicaciones y los pares vinculados
ubicaciones = {}       # {id_dispositivo: {lat, lng, timestamp}}
emparejamientos = {}   # {id_dispositivo: id_pareja}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'

app.config['SQLALCHEMY_BINDS'] = {
    'registrados': 'sqlite:///registrados.db',}

db = SQLAlchemy(app)

class registrados(db.Model):
    __bind_key__ = 'registrados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(64), unique=True, nullable=False)
    telefono = db.Column(db.String, default=False)


@app.route('/vincular', methods=['POST'])
def vincular():
    data = request.json
    mi_id = data.get("mi_id")
    pareja_id = data.get("pareja_id")

    if not mi_id or not pareja_id:
        return jsonify({"error": "Faltan datos"}), 400

    emparejamientos[mi_id] = pareja_id
    emparejamientos[pareja_id] = mi_id
    return jsonify({"status": "vinculado"})

@app.route('/ubicacion', methods=['POST'])
def actualizar_ubicacion():
    data = request.json
    dispositivo_id = data.get("id")
    lat = data.get("lat")
    lng = data.get("lng")

    if not dispositivo_id or lat is None or lng is None:
        return jsonify({"error": "Datos incompletos"}), 400

    ubicaciones[dispositivo_id] = {
        "lat": lat,
        "lng": lng,
        "timestamp": datetime.now().isoformat()
    }

    return jsonify({"status": "ok"})


@app.route('/ubicacion/<id_dispositivo>', methods=['GET'])
def obtener_ubicaciones(id_dispositivo):
    mi_ubicacion = ubicaciones.get(id_dispositivo)
    pareja_id = emparejamientos.get(id_dispositivo)
    pareja_ubicacion = ubicaciones.get(pareja_id) if pareja_id else None

    return jsonify({
        "yo": mi_ubicacion,
        "pareja": pareja_ubicacion
    })

     
@app.route("/validar_id/<id_>", methods=["GET"])
def validar_id(id_):
    usuario = registrados.query.filter_by(id=id_).first()
    if usuario:
        return jsonify({"valido": True})
    return jsonify({"valido": False})
     
@app.route("/")
def index():
    return render_template("mapa.html")


@app.route("/registrar", methods=["POST"])
def registrar():
    data = request.json
    id_ = data.get("id")
    nombre = data.get("nombre")
    correo = data.get("correo")
    telefono = data.get("telefono")

    if not id_ or not nombre or not correo or not telefono:
        return jsonify({"error": "Faltan datos"}), 400

    if registrados.query.filter(or_(registrados.id == id_, registrados.correo == correo)).first():
        return jsonify({"error": "ID o correo ya registrado"}), 400

    nuevo = registrados(id=id_, nombre=nombre, correo=correo, telefono=telefono)
    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"status": "ok"})



if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=False)