from flask import Flask, request, jsonify, send_file, Response
import email
from email.message import EmailMessage
from email.mime.base import MIMEBase
import base64
import io

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Analyzer & Editor</title>
    <script src="https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js" referrerpolicy="origin"></script>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #f0f2f5;
            --card-bg: #ffffff;
            --text-color: #333;
            --primary-color: #007bff;
            --secondary-color: #6c757d;
            --accent-color: #28a745;
            --border-color: #e0e0e0;
            --shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        body.dark-theme {
            --bg-color: #121212;
            --card-bg: #1e1e1e;
            --text-color: #e0e0e0;
            --primary-color: #66b3ff;
            --secondary-color: #a0a0a0;
            --accent-color: #28a745;
            --border-color: #333;
            --shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Roboto', sans-serif;
        }

        body {
            background: var(--bg-color);
            color: var(--text-color);
            transition: background 0.5s, color 0.5s;
        }

        .navbar {
            background: linear-gradient(to right, var(--primary-color), var(--accent-color));
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .navbar-brand {
            font-size: 1.5em;
            font-weight: bold;
        }

        .hamburger {
            display: none;
            font-size: 2em;
            cursor: pointer;
            color: white;
            transition: transform 0.3s;
        }

        .hamburger:hover {
            transform: scale(1.1);
            text-shadow: 0 0 10px #fff, 0 0 20px var(--primary-color);
        }

        .navbar-menu {
            display: flex;
            gap: 20px;
            align-items: center;
        }

        .navbar-item {
            color: white;
            text-decoration: none;
            padding: 10px 15px;
            border-radius: 5px;
            transition: background 0.3s;
        }

        .navbar-item:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        .navbar-item.active {
            background: rgba(255, 255, 255, 0.3);
        }

        .theme-toggle {
            background: none;
            border: none;
            font-size: 1.5em;
            cursor: pointer;
            color: white;
            transition: transform 0.3s;
        }

        .theme-toggle:hover {
            transform: rotate(180deg);
        }

        .tab-content {
            display: none;
            padding: 20px;
            animation: fadeIn 0.5s;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .upload-container {
            text-align: center;
            padding: 50px;
            background: var(--card-bg);
            border-radius: 10px;
            box-shadow: var(--shadow);
            max-width: 600px;
            margin: 50px auto;
        }

        .upload-container h1 {
            font-size: 2em;
            margin-bottom: 20px;
            color: var(--primary-color);
        }

        .upload-container p {
            font-size: 1.2em;
            margin-bottom: 30px;
            color: var(--secondary-color);
        }

        .upload-area {
            display: flex;
            justify-content: center;
            gap: 10px;
        }

        input[type="file"] {
            padding: 10px;
            border-radius: 5px;
            background: var(--card-bg);
            color: var(--text-color);
            border: 1px solid var(--border-color);
        }

        button {
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s, transform 0.2s;
        }

        button:hover {
            background: var(--accent-color);
            transform: scale(1.05);
        }

        button.remove {
            background: #dc3545;
        }

        button.remove:hover {
            background: #c82333;
        }

        .card {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 20px;
            box-shadow: var(--shadow);
            margin-bottom: 20px;
        }

        .card h2 {
            font-size: 1.4em;
            margin-bottom: 15px;
            color: var(--primary-color);
        }

        .headers-section .header-row {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }

        .header-row input {
            flex: 1;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid var(--border-color);
            background: var(--card-bg);
            color: var(--text-color);
        }

        .editor-section {
            position: relative;
        }

        .search-bar {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }

        #searchInput {
            flex: 1;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid var(--border-color);
            background: var(--card-bg);
            color: var(--text-color);
        }

        #body {
            width: 100%;
            height: 400px;
            border-radius: 5px;
            padding: 10px;
            border: 1px solid var(--border-color);
            background: var(--card-bg);
            color: var(--text-color);
            resize: vertical;
        }

        .preview-container {
            border: 1px solid var(--border-color);
            border-radius: 5px;
            overflow: hidden;
            background: var(--card-bg);
        }

        .preview-header {
            padding: 10px;
            background: var(--secondary-color);
            color: white;
        }

        #previewIframe {
            width: 100%;
            height: 500px;
            border: none;
        }

        .attachment-item {
            display: flex;
            gap: 10px;
            align-items: center;
            padding: 10px;
            background: var(--card-bg);
            border-radius: 5px;
            margin-bottom: 10px;
            box-shadow: var(--shadow);
        }

        .controls {
            margin-top: 10px;
            display: flex;
            gap: 10px;
            justify-content: space-between;
        }

        .save-container {
            text-align: center;
            margin: 20px 0;
        }

        .popup {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--accent-color);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            box-shadow: var(--shadow);
            display: none;
            animation: slideIn 0.5s;
        }

        .popup-close {
            float: right;
            cursor: pointer;
            margin-left: 10px;
            font-weight: bold;
        }

        @keyframes slideIn {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @media (max-width: 768px) {
            .hamburger {
                display: block;
            }
            .navbar-menu {
                display: none;
                flex-direction: column;
                position: absolute;
                top: 60px;
                left: 0;
                width: 100%;
                background: var(--primary-color);
                padding: 20px;
            }
            .navbar-menu.active {
                display: flex;
            }
            .upload-container {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">Email Analyzer & Editor</div>
        <div class="hamburger" id="hamburger">☰</div>
        <div class="navbar-menu" id="navbarMenu">
            <a href="#" class="navbar-item active" data-tab="upload">Upload</a>
            <a href="#" class="navbar-item" data-tab="headers">Headers</a>
            <a href="#" class="navbar-item" data-tab="editor">Body Editor</a>
            <a href="#" class="navbar-item" data-tab="attachments">Attachments</a>
            <a href="#" class="navbar-item" data-tab="preview">Preview</a>
            <button class="theme-toggle" id="themeToggle">🌙</button>
        </div>
    </nav>

    <div class="tab-content active" id="upload">
        <div class="upload-container">
            <h1>Welcome to Email Analyzer & Editor</h1>
            <p>Upload your .eml file to get started</p>
            <div class="upload-area">
                <input type="file" id="emailFile" accept=".eml">
                <button id="uploadButton">Upload</button>
            </div>
        </div>
    </div>

    <div class="tab-content" id="headers">
        <div class="card headers-section">
            <h2>Headers</h2>
            <div id="headersContainer"></div>
            <button id="addHeaderButton">Add Header</button>
        </div>
    </div>

    <div class="tab-content" id="editor">
        <div class="card editor-section">
            <h2>Body Editor</h2>
            <div class="search-bar">
                <input type="text" id="searchInput" placeholder="Search in body...">
                <button id="searchButton">Find</button>
            </div>
            <textarea id="body" placeholder="Email content will appear here"></textarea>
            <div class="controls">
                <button id="toggleEditorButton">Toggle HTML/Rich Text</button>
            </div>
        </div>
    </div>

    <div class="tab-content" id="attachments">
        <div class="card attachments-section">
            <h2>Attachments</h2>
            <div id="attachmentsContainer"></div>
            <button id="addAttachmentButton">Add Attachment</button>
        </div>
    </div>

    <div class="tab-content" id="preview">
        <div class="card preview-section">
            <h2>Preview</h2>
            <div class="preview-container">
                <div class="preview-header">
                    <div id="previewSubject"></div>
                    <div id="previewFrom"></div>
                    <div id="previewTo"></div>
                </div>
                <iframe id="previewIframe"></iframe>
            </div>
        </div>
    </div>

    <div class="save-container">
        <button id="saveButton">Save Email</button>
    </div>

    <div class="popup" id="uploadPopup">
        File uploaded successfully! You can now modify Headers, Body Editor, Attachments, or Preview using the menu above.
        <span class="popup-close" onclick="document.getElementById('uploadPopup').style.display='none'">X</span>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            let emailData = { headers: [], body: { type: 'text/plain', content: '' }, attachments: [] };
            let isHtmlMode = false;
            let editorInitialized = false;
            let searchPosition = 0;
            let lastSearch = '';

            // Hamburger Menu Toggle
            const hamburger = document.getElementById('hamburger');
            const navbarMenu = document.getElementById('navbarMenu');
            hamburger.addEventListener('click', function() {
                navbarMenu.classList.toggle('active');
            });

            // Tab Switching
            document.querySelectorAll('.navbar-item').forEach(function(item) {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    document.querySelectorAll('.navbar-item').forEach(function(i) { i.classList.remove('active'); });
                    item.classList.add('active');
                    const tab = item.getAttribute('data-tab');
                    document.querySelectorAll('.tab-content').forEach(function(content) {
                        content.classList.toggle('active', content.id === tab);
                    });
                    if (window.innerWidth <= 768) {
                        navbarMenu.classList.remove('active');
                    }
                });
            });

            // Theme Toggle
            const themeToggle = document.getElementById('themeToggle');
            themeToggle.addEventListener('click', function() {
                document.body.classList.toggle('dark-theme');
                themeToggle.textContent = document.body.classList.contains('dark-theme') ? '☀️' : '🌙';
            });

            // Escape HTML
            function escapeHtml(text) {
                const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
                return text.replace(/[&<>"']/g, function(m) { return map[m]; });
            }

            // Upload Email
            async function uploadEmail() {
                const file = document.getElementById('emailFile').files[0];
                if (!file) return alert('Select an .eml file!');
                const formData = new FormData();
                formData.append('file', file);
                try {
                    const response = await fetch('/upload', { method: 'POST', body: formData });
                    if (!response.ok) throw new Error('Upload failed');
                    emailData = await response.json();
                    renderEmail();
                    initializeEditor();
                    updatePreview();
                    const popup = document.getElementById('uploadPopup');
                    popup.style.display = 'block';
                } catch (error) {
                    console.error('Upload Error:', error);
                    alert('Upload failed: ' + error.message);
                }
            }

            // Initialize TinyMCE
            function initializeEditor() {
                if (emailData.body.type === 'text/html' && !editorInitialized) {
                    tinymce.init({
                        selector: '#body',
                        height: 400,
                        plugins: 'advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table help wordcount',
                        toolbar: 'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
                        setup: function(editor) {
                            editor.on('Change', function() {
                                emailData.body.content = editor.getContent();
                                updatePreview();
                            });
                        }
                    });
                    editorInitialized = true;
                    document.getElementById('toggleEditorButton').style.display = 'block';
                } else {
                    document.getElementById('toggleEditorButton').style.display = 'none';
                }
            }

            // Render Email
            function renderEmail() {
                renderHeaders();
                renderBody();
                renderAttachments();
            }

            // Render Headers
            function renderHeaders() {
                const container = document.getElementById('headersContainer');
                container.innerHTML = '';
                emailData.headers.forEach(function(h, i) {
                    const row = document.createElement('div');
                    row.className = 'header-row';
                    row.innerHTML = `
                        <input type="text" value="${h.key}" placeholder="Key" oninput="emailData.headers[${i}].key = this.value; updatePreview()">
                        <input type="text" value="${h.value}" placeholder="Value" oninput="emailData.headers[${i}].value = this.value; updatePreview()">
                        <button class="remove" onclick="removeHeader(${i})">Remove</button>
                    `;
                    container.appendChild(row);
                });
            }

            // Render Body
            function renderBody() {
                document.getElementById('body').value = emailData.body.content || '';
            }

            // Render Attachments
            function renderAttachments() {
                const container = document.getElementById('attachmentsContainer');
                container.innerHTML = '';
                emailData.attachments.forEach(function(a, i) {
                    const item = document.createElement('div');
                    item.className = 'attachment-item';
                    item.innerHTML = `
                        ${a.filename} (${a.content_type})${a.content_id ? ' [Embedded: ' + a.content_id + ']' : ''}
                        <input type="file" onchange="updateAttachment(${i}, this.files[0])">
                        <button class="remove" onclick="removeAttachment(${i})">Remove</button>
                    `;
                    container.appendChild(item);
                });
            }

            // Add Header
            function addHeader() {
                emailData.headers.push({ key: '', value: '' });
                renderHeaders();
            }

            // Remove Header
            function removeHeader(index) {
                emailData.headers.splice(index, 1);
                renderHeaders();
                updatePreview();
            }

            // Update Attachment
            function updateAttachment(index, file) {
                if (!file) return;
                const reader = new FileReader();
                reader.onload = function() {
                    emailData.attachments[index] = {
                        filename: file.name,
                        content_type: file.type || 'application/octet-stream',
                        content_id: emailData.attachments[index].content_id || null,
                        data: reader.result.split(',')[1]
                    };
                    renderAttachments();
                    updatePreview();
                };
                reader.readAsDataURL(file);
            }

            // Remove Attachment
            function removeAttachment(index) {
                emailData.attachments.splice(index, 1);
                renderAttachments();
                updatePreview();
            }

            // Add Attachment
            function addAttachment() {
                const input = document.createElement('input');
                input.type = 'file';
                input.onchange = function() {
                    const file = input.files[0];
                    if (!file) return;
                    const contentId = prompt('Enter Content-ID (optional):');
                    const reader = new FileReader();
                    reader.onload = function() {
                        emailData.attachments.push({
                            filename: file.name,
                            content_type: file.type || 'application/octet-stream',
                            content_id: contentId || null,
                            data: reader.result.split(',')[1]
                        });
                        renderAttachments();
                        updatePreview();
                    };
                    reader.readAsDataURL(file);
                };
                input.click();
            }

            // Update Preview
            function updatePreview() {
                const subject = emailData.headers.find(function(h) { return h.key.toLowerCase() === 'subject'; })?.value || 'No Subject';
                const from = emailData.headers.find(function(h) { return h.key.toLowerCase() === 'from'; })?.value || '';
                const to = emailData.headers.find(function(h) { return h.key.toLowerCase() === 'to'; })?.value || '';
                
                document.getElementById('previewSubject').textContent = subject;
                document.getElementById('previewFrom').textContent = from ? `From: ${from}` : '';
                document.getElementById('previewTo').textContent = to ? `To: ${to}` : '';
                
                let content = editorInitialized && emailData.body.type === 'text/html' ? 
                    (tinymce.get('body')?.getContent() || document.getElementById('body').value) : 
                    document.getElementById('body').value;
                emailData.body.content = content;

                const iframe = document.getElementById('previewIframe');
                if (emailData.body.type === 'text/html') {
                    emailData.attachments.forEach(function(a) {
                        if (a.content_id && a.data) {
                            content = content.replace(`cid:${a.content_id}`, `data:${a.content_type};base64,${a.data}`);
                        }
                    });
                    iframe.srcdoc = `
                        <style>body { font-family: Arial, sans-serif; padding: 15px; color: var(--text-color); }</style>
                        ${content}
                    `;
                } else {
                    iframe.srcdoc = `<pre style="padding: 15px;">${escapeHtml(content)}</pre>`;
                }
            }

            // Toggle Editor
            function toggleEditor() {
                if (emailData.body.type !== 'text/html') return;
                if (!isHtmlMode) {
                    const content = tinymce.get('body')?.getContent();
                    tinymce.get('body')?.remove();
                    document.getElementById('body').value = content || emailData.body.content;
                    document.getElementById('toggleEditorButton').textContent = 'Switch to Rich Text';
                    editorInitialized = false;
                } else {
                    emailData.body.content = document.getElementById('body').value;
                    initializeEditor();
                    document.getElementById('toggleEditorButton').textContent = 'Switch to HTML';
                }
                isHtmlMode = !isHtmlMode;
                updatePreview();
            }

            // Search in Body
            function searchInBody() {
                if (isHtmlMode || !editorInitialized) {
                    const term = document.getElementById('searchInput').value;
                    if (!term) return;
                    const text = document.getElementById('body').value;
                    const start = (term === lastSearch) ? searchPosition + 1 : 0;
                    const pos = text.indexOf(term, start);
                    if (pos !== -1) {
                        document.getElementById('body').focus();
                        document.getElementById('body').setSelectionRange(pos, pos + term.length);
                        searchPosition = pos;
                        lastSearch = term;
                    } else {
                        const wrapPos = text.indexOf(term, 0);
                        if (wrapPos !== -1 && wrapPos < start) {
                            document.getElementById('body').setSelectionRange(wrapPos, wrapPos + term.length);
                            searchPosition = wrapPos;
                        } else {
                            alert('No more matches found');
                            searchPosition = 0;
                        }
                    }
                } else {
                    alert('Use TinyMCE search (Ctrl+F)');
                }
            }

            // Save Email
            async function saveEmail() {
                if (editorInitialized && !isHtmlMode) {
                    emailData.body.content = tinymce.get('body')?.getContent() || document.getElementById('body').value;
                } else {
                    emailData.body.content = document.getElementById('body').value;
                }
                try {
                    const response = await fetch('/save', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(emailData)
                    });
                    if (!response.ok) throw new Error('Save failed');
                    const blob = await response.blob();
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'modified_email.eml';
                    a.click();
                    URL.revokeObjectURL(url);
                } catch (error) {
                    console.error('Save Error:', error);
                    alert('Save failed: ' + error.message);
                }
            }

            // Event Listeners
            document.getElementById('uploadButton').addEventListener('click', uploadEmail);
            document.getElementById('addHeaderButton').addEventListener('click', addHeader);
            document.getElementById('addAttachmentButton').addEventListener('click', addAttachment);
            document.getElementById('toggleEditorButton').addEventListener('click', toggleEditor);
            document.getElementById('saveButton').addEventListener('click', saveEmail);
            document.getElementById('searchButton').addEventListener('click', searchInBody);
            document.getElementById('searchInput').addEventListener('keypress', function(e) { 
                if (e.key === 'Enter') searchInBody(); 
            });
            document.getElementById('body').addEventListener('input', function() {
                if (!editorInitialized) {
                    emailData.body.content = document.getElementById('body').value;
                    updatePreview();
                }
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return Response(HTML_TEMPLATE, mimetype='text/html')

@app.route('/upload', methods=['POST'])
def upload_email():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    eml_file = request.files['file']
    try:
        msg = email.message_from_binary_file(eml_file.stream, policy=email.policy.default)
    except Exception as e:
        return jsonify({'error': f'Invalid .eml file: {str(e)}'}), 400

    headers = [{'key': k, 'value': v} for k, v in msg.items()]
    body = None
    body_type = 'text/plain'
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
                body_type = 'text/html'
                break
            elif part.get_content_type() == 'text/plain' and not body:
                body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='replace')
        body_type = msg.get_content_type()

    attachments = []
    for part in msg.iter_attachments():
        filename = part.get_filename() or 'unnamed'
        content_type = part.get_content_type()
        content_id = part.get('Content-ID', '').strip('<>')
        data = part.get_payload(decode=True)
        data_b64 = base64.b64encode(data).decode('utf-8') if data else None
        attachments.append({
            'filename': filename,
            'content_type': content_type,
            'content_id': content_id or None,
            'data': data_b64
        })

    return jsonify({
        'headers': headers,
        'body': {'type': body_type, 'content': body or ''},
        'attachments': attachments
    })

@app.route('/save', methods=['POST'])
def save_email():
    try:
        data = request.json
        if not data or 'body' not in data:
            return jsonify({'error': 'Invalid data'}), 400
            
        headers = data.get('headers', [])
        body_type = data['body'].get('type', 'text/plain')
        body_content = data['body'].get('content', '')
        attachments = data.get('attachments', [])
        
        msg = EmailMessage()
        for header in headers:
            if header.get('key') and header.get('value'):
                msg[header['key']] = header['value']
        
        if body_type == 'text/html':
            msg.add_alternative(body_content, subtype='html')
        else:
            msg.set_content(body_content)
        
        for att in attachments:
            if att.get('data'):
                att_data = base64.b64decode(att['data'])
                content_type = att.get('content_type', 'application/octet-stream')
                maintype, subtype = content_type.split('/', 1) if '/' in content_type else ('application', 'octet-stream')
                part = MIMEBase(maintype, subtype)
                part.set_payload(att_data)
                if att.get('filename'):
                    part.add_header('Content-Disposition', 'attachment', filename=att['filename'])
                if att.get('content_id'):
                    part.add_header('Content-ID', f"<{att['content_id']}>")
                msg.attach(part)
        
        eml_data = msg.as_bytes()
        return send_file(
            io.BytesIO(eml_data),
            mimetype='message/rfc822',
            as_attachment=True,
            download_name='modified_email.eml'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
