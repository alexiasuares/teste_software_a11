# Teste de desempenho
from locust import HttpUser, task, between, events
import csv, os
from datetime import datetime, timezone

ARQUIVO = "requests.csv"

if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "endpoint", "status_code", "response_time_ms"])

@events.request.add_listener
def registrar_requisicao(request_type, name, response_time, response_length, response, context, exception, **kwargs):
    ts = datetime.now(timezone.utc).isoformat()
    status = response.status_code if response else 0
    with open(ARQUIVO, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([ts, name, status, response_time])

class ECommerceUser(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def listar_produtos(self):
        self.client.get("/api/produtos", name="/api/produtos")

    @task(3)
    def ver_detalhe(self):
        self.client.get("/api/produtos/1", name="/api/produtos/{id}")

    @task(2)
    def finalizar_compra(self):
        dados = {"produto_id": 1, "quantidade": 1}
        self.client.post("/api/checkout", json=dados, name="/api/checkout")