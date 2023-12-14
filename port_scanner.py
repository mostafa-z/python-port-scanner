import socket
import threading
import queue

def port_scan(target_ip, start_port, end_port, results):
    while True:
        port = port_queue.get()
        if port is None:
            break

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            results[port] = "Open"
        sock.close()
        port_queue.task_done()

# Get the target IP and port range from the user
target_ip = input("Enter the IP address to scan: ")
start_port = int(input("Enter the starting port number: "))
end_port = int(input("Enter the ending port number: "))

num_threads = 100  # Number of threads to use for scanning
port_queue = queue.Queue()
results = {}

# Create worker threads
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=port_scan, args=(target_ip, start_port, end_port, results))
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
