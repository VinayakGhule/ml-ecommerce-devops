# EC2 deployment guide

This repo can run on a single Ubuntu EC2 instance with Docker Compose. For AWS Free Tier, keep the footprint small:

- Prefer `docker-compose.ec2.yml` over the existing `docker-compose.yml`.
- Skip Grafana on a micro instance unless you confirm memory headroom.
- Keep PostgreSQL on the same EC2 box for a demo or portfolio deployment.

## 1. Launch the instance

- Create an EC2 instance in AWS.
- Choose Ubuntu Server 24.04 LTS or 22.04 LTS.
- Use a free-tier eligible instance type such as `t2.micro` or `t3.micro` if AWS shows it as free-tier eligible for your account.
- Security group inbound rules:
  - `22` from your IP
  - `5000` from your IP
  - `5001` from your IP
  - `5002` from your IP
  - `80` from anywhere only if you later add Nginx for the frontend

## 2. Install Docker

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 git
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker
docker --version
docker compose version
```

## 3. Copy the project

```bash
git clone <your-repo-url>
cd ml-ecommerce-devops
```

If the repo is private, copy it with SCP or use a GitHub personal access token.

## 4. Start the stack

```bash
docker compose -f docker-compose.ec2.yml up -d --build
docker compose -f docker-compose.ec2.yml ps
```

## 5. Seed demo data

Run this once after the containers are up:

```bash
curl http://<EC2_PUBLIC_IP>:5000/generate-data
```

Then verify:

```bash
curl http://<EC2_PUBLIC_IP>:5000/sales-summary
curl http://<EC2_PUBLIC_IP>:5001/predict
curl http://<EC2_PUBLIC_IP>:5002/recommend/1
```

## 6. Frontend

The current `frontend/index.html` is still hardcoded to Render URLs, so it will not point to your EC2 APIs until you replace those URLs with your EC2 public IP or a domain.

Replace:

- `https://ml-ecommerce-devops.onrender.com` -> `http://<EC2_PUBLIC_IP>:5000`
- `https://ml-ecommerce-devops-3.onrender.com` -> `http://<EC2_PUBLIC_IP>:5002`
- `https://ml-ecommerce-devops-4.onrender.com` -> `http://<EC2_PUBLIC_IP>:5001`

For a cleaner setup, put Nginx in front and serve the frontend on port `80`.

## 7. Basic operations

```bash
docker compose -f docker-compose.ec2.yml logs -f
docker compose -f docker-compose.ec2.yml restart
docker compose -f docker-compose.ec2.yml down
```

## Notes

- The first boot can take a few minutes because the Python images install scientific packages.
- `host.docker.internal` was removed from the runtime path for EC2 compatibility.
- PostgreSQL credentials in `docker-compose.ec2.yml` are demo defaults and should be changed before any real exposure.
