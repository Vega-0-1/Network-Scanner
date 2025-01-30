import socket
from pythonping import ping

def generate_ip_range(local_ip):
    """Generate a range of IP addresses based on the local subnet."""
    base_ip = ".".join(local_ip.split(".")[:3])
    return [f"{base_ip}.{i}" for i in range(1, 255)]

def scan_network(ip_range, progress_var=None):
    """Scan the network for active hosts."""
    active_hosts = []
    total_ips = len(ip_range)

    for i, ip in enumerate(ip_range):
        response = ping(ip, count=1, timeout=0.5, verbose=False)
        if response.success():
            active_hosts.append(ip)
        if progress_var:
            progress_var.set((i + 1) / total_ips * 100)

    return active_hosts

