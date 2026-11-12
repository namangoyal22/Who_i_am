# WinGo Results Archive

A small Flask website that displays the latest published historical results. It does not generate predictions or betting recommendations.

## Run locally
1. Install Python 3.10+.
2. In this folder run: `pip install -r requirements.txt`
3. Run: `python app.py`
4. Open `http://127.0.0.1:5000`

## Deploy free on Render
1. Create a GitHub repository and upload these files.
2. In Render, choose **New +** → **Web Service** and connect the repository.
3. Render can use the included `render.yaml`; otherwise set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
4. Deploy. Render will provide a public `onrender.com` URL.

The page refreshes every 30 seconds. The source endpoint may change or become unavailable.
