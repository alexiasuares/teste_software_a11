import requests
import os
import time
from datetime import datetime, timezone

# === CONFIGURAÇÕES ===
BASE_URL = "http://127.0.0.1:8000"
saida = "relatorio/teste_seguranca.txt"
os.makedirs("relatorio", exist_ok=True)

print("🛡️ Iniciando teste de segurança...")

data_atual = datetime.now(timezone.utc).isoformat()
with open(saida, "w", encoding="utf-8") as f:
    f.write("=== TESTE DE SEGURANÇA ===\n")
    f.write(f"Data: {data_atual} UTC\n\n")

# === TESTES ===

# 1. Injeção de SQL
payloads = ["1 OR 1=1", "'; DROP TABLE produtos; --", "abc' OR 'x'='x"]
for p in payloads:
    r = requests.get(f"{BASE_URL}/api/produtos/{p}")
    with open(saida, "a", encoding="utf-8") as f:
        f.write(f"SQLi payload '{p}' → Status {r.status_code}\n")

# 2. Campos ausentes
r = requests.post(f"{BASE_URL}/api/checkout", json={"produto_id": 1})
with open(saida, "a", encoding="utf-8") as f:
    f.write(f"Checkout com campo faltando → Status {r.status_code}\n")

# 3. Endpoint inválido
r = requests.get(f"{BASE_URL}/api/nada")
with open(saida, "a", encoding="utf-8") as f:
    f.write(f"Endpoint inexistente → Status {r.status_code}\n")

# 4. Rate limiting (simples)
sucessos, falhas = 0, 0
for i in range(120):
    r = requests.get(f"{BASE_URL}/api/produtos/1")
    if r.status_code == 200:
        sucessos += 1
    else:
        falhas += 1
    time.sleep(0.5)

# === RELATÓRIO FINAL ===
with open(saida, "a", encoding="utf-8") as f:
    f.write(f"\nRequisições bem-sucedidas: {sucessos}\n")
    f.write(f"Requisições bloqueadas: {falhas}\n\n")
    f.write("Meta: Bloquear após 100 req/min/IP → ")
    f.write("APROVADO\n" if falhas > 0 else "REPROVADO\n")

print("✅ Teste de segurança concluído. Relatório salvo em relatorio/teste_seguranca.txt")
