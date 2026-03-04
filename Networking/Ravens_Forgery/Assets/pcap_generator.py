#!/usr/bin/env python3
"""
CTF Challenge Generator: "Raven's Forgery"
Teaches ICMP spoofing — because ICMP has no authentication, a sender's
source IP cannot be trusted. The flag is hidden in ICMP echo-reply packets
that claim to originate from a "trusted" internal address (10.0.0.1),
but are injected by an attacker machine identifiable only by a TTL anomaly.

Actors:
  VICTIM    192.168.1.10   — machine being pinged
  GATEWAY   10.0.0.1       — trusted server (spoofed source)
  ATTACKER  192.168.1.66   — real sender, betrayed by TTL

The smoking gun: legitimate replies from 10.0.0.1 have TTL=128 (Windows).
                 Spoofed replies have TTL=53 (Linux box, ~11 hops away).

Run as root: sudo python3 pcap_generator.py
Output: raven.pcap
"""

from scapy.all import IP, ICMP, Raw, wrpcap
import random
import string

# ── Config ────────────────────────────────────────────────────────────────────
VICTIM_IP   = "192.168.1.10"
GATEWAY_IP  = "10.0.0.1"       # spoofed source
LEGIT_TTL   = 128               # Windows server — legitimate replies
SPOOFED_TTL = 53                # attacker Linux box after routing hops
FLAG        = "FLAME{sp00fed_s0urc3_f$lse_r4v3n}"
# ─────────────────────────────────────────────────────────────────────────────

def rand_payload(n=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n)).encode()

packets = []

# 1. Legitimate echo requests: victim → gateway
for i in range(30):
    packets.append(
        IP(src=VICTIM_IP, dst=GATEWAY_IP, ttl=random.randint(120, 128)) /
        ICMP(type=8, code=0, id=0xAAAA, seq=i) /
        Raw(load=rand_payload())
    )

# 2. Legitimate echo replies: gateway → victim (normal TTL=128)
for i in range(30):
    packets.append(
        IP(src=GATEWAY_IP, dst=VICTIM_IP, ttl=LEGIT_TTL) /
        ICMP(type=0, code=0, id=0xAAAA, seq=i) /
        Raw(load=rand_payload())
    )

# 3. SPOOFED replies: src=gateway but TTL=53 betrays the attacker.
#    Flag split one char per packet. ICMP id=0xDEAD marks this series.
flag_pkts = []
for i, ch in enumerate(FLAG):
    flag_pkts.append(
        IP(src=GATEWAY_IP, dst=VICTIM_IP, ttl=SPOOFED_TTL) /
        ICMP(type=0, code=0, id=0xDEAD, seq=i) /
        Raw(load=ch.encode())
    )

# 4. Decoy spoofed packets (junk payload, anomalous TTL, random id)
for i in range(10):
    packets.append(
        IP(src=GATEWAY_IP, dst=VICTIM_IP, ttl=SPOOFED_TTL) /
        ICMP(type=0, code=0, id=random.randint(0x1000, 0xDEAC), seq=i) /
        Raw(load=rand_payload(8))
    )

# Scatter flag packets throughout the noise
random.shuffle(packets)
positions = sorted(random.sample(range(len(packets) + len(flag_pkts)), len(flag_pkts)))
for offset, pos in enumerate(positions):
    packets.insert(pos, flag_pkts[offset])

wrpcap("raven.pcap", packets)
print(f"[+] Flag:    {FLAG}")
print(f"[+] Total packets: {len(packets)}  ({len(flag_pkts)} carry the flag)")
print(f"[+] Written to raven.pcap")
print(f"\n[!] Spoofed packets: src={GATEWAY_IP}, TTL={SPOOFED_TTL}, ICMP id=0xDEAD")
print(f"[!] Legit    packets: src={GATEWAY_IP}, TTL={LEGIT_TTL},  ICMP id=0xAAAA")