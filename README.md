# Port Scanner

This Python script allows scanning ports on single or multiple IP addresses within a specified range. It utilizes threading for efficient scanning and supports both individual IPs and IP ranges.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)

---

## Features

- **Single IP Scan:** Enables scanning ports for a single specified IP address.
- **IP Range Scan:** Supports scanning ports across a range of IP addresses.
- **Multi-threading:** Utilizes threading for parallel port scanning, enhancing performance.

---

## Installation

1. Clone this repository.
2. Ensure you have Python 3.x installed.
3. Run the script in your terminal or IDE.

```
python port_scanner.py
```

---

## Usage

### Single IP Scan

To perform a single IP scan:
1. Invoke the `single_ip_scan()` function.
2. Follow the prompts:
    - Enter the target IP address.
    - Define the starting and ending port numbers.

### IP Range Scan

For scanning across an IP range:
1. Use the `ip_range_scan()` function.
2. Provide the following details:
    - Starting and ending IP addresses.
    - Starting and ending port numbers.

---

## Contribution

Contributions are welcomed! Whether it's reporting issues or submitting pull requests, your contributions are highly appreciated.

---

## License

This project is licensed under the [MIT License](LICENSE).
