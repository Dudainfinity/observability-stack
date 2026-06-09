import random
import time

from flask import Flask, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)

app = Flask(__name__)

# Métricas expostas para o Prometheus coletar em /metrics.
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total de requisições HTTP recebidas",
    ["method", "endpoint", "http_status"],
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Latência das requisições HTTP em segundos",
    ["endpoint"],
)


@app.route("/")
def home():
    with REQUEST_LATENCY.labels("/").time():
        # Simula um trabalho com latência variável.
        time.sleep(random.uniform(0.05, 0.4))
        REQUEST_COUNT.labels("GET", "/", 200).inc()
        return "Aplicacao monitorada com Prometheus + Grafana\n"


@app.route("/erro")
def erro():
    # Endpoint que gera erro 500, útil para ver as métricas de falha subindo.
    REQUEST_COUNT.labels("GET", "/erro", 500).inc()
    return Response("Erro simulado\n", status=500)


@app.route("/metrics")
def metrics():
    # Endpoint que o Prometheus coleta (scrape).
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
