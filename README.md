# Assignment Five — WorldOfCodes REST API

Python, FastAPI and Pydantic power three workflows for a coding academy.

- Players create and edit profiles. Only the owner can edit or delete a profile.
- Learners complete lessons in prerequisite order. Each completion awards XP once.
- Players submit answers to problems. The first correct answer awards XP and coins.

The service stores related records in memory. Restarting it restores the seed data.
Protected operations use the demo actor header `X-User-Id`.

## Run

From this repository, run:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --reload
```

Open [Swagger UI](http://127.0.0.1:8000/docs). Select an operation, click **Try it out**, enter its parameters and click **Execute**.
For example, submit `{"lesson_id":2}` to `POST /api/users/1/progress` with `X-User-Id: 1`. On a fresh server the first request returns 201, a duplicate returns 409 and using actor 2 returns 403.

## Tests

```sh
.venv/bin/python -m pytest -q
```

Routes are in `routers/`, request and response models in `schemas.py`, business rules in `services.py`, and seeded storage in `storage.py`.
