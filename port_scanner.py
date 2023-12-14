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

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            results[port] = "Open"
        sock.close()
        port_queue.task_done()

    sys.stdout.write('\n')

# Function to scan a single IP
def single_ip_scan():
    target_ip = input("Enter the IP address to scan: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))
    results = {}  # Initialize results dictionary
    scan(target_ip, start_port, end_port, results)  # Pass results to the scan function

    # Display open ports for the scanned IP
    print(f"\nOpen ports on {target_ip}:")
    for port, status in sorted(results.items()):
        if status == "Open":
            print(f"Port {port}: {status}")

# Function to scan a range of IPs
def ip_range_scan():
    start_ip = input("Enter the starting IP address: ")
    end_ip = input("Enter the ending IP address: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))
    
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
print("Select the scan type:")
print("1. Single IP")
print("2. IP Range")
scan_type = input("Enter your choice (1 or 2): ")

if scan_type == "1":
    single_ip_scan()
elif scan_type == "2":
    ip_range_scan()
else:
    print("Invalid choice. Please enter 1 or 2.")
