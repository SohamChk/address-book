from accounts.views import router as AcountRouter   # Account route imports
from address.views import router as AddressRouter   # Address Route Import
from backend.views import router as BaseRouter

def include_router(app):
    app.include_router(BaseRouter)

    #  Accounts route registration
    app.include_router(AcountRouter)

    #  Address route registration
    app.include_router(AddressRouter)