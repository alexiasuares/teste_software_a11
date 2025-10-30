import psutil
import csv
import signal
from datetime import datetime

# Variável para controlar o loop
running = True

def signal_handler(sig, frame):
    global running
    print('\nParando monitoramento...')
    running = False

# Registrar o handler para Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Criar arquivo CSV com cabeçalho
print("Iniciando monitoramento do sistema...")
print("Pressione Ctrl+C para parar")

with open("monitor.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "cpu_percent", "mem_percent", "disk_usage_percent"])

try:
    while running:
        ts = datetime.utcnow().isoformat()
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        with open("monitor.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([ts, cpu, mem, disk])
        
        print(f"[{ts}] CPU: {cpu}% | RAM: {mem}% | DISK: {disk}%")
        
        if not running:
            break
            
except KeyboardInterrupt:
    print("\nMonitoramento interrompido pelo usuário")
except Exception as e:
    print(f"Erro durante monitoramento: {e}")
finally:
    print("Monitor finalizado. Dados salvos em monitor.csv")