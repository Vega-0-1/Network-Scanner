from scapy.all import ARP, Ether, srp

def scan_arp(ip, iface=None):
    """Perform ARP scan on a specific IP."""
    try:
        arp_request = ARP(pdst=ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp_request
        result = srp(packet, iface=iface, timeout=2, verbose=False)[0]
        if result:
            return {"ip": result[0][1].psrc, "mac": result[0][1].hwsrc}
    except Exception as e:
        print(f"Error scanning ARP for {ip}: {e}")
    return {"ip": ip, "mac": "N/A"}
