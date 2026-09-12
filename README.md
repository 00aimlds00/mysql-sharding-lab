# MySQL Database Sharding Lab

## Overview

This project demonstrates hash-based database sharding using:

- MySQL 8.0
- Docker
- Python
- PowerShell

## Architecture

5 MySQL shards running in Docker containers.

Routing formula:

```python
user_id % 5
```

## Technology Stack

- Windows 11
- Docker Desktop
- MySQL 8.0
- Python 3.x
- VS Code

## Shard Mapping

| Shard | Port |
|--------|--------|
| Shard 0 | 3310 |
| Shard 1 | 3311 |
| Shard 2 | 3307 |
| Shard 3 | 3308 |
| Shard 4 | 3309 |

## Results

- 10,000 users inserted
- Even 20% distribution across shards
- Deterministic routing
- Physical data isolation verified

## Example

```text
2080 → Shard 0
2081 → Shard 1
2082 → Shard 2
2083 → Shard 3
2084 → Shard 4
```

## Project Structure

```text
mysql-sharding-lab
│
├── docker-compose.yml
├── init_shard.sql
├── shard_router.py
│
└── scripts
    ├── seed_data.py
    └── verify_distribution.py
```

## Key Learnings

- Database Sharding
- Docker Volumes
- Environment Variables
- Distributed Database Design
- Hash-Based Routing
