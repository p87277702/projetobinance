from flask import Flask, render_template, jsonify
import requests
import threading
import time

app = Flask(__name__)

# Variável para armazenar os preços
crypto_prices = {
    "ENAUSDT": 0,
    "AAVEUSDT": 0,
    "BTCUSDT": 0
}

# Função para buscar preços da Binance
def fetch_prices():
    global crypto_prices
    symbols = list(crypto_prices.keys())  # Corrigir para usar 'symbols'
    while True:
        try: 
            for symbol in symbols:
                url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
                response = requests.get(url)
                data = response.json()
                crypto_prices[symbol] = float(data.get("price", 0))
        except Exception as e:
            print(f"ERROR AO BUSCAR PREÇOS: {e}")
        time.sleep(1)  # Atualiza a cada 1 segundo

# Rota principal para renderizar a página com o HTML
@app.route("/")
def index():
    return render_template("index.html")

# Rota para retornar os preços em formato JSON
@app.route("/get_prices")
def get_prices():
    return jsonify(crypto_prices)

# Inicia a thread para buscar preços
threading.Thread(target=fetch_prices, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Definindo a porta 5001
