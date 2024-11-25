from flask import Flask, request, jsonify
import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Маршрут 1: Отправка HTTP-запроса
@app.route('/sendhttp', methods=['POST'])
def send_http():
    """Обрабатывает HTTP-запрос пользователя и отправляет его указанной цели."""
    data = request.json
    header = {data.get("Header"): data.get("Header-value")}
    target = data.get("Target")
    method = data.get("Method", "GET").upper()

    try:
        # Отправляем HTTP-запрос
        response = requests.request(method, target, headers=header)
        return jsonify({
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text
        })
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Маршрут 2: Сканирование сети
@app.route('/scan', methods=['GET'])
def scan_network():
    """Сканирует указанный диапазон IP-адресов."""
    data = request.json
    network_prefix = data.get("target", "192.168.1.0").rsplit(".", 1)[0]
    count = int(data.get("count", 20))

    def ping_host(ip):
        """Пингует IP-адрес и возвращает его, если доступен."""
        param = "-n" if subprocess.os.name == "nt" else "-c"
        command = ["ping", param, "1", ip]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return ip if result.returncode == 0 else None

    active_hosts = []
    with ThreadPoolExecutor() as executor:
        ips = [f"{network_prefix}.{i}" for i in range(1, count + 1)]
        results = executor.map(ping_host, ips)
        active_hosts = [ip for ip in results if ip]

    return jsonify({"active_hosts": active_hosts})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
