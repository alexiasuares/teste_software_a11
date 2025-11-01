import subprocess
import os
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import time

# === CONFIGURAÇÕES ===
usuarios_testes = [500, 1000, 5000, 15000]
host = "http://127.0.0.1:8000"
saida_pasta = "relatorio/estresse"
os.makedirs(saida_pasta, exist_ok=True)

print("💥 Iniciando teste de estresse...")

resultados = []

for u in usuarios_testes:
    print(f"➡️ Testando com {u} usuários...")
    comando = [
        "locust", "-f", "locustfile.py", "--headless",
        "-u", str(u), "-r", "20", "--run-time", "30s",
        "--host", host
    ]
    subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    req = pd.read_csv("requests.csv")
    req["timestamp"] = req["timestamp"].astype(str).str.replace(r"\+00:00", "", regex=True)
    tempo = (
        pd.to_datetime(req["timestamp"], format="ISO8601").max() -
        pd.to_datetime(req["timestamp"], format="ISO8601").min()
    ).total_seconds()

    throughput = len(req) / tempo if tempo > 0 else 0
    p95 = np.percentile(req["response_time_ms"], 95)
    resultados.append((u, throughput, p95))
    time.sleep(2)

print("✅ Teste de estresse finalizado. Gerando relatório...")

# === RELATÓRIO ===
data_atual = datetime.now(timezone.utc).isoformat()
with open(f"{saida_pasta}/resumo_estresse.txt", "w", encoding="utf-8") as f:
    f.write("=== TESTE DE ESTRESSE ===\n")
    f.write(f"Data: {data_atual} UTC\n\n")
    for u, thr, p in resultados:
        f.write(f"Usuários: {u} | Throughput: {thr:.2f} req/s | P95: {p:.2f} ms\n")
    f.write("\nMeta: Ponto de quebra > 15000 usuários → ")
    f.write("APROVADO\n" if resultados[-1][1] > 0 else "REPROVADO\n")

print("📄 Relatório salvo em relatorio/estresse/resumo_estresse.txt")
