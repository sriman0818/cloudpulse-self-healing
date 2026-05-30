# CloudPulse Self-Healing DevOps Application

## Project Description

CloudPulse Self-Healing is a Python-based web application created for a DevOps Capstone Project. The project demonstrates an end-to-end DevOps pipeline using GitHub, Jenkins, Docker, AWS EC2, Prometheus, Grafana, Shell scripting, and Cron jobs.

The application is containerized using Docker and deployed on an AWS EC2 server. Jenkins automates the build and deployment process whenever code changes are pushed to GitHub. Prometheus and Grafana are used to monitor server metrics, while shell scripts and cron jobs automate log backup and disk usage monitoring.

## Tech Stack

* Git
* GitHub
* Jenkins
* Docker
* AWS EC2 Ubuntu
* Python / FastAPI
* Prometheus
* Grafana
* Node Exporter
* Bash Scripting
* Cron Jobs

## Project Architecture

Developer → GitHub → Jenkins → Docker Build → Docker Container on AWS EC2
                                      |
                                      v
                         Prometheus + Grafana Monitoring
                                      |
                                      v
                         Shell Scripts + Cron Jobs

## Repository Structure

```text
cloudpulse-self-healing/
├── app/
│   └── main.py
├── Dockerfile
├── Jenkinsfile
├── compose.yaml
├── requirements.txt
├── README.md
└── scripts/
    ├── backup_cloudpulse_logs.sh
    ├── disk_alert.sh
    ├── mycronjobs.txt
    └── README.md
```


## CI/CD Flow

1. Developer pushes code to GitHub.
2. Jenkins detects the change using SCM polling or webhook trigger.
3. Jenkins pulls the latest code from GitHub.
4. Jenkins builds the Docker image.
5. Jenkins stops and removes the old container.
6. Jenkins runs the updated container.
7. Application is available on AWS EC2 public IP and port 8000.

## Monitoring

Prometheus is configured to scrape metrics from Node Exporter. Grafana is connected to Prometheus as a data source.

Grafana dashboard panels include:

* Target UP Status
* CPU Usage
* Memory Usage
* Disk Usage
* Network Receive Traffic
* Network Transmit Traffic

## Shell Scripts and Cron Jobs

The `scripts` folder contains automation scripts.

### backup_cloudpulse_logs.sh

Backs up logs from the `cloudpulse-engine` Docker container, compresses them, and deletes backups older than 7 days.

### disk_alert.sh

Checks disk usage and records OK or WARNING status based on an 80% threshold.

### Cron Jobs

```cron
0 2 * * * /home/ubuntu/scripts/backup_cloudpulse_logs.sh
0 * * * * /home/ubuntu/scripts/disk_alert.sh
```

The backup script runs daily at 2 AM.
The disk alert script runs every hour.


## Author

SRIMAN_7781
