import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socket import gethostbyname, gethostname
import cgi

UPLOAD_DIR = "shared_files"

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # ShareIt-inspired HTML UI
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Quick Share - Easy File Sharing</title>
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    body {{
                        font-family: 'Poppins', sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        padding: 20px;
                    }}
                    .shareit-container {{
                        background: white;
                        width: 100%;
                        max-width: 450px;
                        border-radius: 20px;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                        overflow: hidden;
                        position: relative;
                    }}
                    .header {{
                        background: linear-gradient(to right, #667eea, #764ba2);
                        color: white;
                        text-align: center;
                        padding: 20px;
                    }}
                    .header h1 {{
                        font-size: 24px;
                        margin-bottom: 10px;
                    }}
                    .upload-section {{
                        padding: 20px;
                        text-align: center;
                    }}
                    .file-input-wrapper {{
                        position: relative;
                        border: 2px dashed #667eea;
                        border-radius: 10px;
                        padding: 40px 20px;
                        margin-bottom: 20px;
                        transition: all 0.3s ease;
                    }}
                    .file-input-wrapper:hover {{
                        background: rgba(102,126,234,0.05);
                    }}
                    #fileInput {{
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        opacity: 0;
                        cursor: pointer;
                    }}
                    .upload-btn {{
                        width: 100%;
                        padding: 15px;
                        background: linear-gradient(to right, #667eea, #764ba2);
                        color: white;
                        border: none;
                        border-radius: 10px;
                        font-size: 16px;
                        cursor: pointer;
                        transition: transform 0.2s;
                    }}
                    .upload-btn:hover {{
                        transform: scale(1.05);
                    }}
                    #uploadStatus {{
                        margin-top: 15px;
                        padding: 10px;
                        border-radius: 5px;
                        text-align: center;
                    }}
                    .success {{
                        background-color: #4caf50;
                        color: white;
                    }}
                    .error {{
                        background-color: #f44336;
                        color: white;
                    }}
                    .file-list {{
                        background: #f4f4f8;
                        max-height: 250px;
                        overflow-y: auto;
                        padding: 15px;
                    }}
                    .file-list h2 {{
                        text-align: center;
                        margin-bottom: 10px;
                        color: #333;
                    }}
                    .file-item {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        background: white;
                        margin: 10px 0;
                        padding: 10px;
                        border-radius: 8px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }}
                    .file-item a {{
                        color: #ea66d8;
                        text-decoration: none;
                        font-weight: 500;
                    }}
                    @media (max-width: 500px) {{
                        .shareit-container {{
                            width: 100%;
                            margin: 0;
                            border-radius: 0;
                        }}
                        .header {{
                            padding: 15px;
                        }}
                        .upload-section {{
                            padding: 15px;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="shareit-container">
                    <div class="header">
                        <h1>🚀 MC QuickShare</h1>
                        <p>Wireless File Sharing</p>
                    </div>
                    
                    <div class="upload-section">
                        <form id="uploadForm" enctype="multipart/form-data">
                            <div class="file-input-wrapper">
                                <input type="file" id="fileInput" name="file" required>
                                <p>Drag and drop or click to select file</p>
                            </div>
                            <button type="submit" class="upload-btn">Upload File</button>
                        </form>
                        <div id="uploadStatus"></div>
                    </div>
                    
                    <div class="file-list">
                        <h2>Shared Files</h2>
                        <ul id="fileList">
            """
            for file_name in os.listdir(UPLOAD_DIR):
                html_content += f'<li class="file-item"><span>{file_name}</span> <a href="/{UPLOAD_DIR}/{file_name}" download>Download</a></li>'
            html_content += """
                        </ul>
                    </div>
                </div>

                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        const uploadForm = document.getElementById('uploadForm');
                        const fileInput = document.getElementById('fileInput');
                        const uploadStatus = document.getElementById('uploadStatus');
                        
                        uploadForm.addEventListener('submit', async (event) => {
                            event.preventDefault();
                            
                            if (!fileInput.files.length) {
                                uploadStatus.textContent = 'Please select a file!';
                                uploadStatus.className = 'error';
                                return;
                            }

                            const formData = new FormData(uploadForm);
                            
                            try {
                                const response = await fetch('/', {
                                    method: 'POST',
                                    body: formData
                                });

                                if (response.ok) {
                                    uploadStatus.textContent = 'File uploaded successfully!';
                                    uploadStatus.className = 'success';
                                    fileInput.value = '';

                                    setTimeout(() => {
                                        window.location.reload();
                                    }, 1500);
                                } else {
                                    throw new Error('Upload failed');
                                }
                            } catch (error) {
                                uploadStatus.textContent = 'File upload failed!';
                                uploadStatus.className = 'error';
                            }
                        });

                        // Drag and drop file input enhancement
                        const fileInputWrapper = document.querySelector('.file-input-wrapper');
                        fileInputWrapper.addEventListener('dragover', (e) => {
                            e.preventDefault();
                            fileInputWrapper.style.background = 'rgba(102,126,234,0.1)';
                        });
                        fileInputWrapper.addEventListener('dragleave', () => {
                            fileInputWrapper.style.background = 'transparent';
                        });
                        fileInputWrapper.addEventListener('drop', (e) => {
                            e.preventDefault();
                            fileInputWrapper.style.background = 'transparent';
                            fileInput.files = e.dataTransfer.files;
                        });
                    });
                </script>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/':
            content_type, params = cgi.parse_header(self.headers.get('Content-Type'))
            if content_type == 'multipart/form-data':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                uploaded_file = form['file']
                if uploaded_file.filename:
                    file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
                    with open(file_path, 'wb') as f:
                        f.write(uploaded_file.file.read())
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"File uploaded successfully!")
                else:
                    self.send_error(400, "No file uploaded")
            else:
                self.send_error(400, "Invalid form submission")

def run_server():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    host = gethostbyname(gethostname())
    port = 8000

    server_address = (host, port)
    httpd = HTTPServer(server_address, CustomHTTPRequestHandler)

    print(f"Server started at http://{host}:{port}")
    print("Press Ctrl+C to stop the server.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()