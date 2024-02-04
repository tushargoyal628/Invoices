import base64
from fastapi import FastAPI,Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from newdatabase import searchinvoice,checksignup,checksignin,checkforgotpass,changepassword
from createinvoice import create_invoice_img
import os

app = FastAPI()

class Item(BaseModel):
    invoiceno: str
    dop: str 

class Items(BaseModel):
    itemName: str
    quantity: str
    price: str
    gst: str
    totalAmount: str

class InvoiceRequest(BaseModel):
    customer_name: str
    customer_num: str
    customer_addr: str
    customer_dop: str
    customer_invoicenum: str
    customer_pos: str
    supplycode: str
    doctype: str
    items: list[Items]
    sgst: str
    cgst: str
    totalamount: str
    totalsubamount: str
    note1: str
    note2: str

class Handlesignup(BaseModel):
    name_of_user:str
    mobileno: str
    username:str
    emailid:str
    password:str
    accformdate:str

class Handlesignin(BaseModel):
    username:str
    password:str

class Handleforgotpass(BaseModel):
    username:str
    email:str
    mobileno: str

class Changepassword(BaseModel):
    Username:str
    Email:str
    Mobileno:str
    NewPassword:str

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"))

@app.get("/main", response_class=HTMLResponse,include_in_schema=False)
async def read_item(request: Request):
    data = {"message": "Hello, FastAPI with Jinja2!"}
    return templates.TemplateResponse("main.html", {"request": request, "data": data})

@app.get("/searchpage", response_class=HTMLResponse,include_in_schema=False)
async def read_item(request: Request):
    data = {"message": "Hello, FastAPI with Jinja2!"}
    return templates.TemplateResponse("search.html", {"request": request, "data": data})

@app.get("/forgotpass", response_class=HTMLResponse,include_in_schema=False)
async def read_item(request: Request):
    data = {"message": "Hello, FastAPI with Jinja2!"}
    return templates.TemplateResponse("forgotpass.html", {"request": request, "data": data})

@app.get("/signup", response_class=HTMLResponse,include_in_schema=False)
async def read_item(request: Request):
    data = {"message": "Hello, FastAPI with Jinja2!"}
    return templates.TemplateResponse("signup.html", {"request": request, "data": data})

@app.get("/signin", response_class=HTMLResponse,include_in_schema=False)
async def read_item(request: Request):
    data = {"message": "Hello, FastAPI with Jinja2!"}
    return templates.TemplateResponse("signin.html", {"request": request, "data": data})


@app.get("/", response_class=HTMLResponse,include_in_schema=False)
async def read_item(request: Request):
    data = {"message": "Hello, FastAPI with Jinja2!"}
    return templates.TemplateResponse("homepage.html", {"request": request, "data": data})

@app.post("/searchinvoice")
async def search_invoice_view(item:Item):
    path=searchinvoice(item)
    if path!="null":
        response=FileResponse(path, media_type="image/jpg")
        return response
    else:
        return "null"

@app.post("/submit")
async def handle_form_submission(item:InvoiceRequest):
    path,invoiceno=create_invoice_img(item)
    if path!="null":
        file=FileResponse(path, media_type="image/jpg")
        with open(path, "rb") as file:
            file = file.read()
        file_content_base64 = base64.b64encode(file).decode("utf-8")
        response={"File":file_content_base64,"Invoice":invoiceno}
        return response
    else:
        return "null"

@app.post("/handlesignup")
async def handle_sign_up(item:Handlesignup):
    response=checksignup(item)
    return response

@app.post("/handlesignin")
async def handle_sign_in(item:Handlesignin):
    status=checksignin(item)
    response={"Status":status}
    return response

@app.post("/handleforgotpass")
async def handle_forgot_pass(item:Handleforgotpass):
    response=checkforgotpass(item)
    return response

@app.post("/changepassword")
async def handle_changepass(item:Changepassword):
    response=changepassword(item)
    return response
