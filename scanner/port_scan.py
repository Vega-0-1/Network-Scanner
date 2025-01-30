import socket

def port_description(port):
    """Return a description for a known port."""
    known_ports = {
        80: "HTTP - Web traffic",
        443: "HTTPS - Secure web traffic",
        22: "SSH - Secure Shell",
        21: "FTP - File Transfer Protocol",
        25: "SMTP - Email Sending",
        110: "POP3 - Email Receiving",
        143: "IMAP - Email Receiving",
        53: "DNS - Domain Name System",
        3306: "MySQL Database",
        3389: "RDP - Remote Desktop Protocol",
    }
    return known_ports.get(port, "Unknown service")

def scan_ports(ip, port_range, progress_var=None):
    """Scan ports on a specific IP."""
    open_ports = []
    total_ports = len(port_range)

    for i, port in enumerate(port_range):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((ip, port)) == 0:
                    open_ports.append({"port": port, "description": port_description(port)})
        except Exception:
            pass

        if progress_var:
            progress_var.set((i + 1) / total_ports * 100)

    return open_ports
