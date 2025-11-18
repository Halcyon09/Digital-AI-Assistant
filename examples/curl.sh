#!/bin/bash

API="http://localhost:8000/chat"

curl -X POST $API \
-H "Content-Type: application/json" \
-d '{
  "messages": [
    {"role": "system", "content": "Eres un asistente técnico."},
    {"role": "user", "content": "Explica qué es una API en 2 líneas."}
  ]
}'