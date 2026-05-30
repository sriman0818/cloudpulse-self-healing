from flask import Flask, jsonify, render_template_string
from datetime import datetime
import socket
import platform
import os

app = Flask(__name__)

START_TIME = datetime.now()


@app.route("/")
def home():
    html_page = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CloudPulse Self-Healing DevOps Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Arial, Helvetica, sans-serif;
                background: #f3f4f6;
                color: #111827;
            }

            .header {
                background: linear-gradient(135deg, #111827, #1f2937);
                color: white;
                padding: 35px 20px;
                text-align: center;
            }

            .header h1 {
                margin: 0;
                font-size: 34px;
            }

            .header p {
                margin-top: 10px;
                font-size: 17px;
                color: #d1d5db;
            }

            .container {
                max-width: 1100px;
                margin: 30px auto;
                padding: 0 20px;
            }

            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 20px;
            }

            .card {
                background: white;
                padding: 22px;
                border-radius: 14px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                border-left: 5px solid #2563eb;
            }

            .card h2 {
                margin-top: 0;
                font-size: 21px;
                color: #1f2937;
            }

            .card p {
                color: #4b5563;
                line-height: 1.5;
            }

            .status {
                display: inline-block;
                padding: 8px 14px;
                border-radius: 20px;
                background: #dcfce7;
                color: #166534;
                font-weight: bold;
            }

            .warning {
                display: inline-block;
                padding: 8px 14px;
                border-radius: 20px;
                background: #fef3c7;
                color: #92400e;
                font-weight: bold;
            }

            .section-title {
                margin-top: 35px;
                margin-bottom: 15px;
                font-size: 25px;
                color: #111827;
            }

            .pipeline {
                background: white;
                padding: 22px;
                border-radius: 14px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }

            .pipeline-step {
                padding: 12px;
                margin: 10px 0;
                background: #eff6ff;
                border-left: 4px solid #2563eb;
                border-radius: 8px;
            }

            .footer {
                text-align: center;
                padding: 20px;
                margin-top: 40px;
                background: #111827;
                color: #d1d5db;
            }

            a {
                color: #2563eb;
                text-decoration: none;
                font-weight: bold;
            }

            .small {
                font-size: 14px;
                color: #6b7280;
            }
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
                    <p>The Flask application container is active and serving traffic on port 8000.</p>
                </div>

                <div class="card">
                    <h2>Containerization</h2>
                    <p><span class="status">Docker Enabled</span></p>
                    <p>The application is packaged and deployed as a Docker container.</p>
                </div>

                <div class="card">
                    <h2>CI/CD Pipeline</h2>
                    <p><span class="status">Jenkins Automated</span></p>
                    <p>Jenkins pulls code from GitHub, builds the Docker image and deploys the container.</p>
                </div>

                <div class="card">
                    <h2>Monitoring</h2>
                    <p><span class="status">Prometheus + Grafana</span></p>
                    <p>Infrastructure metrics are collected using Node Exporter and visualized in Grafana.</p>
                </div>
            </div>

            <h2 class="section-title">Project Architecture</h2>

            <div class="pipeline">
                <div class="pipeline-step">
                    <strong>1. GitHub:</strong> Developer pushes source code to the GitHub repository.
                </div>

                <div class="pipeline-step">
                    <strong>2. Jenkins:</strong> Jenkins detects the code change and starts the CI/CD pipeline.
                </div>

                <div class="pipeline-step">
                    <strong>3. Docker:</strong> Jenkins builds the Docker image and starts the application container.
                </div>

                <div class="pipeline-step">
                    <strong>4. AWS EC2:</strong> The application runs on an Ubuntu EC2 server.
                </div>

                <div class="pipeline-step">
                    <strong>5. Monitoring:</strong> Prometheus scrapes Node Exporter metrics and Grafana displays dashboards.
                </div>

                <div class="pipeline-step">
                    <strong>6. Automation:</strong> Cron jobs and shell scripts are used for log backup and cleanup.
                </div>
            </div>

            <h2 class="section-title">System Information</h2>

            <div class="grid">
                <div class="card">
                    <h2>Hostname</h2>
                    <p>{{ hostname }}</p>
                </div>

                <div class="card">
                    <h2>Platform</h2>
                    <p>{{ platform_name }}</p>
                </div>

                <div class="card">
                    <h2>Started At</h2>
                    <p>{{ start_time }}</p>
                </div>

                <div class="card">
                    <h2>Current Time</h2>
                    <p>{{ current_time }}</p>
                </div>
            </div>

            <h2 class="section-title">API Endpoints</h2>

            <div class="pipeline">
                <div class="pipeline-step">
                    <strong>Health Check:</strong>
                    <a href="/health">/health</a>
                </div>

                <div class="pipeline-step">
                    <strong>Application Status:</strong>
                    <a href="/api/status">/api/status</a>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>DevOps Capstone Project | CloudPulse Self-Healing Engine</p>
        </div>
    </body>
    </html>
    """

    return render_template_string(
        html_page,
        hostname=socket.gethostname(),
        platform_name=platform.platform(),
        start_time=START_TIME.strftime("%Y-%m-%d %H:%M:%S"),
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "CloudPulse application is running successfully",
        "service": "cloudpulse-self-healing-engine",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route("/api/status")
def api_status():
    uptime = datetime.now() - START_TIME

    return jsonify({
        "application": "CloudPulse Self-Healing DevOps Dashboard",
        "status": "running",
        "container": "cloudpulse-engine",
        "host": socket.gethostname(),
        "platform": platform.platform(),
        "start_time": START_TIME.strftime("%Y-%m-%d %H:%M:%S"),
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "uptime_seconds": int(uptime.total_seconds()),
        "message": "Application deployed successfully using Jenkins and Docker"
    })


@app.route("/api")
def api_home():
    return jsonify({
        "message": "CloudPulse API is running",
        "available_endpoints": [
            "/",
            "/health",
            "/api/status"
        ]
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
