from umqtt.robust import MQTTClient
import network
import time

# Configura la conexión Wi-Fi
SSID = "WIFI_Vinculacion"
PASSWORD = "V1ncul4c10n23"

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        print("Conectando a Wi-Fi...")
        time.sleep(1)
    
    print("Conexión exitosa:", wlan.ifconfig())

# Conectar al Wi-Fi
conectar_wifi()

# Configuración del cliente MQTT
CLIENT_ID = "ESP32_Client"
BROKER = "192.168.32.116"  # Cambia por la IP de tu servidor MQTT
PORT = 1883

# Crear el cliente MQTT
client = MQTTClient(CLIENT_ID, BROKER, port=PORT)

try:
    client.connect()
    print(f"Conectado al broker MQTT en {BROKER}:{PORT}")

    # Publicar un mensaje
    client.publish(b"test/topic", b"Hola desde ESP32!")
    print("Mensaje publicado!")

    # Suscribirse a un tema
    def callback(topic, msg):
        print(f"Recibido en {topic.decode()}: {msg.decode()}")
    
    client.set_callback(callback)
    client.subscribe(b"test/topic")
    print("Suscrito a test/topic")

    while True:
        # Escuchar mensajes
        client.wait_msg()

except Exception as e:
    print(f"Error: {e}")
finally:
    client.disconnect()
    print("Desconectado del broker MQTT")