from fastapi.middleware.wsgi import WSGIMiddleware
from main import app as fastapi_app


# Create a dummy WSGI app that wraps FastAPI
# (PythonAnywhere only runs WSGI, so this is the bridge)
app = WSGIMiddleware(fastapi_app)
