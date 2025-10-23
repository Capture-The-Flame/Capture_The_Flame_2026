#!/bin/bash
set -e

# wait a moment for docker networking to settle
sleep 1

# malicious MAC
MAL_MAC="02:42:ac:11:00:02"

# The "spoofed" IPs (one is the real flagserver, one is the fake gateway/steward)
SPF_IP1="172.28.0.2"   # flagserver (real service listening on 8000)
SPF_IP2="172.28.0.1"   # forged/masquerade address in the rolls

# A few normal/benign hosts to fill the table
DECOY1_IP="172.28.0.3"
DECOY1_MAC="02:42:ac:11:00:03"

DECOY2_IP="172.28.0.4"
DECOY2_MAC="02:42:ac:11:00:04"

DECOY3_IP="172.28.0.5"
DECOY3_MAC="02:42:ac:11:00:05"

# ---------- apply static entries ----------
# Map the two suspicious IPs to the same malicious MAC (static)
arp -s ${SPF_IP1} ${MAL_MAC} -i eth0 || true
arp -s ${SPF_IP2} ${MAL_MAC} -i eth0 || true

# Add some benign-looking ARP entries to create "noise"
arp -s ${DECOY1_IP} ${DECOY1_MAC} -i eth0 || true
arp -s ${DECOY2_IP} ${DECOY2_MAC} -i eth0 || true
arp -s ${DECOY3_IP} ${DECOY3_MAC} -i eth0 || true

# Print the ARP table for verification
echo "=== ARP table (pre-populated) ==="
# prefer arp -an if available, otherwise ip neigh
if command -v arp >/dev/null 2>&1; then
  arp -an
else
  ip neigh show dev eth0
fi

# Keep container interactive (drop to shell)
exec "$@"

