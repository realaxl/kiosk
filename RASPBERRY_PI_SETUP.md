# Raspberry Pi Auto-Update Setup

This guide explains how to set up automatic git monitoring and app restart on a Raspberry Pi.

## Files Created

1. **auto-update.sh** - Shell script that monitors git repository and restarts the app
2. **kiosk-auto-update.service** - Systemd service file to run the script on boot

## Installation Steps

### 1. Update the Configuration

Edit `auto-update.sh` and update the `REPO_DIR` variable to match your actual project path:

```bash
nano auto-update.sh
```

Change this line:
```bash
REPO_DIR="/home/pi/kiosk-with-bob"  # Change this to your actual project path
```

### 2. Make the Script Executable

```bash
chmod +x auto-update.sh
```

### 3. Test the Script Manually (Optional)

Before setting up the service, you can test the script:

```bash
./auto-update.sh
```

Press `Ctrl+C` to stop it.

### 4. Install the Systemd Service

Copy the service file to systemd directory:

```bash
sudo cp kiosk-auto-update.service /etc/systemd/system/
```

### 5. Update Service File Paths (if needed)

If your project is not in `/home/pi/kiosk-with-bob`, edit the service file:

```bash
sudo nano /etc/systemd/system/kiosk-auto-update.service
```

Update the `WorkingDirectory` and `ExecStart` paths.

### 6. Enable and Start the Service

```bash
# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable kiosk-auto-update.service

# Start the service now
sudo systemctl start kiosk-auto-update.service
```

## Managing the Service

### Check Service Status

```bash
sudo systemctl status kiosk-auto-update.service
```

### View Logs

```bash
# View systemd logs
sudo journalctl -u kiosk-auto-update.service -f

# View auto-update script logs
tail -f /tmp/kiosk-auto-update.log

# View Flask app logs
tail -f /tmp/kiosk-app.log
```

### Stop the Service

```bash
sudo systemctl stop kiosk-auto-update.service
```

### Restart the Service

```bash
sudo systemctl restart kiosk-auto-update.service
```

### Disable Auto-Start on Boot

```bash
sudo systemctl disable kiosk-auto-update.service
```

## How It Works

1. The script checks the git repository every 10 seconds
2. It compares the local commit hash with the remote `main` branch
3. If a new commit is detected:
   - Pulls the latest changes
   - Stops the running Flask app
   - Starts the Flask app with the new code
4. All actions are logged to `/tmp/kiosk-auto-update.log`

## Troubleshooting

### Service won't start

Check the logs:
```bash
sudo journalctl -u kiosk-auto-update.service -n 50
```

### App not restarting

Check if the PID file exists and is valid:
```bash
cat /tmp/kiosk-app.pid
ps -p $(cat /tmp/kiosk-app.pid)
```

### Git authentication issues

If your repository requires authentication, set up SSH keys:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
```

Add the public key to your GitHub/GitLab account.

### Check if virtual environment is activated

The script automatically activates `.venv` if it exists. Make sure your virtual environment is set up:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # if you have one
```

## Configuration Options

You can modify these variables in `auto-update.sh`:

- `REPO_DIR` - Path to your project directory
- `BRANCH` - Git branch to monitor (default: "main")
- `CHECK_INTERVAL` - Seconds between checks (default: 10)
- `APP_SCRIPT` - Path to Flask app script (default: "src/app.py")

## Security Notes

- The script runs as the `pi` user by default
- Make sure the `pi` user has read/write access to the project directory
- Consider using SSH keys instead of HTTPS for git authentication
- The Flask app runs on port 5000 by default - adjust firewall rules as needed