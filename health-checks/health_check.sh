#!/bin/bash

# Application Support Toolkit
# Service Health Check
#
# Checks the availability and response time of a web service.

URL="${1:-https://example.com}"

echo "======================================"
echo "       SERVICE HEALTH CHECK"
echo "======================================"
echo "Target: $URL"
echo "Time:   $(date)"
echo "--------------------------------------"

# Check HTTP status and response time
RESULT=$(curl -o /dev/null -s -w "%{http_code} %{time_total}" \
    --connect-timeout 10 \
    --max-time 30 \
    "$URL")

HTTP_STATUS=$(echo "$RESULT" | awk '{print $1}')
RESPONSE_TIME=$(echo "$RESULT" | awk '{print $2}')

echo "HTTP Status:    $HTTP_STATUS"
echo "Response Time:  ${RESPONSE_TIME}s"

echo "--------------------------------------"

if [[ "$HTTP_STATUS" =~ ^2[0-9][0-9]$ ]]; then
    echo "STATUS: HEALTHY"
    exit 0

elif [[ "$HTTP_STATUS" =~ ^3[0-9][0-9]$ ]]; then
    echo "STATUS: REDIRECT"
    exit 0

elif [[ "$HTTP_STATUS" == "000" ]]; then
    echo "STATUS: UNREACHABLE"
    echo "Possible network, DNS, SSL, or connection issue."
    exit 1

else
    echo "STATUS: UNHEALTHY"
    echo "HTTP service returned status $HTTP_STATUS."
    exit 1
fi
