from flask import Flask, render_template, jsonify
import threading
from websocket import WebSocketApp

app = Flask(__name__)

# Variável para armazenar os preços
crypto_prices = {
  "ENAUSDT": 0,
  "AAVEUSDT": 0,
  "PONKEUSDT": 0,
  "BTCUSDT": 0
}

# Função para se conectar ao WebSocket da Bybit e atualizar preços
def on_message(ws, message):
  global crypto_prices
  data = json.loads(message)
  # Extrair o símbolo e preço da mensagem
  symbol = data.get("symbol")
  price = data.get("lastPrice", 0)
  if symbol and price:
    crypto_prices[symbol] = float(price)

def on_error(ws, error):
  print(f"Erro no WebSocket: {error}")

def on_close(ws):
  print("Conexão WebSocket fechada")

def connect_websocket():
  # URL do WebSocket da Bybit para o canal de ticker
  ws_url = "wss://stream.bybit.com/spot/v2/ticker"
  ws = WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)
  # Inscrever-se em símbolos específicos
  symbols = list(crypto_prices.keys())
  for symbol in symbols:
    ws.send(f'{"subscribe": {"symbol": "{symbol}"}}')
  ws.run_forever()

# Inicia a thread para conectar ao WebSocket
websocket_thread = threading.Thread(target=connect_websocket, daemon=True)
websocket_thread.start()

# Rota principal para renderizar a página com o HTML
@app.route("/")
def index():
  return render_template("index.html")

# Rota para retornar os preços em formato JSON
@app.route("/get_prices")
def get_prices():
  return jsonify(crypto_prices)

if __name__ == "__main__":
  app.run(debug=True, port=5001)  # Definindo a porta 5001