from fastapi import FastAPI
from fastapi.responses import Response
from datetime import datetime
from threading import Thread

import docker
import time
import psutil
import socket

from prometheus_client import Counter, generate_latest

# ---------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------

app = FastAPI(
    title="CloudPulse Self-Healing Infrastructure",
    description="Autonomous Infrastructure Recovery Platform",
    version="3.0"
)

# ---------------------------------------------------
# DOCKER CLIENT
# ---------------------------------------------------

docker_client = docker.from_env()

# ---------------------------------------------------
# PROMETHEUS METRICS
# ---------------------------------------------------

recovery_counter = Counter(
    "container_recoveries_total",
    "Total auto-recovered containers"
)

# ---------------------------------------------------
# INCIDENT STORAGE
# ---------------------------------------------------

incident_logs = []

# ---------------------------------------------------
# SELF-HEALING ENGINE
# ---------------------------------------------------

def monitor_containers():

    print("[MONITOR] Self-healing engine started", flush=True)

    while True:

        try:

            containers = docker_client.containers.list(all=True)

            print(f"[SCAN] Found {len(containers)} containers", flush=True)

            for container in containers:

                name = container.name

                if name == "cloudpulse-engine":
                    continue

                try:

                    fresh_container = docker_client.containers.get(container.id)

                    status = fresh_container.attrs["State"]["Status"]

                    print(f"[CHECK] {name} -> {status}", flush=True)

                    if status in ["exited", "dead", "paused"]:

                        print(f"[RECOVERY] Restarting {name}", flush=True)

                        fresh_container.restart()

                        recovery_counter.inc()

                        incident_logs.append({
                            "timestamp": str(datetime.now()),
                            "container": name,
                            "status": status,
                            "action": "auto-restarted"
                        })

                        print(f"[SUCCESS] {name} restarted", flush=True)

                except Exception as e:

                    print(f"[CONTAINER ERROR] {e}", flush=True)

        except Exception as e:

            print(f"[MONITOR ERROR] {e}", flush=True)

        time.sleep(10)

# ---------------------------------------------------
# START BACKGROUND MONITOR
# ---------------------------------------------------

@app.on_event("startup")
def startup_event():

    thread = Thread(
        target=monitor_containers,
        daemon=True
    )

    thread.start()

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

@app.get("/")
def home():

    return {
        "project": "CloudPulse Self-Healing Infrastructure",
        "status": "running",
        "version": "3.0",
        "timestamp": str(datetime.now())
    }

# ---------------------------------------------------
# SYSTEM HEALTH
# ---------------------------------------------------

@app.get("/system-health")
def system_health():

    return {
        "hostname": socket.gethostname(),
        "cpu_usage_percent": psutil.cpu_percent(),
        "memory_usage_percent": psutil.virtual_memory().percent,
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "timestamp": str(datetime.now())
    }

# ---------------------------------------------------
# CONTAINER STATUS
# ---------------------------------------------------

@app.get("/containers")
def containers():

    containers = docker_client.containers.list(all=True)

    container_data = []

    for c in containers:

        try:
            info = docker_client.containers.get(c.id).attrs

            container_data.append({
                "name": c.name,
                "status": info["State"]["Status"],
                "image": c.image.tags,
            })

        except Exception as e:

            container_data.append({
                "name": c.name,
                "error": str(e)
            })

    return {
        "total_containers": len(container_data),
        "containers": container_data
    }

# ---------------------------------------------------
# INCIDENT LOGS
# ---------------------------------------------------

@app.get("/incidents")
def incidents():

    return {
        "total_incidents": len(incident_logs),
        "logs": incident_logs[-20:]
    }

# ---------------------------------------------------
# MANUAL CLEANUP
# ---------------------------------------------------

@app.post("/cleanup")
def cleanup():

    try:

        docker_client.containers.prune()

        return {
            "status": "success",
            "message": "Stopped containers cleaned"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

# ---------------------------------------------------
# MANUAL CONTAINER RESTART
# ---------------------------------------------------

@app.post("/restart/{container_name}")
def restart_container(container_name: str):

    try:

        container = docker_client.containers.get(container_name)

        container.restart()

        recovery_counter.inc()

        log = {
            "timestamp": str(datetime.now()),
            "container": container_name,
            "action": "manual-restart",
            "result": "success"
        }

        incident_logs.append(log)

        return {
            "status": "success",
            "container": container_name,
            "action": "restarted"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

# ---------------------------------------------------
# PROMETHEUS METRICS
# ---------------------------------------------------

@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type="text/plain"
    )
