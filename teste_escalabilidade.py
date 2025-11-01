import subprocess
import os
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import time

# === CONFIGURAÇÕES ===
usuarios_testes = [50, 100, 200, 400]
host = "http://127.0.0.1:8000"
saida_pasta = "relatorio/escalabilidade"
os.makedirs(saida_pasta, exist_ok=True)

print("📈 Iniciando teste de escalabilidade...")

dados = []

for u in usuarios_testes:
    print(f"➡️ Executando com {u} usuários...")
    comando = [
        "locust", "-f", "locustfile.py", "--headless",
        "-u", str(u), "-r", "10", "--run-time", "30s",
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
    dados.append((u, throughput))
    time.sleep(2)

print("✅ Teste de escalabilidade concluído. Gerando relatório...")

# === CÁLCULO DE EFICIÊNCIA ===
base_thr = dados[0][1]
ef_final = (dados[-1][1] / base_thr) / (usuarios_testes[-1] / usuarios_testes[0]) * 100 if base_thr > 0 else 0

# === RELATÓRIO ===
data_atual = datetime.now(timezone.utc).isoformat()
with open(f"{saida_pasta}/resumo_escalabilidade.txt", "w", encoding="utf-8") as f:
    f.write("=== TESTE DE ESCALABILIDADE ===\n")
    f.write(f"Data: {data_atual} UTC\n\n")
    for u, thr in dados:
        f.write(f"Usuários: {u} | Throughput: {thr:.2f} req/s\n")
    f.write(f"\nEficiência horizontal final: {ef_final:.2f}%\n")
    f.write("Meta: Eficiência > 80% → ")
    f.write("APROVADO\n" if ef_final > 80 else "REPROVADO\n")

print("📄 Relatório salvo em relatorio/escalabilidade/resumo_escalabilidade.txt")
