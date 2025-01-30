from datetime import datetime

def save_log(log_data, filename):
    """Save the scan results to a log file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Network Scan Report\n")
        f.write(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for host, data in log_data.items():
            f.write(f"Host: {host}\n")
            if "mac" in data:
                f.write(f"MAC Address: {data['mac']}\n")
            if "vendor" in data:
                f.write(f"Vendor: {data['vendor']}\n")
            if "ports" in data:
                f.write("Open Ports:\n")
                for port in data["ports"]:
                    f.write(f" - Port {port['port']} ({port['description']})\n")
            f.write("\n")
