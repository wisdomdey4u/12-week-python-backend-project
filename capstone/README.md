# Learning Hub API — first vertical slice

Learning Hub is the capstone for this curriculum: a multi-tenant learning and
workspace API that will grow to include an AI assistant and MLOps practices.
This first milestone focuses on the backend foundations and a working,
workspace-scoped resource flow.

## What works now

- Register an account and log in for a short-lived bearer token.
- Create a workspace; its creator becomes its owner.
- Save and list links/resources inside a workspace.
- Enforce workspace membership before returning workspace data.
- Run the API and automated tests locally with SQLite.

## Run locally (PowerShell)

From this `capstone` directory:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
# Edit .env and replace the development JWT secret before starting the API.
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs> for the interactive API. The default database
is `learning_hub.db` in the current directory. The secret shown above is for
local development only; use a managed secret and a strong, unique key for any
deployed environment.

Run the test suite from this directory:

```powershell
pytest
```

## Try the main flow

Use the interactive docs or an HTTP client:

1. `POST /auth/register`
   ```json
   {"email": "learner@example.com", "password": "a-long-example-passphrase"}
   ```
2. `POST /auth/login` with the same JSON and copy `access_token`.
3. Click **Authorize** and enter the access-token value. Swagger UI adds the
   `Bearer` prefix.
4. `POST /workspaces` with `{"name": "Backend learning"}`.
5. `POST /workspaces/{workspace_id}/resources`:
   ```json
   {
     "title": "FastAPI documentation",
     "url": "https://fastapi.tiangolo.com/",
     "notes": "Review dependency injection."
   }
   ```
6. `GET /workspaces/{workspace_id}/resources` to retrieve saved resources.

An authenticated user who is not a member receives `404` for another
workspace's resources. The API does not accept a client-supplied owner ID; the
identity comes from the signed token and membership is checked on every
workspace request.

## First learning notes

### Why start with a vertical slice?

A thin end-to-end path teaches more than a large set of disconnected models:
the request is validated, the user is authenticated, the workspace boundary is
checked, and the result is persisted. Tests can then protect that behavior as
we add features.

### Why store membership separately?

A resource belongs to a workspace, not directly to a user. A membership table
connects users to workspaces and gives the next milestone a place to add roles
and invitations. Every resource query is scoped to a workspace after membership
has been verified.

### What is not solved yet?

This is not production-ready authentication or deployment. It does not yet
include refresh tokens, email verification, rate limiting, database migrations,
workspace invitations, or a production secrets manager. The development
database creates tables at startup; schema evolution will move to migrations in
a later milestone. Do not expose this starter configuration as a production
service.

## Next milestones

1. Improve CRUD and workspace membership/roles.
2. Add migrations, PostgreSQL configuration, and CI.
3. Add a provider-neutral AI assistant with explicit data boundaries.
4. Evaluate AI behavior, add observability, and build deployment/MLOps workflows.

The precise week-by-week mapping will be kept aligned with the curriculum PDF
as each topic is taken on.
