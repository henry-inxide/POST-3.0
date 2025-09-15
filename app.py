from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stylish Web Panel</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            display: flex;
            height: 100vh;
            background-color: #f4f4f4;
        }

        /* Sidebar */
        .sidebar {
            width: 250px;
            background: #1e1e2f;
            color: white;
            display: flex;
            flex-direction: column;
            padding: 20px;
        }

        .sidebar h2 {
            text-align: center;
            margin-bottom: 30px;
        }

        .sidebar a {
            color: white;
            text-decoration: none;
            padding: 12px 15px;
            margin: 5px 0;
            border-radius: 8px;
            display: block;
            transition: background 0.3s ease;
        }

        .sidebar a:hover {
            background: #3e3e5e;
        }

        /* Main content */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        /* Top bar */
        .topbar {
            background: white;
            padding: 15px 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Dashboard content */
        .content {
            padding: 20px;
        }

        .card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
    </style>
</head>
<body>

    <div class="sidebar">
        <h2>HENRY-X</h2>
        <a href="#">Dashboard</a>
        <a href="#">Users</a>
        <a href="#">Settings</a>
        <a href="#">Reports</a>
        <a href="#">Logout</a>
    </div>

    <div class="main-content">
        <div class="topbar">
            <h3>Dashboard</h3>
            <p>Hello, Henry 👋</p>
        </div>

        <div class="content">
            <div class="card">
                <h4>Welcome!</h4>
                <p>This A Stylish Web Servers Made By Henry.</p>
            </div>

            <div class="card">
                <h4>Statistics</h4>
                <p>Show data visualizations or recent activity here.</p>
            </div>
        </div>
    </div>

</body>
</html>
''')

if __name__ == "__main__":
    app.run(debug=True)
