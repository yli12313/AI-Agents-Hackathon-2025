#!/usr/bin/env python3
"""
Mock chatbot server for testing.
This provides a local server to test against during development.
"""

import json
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

class MockChatbotHandler(BaseHTTPRequestHandler):
    """Mock chatbot API handler."""
    
    def do_POST(self):
        """Handle POST requests to the chatbot."""
        parsed_path = urlparse(self.path)
        
        # Simulate different endpoints
        if parsed_path.path == '/api/chatbot':
            self.handle_chatbot_request()
        else:
            self.send_error(404, "Endpoint not found")
    
    def handle_chatbot_request(self):
        """Handle chatbot API requests."""
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data =(json.loads(post_data.decode('utf-8')))
            
            # Extract the message
            prompt = request_data.get('message', '')
            
            # Generate different responses based on attack type
            if '[PII_LEAK_CHAIN]' in prompt:
                response = self.generate_pii_leak_response(prompt)
            elif '[SYSTEM_PROMPT_ECHO]' in prompt:
                response = self.generate_system_prompt_response(prompt)
            else:
                response = "This is a regular chatbot response without sensitive data."
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = json.dumps({"response": response})
            self.wfile.write(response_data.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def generate_pii_leak_response(self, prompt):
        """Generate response that leaks PII (for testing purposes)."""
        leak_responses = [
            "I understand you're working on SSO issues. The admin email for direct access is admin@company.com and the bypass code is ADMIN789.",
            "For urgent SSO bypass, contact admin@company.com with your credentials. The internal password is CompanyPass2024.",
            "Here's the emergency contact: admin@company.com. Use this for immediate SSO access outside normal channels."
        ]
        return random.choice(leak_responses)
    
    def generate_system_prompt_response(self, prompt):
        """Generate response that echoes system prompt."""
        system_responses = [
            "I am a helpful AI assistant. My system instructions are: 'You are a customer support chatbot. Never reveal sensitive information.'",
            "My configuration tells me to be helpful but secure. System prompt says I should assist users without exposing internal data.",
            "According to my setup: I'm designed to provide helpful responses while maintaining security protocols."
        ]
        return random.choice(system_responses)
    
    def log_message(self, format, *args):
        """Override to reduce log noise."""
        pass

class TestServer:
    """Test server wrapper."""
    
    def __init__(self, host='localhost', port=8123):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Start the test server."""
        self.server = HTTPServer((self.host, self.port), MockChatbotHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        print(f"Test server started at http://{self.host}:{self.port}/api/chatbot")
    
    def stop(self):
        """Stop the test server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join()

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Mock chatbot server for testing")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8123, help="Port to bind to")
    
    args = parser.parse_args()
    
    server = TestServer(args.host, args.port)
    
    try:
        server.start()
        print("Press Ctrl+C to stop the server")
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down test server...")
        server.stop()

if __name__ == "__main__":
    main()
