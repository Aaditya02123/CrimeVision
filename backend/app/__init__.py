# CrimeVision AI Backend Package
# Ensure compatibility between Starlette 1.3.x and FastAPI 0.111.x
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
