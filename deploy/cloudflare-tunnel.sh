#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
nohup cloudflared tunnel --url http://localhost:80 > /tmp/cloudflared.log 2>&1 &
echo $! > /tmp/cloudflared.pid
sleep 5
cat /tmp/cloudflared.log | grep -oP 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' | head -1
