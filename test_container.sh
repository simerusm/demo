#!/bin/bash
# test_container.sh - Test script for gVisor container functionality

echo "🧪 Container Test Script Starting..."
echo "=================================="

# Basic system info
echo "📋 System Information:"
echo "  Date: $(date)"
echo "  Hostname: $(hostname)"
echo "  User: $(whoami) (UID: $(id -u))"
echo "  Working Directory: $(pwd)"
echo "  Shell: $SHELL"

# Environment variables
echo ""
echo "🌍 Environment Variables:"
echo "  USER_ID: ${USER_ID:-'Not set'}"
echo "  WORKFLOW_ID: ${WORKFLOW_ID:-'Not set'}"
echo "  HOME: $HOME"
echo "  PATH: $PATH"

# System resources
echo ""
echo "📊 System Resources:"
echo "  Memory: $(free -h | grep Mem | awk '{print $3"/"$2" used"}')"
echo "  Disk Usage: $(df -h . | tail -1 | awk '{print $3"/"$2" used ("$5" full)"}')"
echo "  Load Average: $(uptime | awk -F'load average:' '{print $2}')"

# Available tools
echo ""
echo "🛠️  Available Tools:"
command -v python3 >/dev/null && echo "  ✅ Python: $(python3 --version)" || echo "  ❌ Python not found"
command -v git >/dev/null && echo "  ✅ Git: $(git --version)" || echo "  ❌ Git not found"
command -v aws >/dev/null && echo "  ✅ AWS CLI: $(aws --version 2>&1 | head -1)" || echo "  ❌ AWS CLI not found"
command -v kubectl >/dev/null && echo "  ✅ kubectl: $(kubectl version --client --short 2>/dev/null)" || echo "  ❌ kubectl not found"
command -v curl >/dev/null && echo "  ✅ curl: $(curl --version | head -1)" || echo "  ❌ curl not found"

# Directory contents
echo ""
echo "📁 Current Directory Contents:"
ls -la

# Git status (if in git repo)
echo ""
echo "🔄 Git Status:"
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "  Repository: $(git remote get-url origin 2>/dev/null || echo 'No remote')"
    echo "  Branch: $(git branch --show-current 2>/dev/null || echo 'No branch')"
    echo "  Status: $(git status --porcelain | wc -l) modified files"
    echo "  Last commit: $(git log -1 --pretty=format:'%h - %s (%cr)' 2>/dev/null || echo 'No commits')"
else
    echo "  Not a git repository"
fi

# Create test file
echo ""
echo "📝 File Operations Test:"
echo "Creating test file..."
echo "Hello from gVisor container at $(date)" > test_output.txt
echo "Container test successful!" >> test_output.txt
echo "  ✅ Created test_output.txt"
echo "  Content: $(cat test_output.txt)"

# Python test
echo ""
echo "🐍 Python Test:"
python3 -c "
import sys
import os
import platform
print(f'  Python version: {sys.version.split()[0]}')
print(f'  Platform: {platform.platform()}')
print(f'  Current working directory: {os.getcwd()}')
print(f'  Python executable: {sys.executable}')
"

# Network test
echo ""
echo "🌐 Network Test:"
if curl -s --max-time 5 https://httpbin.org/ip >/dev/null 2>&1; then
    echo "  ✅ Internet connectivity: OK"
    IP_INFO=$(curl -s --max-time 3 https://httpbin.org/ip | grep -o '"origin": "[^"]*' | cut -d'"' -f4)
    echo "  Public IP: ${IP_INFO:-'Unknown'}"
else
    echo "  ❌ Internet connectivity: Failed"
fi

# Performance test
echo ""
echo "⚡ Performance Test:"
echo "  CPU test (calculating primes)..."
START_TIME=$(date +%s.%N)
python3 -c "
count = 0
for num in range(2, 1000):
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            break
    else:
        count += 1
print(f'  Found {count} prime numbers under 1000')
"
END_TIME=$(date +%s.%N)
DURATION=$(python3 -c "print(f'{float('$END_TIME') - float('$START_TIME'):.2f}')")
echo "  Execution time: ${DURATION}s"

echo ""
echo "✅ Container test completed successfully!"
echo "=================================="
