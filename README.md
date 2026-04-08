# CI/CD Pipeline for Edge Computing
### Course Project — Edge Computing

---

## 📌 Project Overview

This project demonstrates a **complete CI/CD (Continuous Integration / Continuous Deployment) pipeline** for an **edge computing application**.

An **edge device** (like a smart sensor, factory machine, or IoT gateway) runs a small app that collects sensor data. Every time a developer changes the code, the CI/CD pipeline **automatically tests, builds, scans, and deploys** the updated app to the edge device — without manual intervention.

---

## 🧠 Key Concepts (For Beginners)

| Term | What it means |
|------|--------------|
| **CI** (Continuous Integration) | Automatically test code every time it's changed |
| **CD** (Continuous Deployment) | Automatically deploy tested code to the device |
| **Edge Computing** | Processing data close to where it's generated (not in the cloud) |
| **Docker** | A tool to package an app + its dependencies into a portable "container" |
| **GitHub Actions** | A free tool that runs your pipeline automatically on every push |
| **Pipeline** | A series of automated steps: Test → Build → Scan → Deploy |

---

## 🏗️ Project Architecture

```
Developer pushes code
        │
        ▼
┌─────────────────────────────────────────────────────┐
│              GitHub Actions Pipeline                 │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐  │
│  │ Stage 1  │→ │ Stage 2  │→ │ Stage 3  │→ │   Stage 4   │  │
│  │   TEST   │  │  BUILD   │  │   SCAN   │  │   DEPLOY    │  │
│  │          │  │          │  │          │  │             │  │
│  │ Run unit │  │ Build    │  │ Security │  │ Push to     │  │
│  │ tests    │  │ Docker   │  │ scan     │  │ edge device │  │
│  │          │  │ image    │  │ (Trivy)  │  │             │  │
│  └──────────┘  └──────────┘  └──────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────┐
│   Edge Device     │
│  (Simulated)      │
│                   │
│  ┌─────────────┐  │
│  │ Flask App   │  │
│  │ Sensor API  │  │
│  │ Port: 5000  │  │
│  └─────────────┘  │
└───────────────────┘
```

---

## 📁 Project Structure

```
edge-cicd/
├── app.py                          # Main Flask application (edge sensor API)
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container build instructions
├── docker-compose.yml              # Local development setup
├── tests/
│   └── test_app.py                 # Unit tests (run in CI pipeline)
├── .github/
│   └── workflows/
│       └── edge-pipeline.yml       # GitHub Actions CI/CD pipeline
└── README.md                       # This file
```

---

## 🔧 The Application

The **Edge Sensor Node** is a REST API that simulates an IoT edge device reading sensor data.

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info and version |
| `/health` | GET | Health check (used by pipeline) |
| `/sensors` | GET | All sensor readings |
| `/sensors/temperature` | GET | Temperature reading (°C) |
| `/sensors/humidity` | GET | Humidity reading (%) |
| `/sensors/cpu` | GET | CPU load reading (%) |
| `/alerts` | GET | Active threshold alerts |

### Sample Response — `/sensors`
```json
{
  "device_id": "edge-node-001",
  "location": "Factory Floor A",
  "timestamp": "2024-01-15T10:30:00Z",
  "readings": {
    "temperature_c": 32.5,
    "humidity_percent": 65.2,
    "cpu_load_percent": 45.8
  }
}
```

---

## 🚀 CI/CD Pipeline — Step by Step

### Stage 1: TEST ✅
- **Trigger:** Code is pushed to GitHub
- **What happens:** GitHub Actions runs all 15 unit tests using `pytest`
- **Why:** Catch bugs before they reach the edge device
- **If fails:** Pipeline stops — broken code is never deployed

### Stage 2: BUILD 🐳
- **Trigger:** All tests pass
- **What happens:** Docker builds a container image of the app
- **Why:** Package app + dependencies together so it runs the same on any device
- **Output:** A Docker image tagged with the commit hash

