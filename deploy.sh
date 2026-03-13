#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Load config
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "Error: .env file not found"
    exit 1
fi
source "$SCRIPT_DIR/.env"

SSH="ssh -i $SSH_KEY $EC2_USER@$EC2_HOST"
SCP="scp -i $SSH_KEY"

echo "Deploying to $EC2_HOST..."

# Copy app files
$SCP "$SCRIPT_DIR/app.py" "$SCRIPT_DIR/resume_generator.py" "$EC2_USER@$EC2_HOST:~/"

# Restart the service
$SSH "sudo systemctl restart resume"

echo "Deploy complete. App running at http://$EC2_HOST"
