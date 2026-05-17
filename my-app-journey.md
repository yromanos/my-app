# From Zero to Deployed App — Full Summary
**User:** yromanos | **OS:** CachyOS (Arch-based Linux) | **Date:** May 2026

---

## What We Built
A Python Flask web app that serves an HTML page, packaged into a Docker image, automatically built and published via GitHub Actions, and deployed on a local server using Docker Compose.

---

## Step 1 — Local Setup on PC

### Installed Tools
```bash
sudo pacman -S code        # VS Code
sudo pacman -S git         # Git (if not already installed)
pip install flask --break-system-packages
```

### Folder Structure Created
```
~/Projects/
└── my-app/
    ├── .gitignore
    ├── readme.md
    ├── requirements.txt
    ├── Dockerfile
    ├── .github/
    │   └── workflows/
    │       └── docker.yml
    └── src/
        └── main.py
```

### Git Initialized
```bash
mkdir -p ~/Projects/my-app
cd ~/Projects/my-app
git init
```

### Git Global Config (one time)
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---

## Step 2 — The App

### `src/main.py`
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>My First App</title>
        </head>
        <body>
            <h1>This is my first app written in VS Code and downloaded from GitHub</h1>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### `requirements.txt`
```
flask
```

### Run locally to test
```bash
python src/main.py
# Open browser at http://localhost:5000
```

---

## Step 3 — Git & GitHub

### GitHub Account
- URL: https://github.com/yromanos
- Repository: https://github.com/yromanos/my-app

### Connect local project to GitHub
```bash
git remote add origin https://github.com/yromanos/my-app.git
git push -u origin master
```

> ⚠️ GitHub requires a **Personal Access Token** instead of your password.
> Get it at: GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic) → Generate new token → check **repo** → copy it.

### Daily Git Workflow
```bash
git add .
git commit -m "Describe what you changed"
git push
```

---

## Step 4 — Dockerfile

### `Dockerfile`
```dockerfile
# Start from an official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of your app
COPY . .

# Tell Docker what port your app uses
EXPOSE 5000

# The command to run your app
CMD ["python", "src/main.py"]
```

---

## Step 5 — GitHub Actions (Auto Build & Publish)

### `.github/workflows/docker.yml`
```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [master]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/yromanos/my-app:latest
```

### Important GitHub Setting (do once)
Go to: **Repository → Settings → Actions → General → Workflow Permissions**
Select: **Read and write permissions** → Save

### What this does automatically on every `git push`:
1. Pulls your latest code
2. Builds the Docker image
3. Publishes it to `ghcr.io/yromanos/my-app:latest`

---

## Step 6 — Deploy on Server

### `docker-compose.yml` (lives on the server only, not in the project)
```yaml
services:
  my-app:
    image: ghcr.io/yromanos/my-app:latest
    ports:
      - "5000:5000"
    restart: unless-stopped
```

### First time setup on server
```bash
mkdir -p ~/apps/my-app
nano ~/apps/my-app/docker-compose.yml
# Paste the compose file above, then:
docker compose up -d
```

### Update server after pushing new code
```bash
docker compose pull
docker compose up -d
```

---

## The Complete Workflow (Ongoing)

```
1. Write/edit code in VS Code
       ↓
2. git add .
   git commit -m "what changed"
   git push
       ↓
3. GitHub Actions automatically builds & publishes Docker image
       ↓
4. On server: docker compose pull && docker compose up -d
       ↓
5. App is live at http://SERVER_IP:5000
```

---

## VS Code Extensions Installed
| Extension | Purpose |
|---|---|
| GitLens | See git history visually |
| Git Graph | Visual branch/commit tree |
| Prettier | Auto-formats code |
| Error Lens | Shows errors inline |

---

## Key Concepts

| Tool | Role |
|---|---|
| **Git** | Track changes to code locally |
| **GitHub** | Host code + run automation |
| **Flask** | Python web framework |
| **Docker** | Package app + environment into one image |
| **GitHub Actions** | Auto-build on every push |
| **ghcr.io** | GitHub's Docker image registry |
| **Docker Compose** | Run the image on a server easily |
