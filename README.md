# RAG Commercial Analytics System

RAG system for private companies

Sistema RAG (Retrieval-Augmented Generation) completamente locale per l'analisi intelligente dei dati di performance commerciali con workflow n8n agentici.

## 🚀 Panoramica

Questo sistema combina:
- **RAG Architecture**: Retrieval-Augmented Generation per query intelligenti
- **Workflow n8n**: Automazione e orchestrazione dei processi
- **Architettura Agent-based**: Agenti specializzati per diverse funzioni
- **Sicurezza locale**: Tutti i dati rimangono on-premise
- **Monitoring avanzato**: Grafana + Prometheus per osservabilità
- **Embedding semantici**: ChromaDB per ricerche vettoriali
- **API Gateway**: FastAPI per gestione sicura delle richieste

## 📋 Componenti del Sistema

### 1. API Gateway (FastAPI)
- **Endpoint RESTful** per interazione con il sistema
- **Autenticazione e autorizzazione** con JWT
- **Rate limiting** e throttling
- **Validazione input** e sanitizzazione
- **Routing intelligente** verso i servizi appropriati

### 2. Servizi Core
- **RAG Service**: Gestione query e retrieval
- **Embedding Service**: Generazione embeddings con modelli locali
- **Guardrails Service**: Validazione e sicurezza delle query

### 3. Database Layer
- **PostgreSQL**: Dati strutturati e metadati
- **ChromaDB**: Vector store per embeddings
- **Redis**: Caching e sessioni

### 4. Workflow n8n
- **Agenti specializzati** per diverse funzioni
- **Orchestrazione** di processi complessi
- **Integrazione** con sistemi esistenti
- **Monitoring** e alerting automatico

### 5. Monitoring e Observability
- **Grafana**: Dashboard e visualizzazioni
- **Prometheus**: Metriche e alerting
- **Logging strutturato** per debugging

## 🏗️ Architettura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   RAG Service   │
│   (Web/Mobile)  │───▶│   (FastAPI)     │───▶│   (Core Logic)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   n8n Workflow  │    │   Embedding     │
                       │   (Orchestrator)│    │   Service       │
                       └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   PostgreSQL    │    │   ChromaDB      │
                       │   (Metadata)    │    │   (Vectors)     │
                       └─────────────────┘    └─────────────────┘
```

## 🚀 Setup e Installazione

### Prerequisiti
- Docker e Docker Compose
- Python 3.11+
- Git

### Installazione Rapida

1. **Clona il repository**:
```bash
git clone https://github.com/Codencore/rag-a-muffin.git
cd rag-a-muffin
```

2. **Configura le variabili d'ambiente**:
```bash
cp .env.example .env
# Edita .env con i tuoi parametri
```

3. **Avvia i servizi**:
```bash
docker-compose up -d
```

4. **Inizializza il database**:
```bash
python database/scripts/init_db.py
```

## 🔧 Configurazione

### Variabili d'Ambiente (.env)
```env
# Database
POSTGRES_DB=rag_commercial
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=secure_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# ChromaDB
CHROMA_HOST=localhost
CHROMA_PORT=8000

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# API Gateway
API_HOST=0.0.0.0
API_PORT=8080
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256

# n8n
N8N_HOST=localhost
N8N_PORT=5678

# Monitoring
GRAFANA_HOST=localhost
GRAFANA_PORT=3000
PROMETHEUS_HOST=localhost
PROMETHEUS_PORT=9090
```

## 📊 Utilizzo

### 1. Query RAG
```bash
curl -X POST "http://localhost:8080/api/v1/rag/query" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "Mostra le performance commerciali Q1 2024",
    "context": "sales_data",
    "max_results": 10
  }'
```

### 2. Caricamento Dati
```bash
curl -X POST "http://localhost:8080/api/v1/data/ingest" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "source": "sales_report_q1_2024.csv",
    "type": "commercial_data",
    "metadata": {
      "period": "Q1_2024",
      "department": "sales"
    }
  }'
