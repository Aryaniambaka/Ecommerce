# Ecommerce API

A backend Ecommerce REST API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. The project includes user authentication, product management, cart functionality, order processing, database migrations, Docker support, and CI/CD with GitHub Actions.
## Infrastructure Note

This project was previously deployed on an Azure Virtual Machine using GitHub Actions for automated CI/CD. To avoid recurring cloud costs after development, the VM was intentionally decommissioned. The deployment configuration and CI/CD pipeline are still included in the repository and can be reused by provisioning a new server and updating the deployment secrets.

## Features

- JWT Authentication
- User & Seller APIs
- Product Management
- Shopping Cart
- Order Processing
- PostgreSQL Database
- Alembic Migrations
- Docker & Docker Compose
- Automated Testing with Pytest
- CI/CD using GitHub Actions

## Tech Stack

- FastAPI
- Python
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- GitHub Actions

## Installation

```bash
git clone https://github.com/Aryaniambaka/Ecommerce.git
cd Ecommerce
pip install -r requirement.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

## Docker

```bash
docker-compose up --build
```

## Testing

```bash
pytest
```

## Project Structure

```
app/
alembic/
test/
Dockerfile
docker-compose.yml
.github/workflows/
```

## License

This project is for learning and educational purposes.
<img width="810" height="858" alt="image" src="https://github.com/user-attachments/assets/deb5f645-21ae-4161-8cc2-56b1d982b112" />
<img width="810" height="324" alt="image" src="https://github.com/user-attachments/assets/ab37c43e-e262-46a0-abfd-fe959c9790ed" />
<img width="536" height="950" alt="HabitForge_dev - public" src="https://github.com/user-attachments/assets/d0386172-6671-405e-8296-cb428c5d64d8" />



