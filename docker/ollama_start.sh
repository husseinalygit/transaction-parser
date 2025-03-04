#!/bin/sh
ollama serve &
sleep 10
if [ -n "$OLLAMA_MODEL" ]; then
    echo "Pulling model: $OLLAMA_MODEL"
    ollama pull $OLLAMA_MODEL
else
    echo "No model specified in OLLAMA_MODEL environment variable"
    exit 1
fi
wait

