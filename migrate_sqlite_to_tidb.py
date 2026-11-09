"""Safely copy portfolio.db (SQLite) into the configured TiDB Cloud database.

Run from the project directory:
    python migrate_sqlite_to_tidb.py

If the destination already contains data and you intentionally want to replace
matching portfolio tables:
    python migrate_sqlite_to_tidb.py --replace

The script preserves primary-key IDs and copies every matching table/row.
"""

import argparse
import os
from pathlib import Path

from flask import Flask
from sqlalchemy import create_engine, select, func

from config import config
from models import db


BASE_DIR = Path(__file__).resolve().parent
SQLITE_PATH = BASE_DIR / "portfolio.db"


def main():
    parser = argparse.ArgumentParser(description="Migrate SQLite data to TiDB Cloud")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="replace data in matching destination tables if they are not empty",
    )
    args = parser.parse_args()

    database_url = os.getenv("DATABASE_URL", "")
    if not database_url.startswith("mysql+pymysql://"):
        raise SystemExit(
            "DATABASE_URL must be a mysql+pymysql:// TiDB Cloud connection URL. "
            "Check your .env file."
        )
    if not SQLITE_PATH.is_file():
        raise SystemExit(f"SQLite source database not found: {SQLITE_PATH}")

    source_engine = create_engine(f"sqlite:///{SQLITE_PATH.as_posix()}")
    flask_app = Flask(__name__)
    environment = os.getenv("FLASK_ENV", "development")
    flask_app.config.from_object(config.get(environment, config["default"]))
    db.init_app(flask_app)

    try:
        with flask_app.app_context():
            target_engine = db.engine
            # Create schema only; intentionally do not call the app's seed_data().
            db.create_all()

            target_tables = list(db.metadata.sorted_tables)
            source_table_names = set()
            from sqlalchemy import MetaData
            source_metadata = MetaData()
            source_metadata.reflect(bind=source_engine)
            source_table_names = set(source_metadata.tables.keys())
            matching_tables = [t for t in target_tables if t.name in source_table_names]

            if not matching_tables:
                raise SystemExit("No matching tables found between SQLite and TiDB.")

            # Refuse to overwrite existing destination data unless explicitly allowed.
            existing_counts = {}
            with target_engine.connect() as connection:
                for table in matching_tables:
                    count = connection.execute(
                        select(func.count()).select_from(table)
                    ).scalar_one()
                    if count:
                        existing_counts[table.name] = count
            if existing_counts and not args.replace:
                details = ", ".join(f"{name}: {count}" for name, count in existing_counts.items())
                raise SystemExit(
                    "Destination tables already contain data (" + details + "). "
                    "Nothing was changed. If you intend to replace these tables, "
                    "back up TiDB first and rerun with --replace."
                )

            copied = {}
            with target_engine.begin() as target_connection:
                for target_table in matching_tables:
                    source_table = source_metadata.tables[target_table.name]
                    with source_engine.connect() as source_connection:
                        source_rows = source_connection.execute(
                            select(source_table)
                        ).mappings().all()

                    target_connection.execute(target_table.delete())
                    if source_rows:
                        payload = [
                            {
                                column.name: row[column.name]
                                for column in target_table.columns
                                if column.name in row
                            }
                            for row in source_rows
                        ]
                        target_connection.execute(target_table.insert(), payload)
                    copied[target_table.name] = len(source_rows)

            # Verify destination counts after commit.
            print("Migration completed. Verified row counts:")
            with target_engine.connect() as connection:
                for table in matching_tables:
                    actual = connection.execute(
                        select(func.count()).select_from(table)
                    ).scalar_one()
                    expected = copied[table.name]
                    status = "OK" if actual == expected else "MISMATCH"
                    print(f"  {table.name}: {actual}/{expected} [{status}]")
                    if actual != expected:
                        raise SystemExit(f"Row-count verification failed for {table.name}.")
            print("All matching SQLite tables were copied to TiDB Cloud.")
    finally:
        source_engine.dispose()


if __name__ == "__main__":
    main()
