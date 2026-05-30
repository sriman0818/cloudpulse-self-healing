from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import socket
import platform

app = FastAPI(title="CloudPulse Self-Healing Engine")

START_TIME = datetime.now()


@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CloudPulse DevOps Dashboard</title>
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f3f4f6;
                color: #111827;
            }}
            .header {{
                background: #111827;
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .container {{
                padding: 30px;
                max-width: 1100px;
                margin: auto;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
                gap: 20px;
            }}
            .card {{
                background: white;
                padding: 22px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                border-left: 5px solid #2563eb;
            }}
            .card h2 {{
                margin-top: 0;
                color: #1f2937;
            }}
            .status {{
                color: #15803d;
                font-weight: bold;
                background: #dcfce7;
                padding: 8px 12px;
                border-radius: 20px;
                display: inline-block;
            }}
            .step {{
                background: white;
                margin: 12px 0;
                padding: 15px;
                border-left: 4px solid #2563eb;
                border-radius: 8px;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                background: #111827;
                color: white;
                margin-top: 40px;
            }}
            a {{
                color: #2563eb;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>CloudPulse Self-Healing DevOps Dashboard</h1>
            <p>End-to-End DevOps Pipeline using GitHub, Jenkins, Docker, AWS EC2, Prometheus and Grafana</p>
        </div>

        <div class="container">
            <div class="grid">
                <div class="card">
                    <h2>Application Status</h2>
                    <p><span class="status">Running Successfully</span></p>
                    <p>The application container is running on port 8000.</p>
                </div>

                <div class="card">
                    <h2>CI/CD Pipeline</h2>
                    <p>GitHub and Jenkins are used to automate build and deployment.</p>
                </div>

                <div class="card">
                    <h2>Docker</h2>
                    <p>The application is containerized using Docker.</p>
                </div>

                <div class="card">
                    <h2>Monitoring</h2>
                    <p>Prometheus and Grafana monitor CPU, memory, disk and network usage.</p>
                </div>
            </div>

            <h2>Architecture Flow</h2>

            <div class="step"><b>1. GitHub:</b> Developer pushes code to repository.</div>
            <div class="step"><b>2. Jenkins:</b> Jenkins detects changes and starts pipeline.</div>
            <div class="step"><b>3. Docker:</b> Docker image is built and container is deployed.</div>
            <div class="step"><b>4. AWS EC2:</b> Application runs on Ubuntu EC2 server.</div>
            <div class="step"><b>5. Monitoring:</b> Prometheus and Grafana monitor the infrastructure.</div>
            <div class="step"><b>6. Automation:</b> Cron jobs and shell scripts handle log backups.</div>

            <h2>System Information</h2>

            <div class="grid">
                <div class="card">
                    <h2>Hostname</h2>
                    <p>{socket.gethostname()}</p>
                </div>

                <div class="card">
                    <h2>Platform</h2>
                    <p>{platform.platform()}</p>
                </div>

                <div class="card">
                    <h2>Started At</h2>
                    <p>{START_TIME.strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>

                <div class="card">
                    <h2>Current Time</h2>
                    <p>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
            </div>

            <h2>API Endpoints</h2>
            <div class="step"><a href="/health">/health</a> - Health check endpoint</div>
            <div class="step"><a href="/api/status">/api/status</a> - Application status endpoint</div>
            <div class="step"><a href="/docs">/docs</a> - FastAPI Swagger documentation</div>
        </div>

        <div class="footer">
            <p>DevOps Capstone Project | CloudPulse Self-Healing Engine</p>
        </div>
    </body>
    </html>
    """


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "CloudPulse application is running successfully",
        "service": "cloudpulse-engine",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/api/status")
def api_status():
    uptime = datetime.now() - START_TIME

    return {
        "application": "CloudPulse Self-Healing Engine",
        "status": "running",
        "container": "cloudpulse-engine",
        "host": socket.gethostname(),
        "platform": platform.platform(),
        "start_time": START_TIME.strftime("%Y-%m-%d %H:%M:%S"),
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "uptime_seconds": int(uptime.total_seconds()),
        "message": "Application deployed successfully using Jenkins and Docker"
    }
