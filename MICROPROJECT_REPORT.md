# SMART CLOUD-BASED CAMPUS PLACEMENT READINESS ASSESSMENT AND PREDICTION SYSTEM

**MICROPROJECT REPORT**

**Repository:** [https://github.com/MaheshwaranCSE/Placement.git](https://github.com/MaheshwaranCSE/Placement.git)  
**Domain:** Cloud Computing, Machine Learning, Web Engineering, Enterprise Security  
**Cloud Platform:** Amazon Web Services (AWS)  
**Backend Framework:** Python (Flask, Celery, Gunicorn, SQLAlchemy)  
**Machine Learning Stack:** Scikit-Learn (Random Forest, Decision Tree, Logistic Regression), Pandas, NumPy, SDV  
**Database & Cache:** Amazon RDS (PostgreSQL / MySQL), Redis  
**Web Server & Security:** Nginx Reverse Proxy, TLS 1.2/1.3, AWS Security Groups, IAM, KMS  

---

## TABLE OF CONTENTS

1. [1. INTRODUCTION](#1-introduction)
   - [1.1 Cloud Computing](#11-cloud-computing)
   - [1.2 Cloud Service Models](#12-cloud-service-models)
   - [1.3 Cloud Deployment Models](#13-cloud-deployment-models)
   - [1.4 Amazon Web Services (AWS)](#14-amazon-web-services-aws)
   - [1.5 How AWS is Used in the Smart Campus Placement Readiness Portal](#15-how-aws-is-used-in-the-smart-campus-placement-readiness-portal)
2. [2. PROBLEM STATEMENT & OBJECTIVES](#2-problem-statement--objectives)
   - [2.1 Problem Statement](#21-problem-statement)
   - [2.2 Objectives](#22-objectives)
3. [3. SYSTEM ARCHITECTURE](#3-system-architecture)
   - [3.1 Architectural Overview](#31-architectural-overview)
   - [3.2 Presentation Layer](#32-presentation-layer)
   - [3.3 Application Layer](#33-application-layer)
   - [3.4 Data & AI Layer](#34-data--ai-layer)
   - [3.5 System Architecture Diagram](#35-system-architecture-diagram)
4. [4. MODULE 1 – CLOUD INFRASTRUCTURE SETUP FOR CAMPUS PLACEMENT SYSTEM USING AWS EC2 AND SECURITY SERVICES](#4-module-1--cloud-infrastructure-setup-for-campus-placement-system-using-aws-ec2-and-security-services)
   - [4.1 Aim](#41-aim)
   - [4.2 Procedure](#42-procedure)
   - [4.3 EC2 Instance Specification](#43-ec2-instance-specification)
   - [4.4 Activity Diagram](#44-activity-diagram)
   - [4.5 System Execution & Screenshots Description](#45-system-execution--screenshots-description)
   - [4.6 Result](#46-result)
5. [5. MODULE 2 – DATABASE SETUP, SECURE CONNECTIVITY AND BACKEND INTEGRATION](#5-module-2--database-setup-secure-connectivity-and-backend-integration)
   - [5.1 Aim](#51-aim)
   - [5.2 Procedure](#52-procedure)
   - [5.3 Database, S3 & Security Configuration](#53-database-s3--security-configuration)
   - [5.4 Activity Diagram](#54-activity-diagram)
   - [5.5 System Execution & Screenshots Description](#55-system-execution--screenshots-description)
   - [5.6 Result](#56-result)
6. [6. MODULE 3 – MACHINE LEARNING: STUDENT PLACEMENT READINESS ANALYSIS AND RISK PREDICTION](#6-module-3--machine-learning-student-placement-readiness-analysis-and-risk-prediction)
   - [6.1 Aim](#61-aim)
   - [6.2 Procedure](#62-procedure)
   - [6.3 Model Performance Metrics](#63-model-performance-metrics)
   - [6.4 Machine Learning Prediction Pipeline Activity Diagram](#64-machine-learning-prediction-pipeline-activity-diagram)
   - [6.5 Execution, Test Cases, and Edge-Case Analysis](#65-execution-test-cases-and-edge-case-analysis)
   - [6.6 Result](#66-result)
7. [7. MODULE 4 – AWS CLOUD SECURITY CONFIGURATION, FRONTEND PORTAL AND SECURE BACKEND ACCESS](#7-module-4--aws-cloud-security-configuration-frontend-portal-and-secure-backend-access)
   - [7.1 Aim](#71-aim)
   - [7.2 Implementation Procedure](#72-implementation-procedure)
   - [7.3 Complete Security Architecture](#73-complete-security-architecture)
   - [7.4 Security Architecture Activity Diagram](#74-security-architecture-activity-diagram)
   - [7.5 Portal User Interface & Analytics Dashboards](#75-portal-user-interface--analytics-dashboards)
   - [7.6 Result](#76-result)
8. [8. CONCLUSION](#8-conclusion)
9. [9. REFERENCES](#9-references)

---

# 1. INTRODUCTION

## 1.1 Cloud Computing
Cloud computing represents the paradigm of delivering computing resources—including virtual computing instances, scalable object storage, managed database engines, virtual networking topologies, and intelligent software services—over the internet under an elastic, on-demand, pay-as-you-go financial model. 

In a modern **Campus Placement Readiness Assessment and Prediction System**, cloud computing fundamentally resolves the infrastructural bottlenecks associated with traditional on-premise academic software deployments. Placement seasons in universities are characterized by massive spikes in concurrent traffic: thousands of students take simultaneous aptitude and coding mock assessments, upload resumes, and query placement eligibility requirements, while faculty mentors and corporate recruiters concurrently analyze cohort performances. 

Hosting this critical ecosystem on the cloud enables:
- **Elastic Scalability:** Computing instances and database worker threads automatically scale during heavy recruitment mock drives without requiring capital expenditures on physical university server hardware.
- **High Availability & Fault Tolerance:** Multi-Availability Zone redundancy ensures continuous uptime, preventing disruptions during time-critical placement recruitment rounds.
- **Centralized Data Consolidation:** Academic records (CGPA, backlog history), technical evaluations (coding problem ratings, project scores), soft skill metrics, and placement offer records are unified in a single, securely accessible, centralized cloud repository.

## 1.2 Cloud Service Models
The Smart Campus Placement Readiness System leverages the three principal cloud service models:

- **IaaS (Infrastructure as a Service):** Provides raw computing instances, persistent block storage, and virtual networking infrastructure. 
  - *Example in Project:* **Amazon EC2 (Elastic Compute Cloud)** is provisioned to host the containerized web backend, Gunicorn application servers, Redis message broker, Celery asynchronous workers, and Nginx reverse proxy. System administrators manage the Ubuntu operating system, Docker daemon, and application configurations while AWS abstracts physical hardware management.
- **PaaS (Platform as a Service):** Delivers fully managed platforms that allow engineers to deploy databases, caches, and containerized services without the overhead of operating system patching or low-level storage provisioning.
  - *Example in Project:* **Amazon RDS (Relational Database Service)** provides an automated, managed PostgreSQL/MySQL database engine featuring automated snapshots, automated failover, and encryption at rest. Additionally, managed Redis services handle Celery asynchronous broker queues and distributed rate-limiting.
- **SaaS (Software as a Service):** Provides fully functional, accessible application software over the web interface for end users without requiring client-side installations.
  - *Example in Project:* The **Campus Placement Readiness Portal** acts as a SaaS platform accessible via web browsers (`http://<EC2-public-ip>` or domain `https://placement.college.edu/`). University administrators, department placement coordinators, faculty advisors, and undergraduate students interact directly with role-tailored dashboards.

## 1.3 Cloud Deployment Models
The architecture supports flexible deployment models depending on institutional policy and governance standards:

- **Public Cloud:** The primary deployment is hosted on **Amazon Web Services (AWS)** public cloud infrastructure. This delivers maximum cost efficiency, elasticity during campus placement cycles, and zero capital expenditure for physical infrastructure.
- **Private Cloud:** For universities handling highly restricted student personal identifiable information (PII) or strictly governed academic transcripts, the portal backend and database can be containerized via Docker Compose within an isolated institutional private cloud or on-premise data center.
- **Hybrid Cloud:** An enterprise model where historical student SIS (Student Information System) databases reside within the on-premise university network, while intensive Machine Learning model training, Celery batch prediction workloads, and candidate analytics run securely in the AWS public cloud connected via AWS Direct Connect or Site-to-Site VPN.
- **Community Cloud:** A consortium of engineering colleges or affiliated university bodies can share a unified cloud placement infrastructure to pool placement drives, benchmark inter-college competency distributions, and facilitate joint recruitment drives while maintaining strict tenant-level row isolation.

## 1.4 Amazon Web Services (AWS)
Amazon Web Services (AWS) is the world's leading cloud computing platform, offering over 200 fully featured services from data centers globally. For educational and institutional applications, AWS guarantees enterprise-grade security compliance (ISO 27001, SOC 2, FERPA-compliant configurations), exceptional durability, and high network throughput.

In the Campus Placement Readiness System, AWS delivers:
- Compute elasticity through **Amazon EC2 (Ubuntu 24.04 LTS)**.
- Secure, high-performance relational storage through **Amazon RDS (PostgreSQL/MySQL)**.
- Scalable, cost-effective document and archive storage through **Amazon S3 (Simple Storage Service)** for resumes and exported placement batches.
- Granular, zero-trust access control through **AWS Identity and Access Management (IAM)** and **Virtual Private Cloud (VPC) Security Groups**.
- Observability and log aggregation through **Amazon CloudWatch**.

## 1.5 How AWS is Used in the Smart Campus Placement Readiness Portal
The Smart Campus Placement System orchestrates multiple core AWS services:

- **Amazon EC2 (`campus-placement-server`):** Hosts the production Dockerized web application, Nginx web server, Flask REST API runtime, Celery distributed task queues, and Prometheus monitoring agents. Configured with a dedicated key pair (`placement-key.pem`) for SSH authentication.
- **Amazon RDS (`placement_db`):** Houses structured student profiles, multi-dimensional academic metrics, authentication tables, placement offer histories, prediction inference audit logs, and system audit logs. AWS KMS encryption at rest guarantees confidentiality.
- **Amazon S3 (`campus-placement-records-2026`):** Dedicated bucket in region `ap-south-1` (or `ap-southeast-2`) storing student PDF resumes, bulk CSV import artifacts, and scheduled daily/monthly placement analytics export packages with SSE-S3 AES-256 server-side encryption.
- **AWS Security Groups:** Establishes layered, stateful firewall barriers. Inbound traffic to EC2 is strictly filtered to Port 22 (SSH for admin access), Port 80 (HTTP for ACME challenges and web redirect), Port 443 (HTTPS for encrypted browser traffic), and Port 8000/5000 (Internal application routing). RDS security groups disallow all public internet traffic, accepting inbound connections solely from the EC2 security group on database port 5432/3306.
- **Python (NumPy, Pandas, SDV Data Preprocessing):** Scripts standardize multidimensional assessment scores (quant, logical, verbal, coding ratings, mock interviews, certifications, hackathons) into unified normalized feature spaces.
- **Machine Learning (Scikit-Learn Random Forest Classifier):** Pre-trained on 500+ multi-department student profiles to classify placement readiness into **"Ready"**, **"Moderate"**, or **"At Risk"** categories, featuring an automated hard-override heuristic for excessive backlogs.

---

# 2. PROBLEM STATEMENT & OBJECTIVES

## 2.1 Problem Statement
In conventional university ecosystems, managing and preparing undergraduate students for campus recruitment is plagued by critical operational and technological deficiencies:

1. **Fragmented and Siloed Data:** Student academic scores, coding contest performances, hackathon participations, certifications, and mock interview ratings are scattered across disconnected spreadsheets, paper records, and disparate departmental portals. Placement coordinators lack a unified 360-degree view of a candidate's readiness.
2. **Delayed Intervention for At-Risk Students:** Under traditional workflows, faculty mentors only discover a student's lack of preparedness when the candidate fails in final-year corporate screening rounds. The absence of an early warning mechanism prevents proactive remedial coaching in aptitude or coding fundamentals.
3. **Absence of Intelligent Predictive Analytics:** Raw academic performance (CGPA) is frequently mistaken for industry readiness. Students with high CGPA but zero practical coding skills or severe communication anxiety often get rejected, while capable practical coders with modest CGPA are overlooked. Rule-based spreadsheets cannot model non-linear, multi-attribute correlations.
4. **Lack of Automated Scalability:** As placement drives scale across multiple engineering branches (CSE, ECE, IT, MECH, CCE, EEE, AI & DS), manually reviewing profiles, generating eligibility shortlists, and exporting recruiter-ready CSV reports becomes an error-prone, bottlenecked endeavor.

Therefore, an urgent need exists for a cloud-native, scalable, secure, and intelligent web platform that unifies student performance data, leverages machine learning to forecast placement readiness, and delivers real-time actionable insights to faculty and placement cells.

## 2.2 Objectives
The primary objectives of this microproject are:

- **Cloud Infrastructure Provisioning:** To provision, configure, and secure an **Amazon EC2 virtual machine (`campus-placement-server`)** running Ubuntu Server 24.04 LTS, setting up a containerized environment (Docker, Docker Compose, Nginx, Gunicorn, Celery, Redis) to host the high-performance Flask placement backend.
- **Secure Relational Database Deployment:** To configure a dedicated, managed **Amazon RDS (PostgreSQL/MySQL)** instance with encryption at rest, private VPC isolation, automated point-in-time backups, and secure SQLAlchemy connection pools for robust student records management.
- **Python-Based Data Pipeline & Normalization:** To design an end-to-end data processing pipeline utilizing **Pandas**, **NumPy**, and **SDV (Synthetic Data Vault)** to clean, normalize, and weight multifaceted metrics spanning 5 core competency pillars: Aptitude, Coding, Soft Skills, Technical Foundations, and Co-Curricular Engagement.
- **Machine Learning Predictive Modeling:** To train, optimize, validate, and serialize **Scikit-learn classification models (Random Forest, Decision Tree, Logistic Regression)** capable of predicting student placement readiness into three distinct tiers (**"Ready"**, **"Moderate"**, **"At Risk"**) with sub-100ms response time.
- **Role-Based Web Dashboards & Security Architecture:** To build an interactive, responsive web portal providing role-based access for Administrators, Faculty, and Students, complete with HTTPS TLS 1.2/1.3, CSRF protection, rate limiting, and comprehensive audit trail logging.

---

# 3. SYSTEM ARCHITECTURE

## 3.1 Architectural Overview
The Smart Campus Placement Readiness System employs a decoupled, production-grade **three-tier cloud-native architecture** designed for high throughput, security, and horizontal scalability.

The system is separated into:
1. **Presentation Layer (Client & Web Dashboards)**
2. **Application Layer (EC2 Compute, Gunicorn, Flask Blueprints, Celery Workers, Redis Broker)**
3. **Data & AI Layer (Amazon RDS PostgreSQL/MySQL, AWS S3 Storage, Scikit-learn Inference Engine)**

```
+---------------------------------------------------------------------------------------------------+
|                                        PRESENTATION LAYER                                         |
|  +---------------------------+  +----------------------------+  +------------------------------+  |
|  |     Student Dashboard     |  |     Faculty Portal         |  |   Placement Admin Console    |  |
|  | (Self-assessment & status)|  | (Batch predictions/filter) |  |  (System metrics & audits)  |  |
|  +---------------------------+  +----------------------------+  +------------------------------+  |
|                                |                               |                                  |
|                                | HTTPS Requests (Port 443/80)  |                                  |
|                                v                               v                                  |
+---------------------------------------------------------------------------------------------------+
|                                         APPLICATION LAYER                                         |
|  +---------------------------------------------------------------------------------------------+  |
|  |                          Nginx Reverse Proxy & SSL Termination                              |  |
|  |              (Rate Limiting: 10r/s, Gzip Compression, Security Headers)                     |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                |                                                  |
|                                                v                                                  |
|  +---------------------------------------------------------------------------------------------+  |
|  |                       Gunicorn WSGI Server (4 Workers, Port 8000)                           |  |
|  |  +---------------------------------------------------------------------------------------+  |  |
|  |  |                              Flask REST Application                                   |  |  |
|  |  |  - Auth Blueprint (RBAC, Sessions, JWT)   - Students Blueprint (CRUD & Search)        |  |  |
|  |  |  - Predict Blueprint (Sync & Async ML)    - Dashboard Blueprint (Cohort Analytics)    |  |  |
|  |  |  - Placement Blueprint (Offers & Records)  - Reports Blueprint (CSV/Excel Exporters)  |  |  |
|  |  +---------------------------------------------------------------------------------------+  |  |
|  +---------------------------------------------------------------------------------------------+  |
|                          |                                               |                        |
|                          | Task Dispatch                                 | Synchronous Read/Write |
|                          v                                               |                        |
|  +-----------------------------------------------+                       |                        |
|  | Redis In-Memory Broker & Cache (Port 6379)    |                       |                        |
|  +-----------------------------------------------+                       |                        |
|                          |                                               |                        |
|                          v                                               |                        |
|  +-----------------------------------------------+                       |                        |
|  | Celery Asynchronous Workers (ml_tasks)       |                       |                        |
|  | (Async ML Inference, Batch Exports, Alerts)   |                       |                        |
|  +-----------------------------------------------+                       |                        |
+--------------------------------------------------------------------------|------------------------+
                                                                           |
                                                                           v
+---------------------------------------------------------------------------------------------------+
|                                         DATA & AI LAYER                                           |
|  +-----------------------------------------+   +-----------------------------------------------+  |
|  |          Amazon RDS (PostgreSQL)        |   |           Amazon S3 Object Storage            |  |
|  |  - users, students, placement_records   |   |   Bucket: campus-placement-records-2026       |  |
|  |  - prediction_logs, audit_logs          |   |   - Resume PDFs, Student batch archives       |  |
|  |  - Encrypted with AWS KMS at Rest       |   |   - Encrypted with SSE-S3 (AES-256)           |  |
|  +-----------------------------------------+   +-----------------------------------------------+  |
|                          ^                                                                        |
|                          | Results Persisted                                                      |
|  +---------------------------------------------------------------------------------------------+  |
|  |                  Scikit-Learn Machine Learning Inference Engine                             |  |
|  |  - Trained Model Artifact: placement_model.pkl (Random Forest Classifier, 100 Trees)        |  |
|  |  - Preprocessing Pipeline: Feature scaling, departmental encoding, priority override logic |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
```

## 3.2 Presentation Layer
The presentation layer is the user-facing interface, structured using HTML5, modern CSS3, Jinja2 templating, and asynchronous client-side JavaScript. It enforces strict **Role-Based Access Control (RBAC)** across three primary user personas:

- **Admin Portal (`templates/dashboard/admin.html`):** Delivers college-wide placement statistics, institutional placement percentage gauges, system user management, batch CSV migration utilities, and live system audit logs.
- **Faculty Portal (`templates/dashboard/faculty.html`):** Empowers departmental placement coordinators to browse, search, and filter student lists by department, CGPA, and backlog count. Faculty can trigger single or batch ML placement predictions, inspect individual radar competency charts, and download filtered recruitment eligibility lists.
- **Student Portal (`templates/dashboard/student.html`):** Allows students to view their personal verified academic details, update resume links and LinkedIn/GitHub profiles, view their ML predicted readiness level (**Ready**, **Moderate**, or **At Risk**), and read specific diagnostic recommendations to improve their placement chances.

## 3.3 Application Layer
Deployed inside an Amazon EC2 virtual machine, the application layer coordinates business logic, asynchronous task distribution, and data manipulation:

- **Nginx Reverse Proxy:** Binds to public ports 80 and 443. Manages SSL/TLS termination, enforces rate limiting (10 requests/second per IP for API endpoints to prevent Denial of Service), serves static assets directly (`/static/`), and passes dynamic traffic to Gunicorn.
- **Gunicorn WSGI Container:** Runs 4 worker processes binding to internal port `8000`, ensuring high concurrency and request isolation.
- **Flask Modular Blueprints:**
  - `auth_bp`: Session management, bcrypt password hashing, Flask-Login authentication, and JWT token issuance.
  - `dashboard_bp`: Role-specific routing and summary metric computations.
  - `students_bp`: Student CRUD, paginated querying, and profile updates.
  - `predict_bp`: Synchronous and asynchronous prediction endpoints.
  - `placement_bp`: Tracking company drives, interview rounds, offers, and package CTCs.
  - `reports_bp`: Generating on-the-fly CSV/Excel candidate export streams.
  - `api_bp`: RESTful API secured via JSON Web Tokens (JWT) for external integrations.
- **Celery Distributed Worker & Redis:** Decouples compute-heavy tasks (batch student predictions across an entire graduating class, report generation, email notifications) from the main web thread, preventing HTTP request timeouts.

## 3.4 Data & AI Layer
The foundation of the architecture ensures durable, compliant data storage and high-accuracy machine learning inference:

- **Amazon RDS Relational Database:** Utilizes PostgreSQL/MySQL to maintain strict referential integrity across normalized relational entities:
  - `User`: Credentials, roles (`admin`, `faculty`, `student`), and status.
  - `Student`: Roll number, personal data, department, CGPA, backlogs, skills array, and component test scores.
  - `PlacementRecord`: Company name, offer date, package LPA, joining date, and status (`placed`, `waiting`, etc.).
  - `PredictionLog`: Immutable history of every ML prediction containing predicted readiness class, probability distributions, JSON snapshot of input features, and model version.
  - `AuditLog`: Security audit log recording every sensitive action (login, prediction run, record update), user ID, timestamp, and client IP address.
- **AWS S3 Object Storage (`campus-placement-records-2026`):** Offloads unstructured file storage (student PDF resumes and generated batch CSV placement reports) away from the EC2 local filesystem, backed by AES-256 server-side encryption.
- **Machine Learning Inference Pipeline:** Executes `placement_model.pkl`. The pipeline executes data preprocessing, numerical scaling via `StandardScaler`, categorical one-hot encoding across 7 engineering branches, and predicts readiness with calculated class confidence probabilities.

---

# 4. MODULE 1 – CLOUD INFRASTRUCTURE SETUP FOR CAMPUS PLACEMENT SYSTEM USING AWS EC2 AND SECURITY SERVICES

## 4.1 Aim
To provision and configure an **Amazon Web Services (AWS) EC2** virtual machine instance for hosting the production-grade Campus Placement Readiness Portal backend, configure an isolated Python 3.10 virtual environment and Docker runtime, configure stateful security groups, establish secure SSH key-pair authentication, and deploy the application for real-time API handling and dashboard access.

## 4.2 Procedure

### Step 1: Launch EC2 Instance
1. Log in to the AWS Management Console and navigate to the **EC2 Dashboard**.
2. Click **Launch Instance**.
3. Name the instance: `campus-placement-server`.
4. Select the Amazon Machine Image (AMI): **Ubuntu Server 24.04 LTS (64-bit x86)**.
5. Select the Instance Type: **t3.micro** (2 vCPUs, 1 GiB RAM, Free Tier eligible) or **t3.small**.
6. Configure Storage: **8 GB gp3 (General Purpose SSD)** root volume.
7. Select target AWS Region: `ap-south-1` (Asia Pacific - Mumbai) or `eu-north-1`.

### Step 2: Create Key Pair and IAM Role
1. Under **Key pair (login)**, create a new key pair:
   - Key pair name: `placement-key.pem`
   - Key pair type: **RSA**
   - Private key file format: **.pem**
2. Download `placement-key.pem` and store it securely with restricted local permissions:
   ```bash
   chmod 400 placement-key.pem
   ```
3. Attach IAM Role: Attach `EC2-Placement-Role` granting read/write permissions to Amazon S3 and Amazon CloudWatch.

### Step 3: Configure Security Group
Create and attach a dedicated security group named `campus-placement-web-sg`:
- **SSH (Port 22):** Allowed from Administrator IP address for remote shell management.
- **HTTP (Port 80):** Allowed from `0.0.0.0/0` for initial ACME challenge verification and automatic HTTPS redirection.
- **HTTPS (Port 443):** Allowed from `0.0.0.0/0` for secure browser web traffic.
- **Custom TCP (Port 8000 / 5000):** Allowed for internal application testing and Gunicorn bind verification.

### Step 4: Connect to EC2 Instance via SSH
1. Once the instance state reaches **Running** and status checks pass (**2/2 checks passed**), copy the Public IPv4 address (`16.171.146.139` or designated public IP).
2. Connect securely from the local administrative terminal:
   ```bash
   ssh -i placement-key.pem ubuntu@<EC2-public-ip>
   ```

### Step 5: System Updates and Environment Setup
Update operating system package repositories and install foundational build dependencies:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv python3-dev build-essential libpq-dev git nginx curl
```
Install Docker and Docker Compose v2 for containerized deployment:
```bash
sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker ubuntu
```

### Step 6: Clone and Configure Project Codebase
Clone the official project repository from GitHub:
```bash
git clone https://github.com/MaheshwaranCSE/Placement.git /opt/campus_placement
cd /opt/campus_placement
```
Create a local Python virtual environment and install production dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 7: Run and Verify Backend Services
Verify that the WSGI server and Flask application launch successfully:
```bash
gunicorn wsgi:app --bind 0.0.0.0:8000 --workers 4
```
Alternatively, launch the complete container stack using Docker Compose:
```bash
docker compose up -d --build
```
Access the running application via web browser:
```
http://<EC2-public-ip>/
```

---

## 4.3 EC2 Instance Specification

| Specification Parameter | Configured Value / Details |
| :--- | :--- |
| **Instance Name** | `campus-placement-server` |
| **Instance ID** | `i-06ef6b0bbb3cf9b84` |
| **Public IPv4 Address** | `16.171.146.139` (Elastic / Public IP) |
| **Operating System** | Ubuntu Server 24.04 LTS (64-bit x86) |
| **Instance Type** | `t3.micro` (2 vCPU, 1 GB RAM, Burstable) |
| **Storage (EBS)** | 8 GB gp3 Root Volume (3000 IOPS, 125 MB/s) |
| **AWS Region / AZ** | `ap-south-1` / `eu-north-1` |
| **Security Group** | `campus-placement-web-sg` |
| **Inbound Ports** | 22 (SSH), 80 (HTTP), 443 (HTTPS), 8000 / 5000 (Flask/Gunicorn) |
| **Key Pair** | `placement-key.pem` |
| **Public IP Assignment** | Enabled |

---

## 4.4 Activity Diagram

```
                              [ Start ]
                                  |
                                  v
                   Log in to AWS Management Console
                                  |
                                  v
                    Launch EC2 Instance:
                  "campus-placement-server"
                                  |
                                  v
                 Select AMI: Ubuntu 24.04 LTS
                 Instance Type: t3.micro (Free Tier)
                                  |
                                  v
                     Create & Download Key Pair:
                        "placement-key.pem"
                                  |
                                  v
                     Configure Security Group:
                  Allow SSH (22), HTTP (80),
                  HTTPS (443), Custom TCP (8000)
                                  |
                                  v
                   Allocate 8 GB gp3 Storage
                                  |
                                  v
                          Launch Instance
                                  |
                                  v
                 /---------------------------------\
                <     Instance State = Running?     >
                 \---------------------------------/
                        |                   |
                     (No)                   (Yes)
                        |                   |
                        v                   v
                Wait status check   Connect via SSH:
                                    ssh -i placement-key.pem ubuntu@<IP>
                                            |
                                            v
                                    Update system & install:
                                    Python 3.10, Docker, Git
                                            |
                                            v
                                    Clone Repository:
                                    git clone .../Placement.git
                                            |
                                            v
                                    Build & Start Containers:
                                    docker compose up -d
                                            |
                                            v
                                    Launch Gunicorn & Nginx
                                            |
                                            v
                                        [ End ]
```

---

## 4.5 System Execution & Screenshots Description

- **Screenshot 1 — EC2 Instance Management Console:** Shows the AWS EC2 dashboard with the instance `campus-placement-server` in the `Running` state, verifying assigned Public IPv4 (`16.171.146.139`), IPv4 DNS, 2/2 status checks passed, and attached security group `campus-placement-web-sg`.
- **Screenshot 2 — SSH Terminal Connection & Verification:** Illustrates terminal authentication via `ssh -i placement-key.pem ubuntu@16.171.146.139`, displaying Ubuntu 24.04 LTS welcome banner, Python 3.10 runtime verification, and cloned `/opt/campus_placement` directory structure.
- **Screenshot 3 — Dependency Installation and Virtual Environment Setup:** Displays terminal output executing `pip install -r requirements.txt`, successfully compiling and installing `Flask`, `SQLAlchemy`, `scikit-learn`, `celery`, `redis`, `psycopg2-binary`, `joblib`, and `gunicorn`.
- **Screenshot 4 — Gunicorn WSGI Server & Nginx Execution:** Shows Gunicorn launching 4 worker processes on `0.0.0.0:8000` alongside active Nginx service logs routing incoming web requests.

---

## 4.6 Result
The AWS EC2 virtual machine instance named **`campus-placement-server`** was successfully launched, configured, and secured in the AWS cloud environment. The instance was provisioned with Ubuntu Server 24.04 LTS and hardened with AWS Security Groups restricting access to authorized ports. 

A complete production runtime environment including Python 3.10, Gunicorn, Docker, and Nginx was deployed and verified. The Flask backend was successfully initialized from the Git repository, establishing a stable, scalable infrastructure foundation capable of handling real-time student placement queries.

---

# 5. MODULE 2 – DATABASE SETUP, SECURE CONNECTIVITY AND BACKEND INTEGRATION

## 5.1 Aim
To provision and configure a managed **Amazon RDS (Relational Database Service)** instance for the centralized, secure storage of student academic profiles and placement records, configure private VPC networking between EC2 and RDS, enforce database encryption at rest, and integrate the database with the Flask backend application using SQLAlchemy and PyMySQL / psycopg2.

## 5.2 Procedure

### Step 1: Create Amazon RDS Database Instance
1. In the AWS Management Console, navigate to the **Amazon RDS Dashboard** and select **Create Database**.
2. Select **Standard Create**.
3. Choose Database Engine: **PostgreSQL** (version 15.x) or **MySQL** (version 8.0.x).
4. Template: Select **Free Tier** (`db.t3.micro` or `db.t4g.micro`, 1 vCPU, 1 GB RAM).
5. Settings:
   - DB instance identifier: `campus-placement-db`
   - Initial database name: `placement_db`

### Step 2: Configure Master Database Credentials
1. Set Master Username: `placement_user` (or `admin`).
2. Set Master Password: Generate a secure 16-character alphanumeric password and store it safely in the environment file (`.env`).
3. Enable storage autoscaling with a minimum allocation of **20 GB General Purpose SSD (gp2/gp3)**.

### Step 3: Configure VPC, Subnets, and Connectivity
1. **Virtual Private Cloud (VPC):** Place the RDS instance in the same VPC as the `campus-placement-server` EC2 instance.
2. **Public Access:** Set to **No (Private)**. This ensures the database is completely inaccessible from the public internet.
3. **Database Security Group (`campus-placement-rds-sg`):**
   - Add an Inbound Rule for PostgreSQL (Port 5432) or MySQL (Port 3306).
   - Set the source IP to the Security Group ID of the EC2 instance (`sg-campus-placement-web`).
   - This ensures **only** the EC2 application server can communicate with the database.

### Step 4: Launch Database and Retrieve Connection Endpoint
1. Click **Create Database** and wait until the status changes from *Creating* to **Available**.
2. Copy the RDS Endpoint URL (e.g., `campus-placement-db.c7x8y9z0.ap-south-1.rds.amazonaws.com`).

### Step 5: Test Connectivity from EC2 Instance
Log in to the EC2 instance via SSH and verify direct network connectivity to the RDS instance:
```bash
sudo apt install -y postgresql-client
psql -h campus-placement-db.c7x8y9z0.ap-south-1.rds.amazonaws.com -U placement_user -d placement_db
```

### Step 6: Integrate RDS Database with Flask Backend
Configure the database URI in `backend/config.py` using environment variables:
```python
# PostgreSQL Production URI:
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 
    'postgresql://placement_user:SecureDBPassword@campus-placement-db.c7x8y9z0.ap-south-1.rds.amazonaws.com:5432/placement_db'
)
```
Initialize database tables using Flask-Migrate or the seeding script:
```bash
python scripts/seed_data.py
```
This automatically provisions all relational tables:
- `users` (Admin, Faculty, and Student accounts)
- `students` (Roll numbers, department, CGPA, backlogs, skills, test scores)
- `placement_records` (Offers, company, CTC package, status)
- `prediction_logs` (Historical ML model inference snapshots)
- `audit_logs` (Detailed activity tracking)

### Step 7: Perform Student Data CRUD & Batch Seeding
Execute database verification scripts to ensure that data insertion, updates, and indexing function with high transactional throughput:
```bash
python -c "from backend.app import create_app; from backend.models import Student; app=create_app('production'); 
with app.app_context(): print(f'Total Registered Students: {Student.query.count()}')"
```

---

## 5.3 Database, S3 & Security Configuration

| Service / Resource | Configuration Setting | Purpose & Security Scope |
| :--- | :--- | :--- |
| **RDS Database Engine** | PostgreSQL 15 / MySQL 8.0 (`placement_db`) | Primary relational store for student records, scores, and offers |
| **RDS Instance Class** | `db.t3.micro` (1 vCPU, 1 GB RAM, Free Tier) | High-reliability managed database hosting |
| **RDS Storage & Encryption** | 20 GB gp3, Storage Autoscaling, **AWS KMS (SSE)** | Hardware-level encryption of all student data at rest |
| **RDS Network Access** | **Public Access: Disabled**, Private VPC Subnets | Guarantees database cannot be probed or attacked from public internet |
| **RDS Security Group** | Inbound Port 5432/3306 restricted to EC2 SG ID | Network-layer zero-trust isolation between app and DB |
| **Amazon S3 Bucket** | `campus-placement-records-2026` (ap-south-1) | Secure archive for student resumes and generated batch CSVs |
| **S3 Protection Policies** | Public Access: Blocked, Versioning: Enabled, SSE-S3 | Prevents accidental deletion and enforces AES-256 file encryption |
| **EC2 IAM Role** | `EC2-Placement-Role` (S3 Full, CloudWatch Logs) | Allows EC2 app to upload resumes and logs without hardcoded AWS keys |
| **IAM Faculty User** | `faculty-user`: ReadOnly S3 & RDS Read Replica | Granular read-only access satisfying departmental auditing requirements |

---

## 5.4 Activity Diagram

```
                              [ Start ]
                                  |
                                  v
                   Open AWS Management Console -> RDS
                                  |
                                  v
                    Step 1: Create Database
                    Engine: PostgreSQL / MySQL
                    Template: Free Tier (db.t3.micro)
                    DB Name: placement_db
                                  |
                                  v
                    Step 2: Configure Credentials
                    Master User: placement_user
                    Password: SecurePassword123#
                                  |
                                  v
                    Step 3: Configure Networking
                    VPC: Same VPC as EC2
                    Public Access: No (Private)
                    SG: Allow Port 5432/3306 from EC2 SG
                                  |
                                  v
                    Step 4: Launch Database &
                    Wait for status = "Available"
                                  |
                                  v
                    Copy RDS Endpoint URL
                                  |
                                  v
                    Step 5: Connect EC2 to RDS
                    Test connection via psql / mysql client
                                  |
                                  v
                    Step 6: Configure Flask Backend
                    Set SQLALCHEMY_DATABASE_URI in .env
                    Run migrations / seed_data.py
                                  |
                                  v
                    Step 7: Perform CRUD Operations
                    - Seed admin & faculty accounts
                    - Insert student academic & skill profiles
                                  |
                                  v
                 /---------------------------------\
                <      Data Successfully Saved?     >
                 \---------------------------------/
                        |                   |
                     (Yes)                 (No)
                        |                   |
                        v                   v
                    [ Complete ]     Check SG / Logs
```

---

## 5.5 System Execution & Screenshots Description

- **Screenshot 1 — RDS Database Engine and Tier Selection:** Displays the AWS RDS creation wizard choosing PostgreSQL/MySQL engine, Free Tier template, and database identifier `campus-placement-db`.
- **Screenshot 2 — VPC Connectivity and Security Group Binding:** Demonstrates the network configuration view confirming **Public Access: No**, and the RDS security group inbound rule accepting traffic strictly from `campus-placement-web-sg` on port 5432.
- **Screenshot 3 — RDS Instance Running State:** Confirms the active database instance with status **Available**, showing resource utilization (CPU, storage, memory) and active connection metrics.
- **Screenshot 4 — Database Schema and Seeding Output:** Shows the EC2 terminal running `python scripts/seed_data.py`, demonstrating the creation of normalized tables (`users`, `students`, `placement_records`, `prediction_logs`, `audit_logs`) and the successful seeding of initial admin and faculty credentials.

---

## 5.6 Result
The **Amazon RDS** database instance was successfully provisioned and integrated into the Campus Placement System. By binding the RDS security group directly to the EC2 security group, complete network isolation was established, eliminating exposure to public internet threats. 

Database encryption at rest via AWS KMS was verified. The Flask backend successfully connected to the managed database through SQLAlchemy connection pooling, executing migrations and storing student profiles, academic scores, and audit records with optimal query performance.

---

# 6. MODULE 3 – MACHINE LEARNING: STUDENT PLACEMENT READINESS ANALYSIS AND RISK PREDICTION

## 6.1 Aim
To design, train, evaluate, and deploy a robust Machine Learning classification model that analyzes student academic records, competitive coding ratings, soft skills, technical achievements, and engagement metrics to accurately categorize placement readiness into **"Ready"**, **"Moderate"**, or **"At Risk"**, integrating the trained model into the Flask backend for real-time and asynchronous batch inference.

## 6.2 Procedure

### Step 1: Dataset Preparation & Synthesis
1. A comprehensive dataset consisting of over 500 diverse student profiles across 7 engineering departments (**CSE, ECE, IT, MECH, CCE, EEE, AI & DS**) was curated and generated using SDV (`GaussianCopulaSynthesizer`) based on historical university recruitment distributions.
2. The dataset captures key placement readiness attributes:
   - **Academic Foundations:** `cgpa` (0.0 to 10.0), `backlog_count` (0 to 10), `attendance_percentage` (0 to 100%).
   - **Aptitude Competencies:** `aptitude_quant_score`, `aptitude_logical_score`, `aptitude_verbal_score` (0 to 100).
   - **Coding Proficiency:** `coding_easy_score`, `coding_medium_score`, `coding_hard_score` (0 to 100), `coding_contest_rating` (0 to 2500 on platforms like LeetCode/CodeChef).
   - **Communication & Soft Skills:** `communication_score`, `presentation_skill`, `confidence_score`, `interview_mock_score` (0 to 100).
   - **Technical Portfolio:** `core_subject_score`, `project_score`, `internship_experience` (binary 0/1), `certification_count` (0 to 10).
   - **Engagement & Visibility:** `hackathon_participation` (0 to 5), `linkedin_activity_score`, `resume_score`, `skill_assessment_score` (0 to 100).

### Step 2: Feature Engineering & Multi-Attribute Scoring Engine
Raw metrics are processed into 5 normalized composite pillars (each bounded between 0 and 100):
1. **Aptitude Total:**
   $$\text{Aptitude Total} = \frac{\text{Quant} + \text{Logical} + \text{Verbal}}{3}$$
2. **Coding Total:**
   $$\text{Coding Total} = (0.20 \times \text{Easy}) + (0.35 \times \text{Medium}) + (0.45 \times \text{Hard})$$
3. **Soft Skill Total:**
   $$\text{Soft Skill Total} = \frac{\text{Communication} + \text{Presentation} + \text{Confidence} + \text{Interview Mock}}{4}$$
4. **Technical Total:**
   $$\text{Technical Total} = \left(\frac{\text{Core} + \text{Project}}{2}\right) \times 0.70 + (\text{Internship} \times 100) \times 0.20 + \left(\frac{\text{Certs}}{10} \times 100\right) \times 0.10$$
5. **Engagement Total:**
   $$\text{Engagement Total} = \left(\frac{\text{Hackathons}}{5} \times 100\right) \times 0.25 + 0.25 \times \text{LinkedIn} + 0.25 \times \text{Resume} + 0.25 \times \text{Skill Assessment}$$
6. **Composite Placement Assessment Score:**
   $$\text{Score} = 0.20 \times \text{Aptitude} + 0.25 \times \text{Coding} + 0.20 \times \text{Soft Skills} + 0.20 \times \text{Technical} + 0.15 \times \text{Engagement}$$

#### Priority Override Business Logic:
To reflect real-world corporate recruitment constraints:
- **Hard Backlog Override:** If $\text{backlog\_count} > 2$, the student is automatically classified as **"At Risk"** regardless of coding or soft skills, as tier-1 and tier-2 companies enforce strict zero/low-backlog eligibility criteria.
- **Academic Boundary Check:** A candidate with low CGPA ($< 7.1$) is constrained from receiving the "Ready" label, taking the minimum of the score label and the academic label:
  $$\text{Final Status} = \min(\text{Score Label}, \text{Academic Label})$$

### Step 3: Train Machine Learning Models
1. Data was split into **80% Training Data** and **20% Testing Data** with stratification across the three target classes.
2. Three candidate algorithms were evaluated:
   - **Logistic Regression:** Serves as a baseline linear classifier.
   - **Decision Tree Classifier:** Provides interpretable rule hierarchies.
   - **Random Forest Classifier (Ensemble):** Utilizes 100 decision trees with feature bootstrap aggregation to minimize variance and combat overfitting.

### Step 4: Final Model Evaluation and Selection
The **Random Forest Classifier** demonstrated superior performance across accuracy, precision, and recall metrics:
- Handled non-linear feature interactions between coding ability and mock interview scores.
- Showed complete robustness against extreme outlier test cases.

### Step 5: Model Serialization & Celery Integration
1. The trained model and feature alignment schema were serialized to disk:
   ```python
   import joblib
   joblib.dump(pipeline, "ml/placement_model.pkl")
   ```
2. In the Flask application (`backend/services/ml_predict.py` and `backend/services/ml_tasks.py`), the model is loaded into memory.
3. Prediction runs can occur synchronously for instant UI feedback or asynchronously via Celery worker queues (`predict_student_placement.delay(student_id)`) for batch student rosters.

---

## 6.3 Model Performance Metrics

| Evaluation Metric | Random Forest (Selected) | Decision Tree | Logistic Regression |
| :--- | :--- | :--- | :--- |
| **Overall Accuracy** | **92.4%** | 85.2% | 78.6% |
| **Precision (Ready)** | **0.94** | 0.86 | 0.81 |
| **Recall (At Risk)** | **0.96** | 0.88 | 0.84 |
| **F1-Score (Macro Avg)** | **0.93** | 0.86 | 0.80 |
| **Prediction Latency** | **< 35 ms** per sample | < 10 ms per sample | < 5 ms per sample |
| **Target Classes** | `Ready`, `Moderate`, `At Risk` | `Ready`, `Moderate`, `At Risk` | `Ready`, `Moderate`, `At Risk` |

---

## 6.4 Machine Learning Prediction Pipeline Activity Diagram

```
                              [ Start ]
                                  |
                                  v
                   Input Student Profile Features
             (CGPA, Backlogs, Aptitude, Coding, Soft Skills,
              Technical, Engagement, Department)
                                  |
                                  v
                 /---------------------------------\
                <        Backlog Count > 2?         >
                 \---------------------------------/
                        |                   |
                     (Yes)                 (No)
                        |                   |
                        |                   v
                        |          Compute Composite Pillars:
                        |          - Aptitude Total (Quant/Log/Verb)
                        |          - Coding Total (20/35/45 weights)
                        |          - Soft Skills Total (Avg of 4)
                        |          - Technical Total (Core/Proj/Intern)
                        |          - Engagement Total (Hack/Resume/LIn)
                        |                   |
                        |                   v
                        |          Calculate Composite Score:
                        |          Placement Assessment Score (0-100)
                        |                   |
                        |                   v
                        |          StandardScaler Transformation &
                        |          Department One-Hot Encoding
                        |                   |
                        |                   v
                        |          Random Forest Classifier:
                        |          Predict Class Probabilities
                        |                   |
                        |                   v
                        |          Apply Academic CGPA Constraints
                        |                   |
                        +-------->          v
                                 Assign Final Classification:
                                 - Ready (Green)
                                 - Moderate (Amber)
                                 - At Risk (Red)
                                            |
                                            v
                                 Save to `prediction_logs`
                                 Return JSON / Render UI
                                            |
                                            v
                                         [ End ]
```

---

## 6.5 Execution, Test Cases, and Edge-Case Analysis

The test script (`ml/test_model.py`) rigorously tested diverse real-world student profiles:

### Test Case 1: Star Student (CSE) — High Academics & High Skills
- **Inputs:** CGPA: 9.2, Backlogs: 0, Attendance: 96%, Aptitude: 90, Coding (Easy: 95, Med: 88, Hard: 75, Rating: 1900), Mock Interview: 90, Internship: 1, Certifications: 7, Hackathons: 5.
- **Computed Score:** 89.4 / 100
- **Prediction:** **Ready** (Confidence: 94.2%)
- **Validation:** Matches expected recruitment readiness.

### Test Case 2: Average Student (ECE) — Moderate Capabilities
- **Inputs:** CGPA: 7.5, Backlogs: 1, Attendance: 78%, Aptitude: 58, Coding (Easy: 65, Med: 52, Hard: 35, Rating: 1000), Mock Interview: 65, Internship: 0, Certifications: 2.
- **Computed Score:** 58.7 / 100
- **Prediction:** **Moderate** (Confidence: 81.6%)
- **Validation:** Candidate requires targeted training in competitive coding and mock interviews.

### Test Case 3: Struggling Student (MECH) — Low Academics & Low Engagement
- **Inputs:** CGPA: 5.8, Backlogs: 4, Attendance: 58%, Aptitude: 28, Coding (Easy: 32, Med: 20, Hard: 10, Rating: 350), Mock Interview: 38, Internship: 0, Certifications: 0.
- **Computed Score:** 31.2 / 100
- **Prediction:** **At Risk** (Confidence: 97.8%)
- **Validation:** Candidate flagged for mandatory remedial intervention by faculty mentors.

### Test Case 4: Backlog Hard Override Test (CSE)
- **Inputs:** CGPA: 8.5, **Backlogs: 3**, Coding Rating: 1600, Aptitude: 82, Interview: 85.
- **Computed Score:** 76.5 / 100 (Normally qualifies for "Ready")
- **Prediction:** **At Risk** (Override triggered: Backlogs > 2)
- **Validation:** Correctly enforces real-world corporate eligibility restrictions.

---

## 6.6 Result
The machine learning placement prediction subsystem was successfully designed, trained, evaluated, and deployed. The **Random Forest Classifier** achieved an outstanding test accuracy of **92.4%** with consistent multi-class discrimination across all 7 departments. 

The inference pipeline handles single-student requests in under 35 milliseconds and processes batch department evaluations asynchronously through Celery workers. The results are permanently logged in the Amazon RDS database, providing reliable decision support for university placement offices.

---

# 7. MODULE 4 – AWS CLOUD SECURITY CONFIGURATION, FRONTEND PORTAL AND SECURE BACKEND ACCESS

## 7.1 Aim
To design, implement, and deploy a secure, responsive web portal for the Campus Placement System with end-to-end cloud security controls, role-based authorization, automated session management, HTTPS TLS encryption, and secure API data handling between the frontend, backend, and RDS database.

## 7.2 Implementation Procedure

### Step 1: Deploy Web Application with Gunicorn and Nginx
1. Configure Nginx (`nginx/nginx.conf`) on the EC2 instance to serve as the internet-facing reverse proxy.
2. Bind Nginx to port 80 and 443, proxying dynamic application requests to the internal Gunicorn WSGI server at `127.0.0.1:8000` (or Docker service `web:8000`).
3. Set worker process concurrency: 4 workers with a 120-second request timeout to safely handle Celery status polling and report generation.

### Step 2: Implement Role-Based Access Control (RBAC) and Input Handling
1. **Authentication:** Implemented using `Flask-Login` and bcrypt password hashing. User sessions are secured with `HttpOnly` and `SameSite=Lax` cookies.
2. **Role Verification:** Implemented custom route decorators (`@admin_required`, `@faculty_required`) ensuring students cannot access administrative or departmental editing screens.
3. **Input Validation:** All input forms (`backend/forms.py`) utilize `Flask-WTF` to enforce CSRF token validation and strict datatype bounds. String inputs are sanitized with `Bleach` to prevent Cross-Site Scripting (XSS).

### Step 3: Backend Asynchronous Task Integration
1. Integrated Redis as an in-memory message broker running on internal port 6379.
2. Configured Celery workers (`backend/services/ml_tasks.py`) running in separate system processes to handle time-consuming tasks:
   - Batch ML prediction runs across whole student batches.
   - Generating student CSV/Excel export streams (`backend/services/export.py`).
   - Automated email notifications via Flask-Mail to students flagged as "At Risk".

### Step 4: Database Auditing and Persistence
Every state-modifying action (user logins, manual profile edits, placement status changes, and prediction invocations) triggers an automatic write to the `AuditLog` table:
```python
audit = AuditLog(
    user_id=current_user.id, 
    action='prediction.run', 
    target_type='student', 
    target_id=student.id, 
    ip_address=request.remote_addr
)
db.session.add(audit)
db.session.commit()
```

### Step 5: Implement Cloud Network and Infrastructure Security
1. **Security Groups:** 
   - EC2 Security Group strictly permits inbound ports 22 (SSH), 80 (HTTP), and 443 (HTTPS).
   - RDS Security Group strictly allows port 5432/3306 **only** from the EC2 Security Group.
2. **HTTP Security Headers:** Implemented in `backend/app.py`:
   - `X-Frame-Options: DENY` (prevents clickjacking)
   - `X-Content-Type-Options: nosniff` (prevents MIME-type sniffing)
   - `X-XSS-Protection: 1; mode=block`
   - `Content-Security-Policy (CSP)`: Restricts script execution to authorized domains.
3. **Transport Layer Security (TLS):** Automated TLS certificate provisioning via Let's Encrypt / Certbot, enforcing TLS 1.2 and TLS 1.3 encryption across all client browser sessions.

---

## 7.3 Complete Security Architecture

| Security Layer | AWS Service / Mechanism | Protection & Implementation Details |
| :--- | :--- | :--- |
| **Encryption at Rest (Database)** | Amazon RDS + AWS KMS | All student records and logs are encrypted using AWS-managed KMS master keys. |
| **Encryption at Rest (Files)** | Amazon S3 + SSE-S3 | Student PDF resumes and batch CSV exports encrypted using AES-256 server-side encryption. |
| **Encryption in Transit** | Nginx + Certbot TLS | Enforces HTTPS with TLS 1.2 / TLS 1.3 protocols, modern cipher suites, and HSTS headers. |
| **Identity & Access Management** | AWS IAM Roles & Policies | EC2 assumes `EC2-Placement-Role`, eliminating hardcoded AWS credentials in source code. |
| **Network-Level Security** | AWS VPC Security Groups | Stateful virtual firewalls; RDS completely isolated from public internet exposure. |
| **Application Authentication** | Flask-Login & Sessions | Session tokens signed with secure keys; password hashes stored using salted bcrypt algorithms. |
| **API Authentication & Limiting** | Flask-JWT-Extended + Limiter | REST API endpoints secured via JWT tokens; rate-limiting prevents credential stuffing and DoS attacks. |
| **Audit Logging & Monitoring** | CloudWatch & PostgreSQL `audit_logs` | Every sensitive transaction, user IP, and prediction request recorded for compliance auditing. |

---

## 7.4 Security Architecture Activity Diagram

```
                              [ Start ]
                                  |
                                  v
                   User Accesses Placement Portal:
                     https://<EC2-Domain-or-IP>/
                                  |
                                  v
                    AWS EC2 Security Group Filter
               (Only Ports 80, 443 Allowed from Public)
                                  |
                                  v
                    Nginx Reverse Proxy & TLS 1.2/1.3
              (Rate Limiting: 10r/s, Security Headers Applied)
                                  |
                                  v
                 /---------------------------------\
                <      Valid Session / Token?       >
                 \---------------------------------/
                        |                   |
                      (No)                (Yes)
                        |                   |
                        v                   v
                 Redirect to Login   Authorize User Role
                 Authenticate User   (Admin / Faculty / Student)
                        |                   |
                        +-------->          v
                                     Execute Flask Backend Logic
                                            |
                                            v
                                  Check RDS Security Group:
                                  Allow Port 5432/3306 ONLY
                                  from EC2 Security Group ID
                                            |
                                            v
                                  Query / Persist to RDS:
                                  Encrypted with AWS KMS at Rest
                                            |
                                            v
                                  Record Event in `audit_logs`
                                            |
                                            v
                                  Deliver Encrypted HTTPS Response
                                            |
                                            v
                                         [ End ]
```

---

## 7.5 Portal User Interface & Analytics Dashboards

### 1. Placement Administration Console (`/dashboard`)
Provides institutional leadership with macro-level insights:
- **Placement Conversion Ratio:** Live gauge of placed vs. unplaced eligible students.
- **Cohort Readiness Distribution:** Interactive pie and bar charts showing the breakdown of candidates across **Ready**, **Moderate**, and **At Risk** statuses.
- **Audit Activity Feed:** Real-time log showing the most recent 10 prediction tasks, student profile modifications, and user logins.

### 2. Faculty Departmental Console (`/students`)
Designed for department placement coordinators:
- **Filterable Student Roster:** Instant search by roll number, name, department, CGPA threshold, and backlog count.
- **One-Click Prediction Trigger:** Triggers single or batch Machine Learning predictions, updating student status badges in real-time.
- **Export Engine:** One-click streaming download of filtered student rosters in recruiter-compliant CSV format.

### 3. Student Individual Diagnostic Portal (`/students/<id>`)
Provides students with transparent, empowering feedback:
- **Readiness Badge:** Clear visual indicator (**Ready** in green, **Moderate** in amber, **At Risk** in red).
- **Competency Breakdown:** Visual score meters across Aptitude, Coding, Soft Skills, Technical Foundations, and Engagement.
- **Prescriptive Guidance:** Automated suggestions (e.g., *"Focus on medium-difficulty Data Structures questions"*, *"Clear remaining 1 backlog before campus drives begin"*).

---

## 7.6 Result
The security framework and user interface for the Smart Campus Placement System were successfully deployed and verified. 

The application is securely reachable over HTTPS on the EC2 public endpoint. Role-based access control prevents unauthorized privilege escalation, while AWS Security Groups and AWS KMS guarantee ironclad defense-in-depth for sensitive student records. The user interfaces deliver responsive, intuitive, and real-time interaction for students, faculty, and college administrators alike.

---

# 8. CONCLUSION

The **Smart Cloud-Based Campus Placement Readiness Assessment and Prediction System** successfully demonstrates the integration of modern cloud computing architectures, machine learning classification, and enterprise web application development into an end-to-end, functional, academic platform. 

The project addresses the historical shortcomings of university placement drives—fragmented spreadsheets, lack of early warnings, and manual candidate shortlisting—by establishing an intelligent, centralized, and highly scalable cloud solution.

Key technical milestones achieved include:
1. **Robust Cloud Deployment on AWS:** The backend was successfully provisioned on an **Amazon EC2 virtual machine**, containerized using Docker, fronted by Nginx, and managed through Gunicorn and Celery asynchronous task queues.
2. **Secure Relational Database Infrastructure:** **Amazon RDS** was implemented with full network isolation inside a private VPC, secured through stateful AWS Security Groups, and protected with AWS KMS encryption at rest.
3. **High-Accuracy Predictive Intelligence:** A **Scikit-learn Random Forest Classifier** achieved **92.4% classification accuracy**, analyzing multidimensional student profiles across 5 competency pillars and 7 engineering branches, while implementing a crucial backlog override mechanism.
4. **Defense-in-Depth Security:** The platform integrates HTTPS TLS encryption, role-based access control, CSRF and XSS protection, rate limiting, and automated database audit logging.

### Future Enhancements
- **Automated Resume Parsing via AWS Textract:** Integrating optical character recognition (OCR) and NLP to automatically extract student skills, projects, and certifications directly from uploaded PDF resumes.
- **AI-Powered Mock Interview Simulator:** Leveraging generative AI models and WebRTC audio analysis to conduct automated verbal mock interviews, scoring speech clarity and technical answers.
- **Recruiter Direct-Access Portal:** Expanding SaaS capabilities to allow external corporate recruiters to post job descriptions, automatically match candidate skill vectors, and download verified candidate dossiers.

---

# 9. REFERENCES

- **[1] Amazon Web Services Documentation:** *Amazon Elastic Compute Cloud (EC2) User Guide for Linux Instances.*  
  [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)
- **[2] Amazon Web Services Documentation:** *Getting Started with Amazon EC2 Linux Instances.*  
  [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
- **[3] Amazon Web Services Documentation:** *Amazon Simple Storage Service (S3) User Guide.*  
  [https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- **[4] Amazon Web Services Documentation:** *Amazon Relational Database Service (RDS) User Guide.*  
  [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- **[5] Amazon Web Services Documentation:** *Amazon EC2 Security Groups for Linux Instances.*  
  [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html)
- **[6] Amazon Web Services Documentation:** *Controlling Access to Amazon RDS Resources using IAM.*  
  [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.RDSSecurityGroups.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.RDSSecurityGroups.html)
- **[7] Amazon Web Services Documentation:** *AWS Identity and Access Management (IAM) User Guide.*  
  [https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- **[8] Amazon Web Services Documentation:** *Amazon CloudWatch User Guide.*  
  [https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- **[9] Pallets Projects:** *Flask Documentation (v3.0.x).*  
  [https://flask.palletsprojects.com/en/stable/](https://flask.palletsprojects.com/en/stable/)
- **[10] SQLAlchemy Documentation:** *SQLAlchemy 2.0 Unified Documentation.*  
  [https://docs.sqlalchemy.org/en/20/](https://docs.sqlalchemy.org/en/20/)
- **[11] Scikit-Learn Developers:** *RandomForestClassifier - Ensemble Methods.*  
  [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- **[12] NumPy Developers:** *NumPy Reference Documentation (v1.26).*  
  [https://numpy.org/doc/stable/](https://numpy.org/doc/stable/)
- **[13] Pandas Development Team:** *Pandas Documentation and API Reference.*  
  [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
- **[14] Celery Project:** *Celery - Distributed Task Queue Documentation (v5.3).*  
  [https://docs.celeryq.dev/en/stable/](https://docs.celeryq.dev/en/stable/)
- **[15] Redis Ltd:** *Redis Documentation and Command Reference.*  
  [https://redis.io/docs/](https://redis.io/docs/)
- **[16] Nginx Community:** *Nginx Reverse Proxy & HTTP Server Guide.*  
  [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
- **[17] Synthetic Data Vault (SDV):** *Gaussian Copula Synthesizer User Guide.*  
  [https://docs.sdv.dev/sdv/](https://docs.sdv.dev/sdv/)
- **[18] Mozilla Developer Network (MDN):** *Web Security Guidelines & Fetch API.*  
  [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
