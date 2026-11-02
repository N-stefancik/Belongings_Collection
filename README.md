# Belongings_Collection

An early-stage **digital library of physical possessions**. The initial version is a local REST API for creating, organizing with basic category labels, and maintaining possession records. This is a starter project, not a deployed multi-user service.

## Included in milestone 1

- Python 3.12+ / FastAPI HTTP API
- SQLite persistence via SQLAlchemy 2.x
- Pydantic request and response validation
- UUID identifiers and creation/update timestamps
- Flexible JSON custom attributes
- Create, list, retrieve, update, and delete endpoints
- Basic `limit`/`offset` pagination
- Automated API tests using temporary SQLite databases

**Not implemented:** a web UI, accounts/authentication, image uploads, collections/locations, 3D generation, recognition, valuation, cloud deployment.

## Open in VS Code

1. Unzip the downloaded archive.
2. Open VS Code, select **File > Open Folder**, and choose `Belongings_Collection`.
3. Open the integrated terminal (**Terminal > New Terminal**).
4. Install Python 3.12 or later if necessary. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

5. Activate it:

   - macOS/Linux: `source .venv/bin/activate`
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - Windows Command Prompt: `.venv\Scripts\activate.bat`

6. Install dependencies:

   ```bash
   python -m pip install -e ".[dev]"
   ```

7. Start the API:

   ```bash
   python -m uvicorn app.main:app --reload
   ```

8. Open **http://127.0.0.1:8000/docs** to use the automatically generated interactive Swagger UI.

Alternatively, use the included VS Code debug launch configuration (Run and Debug > **Run Belongings API**). On Windows, select `.venv\Scripts\python.exe` as the interpreter in VS Code. The default interpreter path in `.vscode/settings.json` is for macOS/Linux.

## Run the tests

With the virtual environment activated:

```bash
python -m pytest -v
```

Tests use fresh temporary databases rather than the development database.

## API

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/possessions` | Create a possession |
| GET | `/possessions?limit=50&offset=0` | List possessions |
| GET | `/possessions/{id}` | Read possession |
| PATCH | `/possessions/{id}` | Partial update |
| DELETE | `/possessions/{id}` | Delete possession |

Example JSON for **POST /possessions**:

```json
{
  "name": "Fender Stratocaster",
  "description": "My first electric guitar",
  "category": "Instruments",
  "attributes": {"color": "Sunburst", "year": 2018}
}
```

Responses include `id`, `created_at`, and `updated_at`. `id` is a UUID. Names must be nonblank. The `attributes` field accepts a JSON object; keys are not standardized at this stage. `PATCH` only changes supplied fields; supplying a full `attributes` object replaces the previous object.

## Project structure

```text
Belongings_Collection/
├── .vscode/              # Recommended extensions and debug configuration
├── app/
│   ├── main.py           # FastAPI application, initial table creation, health endpoint
│   ├── database.py       # SQLAlchemy engine and sessions
│   ├── models/           # Persisted ORM models
│   ├── schemas/          # Pydantic request/response contracts
│   └── routers/          # HTTP endpoints
├── tests/                # Isolated API tests
├── pyproject.toml        # Package dependencies / pytest config
├── .gitignore
└── README.md
```

## Design choices and limitations

- **SQLite:** simple for a single local developer. Later consider PostgreSQL for concurrent multi-user use.
- **No authentication:** do **not** expose this API to the public internet or use it for real multi-user data.
- **Basic category string:** does not yet implement category entities, spaces, or collections.
- **JSON custom attributes:** flexible for heterogeneous objects, but category-specific validation and indexed search are deferred.
- **Table creation on startup:** suitable for an empty prototype only; add Alembic migrations before evolving a database that contains important data. `create_all()` does not update existing tables.
- **SQLite timestamp storage:** timestamps are produced in UTC, but SQLite's default date-time storage does not retain timezone offsets. Normalize to UTC when exposing dates to clients in a production implementation.
- **Local database path:** by default, `belongings.db` is created in the directory from which you run the server. Set the `DATABASE_URL` environment variable to override it.
- **No media:** photograph storage and 3D assets will be added later as separate related entities.

## Next milestone

Introduce multiple images per possession and explicit organization into locations, categories, and collections, with tests for file validation and record relationships. Do not build 3D reconstruction until the image model and storage workflow are stable.
