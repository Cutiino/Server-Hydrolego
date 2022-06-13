from flask import Flask, render_template                                    #Librería para servidor
from flask_socketio import SocketIO, emit                                   #Librería para WebSocket
import json                                                                 #Librería para JSON
from flask_mqtt import Mqtt                                                 #Librería para conectar a MQTT Flask

async_mode = None

app = Flask(__name__)                                                       #Establece servidor
app.config['MQTT_BROKER_URL'] = 'prawn.rmq.cloudamqp.com'                   # Configura Server MQTT
app.config['MQTT_BROKER_PORT'] = 1883                                       # Configura el puerto MQTT
app.config['MQTT_USERNAME'] = 'sqkvapkq:sqkvapkq'                           # Configura User MQTT
app.config['MQTT_PASSWORD'] = 'IvceJSeyw9xrqdzzJlN-08MWWkyZYrGH'            # Configura Pass MQTT
mqtt = Mqtt(app)                                                            #
app.config['SECRET_KEY'] = 'secret!'                                        #Configura contraseña para socket
socketio = SocketIO(app, async_mode=async_mode)                             #Establece el servidor como socket

@app.route('/')                                                             #Ruta pah inicial
def index():                                                                #Función para cargar html pag inicial
    return render_template('index.html', async_mode=socketio.async_mode)    #Carga el archivo HTML

#@socketio.event
#def SensoresWeb():
#    with open ('D:\WingBox\Pag Web\Flask\WebSocket\datos.json', 'r') as fp: #Abre archivo Json con valor sensores
#        datosJson = json.load(fp)                                           #Traspaso Json a variable
#    emit('SensoresWeb2', datosJson)                                         #Envío a web el Json

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('hydrolego')

@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data)
    #print(data)
    emit('SensoresWeb2', data)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    JsonDatos1 = message.payload.decode()
    JsonDatos2 =  json.loads(JsonDatos1)
    print(JsonDatos2)
    socketio.emit('SensoresWeb2', JsonDatos2)

if __name__ == '__main__':
    #host = 0.0.0.0 correra el servidor en IP de la máquina
    socketio.run(app)                                                        #Corre el servidor
    #socketio.run(app, host='0.0.0.0')                                       #Corre el servidor