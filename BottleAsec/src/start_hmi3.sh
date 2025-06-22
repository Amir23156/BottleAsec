#!/bin/bash

# Wrapper to launch HMI3 with optional office network bridge
if [ "$WIFI_BRIDGE_ENABLED" = "false" ]; then
    echo "WIFI_BRIDGE_ENABLED=false - disabling office network interface"
    if ip link show eth1 >/dev/null 2>&1; then
        ip link set eth1 down
        iptables -A INPUT -i eth1 -j DROP
        iptables -A OUTPUT -o eth1 -j DROP
    fi
fi

./start.sh HMI3.py
