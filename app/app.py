from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time

# Inicialización de Flask
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de SQLAlchemy
db = SQLAlchemy(app)

# Modelo de ejemplo
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

with app.app_context():
    db.create_all()
    

# Función para enviar métricas a Zabbix
import subprocess

def send_to_zabbix(key, value):
    subprocess.run([
        "zabbix_sender",
        "-z", "zabbix-server",
        "-p", "10051",
        "-s", "python_app",
        "-k", key,
        "-o", str(value)
    ])

# Ruta principal
@app.route('/')
def hello():
    send_to_zabbix('web.page_views', 1)
    return "Hello from Flask with Zabbix!"

# Ruta simulando carga lenta
@app.route('/slow')
def slow():
    start = time.time()
    time.sleep(2)
    duration = time.time() - start
    send_to_zabbix('web.slow_response_time', duration)
    return "Simulated slow response"

# Ruta de login simulado
@app.route('/login')
def login():
    user_id = 123
    send_to_zabbix(f'web.login.success[{user_id}]', 1)
    return "Login successful"

# Ruta de carrito simulado
@app.route('/cart')
def cart():
    item_count = 5
    send_to_zabbix('web.cart.items', item_count)
    return f"Cart has {item_count} items"

@app.route('/add/<name>')
def add_user(name):
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    send_to_zabbix('web.user_created', 1)
    return f"User '{name}' added successfully!"

@app.route('/users')
def list_users():
    users = User.query.all()
    send_to_zabbix('web.user_listed', 1)
    return "<br>".join([f"{user.id}: {user.name}" for user in users])

# Ejecución del servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
