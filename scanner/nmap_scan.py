import nmap

def advanced_scan(ip_range, progress_callback=None):
    """Perform an advanced Nmap scan."""
    scanner = nmap.PortScanner()
    results = {}
    try:
        scan_result = scanner.scan(
            hosts=ip_range,
            arguments="-sS -sV -O -T4 -p-"
        )
        hosts = scanner.all_hosts()
        total_hosts = len(hosts)

        for idx, host in enumerate(hosts, start=1):
            host_data = {"mac": "N/A", "ports": []}
            if "addresses" in scan_result["scan"][host]:
                host_data["mac"] = scan_result["scan"][host]["addresses"].get("mac", "N/A")

            for port, details in scan_result["scan"][host].get("tcp", {}).items():
                port_data = {
                    "port": port,
                    "service": details.get("name", "Unknown service"),
                    "description": details.get("product", "N/A")
                }
                host_data["ports"].append(port_data)

            results[host] = host_data

            if progress_callback:
                progress_callback(idx, total_hosts)

    except Exception as e:
        print(f"Error during scan: {e}")

    return results
