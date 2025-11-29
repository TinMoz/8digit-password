# 8-Digit Number Generator

A Python script that creates and stores 8-digit numeric strings using SQLite.

## Requirements
- Python 3.x

## Setup
- Install deps: `pip install -r requirements.txt`
- Configure DB access:
  - Preferred: set `DB_URL` as an environment variable on the remote config server (default host `p01--eightdigit--vnwzhrpwlmrg.code.run`). The app will fetch it automatically.
  - Local override (optional): set `DB_URL` in `.env`, e.g. `DB_URL=mysql+pymysql://<user>:<password>@<host>:<port>/<database>`. You can also override the config host with `REMOTE_ENV_HOST`.

## Usage
- Interactively view or generate: `python src/A.py`
  - Behavior: loads `.env`, prompts for action (1 = view latest 5 numbers, 2 = generate/store a new 8-digit number and then show latest 5), keeps only the latest 10 stored numbers, then waits for Enter before exit.
- View the latest unseen number once, then auto-close after 5 seconds: `python src/b.py` (re-run shows nothing until A.py creates a new number)

## Docker
- Build the image: `docker build -t random-number-app .`
- Run with your `.env` for DB connection: `docker run --rm --env-file .env random-number-app`
  - Default command runs `python src/A.py`; override with `docker run --rm --env-file .env random-number-app python src/b.py` to use `b.py`.

## Testing
- Run unit tests: `python -m unittest discover -s tests -t . -p *_tests.py`

## Notes
- Defaults to 8 digits via `DEFAULT_LENGTH`; call `generate_random_digits(length)` from `lib.random_digits` for a different length.
- History is stored locally via SQLite; remove the `data/` folder to clear it.
