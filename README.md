# Network Scanner - Advanced Python-Based Network Scanning Tool

## Overview

This project is an **advanced network scanning tool** developed in **Python**, featuring a **Tkinter-based user interface**. The tool utilizes **Nmap** and other advanced libraries to perform comprehensive network scans, providing detailed insights into network components, active services, open ports, and more.

### Features:

- **Graphical User Interface (GUI)**: Built with **Tkinter** for an intuitive and user-friendly experience.
- **Custom Network Scans**: Supports scanning **IP ranges, ports, and services**.
- **Advanced Detection Capabilities**: Identifies **MAC addresses, running services, and operating systems**.
- **Real-Time Scan Progress**: Displays dynamic **progress bars** and logs scan activities.
- **Extensible and Modular Code**: Easily maintainable and expandable for future enhancements.

---

## Installation

### Prerequisites

Before running the tool, ensure that the following dependencies are installed:

- **Python 3.8+** ([Download Here](https://www.python.org/downloads/))
- **Nmap** (Required for scanning capabilities) - [Installation Guide](https://nmap.org/download.html)
- **Npcap** (Required for network packet capturing) - [Download Here](https://nmap.org/npcap/)

### Install Required Python Packages

Clone the repository and install dependencies using `pip`:

```sh
# Clone the repository
git clone https://github.com/yourusername/network-scanner.git
cd network-scanner

# Install dependencies
pip install -r requirements.txt
```

If you do not have `pip` installed, follow the [pip installation guide](https://pip.pypa.io/en/stable/installation/).

### Required External Tools

- **Nmap** ([Download Here](https://nmap.org/download.html))
  - Make sure `nmap` is installed and added to your system's PATH.
- **Npcap** ([Download Here](https://nmap.org/npcap/))
  - Required for network packet capturing on Windows systems.

To verify the installation, run:

```sh
nmap --version
```

Expected Output:

```
Nmap version 7.x.x ( https://nmap.org )
```

---

## Usage

To launch the network scanner, simply run:

```sh
python main.py
```

### How to Use the Tool

1. **Enter IP Range**: Provide an IP range or a specific address to scan.
2. **Select Scan Type**: Choose from different scanning options (e.g., basic scan, service detection, OS detection).
3. **Start Scan**: Click the "Start Scan" button to begin scanning.
4. **View Results**: The results will display **open ports, running services, and detected devices** in real time.
5. **Save Logs**: Scan results and logs are automatically saved for later analysis.

---

## Example Output

```
Scanning network...
----------------------------------
Host: 192.168.1.1
Open Ports: 80, 443
MAC Address: XX:XX:XX:XX:XX:XX
Operating System: Linux
----------------------------------
```

---

## Contribution

Contributions are welcome! If you'd like to improve this project, feel free to fork the repository and submit a pull request.

---

## Credits

This tool was extensively tested and optimized using **ChatGPT by OpenAI**, ensuring high accuracy and efficiency in network scanning functionalities. Special thanks to **OpenAI** for providing advanced AI capabilities that contributed to the development and refinement of this project.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For any inquiries or issues, feel free to open an issue on GitHub or reach out via email.

📧 Email: [mtnhb355@gmail.com](mailto\:mtnhb355@gmail.com)\


