import docker
import time

INTERVAL = 10

client = docker.from_env()


def calculate_cpu_percent(stats):
    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    cpu_count = len(stats['cpu_stats']['cpu_usage'].get('percpu_usage', [])) or 1
    cpu_percent = (cpu_delta / system_delta) * cpu_count * 100 if system_delta > 0 else 0
    return cpu_percent


def monitor_containers():
    print(f"{'Time':<10} {'Container':<30} {'CPU %':<10} {'RAM Usage':<20}")
    while True:
        timestamp = time.strftime("%H:%M:%S")
        print(f"{timestamp:<10}------------------------------------------------")
        for container in client.containers.list():
            try:
                stats = container.stats(stream=False)

                cpu_percent = calculate_cpu_percent(stats)

                mem_usage = stats['memory_stats']['usage']
                mem_limit = stats['memory_stats']['limit']
                mem_percent = (mem_usage / mem_limit) * 100 if mem_limit > 0 else 0

                print(
                    f"{timestamp:<10} {container.name:<30} | {cpu_percent:<10.2f} | {mem_usage / 1024 / 1024:.2f} MiB ({mem_percent:.1f}%)", flush=True)
            except Exception as e:
                print(f"{timestamp:<10} {container.name:<30} | Error: {e}")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    monitor_containers()
