# Ecommerce API

A backend Ecommerce REST API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. The project includes user authentication, product management, cart functionality, order processing, database migrations, Docker support, and CI/CD with GitHub Actions.

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
## Project Idea
```
https://roadmap.sh/projects/ecommerce-api
```
## License

This project is for learning and educational purposes.
