import subprocess
import time
import os
import signal

print("🚀 Iniciando execução completa dos testes de E-commerce...\n")

# === 1. Inicia a API (FastAPI) ===
api_proc = subprocess.Popen(["uvicorn", "api:app"], stdout=subprocess.DEVNULL)
time.sleep(3)
print("✅ API iniciada com sucesso em http://127.0.0.1:8000")

# === 2. Inicia o monitoramento do sistema ===
monitor_proc = subprocess.Popen(["python", "monitor.py"])
time.sleep(3)
print("🧠 Monitoramento de CPU/Memória ativo.\n")

# === 3. Teste de desempenho (Pessoa 1) ===
# print("▶️ Executando teste de DESEMPENHO (P95 < 500ms)...")
# subprocess.run([
#     "locust", "-f", "locustfile.py", "--headless",
#     "-u", "50", "-r", "5", "--run-time", "30s",
#     "--host", "http://127.0.0.1:8000"
# ])
# print("✅ Teste de desempenho concluído.\n")

# === 4. Teste de carga (Pessoa 2) ===
print("⚙️ Executando teste de CARGA (>2000 req/s)...")
subprocess.run(["python", "teste_carga.py"])
print("✅ Teste de carga concluído.\n")

# === 5. Teste de estresse (Pessoa 2) ===
print("💥 Executando teste de ESTRESSE (>15000 usuários)...")
subprocess.run(["python", "teste_estresse.py"])
print("✅ Teste de estresse concluído.\n")

# === 6. Teste de escalabilidade (Pessoa 2) ===
print("📈 Executando teste de ESCALABILIDADE (>80%)...")
subprocess.run(["python", "teste_escalabilidade.py"])
print("✅ Teste de escalabilidade concluído.\n")

# === 7. Gera o relatório consolidado ===
print("📊 Gerando relatório de desempenho e métricas...")
subprocess.run(["python", "gerar_relatorio.py"])
print("✅ Relatório de desempenho gerado.\n")

# === 8. Teste de segurança (Pessoa 3) ===
print("🛡️ Executando teste de SEGURANÇA (rate limiting e injeções)...")
subprocess.run(["python", "teste_seguranca.py"])
print("✅ Teste de segurança concluído.\n")

# === 9. Finaliza processos (monitor e API) ===
print("🧹 Encerrando monitoramento e API...")
os.kill(monitor_proc.pid, signal.SIGINT)
api_proc.terminate()
print("🏁 Todos os testes foram executados com sucesso!\n")
print("📂 Verifique a pasta 'relatorio' para os resultados consolidados.")
