# 🛒 Sistema de Testes de E-commerce - Black Friday

Sistema completo de testes não funcionais para validar performance, carga e estresse de uma API de e-commerce durante eventos de alta demanda como Black Friday.

## 📋 Requisitos do Sistema

- **👥 Usuários simultâneos:** 10.000 (Black Friday)
- **⚡ Tempo de resposta:** < 500ms para 95% das requisições
- **🔄 Disponibilidade:** 99.9% durante o evento
- **🔒 Segurança:** Proteção contra ataques

## 🎯 Métricas e Metas

| Tipo de Teste | Métrica Obrigatória | Meta Definida |
|---------------|-------------------|---------------|
| **Desempenho** | Tempo de resposta P95 | < 500ms |
| **Carga** | Throughput sustentado | > 2000 req/s |
| **Estresse** | Ponto de quebra | > 15.000 usuários |

## 🚀 Como Executar

### 1️⃣ **Preparação do Ambiente**

```bash
# Clone o repositório e navegue até a pasta
cd /Users/alexiasuares/Desktop/TCC/teste_software_a11

# Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 2️⃣ **Executar os Serviços (3 Terminais)**

#### **Terminal 1 - API (FastAPI)**
```bash
cd /Users/alexiasuares/Desktop/TCC/teste_software_a11
source venv/bin/activate
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```
- ✅ **Status:** Deve exibir "Uvicorn running on http://0.0.0.0:8000"
- 🔄 **Manter rodando durante TODOS os testes**

#### **Terminal 2 - Monitor do Sistema**
```bash
cd /Users/alexiasuares/Desktop/TCC/teste_software_a11
source venv/bin/activate
python3 monitor.py
```
- 📊 **Função:** Monitora CPU, RAM e Disco
- ⏹️ **Controle:** Parar com `Ctrl+C` após cada teste

#### **Terminal 3 - Locust (Gerador de Carga)**
```bash
cd /Users/alexiasuares/Desktop/TCC/teste_software_a11
source venv/bin/activate
locust -f locustfile.py
```
- 🌐 **Interface:** Acesse http://localhost:8089
- 🔄 **Manter rodando para todos os testes**

### 3️⃣ **Executar os Testes**

Acesse **http://localhost:8089** e configure cada teste:

#### **🔥 Teste 1: Desempenho**
- **Number of users:** `100`
- **Spawn rate:** `5`
- **Host:** `http://localhost:8000`
- **Run time:** `5m`

#### **⚡ Teste 2: Carga**
- **Number of users:** `2000`
- **Spawn rate:** `20`
- **Host:** `http://localhost:8000`
- **Run time:** `10m`

#### **💥 Teste 3: Estresse**
- **Number of users:** `15000`
- **Spawn rate:** `100`
- **Host:** `http://localhost:8000`
- **Run time:** `15m`

#### **🎯 Teste 4: Simulação Black Friday**
- **Number of users:** `10000`
- **Spawn rate:** `50`
- **Host:** `http://localhost:8000`
- **Run time:** `30m`

### 4️⃣ **Procedimento para Cada Teste**

1. **🟢 INICIAR** Monitor no Terminal 2
2. **⚙️ CONFIGURAR** teste no Locust (http://localhost:8089)
3. **▶️ INICIAR** clicando "Start swarming"
4. **⏳ AGUARDAR** até o tempo definido
5. **⏹️ PARAR** clicando "Stop" no Locust
6. **🔴 FINALIZAR** Monitor com `Ctrl+C`
7. **📁 RENOMEAR** arquivos gerados:
   ```bash
   mv monitor.csv monitor_[TIPO_TESTE].csv
   mv requests.csv requests_[TIPO_TESTE].csv
   ```

## 📊 Gerando Relatórios

Após executar todos os testes, gere o relatório final:

```bash
python3 gerar_relatorio.py
```

## 📁 Estrutura do Projeto

```
teste_software_a11/
├── api.py              # API FastAPI com endpoints do e-commerce
├── locustfile.py       # Scripts de teste de carga
├── monitor.py          # Monitor de recursos do sistema
├── gerar_relatorio.py  # Gerador de relatórios
├── requirements.txt    # Dependências Python
├── README.md          # Este arquivo
├── venv/              # Ambiente virtual Python
└── dados_gerados/     # CSVs e relatórios dos testes
    ├── monitor_performance.csv
    ├── monitor_load.csv
    ├── monitor_stress.csv
    ├── requests_performance.csv
    ├── requests_load.csv
    └── requests_stress.csv
```

## 🔧 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/produtos` | Lista todos os produtos |
| `GET` | `/api/produtos/{id}` | Detalhes de um produto |
| `POST` | `/api/checkout` | Finalizar compra |
| `POST` | `/api/pedido` | Criar pedido |

## 📈 Interpretação dos Resultados

### **✅ Critérios de Aprovação:**
- **P95 Response Time** < 500ms
- **Throughput** > 2000 req/s
- **Error Rate** < 1%
- **CPU Usage** < 80%
- **Memory Usage** < 90%

### **❌ Critérios de Reprovação:**
- Tempo de resposta P95 > 500ms
- Taxa de erro > 1%
- Sistema não suporta carga alvo
- Recursos do sistema saturados

## 🚨 Troubleshooting

### **Problema: API não inicia**
```bash
# Verificar se a porta 8000 está livre
lsof -i :8000
# Matar processo se necessário
kill -9 [PID]
```

### **Problema: Monitor não funciona**
```bash
# Usar python3 em vez de python
python3 monitor.py
```

### **Problema: Locust não conecta**
- Verificar se API está rodando: http://localhost:8000
- Verificar se Locust está acessível: http://localhost:8089

### **Problema: Falta de dependências**
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar se todos os terminais estão ativos
2. Confirmar que o ambiente virtual está ativado
3. Validar se as portas 8000 e 8089 estão livres
4. Consultar logs de erro nos terminais

---

🎯 **Objetivo:** Validar se o sistema está preparado para suportar 10.000 usuários simultâneos durante a Black Friday com qualidade de serviço adequada.