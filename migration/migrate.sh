#!/usr/bin/env bash
set -e

echo "current env is dev"
ls
echo "Running migrations ..."
alembic upgrade head
