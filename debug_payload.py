import json
import psutil
import time
import uuid

SERVER_UUID = "master_8"
HOSTNAME    = "master_8.A.local"
START_TIME  = time.time() - 60  # simula 60s de uptime

cpu_pct = psutil.cpu_percent(interval=1)
try:
    load1, load5, _ = psutil.getloadavg()
except AttributeError:
    load1 = cpu_pct / 100.0
    load5 = cpu_pct / 100.0

mem  = psutil.virtual_memory()
disk = psutil.disk_usage('/')

payload = {
    "server_uuid":     SERVER_UUID,
    "hostname":        HOSTNAME,
    "role":            "master",
    "task":            "performance_report",
    "timestamp":       time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "message_id":      str(uuid.uuid4()),
    "payload_version": "sprint4-monitor-v2",
    "performance": {
        "system": {
            "uptime_seconds":  int(time.time() - START_TIME),
            "load_average_1m": round(load1, 2),
            "load_average_5m": round(load5, 2),
            "cpu": {
                "usage_percent":  round(cpu_pct, 2),
                "count_logical":  psutil.cpu_count(logical=True),
                "count_physical": psutil.cpu_count(logical=False) or 1
            },
            "memory": {
                "total_mb":     int(mem.total     / 1024 / 1024),
                "available_mb": int(mem.available / 1024 / 1024),
                "percent_used": round(mem.percent, 2),
                "memory_used":  int(mem.used      / 1024 / 1024)
            },
            "disk": {
                "total_gb":     round(disk.total / 1024**3, 1),
                "free_gb":      round(disk.free  / 1024**3, 1),
                "percent_used": round(disk.percent, 1)
            }
        },
        "farm_state": {
            "workers": {
                "total_registered":          5,
                "workers_utilization":        0,
                "workers_alive":              5,
                "workers_idle":               5,
                "workers_borrowed":           0,
                "workers_received":           0,
                "workers_failed":             0,
                "workers_home":               5,
                "workers_available_capacity": 5,
                "borrowed_workers":           []
            },
            "tasks": {
                "tasks_pending":     10,
                "tasks_running":     0,
                "tasks_completed":   50,
                "tasks_failed":      0,
                "oldest_task_age_s": 0
            }
        },
        "config_thresholds": {
            "max_task":            10,
            "warn_cpu_percent":    85,
            "warn_memory_percent": 85,
            "release_task":        4
        },
        "neighbors": []
    }
}

print("=== PAYLOAD QUE SERÁ ENVIADO ===\n")
print(json.dumps(payload, indent=2, ensure_ascii=False))

print("\n=== VERIFICAÇÃO DE TIPOS ===")
p = payload["performance"]
checks = [
    ("uptime_seconds",   type(p["system"]["uptime_seconds"])),
    ("cpu.usage_percent",type(p["system"]["cpu"]["usage_percent"])),
    ("count_logical",    type(p["system"]["cpu"]["count_logical"])),
    ("total_mb",         type(p["system"]["memory"]["total_mb"])),
    ("memory_used",      type(p["system"]["memory"]["memory_used"])),
    ("total_gb",         type(p["system"]["disk"]["total_gb"])),
    ("total_registered", type(p["farm_state"]["workers"]["total_registered"])),
    ("tasks_pending",    type(p["farm_state"]["tasks"]["tasks_pending"])),
    ("oldest_task_age_s",type(p["farm_state"]["tasks"]["oldest_task_age_s"])),
    ("max_task",         type(p["config_thresholds"]["max_task"])),
]
for campo, tipo in checks:
    status = "✓" if tipo in (int, float) else "✗ PROBLEMA"
    print(f"  {status} {campo}: {tipo.__name__}")
