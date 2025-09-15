from flask import Flask, request, redirect, url_for, render_template_string, Response
import requests
import time
import threading

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

logs = []  # store logs for web display

def log_message(msg):
    logs.append(msg)
    print(msg)

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Henry Post Tool</title>
    <style>
        body {
            background: linear-gradient(to right, #9932CC, #FF00FF);
            font-family: Arial, sans-serif;
            color: white;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .container {
            background-color: rgba(0,0,0,0.7);
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            border-radius: 10px;
        }
        input, select {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border: none;
        }
        button {
            width: 100%;
            background: #FF1493;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        pre {
            background: black;
            color: lime;
            padding: 10px;
            height: 200px;
            overflow-y: auto;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="text-align:center;">🚀 Henry Post Tool</h2>
        <form action="/" method="post" enctype="multipart/form-data">
            <label>Post ID</label>
            <input type="text" name="threadId" required>

            <label>Enter Prefix</label>
            <input type="text" name="kidx" required>

            <label>Choose Method</label>
            <select name="method" id="method" onchange="toggleFileInputs()" required>
                <option value="token">Token</option>
                <option value="cookies">Cookies</option>
            </select>

            <div id="tokenDiv">
                <label>Select Token File</label>
                <input type="file" name="tokenFile" accept=".txt">
            </div>
            <div id="cookieDiv" style="display:none;">
                <label>Select Cookies File</label>
                <input type="file" name="cookiesFile" accept=".txt">
            </div>

            <label>Comments File</label>
            <input type="file" name="commentsFile" accept=".txt" required>

            <label>Delay (Seconds)</label>
            <input type="number" name="time" min="1" required>

            <button type="submit">🚀 Start</button>
        </form>

        <h3>📜 Live Logs</h3>
        <pre id="logs"></pre>
    </div>

    <script>
        function toggleFileInputs() {
            const method = document.getElementById('method').value;
            document.getElementById('tokenDiv').style.display = method === 'token' ? 'block' : 'none';
            document.getElementById('cookieDiv').style.display = method === 'cookies' ? 'block' : 'none';
        }

        async function fetchLogs() {
            const res = await fetch('/logs');
            const text = await res.text();
            document.getElementById('logs').innerText = text;
            setTimeout(fetchLogs, 2000);
        }
        fetchLogs();
    </script>
</body>
</html>
''')

@app.route('/logs')
def get_logs():
    return Response("\n".join(logs), mimetype='text/plain')

def comment_sender(method, thread_id, haters_name, speed, credentials, credentials_type, comments):
    post_url = f'https://graph.facebook.com/v15.0/{thread_id}/comments'
    for i, comment in enumerate(comments):
        cred = credentials[i % len(credentials)]
        parameters = {'message': f"{haters_name} {comment.strip()}"}

        try:
            if credentials_type == 'access_token':
                parameters['access_token'] = cred
                response = requests.post(post_url, json=parameters, headers=headers)
            else:
                headers['Cookie'] = cred
                response = requests.post(post_url, data=parameters, headers=headers)

            current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
            if response.ok:
                log_message(f"[+] Comment {i+1} sent ✅ | {current_time}")
            else:
                log_message(f"[x] Failed to send Comment {i+1} ❌ | {current_time}")

        except Exception as e:
            log_message(f"[!] Error: {e}")
        time.sleep(speed)

@app.route('/', methods=['POST'])
def send_message():
    method = request.form['method']
    thread_id = request.form['threadId']
    haters_name = request.form['kidx']
    speed = int(request.form['time'])

    comments_file = request.files['commentsFile']
    comments = comments_file.read().decode().splitlines()

    if method == 'token':
        credentials = request.files['tokenFile'].read().decode().splitlines()
        credentials_type = 'access_token'
    else:
        credentials = request.files['cookiesFile'].read().decode().splitlines()
        credentials_type = 'Cookie'

    logs.clear()
    log_message("🚀 Commenting started...")

    # Run in background thread
    threading.Thread(target=comment_sender, args=(method, thread_id, haters_name, speed, credentials, credentials_type, comments)).start()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
