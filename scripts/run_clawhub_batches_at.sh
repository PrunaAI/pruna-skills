#!/usr/bin/env bash
# Wrapper for at(1) / cron — runs remaining ClawHub batches with logging.
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"
exec ./scripts/publish_clawhub_batches.sh >>"${REPO_ROOT}/output/clawhub-publish-batch.log" 2>&1
