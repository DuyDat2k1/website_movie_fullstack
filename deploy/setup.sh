#!/bin/bash
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$(dirname "$DIR")"

echo "=== Deploy Web Movie (Cloudflare Tunnel) ==="
echo "Project: $PROJECT"

echo "[1/4] Cấu hình Nginx..."
sudo cp "$DIR/nginx-movie.conf" /etc/nginx/sites-available/movie
sudo ln -sf /etc/nginx/sites-available/movie /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
echo "OK"

echo "[2/4] Cài đặt Gunicorn systemd service..."
sudo cp "$DIR/movie.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable movie
sudo systemctl restart movie
echo "OK"

echo "[3/4] Collect static files..."
cd "$PROJECT"
source venv/bin/activate
python manage.py collectstatic --noinput
echo "OK"

echo "[4/4] Kiểm tra..."
sudo systemctl status movie --no-pager | head -10
echo "OK"
echo "---"
echo "Cloudflare Tunnel sẽ chạy tự động qua systemd user service."
echo "Chạy lệnh sau để xem URL tunnel: journalctl --user -u cloudflared-tunnel -n 20 | grep -oP 'https://[a-zA-Z0-9-]+\.trycloudflare\.com'"
