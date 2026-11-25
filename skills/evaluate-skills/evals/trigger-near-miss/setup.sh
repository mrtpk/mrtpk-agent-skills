#!/usr/bin/env bash
set -e
mk() {
  mkdir -p "skills/$1"
  printf -- '---\nname: %s\ndescription: %s\n---\n\n# %s\n\nSee the description.\n' "$1" "$2" "$1" > "skills/$1/SKILL.md"
}
mk sql-review "Review SQL queries for correctness and performance. Use when the user asks to review, check or optimize a SQL query. Do not use it for schema migrations (sql-migrate) or for database documentation (db-schema-docs)."
mk sql-migrate "Write and check database schema migrations. Use when the user wants to add, change or remove tables, columns or indexes with a migration."
mk db-schema-docs "Write documentation for a database schema: tables, columns, relations. Use when the user asks to document a database."
