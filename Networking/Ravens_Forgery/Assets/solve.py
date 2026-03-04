#!/usr/bin/env python3
"""
CTF "The Raven's Forgery" — Solution Script

Step 1: Notice two flocks of ravens from 10.0.0.1 with different TTLs.
Step 2: The weary birds (TTL=53) carry id=0xDEAD and single-char payloads.
Step 3: Reassemble by ICMP sequence number.
"""

from scapy.all import rdpcap, IP, ICMP, ARP, TCP, UDP, DNS, Raw
from collections import Counter

pcap = rdpcap("raven.pcap")

print("=== Protocol breakdown ===")
protos = Counter()
for p in pcap:
    if p.haslayer(ARP):   protos["ARP"] += 1
    elif p.haslayer(DNS):  protos["DNS"] += 1
    elif p.haslayer(TCP):  protos["TCP"] += 1
    elif p.haslayer(ICMP): protos["ICMP"] += 1
    else:                  protos["Other"] += 1
for k, v in protos.most_common():
    print(f"  {k:<8} {v}")

print("\n=== ICMP reply TTL distribution (src=10.0.0.1) ===")
ttls = Counter()
for p in pcap:
    if p.haslayer(IP) and p.haslayer(ICMP) and p[ICMP].type == 0:
        if p[IP].src == "10.0.0.1":
            ttls[p[IP].ttl] += 1
for ttl, count in sorted(ttls.items()):
    marker = " ← ANOMALY — these birds flew too far" if ttl != 128 else ""
    print(f"  TTL={ttl}: {count} packets{marker}")

print("\n=== Intercepting the spy's ravens (TTL=53, id=0xDEAD) ===")
secret = {}
for p in pcap:
    if (p.haslayer(IP) and p.haslayer(ICMP) and p.haslayer(Raw)
            and p[IP].src == "10.0.0.1"
            and p[IP].ttl == 53
            and p[ICMP].id == 0xDEAD):
        secret[p[ICMP].seq] = p[Raw].load.decode()

flag = ''.join(secret[k] for k in sorted(secret))
print(f"[+] The message reads: {flag}")
