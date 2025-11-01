import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import os

# === CRIA PASTA DE RELATÓRIO ===
os.makedirs("relatorio", exist_ok=True)

# === LEITURA DOS DADOS ===
req = pd.read_csv("requests.csv")
mon = pd.read_csv("monitor.csv")

# Corrige timestamps no formato ISO com fuso
req["timestamp"] = req["timestamp"].astype(str).str.replace(r"\+00:00", "", regex=True)
mon["timestamp"] = mon["timestamp"].astype(str).str.replace(r"\+00:00", "", regex=True)

# === CÁLCULOS PRINCIPAIS ===
p95 = np.percentile(req["response_time_ms"], 95)
media = req["response_time_ms"].mean()
tempo_total = (
    pd.to_datetime(req["timestamp"], format="ISO8601").max() -
    pd.to_datetime(req["timestamp"], format="ISO8601").min()
).total_seconds()
throughput = len(req) / tempo_total if tempo_total > 0 else 0

# === GRÁFICOS ===
plt.figure()
plt.hist(req["response_time_ms"], bins=50, color='skyblue')
plt.title("Distribuição dos Tempos de Resposta (ms)")
plt.xlabel("Tempo (ms)")
plt.ylabel("Quantidade")
plt.savefig("relatorio/histograma.png")

plt.figure()
plt.plot(pd.to_datetime(mon["timestamp"], format="ISO8601"), mon["cpu_percent"], label="CPU %")
plt.plot(pd.to_datetime(mon["timestamp"], format="ISO8601"), mon["mem_percent"], label="Memória %")
plt.legend()
plt.title("Uso de Recursos")
plt.savefig("relatorio/recursos.png")

# === RELATÓRIO DE DESEMPENHO PADRONIZADO ===
data_atual = datetime.now(timezone.utc).isoformat()
with open("relatorio/relatorio_desempenho.txt", "w", encoding="utf-8") as f:
    f.write("=== TESTE DE DESEMPENHO (AULA 11) ===\n")
    f.write(f"Data: {data_atual} UTC\n\n")
    f.write(f"Total de requisições: {len(req)}\n")
    f.write(f"Throughput médio: {throughput:.2f} req/s\n")
    f.write(f"Tempo médio: {media:.2f} ms\n")
    f.write(f"P95: {p95:.2f} ms\n\n")
    f.write("Meta: P95 < 500 ms → ")
    f.write("APROVADO\n" if p95 < 500 else "REPROVADO\n")

# === AGREGA RESULTADOS ADICIONAIS (SE EXISTIREM) ===
def incluir_secao(f, titulo, caminho):
    if os.path.exists(caminho):
        f.write("\n\n" + titulo + "\n")
        f.write(open(caminho, "r", encoding="utf-8").read().strip() + "\n")

with open("relatorio/relatorio_desempenho.txt", "a", encoding="utf-8") as f:
    f.write("\n\n=== SEÇÕES ADICIONAIS ===")

    incluir_secao(f, "\n=== TESTE DE CARGA ===", "relatorio/carga/resumo_carga.txt")
    incluir_secao(f, "\n=== TESTE DE ESTRESSE ===", "relatorio/estresse/resumo_estresse.txt")
    incluir_secao(f, "\n=== TESTE DE ESCALABILIDADE ===", "relatorio/escalabilidade/resumo_escalabilidade.txt")
    incluir_secao(f, "\n=== TESTE DE SEGURANÇA ===", "relatorio/teste_seguranca.txt")

print("✅ Relatório final gerado em: relatorio/relatorio_desempenho.txt")
