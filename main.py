# main.py
# Week 7 – Store Logs in SQLite
# Requirements: psutil (pip install psutil)

import sqlite3
import psutil
import subprocess
import datetime
import time
import platform
from pathlib import Path


DB_PATH = Path("log.db")
TABLE_NAME = "system_log"
PING_HOST = "google.com"  # 需要的話可改成你的目標主機
SAMPLES = 5               # 紀錄次數
INTERVAL_SEC = 10         # 每次間隔秒數


def init_db():
    """Create SQLite database and table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu REAL NOT NULL,
            memory REAL NOT NULL,
            disk REAL NOT NULL,
            ping_status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def ping_status(host: str = PING_HOST, timeout_sec: int = 3) -> str:
    """
    Return 'UP' if ping 1 packet succeeds, else 'DOWN'.
    Cross-platform: Windows uses -n, Unix-like uses -c.
    """
    system = platform.system().lower()
    count_flag = "-n" if system == "windows" else "-c"
    cmd = ["ping", count_flag, "1", host]

    try:
        # 若無 ping 指令、逾時或非 0 return code，皆視為 DOWN
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout_sec,
            check=True,
        )
        return "UP"
    except Exception:
        return "DOWN"


def get_system_info():
    """Collect timestamp, cpu%, memory%, disk%, and ping status."""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=0.5)  # 輕量取樣以更穩定
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    pstat = ping_status()
    return (ts, cpu, memory, disk, pstat)


def insert_log(entry):
    """Insert one log row into SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        f"""INSERT INTO {TABLE_NAME}
            (timestamp, cpu, memory, disk, ping_status)
            VALUES (?, ?, ?, ?, ?)""",
        entry,
    )
    conn.commit()
    conn.close()


def show_last_logs(limit: int = 5):
    """Print the last N rows in reverse chronological order."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        f"""SELECT id, timestamp, cpu, memory, disk, ping_status
            FROM {TABLE_NAME}
            ORDER BY id DESC
            LIMIT ?""",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()

    print("\n=== Last", limit, "entries ===")
    if not rows:
        print("(No data)")
        return

    for r in rows:
        _id, ts, cpu, mem, disk, pstat = r
        print(
            f"#{_id:>4} | {ts} | CPU {cpu:5.1f}% | MEM {mem:5.1f}% | "
            f"DISK {disk:5.1f}% | PING {pstat}"
        )


def show_failed_pings():
    """Bonus: show rows where ping failed."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        f"""SELECT id, timestamp, cpu, memory, disk, ping_status
            FROM {TABLE_NAME}
            WHERE ping_status = 'DOWN'
            ORDER BY id DESC"""
    )
    rows = cur.fetchall()
    conn.close()

    print("\n=== Failed pings (DOWN) ===")
    if not rows:
        print("(None)")
        return
    for r in rows:
        _id, ts, cpu, mem, disk, pstat = r
        print(
            f"#{_id:>4} | {ts} | CPU {cpu:5.1f}% | MEM {mem:5.1f}% | "
            f"DISK {disk:5.1f}% | PING {pstat}"
        )


def main():
    print("Initializing database...")
    init_db()

    print(f"Collecting {SAMPLES} samples every {INTERVAL_SEC} seconds...")
    for i in range(SAMPLES):
        entry = get_system_info()
        insert_log(entry)
        print(
            f"[{i+1}/{SAMPLES}] Logged at {entry[0]} | "
            f"CPU {entry[1]:.1f}% MEM {entry[2]:.1f}% DISK {entry[3]:.1f}% PING {entry[4]}"
        )
        if i < SAMPLES - 1:
            time.sleep(INTERVAL_SEC)

    show_last_logs(limit=5)
    # Bonus（需要就解除註解）
    # show_failed_pings()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting…")
