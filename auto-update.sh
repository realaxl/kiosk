#!/bin/bash

# Auto-update script for Raspberry Pi
# Checks git repository every 10 seconds for new commits on main branch
# Pulls changes and restarts the Flask app if updates are found

# Configuration
REPO_DIR="/home/pi/kiosk-with-bob"  # Change this to your actual project path
BRANCH="main"
CHECK_INTERVAL=10
APP_SCRIPT="src/app.py"
PID_FILE="/tmp/kiosk-app.pid"
LOG_FILE="/tmp/kiosk-auto-update.log"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to start the Flask app
start_app() {
    log "Starting Flask app..."
    cd "$REPO_DIR" || exit 1
    
    # Activate virtual environment if it exists
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
    
    # Start the app in background and save PID
    python "$APP_SCRIPT" > /tmp/kiosk-app.log 2>&1 &
    echo $! > "$PID_FILE"
    log "Flask app started with PID $(cat $PID_FILE)"
}

# Function to stop the Flask app
stop_app() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            log "Stopping Flask app (PID: $PID)..."
            kill "$PID"
            sleep 2
            
            # Force kill if still running
            if ps -p "$PID" > /dev/null 2>&1; then
                log "Force killing Flask app..."
                kill -9 "$PID"
            fi
        fi
        rm -f "$PID_FILE"
    fi
}

# Function to restart the Flask app
restart_app() {
    log "Restarting Flask app..."
    stop_app
    start_app
}

# Change to repository directory
cd "$REPO_DIR" || {
    log "ERROR: Repository directory not found: $REPO_DIR"
    exit 1
}

# Start the app initially
start_app

log "Auto-update script started. Monitoring branch '$BRANCH' every $CHECK_INTERVAL seconds..."

# Main loop
while true; do
    # Fetch latest changes from remote
    git fetch origin "$BRANCH" > /dev/null 2>&1
    
    # Get local and remote commit hashes
    LOCAL_COMMIT=$(git rev-parse HEAD)
    REMOTE_COMMIT=$(git rev-parse origin/"$BRANCH")
    
    # Check if there are new commits
    if [ "$LOCAL_COMMIT" != "$REMOTE_COMMIT" ]; then
        log "New commit detected on $BRANCH branch"
        log "Local:  $LOCAL_COMMIT"
        log "Remote: $REMOTE_COMMIT"
        
        # Pull the changes
        log "Pulling changes..."
        git pull origin "$BRANCH"
        
        if [ $? -eq 0 ]; then
            log "Pull successful. Restarting app..."
            restart_app
            log "Update complete!"
        else
            log "ERROR: Git pull failed"
        fi
    fi
    
    # Wait before next check
    sleep "$CHECK_INTERVAL"
done

# Made with Bob
