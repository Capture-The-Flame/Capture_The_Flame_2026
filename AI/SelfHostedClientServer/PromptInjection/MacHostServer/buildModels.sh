#!/bin/bash
# NOTE: Must be running `ollama serve` in order for ollama to pull the model
ollama create ctf-model-gpt -f ../GPT-OSS/Server/gptCTF
echo "successfully created GPT Flag Model!"
ollama create ctf-model-llama -f ../Llama/Server/llamaCTF
echo "successfully created Llama3 Flag Model!"
