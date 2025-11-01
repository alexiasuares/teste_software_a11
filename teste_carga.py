import subprocess
import os
import pandas as pd
import numpy as np
from datetime import datetime, timezone

# === CONFIGURAÇÕES ===
usuarios = 200          # número fixo de usuários simultâneos
duracao = "60s"         # duração do teste
host = "http://127.0.0.1:8000"
saida_pasta = "relatorio/carga"
os.makedirs(saida_pasta, exist_ok=True)

print("🚀 Iniciando teste de carga sustentada...")

# === EXECUÇÃO DO TESTE COM LOCUST ===
saida_arquivo = f"{saida_pasta}/resultado_carga.txt"
comando = [
    "locust", "-f", "locustfile.py", "--headless",
    "-u", str(usuarios), "-r", "10",
    "--run-time", duracao, "--host", host
]

# Salva a saída bruta do Locust (opcional)
with open(saida_arquivo, "w", encoding="utf-8") as f:
    subprocess.run(comando, stdout=f, stderr=f)

print("✅ Teste de carga concluído. Analisando resultados...")

# === ANÁLISE DOS RESULTADOS ===
req = pd.read_csv("requests.csv")

# Corrige timestamps no formato ISO (com +00:00)
req["timestamp"] = req["timestamp"].astype(str).str.replace(r"\+00:00", "", regex=True)

tempo_total = (
    pd.to_datetime(req["timestamp"], format="ISO8601").max() -
    pd.to_datetime(req["timestamp"], format="ISO8601").min()
).total_seconds()

throughput = len(req) / tempo_total if tempo_total > 0 else 0
media = req["response_time_ms"].mean()
p95 = np.percentile(req["response_time_ms"], 95)

# === RELATÓRIO PADRONIZADO ===
data_atual = datetime.now(timezone.utc).isoformat()

relatorio = (
    "=== TESTE DE CARGA ===\n"
    f"Data: {data_atual} UTC\n\n"
    f"Total de requisições: {len(req)}\n"
    f"Usuários simultâneos: {usuarios}\n"
    f"Duração: {duracao}\n"
    f"Throughput médio: {throughput:.2f} req/s\n"
    f"Tempo médio: {media:.2f} ms\n"
    f"P95: {p95:.2f} ms\n\n"
    f"Meta: Throughput > 2000 req/s → "
    f"{'APROVADO' if throughput > 2000 else 'REPROVADO'}\n"
)

# === SALVA O RELATÓRIO ===
with open(f"{saida_pasta}/resumo_carga.txt", "w", encoding="utf-8") as f:
    f.write(relatorio)

print(relatorio)