```

### 3. Monitoring
- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **n8n**: http://localhost:5678

## 🔄 Workflow n8n

### Agenti Disponibili

1. **Commercial Data Ingestion Agent**
   - Automatizza l'ingestion di dati commerciali
   - Validazione e pulizia automatica
   - Generazione embeddings

2. **RAG Query Agent**
   - Gestisce query complesse
   - Orchestrazione retrieval + generation
   - Ottimizzazione performance

3. **Report Generation Agent**
   - Genera report automatici
   - Schedulazione personalizzabile
   - Multi-formato output

4. **Alert Management Agent**
   - Monitoring anomalie
   - Alerting intelligente
   - Escalation automatica

### Patterns Implementati

- **Manager Agent Pattern**: Coordinamento tra agenti
- **Security Guardrails**: Validazione e controllo accessi
- **Business Logic Guardrails**: Controlli di coerenza business

## 🔒 Sicurezza

### Implementazioni di Sicurezza

1. **Autenticazione Multi-livello**
   - JWT tokens con refresh
   - Role-based access control (RBAC)
   - API key management

2. **Validazione Input**
   - Sanitizzazione automatica
   - Schema validation
   - Injection prevention

3. **Guardrails Avanzati**
   - Query safety checks
   - Content filtering
   - Business logic validation

4. **Audit e Logging**
   - Tracciamento completo delle operazioni
   - Log strutturati per analisi
   - Retention policies

## 📈 Monitoring e Metriche

### Dashboard Grafana

1. **Performance Dashboard**
   - Latenza query RAG
   - Throughput API
   - Utilizzo risorse

2. **Business Dashboard**
   - Metriche commerciali
   - KPI automatici
   - Trend analysis

3. **System Health Dashboard**
   - Stato servizi
   - Errori e anomalie
   - Capacity planning

### Metriche Prometheus

- `rag_query_duration_seconds`
- `api_requests_total`
- `embedding_generation_duration_seconds`
- `database_connection_pool_size`

## 🧪 Testing

### Esecuzione Test

```bash
# Test unitari
pytest api_gateway/tests/

# Test integrazione
pytest tests/integration/

# Test performance
pytest tests/performance/
```

### Coverage

```bash
pytest --cov=api_gateway --cov-report=html
```

## 🚀 Deployment

### Staging Environment

```bash
# Build immagini
docker-compose -f docker-compose.staging.yml build

# Deploy
docker-compose -f docker-compose.staging.yml up -d
```

### Production Environment

```bash
# Usa orchestrator (Kubernetes/Docker Swarm)
kubectl apply -f k8s/
```

## 📚 Documentazione Tecnica

### API Documentation
- **OpenAPI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

### Architettura Interna
- [Database Schema](docs/database_schema.md)
- [API Endpoints](docs/api_endpoints.md)
- [n8n Workflows](docs/n8n_workflows.md)

## 🔧 Troubleshooting

### Problemi Comuni

1. **Connessione Database**
   ```bash
   # Verifica connessione
   docker-compose logs postgres
   ```

2. **ChromaDB Issues**
   ```bash
   # Reset ChromaDB
   docker-compose down chromadb
   docker volume rm rag_chromadb_data
   ```

3. **Performance Issues**
   ```bash
   # Monitoring risorse
   docker stats
   ```

## 🤝 Contributi

### Workflow di Sviluppo

1. Fork del repository
2. Crea feature branch
3. Implementa modifiche
4. Esegui test
5. Crea pull request

### Coding Standards

- **Python**: Black + isort + flake8
- **SQL**: sqlfluff
- **Commit**: Conventional commits

## 📄 License

Copyright (c) 2024 Your Company. All rights reserved.

Per supporto e segnalazioni:
- GitHub Issues
- Email: support@company.com
- Slack: #rag-analytics

---

**Note**: Questo sistema è progettato per uso interno aziendale con dati proprietari. Assicurarsi di seguire le policy di sicurezza aziendali.