# Campus Placement Readiness Portal

A production-grade, college-deployable system for predicting student placement readiness using Machine Learning, built with Flask, PostgreSQL, Celery, and Docker.

## Prerequisites
- Docker 24+
- Docker Compose v2
- Git

## Deployment Setup

1. **Clone the repository:**
   ```bash
   git clone <repo_url> /opt/campus_placement
   cd /opt/campus_placement
   ```

2. **Environment Variables:**
   Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   Update `.env` with strong passwords and your college's SMTP details.

3. **Start the Application:**
   ```bash
   make up
   ```
   This builds the Docker images and starts PostgreSQL, Redis, Web, Celery, Nginx, and Prometheus.

4. **Initialize Database and Seed Data:**
   Initialize the schema:
   ```bash
   make migrate
   ```
   Seed the database with an admin user, sample faculty, and test students:
   ```bash
   make seed
   ```
   *Optional:* If migrating from the legacy JSON setup:
   ```bash
   make migrate_json
   ```

5. **Log In:**
   The portal is accessible via Nginx on port 80/443 pointing to Web. 
   - URL: `http://localhost/` or `https://placement.college.edu/`
   - Admin Login: `admin` / `<ADMIN_PASSWORD from .env>`
   - Faculty Login: `faculty_cse` / `faculty#Password1`

## Makefile Commands
- `make up` - Start containers in background.
- `make down` - Stop containers.
- `make logs` - Tail web and celery logs.
- `make backup` - Trigger a PostgreSQL database backup.
- `make test` - Run pytest suite with coverage.

## Backup & Recovery
Backups are triggered via `/scripts/backup_db.sh` inside the postgres container. Establish a cron job on your host server to run daily:
```bash
0 2 * * * make -C /opt/campus_placement backup
```
