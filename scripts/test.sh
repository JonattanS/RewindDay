#!/usr/bin/env bash
curl -X POST http://localhost:8080/capsule/reconstruct -H "Content-Type: application/json" -d '{"text":"demo"}'
