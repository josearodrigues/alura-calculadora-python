"""
Servidor web nativo da Calculadora Python.
Inicia um servidor HTTP na porta 3000 (127.0.0.1) para servir a interface web Pyodide.
"""

import http.server
import os
import socketserver

PORT = int(os.environ.get("PORT", 3000))
HOST = "127.0.0.1"


class Handler(http.server.SimpleHTTPRequestHandler):
    """Handler para servir os arquivos estáticos da pasta raiz."""
    def end_headers(self):
        # Permite carregar recursos do WebAssembly e desabilita cache durante desenvolvimento
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()


def run():
    # Permite reuso rápido da porta
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print(f"Servidor Web iniciado em http://{HOST}:{PORT}")
        print(f"Servindo interface web complementar com Pyodide...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
            httpd.server_close()


if __name__ == "__main__":
    run()
