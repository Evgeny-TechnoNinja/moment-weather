from app import app


@app.route('/')
def index():
    return "<h1>Work test app</h1>"
