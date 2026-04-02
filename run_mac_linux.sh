#!/bin/bash
echo ""
echo " ============================================="
echo "  LearnVest - Gamified Financial Literacy App"
echo "  Learn Money. Play Smart. Build Wealth."
echo " ============================================="
echo ""

echo "[1/3] Checking Python..."
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python3 not found. Please install Python 3.8+"
    exit 1
fi
python3 --version

echo "[2/3] Installing dependencies..."
pip3 install flask --quiet

echo "[3/3] Launching LearnVest..."
echo ""
echo " App running at: http://localhost:5000"
echo " Press Ctrl+C to stop."
echo ""

# Auto-open browser
if command -v open &>/dev/null; then
    sleep 1.5 && open http://localhost:5000 &
elif command -v xdg-open &>/dev/null; then
    sleep 1.5 && xdg-open http://localhost:5000 &
fi

python3 app.py
