import socket
import logging

class UDPSocketManager:
    def __init__(self, port=50005):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.target_addr = None

    def bind(self):
        """Binds the socket to the configured port on all interfaces."""
        try:
            self.sock.bind(("0.0.0.0", self.port))
            return True
        except Exception as e:
            logging.error(f"Failed to bind to port {self.port}: {e}")
            return False

    def set_target(self, ip, port):
        """Sets the target address for outgoing packets."""
        self.target_addr = (ip, port)

    def send(self, data):
        """Sends data to the target address."""
        if self.target_addr:
            try:
                self.sock.sendto(data, self.target_addr)
            except Exception as e:
                logging.debug(f"Error sending data: {e}")

    def receive(self, buffer_size=4096):
        """Receives data and returns (data, addr)."""
        try:
            data, addr = self.sock.recvfrom(buffer_size)
            # If we haven't set a target yet (Host mode), set it to the first sender
            if not self.target_addr:
                self.target_addr = addr
            return data, addr
        except Exception as e:
            logging.debug(f"Error receiving data: {e}")
            return None, None

    def close(self):
        self.sock.close()

def get_local_ips():
    """Returns a list of local IP addresses for this machine."""
    ips = []
    try:
        # Get host name
        hostname = socket.gethostname()
        # Get all IP addresses associated with the hostname
        # Note: This might only return 127.0.1.1 on some Linux setups
        ips = socket.gethostbyname_ex(hostname)[2]
        
        # Fallback/Additional check using a dummy connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            primary_ip = s.getsockname()[0]
            if primary_ip not in ips:
                ips.append(primary_ip)
        except Exception:
            pass
        finally:
            s.close()
            
    except Exception as e:
        logging.error(f"Could not determine local IPs: {e}")
    
    # Filter out loopback
    return [ip for ip in ips if not ip.startswith("127.")]
