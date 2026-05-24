from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Cukiernia</title>
        </head>
        <body style="
            background-color:#f7d9e3;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
            font-family:Arial;
        ">
            <h1>Cukiernia</h1>
        </body>
    </html>
    """
