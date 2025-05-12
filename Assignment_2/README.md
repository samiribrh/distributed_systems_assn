# Assignment 2 - Distributed Systems

## Services

### Authentication Service
Handles user login and token management. Token includes user role. Roles: Administrator, Secretary, Agent.

### Transaction Service
Allows import, update and result retrieval of transactions. Access only for Administrator and Agent.

## Usage

- Run both services separately with FastAPI
- Authentication tokens must be used in the `Authorization` header for accessing Transaction endpoints.

## Tech Stack

- FastAPI
- SQLite
- In-memory session handling
- Role-based access
