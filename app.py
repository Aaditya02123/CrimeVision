try:
    import starlette.routing
    if not hasattr(starlette.routing.Router, "_crimevision_patched"):
        _orig_router_init = starlette.routing.Router.__init__
        def _patched_router_init(self, *args, on_startup=None, on_shutdown=None, **kwargs):
            self.on_startup = list(on_startup or [])
            self.on_shutdown = list(on_shutdown or [])
            return _orig_router_init(self, *args, **kwargs)
        starlette.routing.Router.__init__ = _patched_router_init
        starlette.routing.Router._crimevision_patched = True
except Exception:
    pass

import os
from fastapi import FastAPI, Request, Response
import httpx

# Top-level ASGI application instances for Vercel
app = FastAPI(title="App Service Gateway")
application = app
handler = app

@app.get("/")
def root():
    backend_url = os.environ.get("BACKEND_URL", "")
    return {
        "service": "app",
        "backend_url_configured": bool(backend_url),
        "status": "online"
    }

@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_to_backend(path: str, request: Request):
    backend_url = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
    target_url = f"{backend_url.rstrip('/')}/api/{path}"
    headers = dict(request.headers)
    headers.pop("host", None)
    body = await request.body()
    async with httpx.AsyncClient(timeout=35.0) as client:
        res = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=dict(request.query_params)
        )
        return Response(content=res.content, status_code=res.status_code, headers=dict(res.headers))
