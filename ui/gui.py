import tkinter as tk
from tkinter import ttk, messagebox
from ui.theme_manager import ThemeManager
from ui.localization import Localization
from scanner.network_scan import generate_ip_range, scan_network
from scanner.port_scan import scan_ports
from scanner.arp_scan import scan_arp
from scanner.nmap_scan import advanced_scan
from utils.logger import save_log
import threading
import ipaddress


def get_port_range(choice, custom_range):
    """Get port range based on selection."""
    if choice == 1:
        return range(1, 1025)
    elif choice == 2:
        return range(1, 65536)
    elif choice == 3 and custom_range:
        return range(custom_range[0], custom_range[1] + 1)
    return range(1, 1025)


class NetworkScannerApp:
    def __init__(self, root):
        self.buttons_to_disable = []
        self.interface_frame = None
        self.log_text = None
        self.root = root
        self.root.title("Network Scanner")
        self.root.geometry("1200x800")

        self.interface_var = tk.StringVar()
        self.port_choice_var = tk.IntVar(value=1)
        self.custom_start_port = tk.IntVar()
        self.custom_end_port = tk.IntVar()
        self.ip_progress_var = tk.DoubleVar()
        self.port_progress_var = tk.DoubleVar()
        self.advanced_scan_progress_var = tk.DoubleVar()
        self.localization = Localization()
        self.theme_manager = ThemeManager(root)
        self.custom_ip_var = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI layout."""
        title_label = ttk.Label(self.root, text="Network Scanner", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        self.interface_frame = ttk.LabelFrame(self.root, text=self.localization.translate("network_interface"))
        self.interface_frame.pack(fill="x", padx=10, pady=5)
        self.populate_interfaces()

        port_frame = ttk.LabelFrame(self.root, text=self.localization.translate("port_range"))
        port_frame.pack(fill="x", padx=10, pady=5)
        self.create_port_selection(port_frame)

        progress_frame = ttk.LabelFrame(self.root, text=self.localization.translate("Progress"))
        progress_frame.pack(fill="x", padx=10, pady=5)
        self.create_progress_bars(progress_frame)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        self.create_buttons(button_frame)

        manual_ip_frame = ttk.LabelFrame(self.root, text="Enter IP Address for Advanced Scan (optional):")
        manual_ip_frame.pack(fill="x", padx=10, pady=5)
        ttk.Entry(manual_ip_frame, textvariable=self.custom_ip_var, width=30).pack(padx=10, pady=5)

        advanced_progress_frame = ttk.LabelFrame(self.root, text="Advanced Scan Progress")
        advanced_progress_frame.pack(fill="x", padx=10, pady=5)
        ttk.Progressbar(
            advanced_progress_frame,
            variable=self.advanced_scan_progress_var,
            maximum=100
        ).pack(fill="x", padx=10, pady=5)

        log_frame = ttk.LabelFrame(self.root, text="Logs")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_text = tk.Text(log_frame, wrap="word", height=15)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=5)

    def populate_interfaces(self):
        """Populate the interface selection frame with available interfaces."""
        from utils.helpers import get_interfaces
        interfaces = get_interfaces()
        for idx, (interface, ip, is_up) in enumerate(interfaces, start=1):
            state = self.localization.translate("Active") if is_up else self.localization.translate("Inactive")
            display_text = f"{idx}. Interface: {interface} ({state})\n   - IPv4 Address: {ip}"
            ttk.Radiobutton(
                self.interface_frame,
                text=display_text,
                variable=self.interface_var,
                value=ip,
            ).pack(anchor="w", pady=2)

    def create_port_selection(self, frame):
        """Create port range selection."""
        ttk.Radiobutton(frame, text=self.localization.translate("default"), variable=self.port_choice_var, value=1).pack(anchor="w")
        ttk.Radiobutton(frame, text=self.localization.translate("full_range"), variable=self.port_choice_var, value=2).pack(anchor="w")
        custom_frame = ttk.Frame(frame)
        custom_frame.pack(fill="x")
        ttk.Radiobutton(custom_frame, text=self.localization.translate("custom_range"), variable=self.port_choice_var, value=3).pack(side="left")
        ttk.Entry(custom_frame, textvariable=self.custom_start_port, width=10).pack(side="left", padx=5)
        ttk.Label(custom_frame, text=self.localization.translate("to")).pack(side="left")
        ttk.Entry(custom_frame, textvariable=self.custom_end_port, width=10).pack(side="left", padx=5)

    def create_progress_bars(self, frame):
        """Create progress bars."""
        ttk.Label(frame, text=self.localization.translate("ip_scan_progress")).pack(anchor="w", padx=10)
        ttk.Progressbar(frame, variable=self.ip_progress_var, maximum=100).pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text=self.localization.translate("port_scan_progress")).pack(anchor="w", padx=10)
        ttk.Progressbar(frame, variable=self.port_progress_var, maximum=100).pack(fill="x", padx=10, pady=5)

    def create_buttons(self, frame):
        """Create action buttons."""
        start_scan_button = ttk.Button(frame, text=self.localization.translate("start_scan"), command=self.start_scan)
        start_scan_button.pack(side="left", padx=5)

        advanced_scan_button = ttk.Button(frame, text=self.localization.translate("advanced_scan"),
                                          command=self.start_advanced_scan)
        advanced_scan_button.pack(side="left", padx=5)

        settings_button = ttk.Button(frame, text=self.localization.translate("Settings"), command=self.open_settings)
        settings_button.pack(side="left", padx=5)

        exit_button = ttk.Button(frame, text=self.localization.translate("exit"), command=self.root.quit)
        exit_button.pack(side="left", padx=5)

        self.buttons_to_disable.extend([start_scan_button, advanced_scan_button, settings_button])

    def start_scan(self):
        """Start basic network scan."""
        self.disable_buttons()

        selected_ip = self.interface_var.get()
        port_choice = self.port_choice_var.get()
        custom_range = (self.custom_start_port.get(), self.custom_end_port.get()) if port_choice == 3 else None

        if not selected_ip:
            messagebox.showerror(self.localization.translate("Error"),
                                 self.localization.translate("error_select_interface"))
            self.enable_buttons()
            return

        port_range = get_port_range(port_choice, custom_range)
        threading.Thread(target=self.run_scan, args=(selected_ip, port_range), daemon=True).start()

    def start_advanced_scan(self):
        """Start advanced scan using Nmap."""
        self.disable_buttons()

        custom_ip = self.custom_ip_var.get().strip()

        if not custom_ip:
            messagebox.showerror("Error", "Please enter a valid IP range or address.")
            self.enable_buttons()
            return

        try:
            if "/" in custom_ip:
                ipaddress.ip_network(custom_ip, strict=False)
            else:
                ipaddress.ip_address(custom_ip)
        except ValueError:
            messagebox.showerror("Error", "Invalid IP address or range. Please try again.")
            self.enable_buttons()
            return

        threading.Thread(target=self.run_advanced_scan, args=(custom_ip,), daemon=True).start()

    def run_scan(self, ip, port_range):
        """Run a basic network scan."""
        try:
            ip_range = generate_ip_range(ip)
            active_hosts = scan_network(ip_range, self.ip_progress_var)

            results = {}
            for host in active_hosts:
                results[host] = {"mac": scan_arp(host), "ports": scan_ports(host, port_range, self.port_progress_var)}

            save_log(results, "basic_scan_results.txt")
            messagebox.showinfo(self.localization.translate("scan_complete"),
                                self.localization.translate("scan_complete"))
        finally:
            self.enable_buttons()

    def run_advanced_scan(self, ip_range):
        """Run an advanced Nmap scan."""
        try:
            self.update_advanced_scan_progress(0, 1)
            self.update_log("Advanced scan started...\n it may take a while...")
            results = advanced_scan(ip_range, self.update_advanced_scan_progress)

            for host, data in results.items():
                self.update_log(f"Host: {host}")
                self.update_log(f"MAC: {data['mac']}")
                for port_info in data['ports']:
                    self.update_log(f"Port: {port_info['port']} - {port_info['service']} ({port_info['description']})")

            save_log(results, "advanced_scan_results.txt")
            self.update_log("Advanced scan completed successfully.")
            messagebox.showinfo("Scan Complete", "Advanced scan completed.")
        finally:
            self.enable_buttons()

    def update_advanced_scan_progress(self, current, total):
        """Update the progress bar for the advanced scan."""
        progress = (current / total) * 100
        self.advanced_scan_progress_var.set(progress)
        self.root.update_idletasks()

    def update_log(self, message):
        """Update the log window."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def disable_buttons(self):
        """Disable buttons during scanning."""
        for button in self.buttons_to_disable:
            button.config(state=tk.DISABLED)

    def enable_buttons(self):
        """Enable buttons after scanning."""
        for button in self.buttons_to_disable:
            button.config(state=tk.NORMAL)

    def open_settings(self):
        """Open the settings window."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title(self.localization.translate("Settings"))
        settings_window.geometry("400x300")
        ttk.Label(settings_window, text=self.localization.translate("Theme") + ":").pack(anchor="w", padx=10, pady=5)
        theme_var = tk.StringVar(value=self.theme_manager.dark_mode)
        ttk.Radiobutton(settings_window, text="Light", variable=theme_var, value=False,
                        command=self.theme_manager.apply_light_theme).pack(anchor="w", padx=10)
        ttk.Radiobutton(settings_window, text="Dark", variable=theme_var, value=True,
                        command=self.theme_manager.apply_dark_theme).pack(anchor="w", padx=10)
        ttk.Label(settings_window, text=self.localization.translate("Language") + ":").pack(anchor="w", padx=10, pady=5)
        lang_var = tk.StringVar(value=self.localization.language)
        ttk.Radiobutton(settings_window, text="English", variable=lang_var, value="en",
                        command=lambda: self.localization.set_language("en")).pack(anchor="w", padx=10)
        ttk.Radiobutton(settings_window, text="Hebrew", variable=lang_var, value="he",
                        command=lambda: self.localization.set_language("he")).pack(anchor="w", padx=10)
        ttk.Button(settings_window, text=self.localization.translate("close"), command=settings_window.destroy).pack(pady=20)
