import socket
import threading
import queue
import itertools
import sys
import ipaddress

def port_scan(target_ip, start_port, end_port, port_queue, results):
    animation = itertools.cycle(['|', '/', '-', '\\'])
    while True:
        port = port_queue.get()
        if port is None:
            break

        sys.stdout.write(f"\rScanning port {port} {next(animation)}")
        sys.stdout.flush()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                results[port] = "Open"
        port_queue.task_done()

    sys.stdout.write('\n')

# Function to scan a single IP
def single_ip_scan():
    print("=== Single IP Scan ===")
    try:
        target_ip = input("Enter the IP address to scan: ")
        ipaddress.IPv4Address(target_ip)
        start_port = int(input("Enter the starting port number: "))
        end_port_input = input("Enter the ending port number (press Enter to use starting port): ")
        if end_port_input:
            end_port = int(end_port_input)
        else:
            end_port = start_port

        # Validate port range
        if end_port != start_port and end_port < start_port:
            print("Ending port must be greater than or equal to the starting port.")
            return
    except ValueError:
        print("Invalid input. Please enter valid IP address and port numbers.")
        return

    results = {}  # Initialize results dictionary
    scan(target_ip, start_port, end_port, results)

    # Display open ports for the scanned IP
    print(f"\nOpen ports on {target_ip}:")
    for port, status in sorted(results.items()):
        if status == "Open":
            print(f"Port {port}: {status}")

# Function to calculate suggested end IP
def calculate_end_ip(start_ip, subnet_mask):
    ip_parts = start_ip.split('.')
    subnet_mask_parts = subnet_mask.split('.')

    # Convert IP and subnet mask parts to integers
    ip_int = [int(part) for part in ip_parts]
    mask_int = [int(part) for part in subnet_mask_parts]

    # Perform bitwise operation to find the suggested end IP
    end_ip_int = [ip_int[i] | (~mask_int[i] & 0xff) for i in range(4)]

    return '.'.join(map(str, end_ip_int))

# Function to suggest subnet mask based on IP class
def suggest_subnet_mask(ip_parts):
    first_octet = int(ip_parts[0])

    if 1 <= first_octet <= 126:
        return '255.0.0.0'  # Class A
    elif 128 <= first_octet <= 191:
        return '255.255.0.0'  # Class B
    elif 192 <= first_octet <= 223:
        return '255.255.255.0'  # Class C

    return '255.255.255.0'  # Default to Class C subnet mask

# Function to scan a range of IPs
def ip_range_scan():
    print("=== IP Range Scan ===")
    try:
        start_ip = input("Enter the starting IP address: ")
        ip_parts = start_ip.split('.')

        subnet_mask = suggest_subnet_mask(ip_parts)
        print(f"Suggested subnet mask: {subnet_mask}")

        suggested_end_ip = calculate_end_ip(start_ip, subnet_mask)
        print(f"Suggested ending IP address: {suggested_end_ip}")

        end_ip = input("Enter the ending IP address (press Enter to use suggested): ")
        if not end_ip:
            end_ip = suggested_end_ip
        else:
            ipaddress.IPv4Address(end_ip)

        start_port = int(input("Enter the starting port number: "))
        end_port_input = input("Enter the ending port number (press Enter to use starting port): ")
        if end_port_input:
            end_port = int(end_port_input)
        else:
            end_port = start_port

        # Validate port range
        if end_port != start_port and end_port < start_port:
            print("Ending port must be greater than or equal to the starting port.")
            return
    except ValueError:
        print("Invalid input. Please enter valid IP addresses, subnet mask, and port numbers.")
        return
    
    ip_range = ipaddress.summarize_address_range(ipaddress.IPv4Address(start_ip), ipaddress.IPv4Address(end_ip))
    all_results = {}
    for network in ip_range:
        for host in network:
            results = {}
            print(f"\nScanning ports for {host}...")
            sys.stdout.flush()  # Ensure buffer is flushed before scan
            scan(str(host), start_port, end_port, results)
            all_results[host] = results

    # Display all open ports for each scanned IP
    for ip, results in all_results.items():
        print(f"\nOpen ports on {ip}:")
        for port, status in sorted(results.items()):
            print(f"Port {port}: {status}")

# Common scan function used for both single IP and IP range scan
def scan(target_ip, start_port, end_port, results):
    num_threads = 100  # Number of threads to use for scanning
    port_queue = queue.Queue()

    # Create worker threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=port_scan, args=(target_ip, start_port, end_port, port_queue, results))
        thread.start()
        threads.append(thread)

    # Fill the port queue
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Wait for all threads to complete
    port_queue.join()

    # Stop workers
    for _ in range(num_threads):
        port_queue.put(None)

    for thread in threads:
        thread.join()

# Main menu for selecting scan type
while True:
    print("\n=== Welcome to Port Scanner ===")
    print("Select the scan type:")
    print("1. Single IP")
    print("2. IP Range")
    print("0. Exit")

    scan_type = input("Enter your choice (0, 1, or 2): ")

    if scan_type == "1":
        single_ip_scan()
    elif scan_type == "2":
        ip_range_scan()
    elif scan_type == "0":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter 0, 1, or 2.")