### Stage 3: SCAN 🔐
- **Trigger:** Image is built successfully
- **What happens:** Trivy scans the image for known security vulnerabilities
- **Why:** Edge devices are often deployed in insecure environments
- **Output:** Security report of HIGH and CRITICAL vulnerabilities

### Stage 4: DEPLOY 📡
- **Trigger:** Scan completes (only on `main` branch)
- **What happens:** Container is started; health check verifies it's running
- **Why:** Confirm the app is healthy before marking deployment as success
- **Output:** Live edge service at `http://edge-node-001:5000`

---

## 🛠️ How to Run Locally

### Prerequisites
- Python 3.11+
- Docker Desktop
- Git

### Step 1: Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/edge-cicd.git
cd edge-cicd
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the app directly
```bash
python app.py
# App runs at http://localhost:5000
```

### Step 4: Run tests
```bash
pytest tests/ -v
```

### Step 5: Run with Docker
```bash
# Build the image
docker build -t edge-sensor-node .

# Run the container
docker run -p 5000:5000 edge-sensor-node

# Or use docker-compose (easier)
docker-compose up
```

### Step 6: Test the API
```bash
curl http://localhost:5000/health
curl http://localhost:5000/sensors
curl http://localhost:5000/alerts
```

---

## ⚙️ How to Set Up GitHub Actions

1. Create a new GitHub repository
2. Push all project files to the repository
3. GitHub automatically detects `.github/workflows/edge-pipeline.yml`
4. Go to **Actions** tab in your repository to see the pipeline run

The pipeline runs **automatically** every time you push code!

---

## 📊 Test Coverage

The project includes **15 unit tests** covering:
- Home endpoint response and content
- Health check endpoint
- All sensor endpoints (temperature, humidity, CPU)
- Value range validation (e.g., temperature always between 20–45°C)
- Alert detection logic
- 404 error handling for invalid routes

Run coverage report:
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

---

## 🔄 CI/CD Flow Diagram

```
git push origin main
       │
       ▼
GitHub Actions Triggered
       │
       ├─► Stage 1: TEST
       │        pip install → pytest → coverage report
       │        PASS ──────────────────────────────────┐
       │        FAIL → Pipeline STOPS ❌               │
       │                                               ▼
       │                                     Stage 2: BUILD
       │                                       docker build
       │                                       PASS ──────────┐
       │                                       FAIL → STOPS ❌ │
       │                                                       ▼
       │                                            Stage 3: SCAN
       │                                              trivy scan
       │                                              PASS ──────────┐
       │                                              FAIL → STOPS ❌ │
       │                                                              ▼
       │                                                   Stage 4: DEPLOY
       │                                                     docker run
       │                                                     /health → 200 OK
       │                                                     ✅ DEPLOYED!
       │
       └─────────────────────────────────────────────────────────────────
```

---

## 🌐 Real-World Extension

In a real edge deployment, Stage 4 would use **SSH** to push to an actual device:

```yaml
# Real deployment to Raspberry Pi / Edge Server
- name: Deploy to Edge Device
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.EDGE_DEVICE_IP }}
    username: ${{ secrets.EDGE_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      docker pull myregistry/edge-sensor-node:latest
      docker stop edge-node || true
      docker rm edge-node || true
      docker run -d --name edge-node -p 5000:5000 myregistry/edge-sensor-node:latest
```

---

## 👨‍💻 Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python 3.11 | Application language |
| Flask | Lightweight web framework |
| Docker | Containerization |
| GitHub Actions | CI/CD automation |
| Pytest | Unit testing framework |
| Trivy | Container security scanning |

---

## 📚 References

1. GitHub Actions Documentation — https://docs.github.com/en/actions
2. Docker Official Docs — https://docs.docker.com
3. Flask Documentation — https://flask.palletsprojects.com
4. Trivy Security Scanner — https://trivy.dev
5. Edge Computing Concepts — IEEE IoT Journal

---

*Project for Edge Computing Course | CI/CD Pipeline for Edge*
