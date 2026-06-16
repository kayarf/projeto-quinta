import socket, ssl, json, time, uuid

SUPERVISOR_HOST = "nuted-ia.dev"
SUPERVISOR_PORT = 443
SUPERVISOR_SNI  = "nuted-ia.dev"

agora = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

payload = {
    "server_uuid":     "master_8",
    "hostname":        "master_8.A.local",
    "role":            "master",
    "task":            "performance_report",
    "timestamp":       agora,
    "message_id":      str(uuid.uuid4()),
    "payload_version": "sprint4-monitor",   # sem o -v2
    "performance": {
        "system": {
            "uptime_seconds":  61,
            "load_average_1m": 0.0,
            "load_average_5m": 0.0,
            "cpu": {
                "usage_percent":  29.0,
                "count_logical":  16,
                "count_physical": 8
            },
            "memory": {
                "total_mb":     16304,
                "available_mb": 3408,
                "percent_used": 79.1,
                "memory_used":  12896
            },
            "disk": {
                "total_gb":    464.8,
                "free_gb":     188.5,
                "percent_used": 59.5
            }
        },
        "farm_state": {
            "workers": {
                "total_registered":          5,
                "workers_utilization":        0,
                "workers_alive":              5,
                "workers_idle":              5,
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
            "max_task":            100,
            "warn_cpu_percent":    85,
            "warn_memory_percent": 85,
            "release_task":        60
        },
        "neighbors": [
            {
                "server_uuid":    "peer_192.168.15.19",
                "status":         "unavailable",
                "last_heartbeat": agora
            }
        ]
    }
}

data = (json.dumps(payload) + "\n").encode("utf-8")
print(f"\nEnviando {len(data)} bytes para {SUPERVISOR_HOST}:{SUPERVISOR_PORT}...")

try:
    raw = socket.create_connection((SUPERVISOR_HOST, SUPERVISOR_PORT), timeout=10)
    ctx = ssl.create_default_context()
    tls = ctx.wrap_socket(raw, server_hostname=SUPERVISOR_SNI)
    tls.sendall(data)
    time.sleep(0.5)
    try:
        tls.unwrap()
    except Exception:
        pass
    raw.close()
    print("✓ Enviado! Acesse https://nuted-ia.dev/supervisor/dashboard/ e aguarde ~15s")
except Exception as e:
    print(f"✗ ERRO: {e}")