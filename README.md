# AI Load Balancer 🚀
An intelligent load balancer using machine learning for dynamic traffic distribution based on system metrics and workload prediction.

---

## ✅ Project Stages Completed

### 1. **Environment Setup**
- Docker & Docker Compose installed
- Project directory structure created
- Shared volumes for metrics logging

### 2. **Services**
- Two Flask microservices (`service1` & `service2`)
  - Expose `/` and `/process` endpoints
  - Gather system metrics via psutil
  - Log to InfluxDB and CSV (`/shared_data/metrics.csv`)

### 3. **Load Balancer**
- NGINX configured for round-robin traffic
- Load testing through Locust
- Grafana dashboards for live monitoring

### 4. **Load Testing & Data Collection**
- Locust scenarios (light, medium, heavy load)
- Headless execution for automation & data collection
- CSV reports from Locust (`results/`)
- InfluxDB time-series data stored (viewable via Grafana)

---

## ⚙️ Docker Compose Services
- **Service1 & Service2** (Flask apps)
- **InfluxDB** (Metrics database)
- **Grafana** (Dashboard visualization)
- **NGINX** (Load balancing)
- **Locust** (Load generation)

---

## 🚀 Load Testing Commands

```powershell
# Light Load
docker-compose run --rm locust `
  -f /mnt/locust/locustfile.py `
  --host http://nginx `
  --headless `
  -u 50 `
  -r 5 `
  --run-time 15m `
  --csv /mnt/locust/results/light_load `
  --loglevel INFO

# Medium Load
docker-compose run --rm locust `
  -f /mnt/locust/locustfile.py `
  --host http://nginx `
  --headless `
  -u 100 `
  -r 10 `
  --run-time 20m `
  --csv /mnt/locust/results/medium_load `
  --loglevel INFO

# Heavy Load
docker-compose run --rm locust `
  -f /mnt/locust/locustfile.py `
  --host http://nginx `
  --headless `
  -u 200 `
  -r 20 `
  --run-time 30m `
  --csv /mnt/locust/results/heavy_load `
  --loglevel INFO



