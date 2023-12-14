import socket

def port_scan(target_ip, start_port, end_port):
    print(f"Scanning {target_ip}...")
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(f"Port {port}: Open")
        sock.close()

# Get the target IP and port range from the user
target_ip = input("Enter the IP address to scan: ")
start_port = int(input("Enter the starting port number: "))
end_port = int(input("Enter the ending port number: "))

port_scan(target_ip, start_port, end_port)
