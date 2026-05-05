#!/bin/bash

echo "Waiting for WireGuard handshake..."

while true; do
    HANDSHAKE=$(wg show wg0 latest-handshakes | awk '{print $2}')

    if [ -n "$HANDSHAKE" ] && [ "$HANDSHAKE" -gt 0 ]; then
        echo "WireGuard tunnel is up!"
        break
    fi

    echo "No handshake yet, retryig in 5s..."
    sleep 5
done

