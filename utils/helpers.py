import psutil

def get_interfaces():
    """Get all available interfaces and their IP addresses."""
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    interface_list = []

    for interface, snics in interfaces.items():
        is_up = stats[interface].isup if interface in stats else False
        for snic in snics:
            if snic.family.name == "AF_INET":  # IPv4 addresses
                interface_list.append((interface, snic.address, is_up))

    return interface_list
