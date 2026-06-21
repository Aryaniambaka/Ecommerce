from fastapi import FastAPI,Depends,status,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.Oauth2 import current_user
from app.Router import user ,auth ,seller,product,cart,Buy
from . import model,schemas,Oauth2


app=FastAPI()
app.include_router(user.router)
app.include_router(product.router)
app.include_router(auth.router)
app.include_router(seller.router)
app.include_router(Buy.router)
app.include_router(cart.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/current",status_code=status.HTTP_200_OK,response_model=schemas.Current_user_detail)
def get_user_detail(current_user:model.User=Depends(Oauth2.current_user)):
    return{"email":current_user.email,"id":current_user.id,"role":current_user.role}
