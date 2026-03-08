import io
from flask import Flask, send_file, render_template_string, request
from resume_generator import generate_pdf

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Resume - Patrick Maclea</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #1a1a2e;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .toolbar {
            background: #16213e;
            padding: 12px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid #0f3460;
        }
        .toolbar h1 {
            color: #e8e8e8;
            font-size: 16px;
            font-weight: 500;
        }
        .btn {
            background: #00b894;
            color: #fff;
            border: none;
            padding: 8px 20px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            text-decoration: none;
            transition: background 0.2s;
        }
        .btn:hover { background: #00a381; }
        .viewer {
            flex: 1;
            display: flex;
            justify-content: center;
            padding: 0;
        }
        .viewer iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
</head>
<body>
    <div class="toolbar">
        <h1>Patrick Maclea - Resume</h1>
        <a class="btn" href="/pdf?download=1">Download PDF</a>
    </div>
    <div class="viewer">
        <iframe src="/pdf"></iframe>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/pdf")
def pdf():
    buf = generate_pdf(io.BytesIO())
    download = request.args.get("download")
    if download:
        return send_file(buf, mimetype="application/pdf", as_attachment=True,
                         download_name="patrick_maclea_resume.pdf")
    return send_file(buf, mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=True, port=5050)
