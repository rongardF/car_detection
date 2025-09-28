# Database version control system

This repository uses Alembic to manage database changes. For detailed usage instructions see https://alembic.sqlalchemy.org/.

### Creating a migration script

Run command below to create the python file that will contain your changes:
```
alembic revision -m "<Short phrase to describe the changes you will implement>"
```

You will find new file in [versions folder,](versions) and you will implement your changes in the `upgrade` method.

# TODO: change this behaviour if applicable, but be careful about deleting structures unintentionally
Note that we won't implement rollback logic inside the `downgrade` method to avoid situations where data can be lost.
We must ensure backwards compatibility at service level, so we can roll back only the python code in case of incidents.
