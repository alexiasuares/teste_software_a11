import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

os.makedirs("relatorio", exist_ok=True)

req = pd.read_csv("requests.csv")
mon = pd.read_csv("monitor.csv")

p95 = np.percentile(req["response_time_ms"], 95)
media = req["response_time_ms"].mean()
throughput = len(req) / (pd.to_datetime(req["timestamp"]).max() - pd.to_datetime(req["timestamp"]).min()).total_seconds()

plt.figure()
plt.hist(req["response_time_ms"], bins=50, color='skyblue')
plt.title("Distribuição dos Tempos de Resposta (ms)")
plt.xlabel("Tempo (ms)")
plt.ylabel("Quantidade")
plt.savefig("relatorio/histograma.png")

plt.figure()
plt.plot(pd.to_datetime(mon["timestamp"]), mon["cpu_percent"], label="CPU %")
plt.plot(pd.to_datetime(mon["timestamp"]), mon["mem_percent"], label="Memória %")
plt.legend()
plt.title("Uso de Recursos")
plt.savefig("relatorio/recursos.png")

with open("relatorio/relatorio_desempenho.txt", "w") as f:
    f.write("=== TESTE DE DESEMPENHO (AULA 11) ===\n")
    f.write(f"Data: {datetime.utcnow().isoformat()} UTC\n\n")
    f.write(f"Total de requisições: {len(req)}\n")
    f.write(f"Throughput médio: {throughput:.2f} req/s\n")
    f.write(f"Tempo médio: {media:.2f} ms\n")
    f.write(f"P95: {p95:.2f} ms\n")
    f.write("\nMeta: P95 < 500 ms → ")
    f.write("APROVADO\n" if p95 < 500 else "REPROVADO\n")