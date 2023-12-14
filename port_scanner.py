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
    scan(target_ip, start_port, end_port)

# Function to scan a range of IPs
def ip_range_scan():
    start_ip = input("Enter the starting IP address: ")
    end_ip = input("Enter the ending IP address: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))
    
    ip_range = ipaddress.summarize_address_range(ipaddress.IPv4Address(start_ip), ipaddress.IPv4Address(end_ip))
    for network in ip_range:
        for host in network:
            scan(str(host), start_port, end_port)

# Common scan function used for both single IP and IP range scan
def scan(target_ip, start_port, end_port):
    num_threads = 100  # Number of threads to use for scanning
    port_queue = queue.Queue()
    results = {}

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

    # Sort and print open ports
    sorted_ports = sorted(results.items(), key=lambda x: x[0])
    print(f"Open ports on {target_ip}:")
    for port, status in sorted_ports:
        print(f"Port {port}: {status}")

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
