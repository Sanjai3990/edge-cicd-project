"""
Edge Computing Node - Sensor Data API
======================================
Simulates an edge device that collects IoT sensor data
(temperature, humidity, CPU load) and exposes it via REST API.
"""

from flask import Flask, jsonify
import random
import time
import datetime

app = Flask(__name__)

# ── Simulated Sensor Readings ─────────────────────────────────────────────────

def read_temperature():
    """Simulate temperature sensor (°C)"""
    return round(random.uniform(20.0, 45.0), 2)

def read_humidity():
    """Simulate humidity sensor (%)"""
    return round(random.uniform(30.0, 90.0), 2)

def read_cpu_load():
    """Simulate edge device CPU load (%)"""
    return round(random.uniform(5.0, 95.0), 2)

# ── API Routes ────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Edge Sensor Node",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint — used by CI/CD pipeline to verify deployment"""
    return jsonify({"status": "healthy"}), 200

@app.route("/sensors", methods=["GET"])
def get_all_sensors():
    """Return all sensor readings from the edge device"""
    return jsonify({
        "device_id": "edge-node-001",
        "location": "Factory Floor A",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "readings": {
            "temperature_c": read_temperature(),
            "humidity_percent": read_humidity(),
            "cpu_load_percent": read_cpu_load()
        }
    })

@app.route("/sensors/temperature", methods=["GET"])
def get_temperature():
    return jsonify({
        "sensor": "temperature",
        "value": read_temperature(),
        "unit": "°C",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })

@app.route("/sensors/humidity", methods=["GET"])
def get_humidity():
    return jsonify({
        "sensor": "humidity",
        "value": read_humidity(),
        "unit": "%",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })

@app.route("/sensors/cpu", methods=["GET"])
def get_cpu():
    return jsonify({
        "sensor": "cpu_load",
        "value": read_cpu_load(),
        "unit": "%",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })

@app.route("/alerts", methods=["GET"])
def get_alerts():
    """Check sensor thresholds and return alerts"""
    temp = read_temperature()
    humidity = read_humidity()
    cpu = read_cpu_load()

    alerts = []
    if temp > 40.0:
        alerts.append({"type": "WARNING", "sensor": "temperature", "message": f"High temp: {temp}°C"})
    if humidity > 80.0:
        alerts.append({"type": "WARNING", "sensor": "humidity", "message": f"High humidity: {humidity}%"})
    if cpu > 85.0:
        alerts.append({"type": "CRITICAL", "sensor": "cpu_load", "message": f"High CPU: {cpu}%"})

    return jsonify({
        "alert_count": len(alerts),
        "alerts": alerts,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })

# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
