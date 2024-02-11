#!/bin/bash
echo "Script executed from: ${PWD}"
cp .env.example .env
cp ./api/.env.example ./api/.env
cp ./consumer/.env.example ./consumer/.env
cp ./producer/.env.example ./producer/.env