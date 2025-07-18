# RAG Commercial Analytics System

Sistema RAG (Retrieval-Augmented Generation) completamente locale per l'analisi intelligente dei dati di performance commerciali con workflow n8n agentici.

## 🚀 Panoramica

Questo sistema combina:
- **RAG Architecture**: Retrieval-Augmented Generation per query intelligenti
- **n8n Workflows**: Automazione agentica per task complessi
- **Local Infrastructure**: Ubuntu Server con Docker per massima privacy
- **AI-Powered Analytics**: Insights avanzati sui dati commerciali

## 📋 Prerequisiti

- Ubuntu Server LTS 22.04+
- Docker & Docker Compose
- 64GB+ RAM (128GB consigliati)
- 2TB+ SSD NVMe
- GPU NVIDIA (opzionale per accelerazione)

## 🏗️ Struttura del Progetto

```
rag-a-muffin/
├── api_gateway/                 # API Gateway FastAPI
│   ├── src/
│   │   ├── main.py
│   │   ├── models.py
│   │   └── services/
│   ├── tests/
│   ├── config/
│   ├── Dockerfile
│   └── requirements.txt
├── n8n_workflows/              # Workflow n8n Agentici
│   ├── agents/                 # Single-Agent specializzati
│   │   ├── commercial_data_ingestion_agent.json
│   │   ├── rag_query_agent.json
│   │   ├── report_generation_agent.json
│   │   └── alert_management_agent.json
│   ├── patterns/               # Pattern orchestrazione
│   │   └── manager_agent_pattern.json
│   └── guardrails/             # Sicurezza e validazione
│       ├── security_guardrails.json
│       └── business_logic_guardrails.json
├── database/                   # Database schemas e scripts
│   ├── schemas/
│   │   ├── commercial_data.sql
│   │   └── n8n_schema.sql
│   ├── migrations/
│   └── scripts/
│       └── init_db.py
├── monitoring/                 # Monitoring & Observability
│   ├── prometheus/
│   │   └── prometheus.yml
│   └── grafana/
│       └── dashboards/
│           └── commercial_analytics_dashboard.json
├── docker/                     # Docker configuration
│   └── docker-compose.yml
├── .env.example
└── README.md
```

## 🔧 Setup e Installazione

### 1. Clonare il Repository

```bash
git clone https://github.com/Codencore/rag-a-muffin.git
cd rag-a-muffin
```

### 2. Configurare Environment Variables

```bash
cp .env.example .env
# Editare .env con i propri valori
```

### 3. Avviare i Servizi

```bash
cd docker
docker-compose up -d
```

### 4. Inizializzare Database

```bash
cd database/scripts
python init_db.py
```

## 🔍 Componenti Principali

### API Gateway
- FastAPI con endpoints per query RAG
- Servizi per embedding e recupero documenti
- Guardrails di sicurezza integrati

### n8n Workflows Agentici
- **Data Ingestion Agent**: Acquisizione dati commerciali
- **RAG Query Agent**: Interrogazione intelligente knowledge base
- **Report Generation Agent**: Creazione report automatici
- **Alert Management Agent**: Gestione notifiche e escalation

### Database
- PostgreSQL per metadati e analytics
- ChromaDB per vector storage
- Redis per caching

### Monitoring
- Prometheus per metriche
- Grafana per dashboard
- Alert manager per notifiche

## 🛡️ Sicurezza

### Guardrails Implementati
- **PII Filter**: Rimozione dati sensibili
- **Input Validation**: Sanitizzazione query
- **Output Safety**: Controllo risposte AI
- **Access Control**: Validazione permessi

### Security Best Practices
- Encryption at rest e in transit
- Network segmentation
- VPN access per amministrazione
- Key management con HashiCorp Vault

## 📊 Utilizzo

### Query RAG
```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Quali sono le performance di vendita del mese scorso?",
    "max_results": 10
  }'
```

### Ingest Documenti
```bash
curl -X POST http://localhost:8080/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "id": "doc1",
        "content": "Dati di vendita...",
        "source": "sales_report",
        "type": "report"
      }
    ]
  }'
```

## 📈 Monitoring

### Metriche Principali
- Query response time < 3 secondi
- System uptime 99.9%
- Data freshness < 1 ora
- RAG accuracy >85%

### Dashboard Grafana
Accesso: http://localhost:3000
- Performance metriche
- System health
- Workflow executions
- Business KPIs

## 🚨 Troubleshooting

### Problemi Comuni

1. **ChromaDB Connection Error**
   ```bash
   docker-compose restart chromadb
   ```

2. **High Memory Usage**
   ```bash
   # Aumentare memoria Docker
   docker-compose down
   # Editare docker-compose.yml
   docker-compose up -d
   ```

3. **n8n Workflow Failures**
   - Verificare API keys in .env
   - Controllare connessioni database
   - Verificare guardrails configuration

## 🔄 Development

### Aggiungere Nuovi Workflow
1. Creare file JSON in `n8n_workflows/agents/`
2. Implementare guardrails necessari
3. Aggiornare manager pattern
4. Testare con dati mock

### Estendere API Gateway
1. Aggiungere endpoint in `api_gateway/src/main.py`
2. Definire modelli in `models.py`
3. Implementare servizi in `services/`
4. Scrivere test

## 📚 Documentazione

- [Architecture Decision Records](./docs/architecture/)
- [API Documentation](./docs/api/)
- [Workflow Guide](./docs/workflows/)
- [Security Guide](./docs/security/)

## 🤝 Contribuire

1. Fork del repository
2. Creare feature branch
3. Commit delle modifiche
4. Push al branch
5. Creare Pull Request

## 📄 License

Questo progetto è rilasciato sotto licenza MIT. Vedere `LICENSE` per dettagli.

## 👥 Team

- **AI Guy**: Project Lead & Technical Architecture
- **PM Umano**: Project Management & Coordination
- **Agenti AI**: Development & Implementation

## 🆘 Support

Per supporto e segnalazioni:
- GitHub Issues
- Email: support@company.com
- Slack: #rag-analytics

---

**Note**: Questo sistema è progettato per uso interno aziendale con dati proprietari. Assicurarsi di seguire le policy di sicurezza aziendali.