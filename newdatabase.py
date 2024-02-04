import random
import string
import sqlite3

def generate_random_code(length):
    characters = string.ascii_letters + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(length))
    checkcode(random_code)
    return random_code

def checkcode(code):
    connection = sqlite3.connect('example.db')

    cursor = connection.cursor()

    cursor.execute("select count(InvoiceNum) from Invoices where InvoiceNum=?",(code,))
    rows=cursor.fetchone()
    
    try:
        if rows[0]==0:
            connection.commit()
            connection.close()
        else:
            connection.commit()
            connection.close()
            generate_random_code(5)
    
    except Exception as e:
        print(e)

def insert_data(data,invoiceno,imgpath):

    customer_name=data.customer_name    
    customer_no=data.customer_num    
    customer_addr=data.customer_addr       
    date_of_purchase=data.customer_dop    
    placeofsupply=data.customer_pos    
    supplytypecode=data.supplycode    
    doctypecode=data.doctype 
    note1=data.note1
    note2=data.note2
    noofitems=len(data.items)
    totalAmount=data.totalamount
    totalsubamount=data.totalsubamount
    sgst=data.sgst
    cgst=data.cgst

    try:
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()
        
        insert_query='''Insert into Invoices 
                        (InvoiceNum,CustomerName,CustomerNum,CustomerAddr,CustomerDop,CustomerPOS,SupplyCode,DocType,NoofItems,Sgst,Cgst,TotalAmount,TotalSubAmount,Note1,Note2,LocalImageURL) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        
        cursor.execute(insert_query,(invoiceno,customer_name,customer_no,customer_addr,date_of_purchase,placeofsupply,supplytypecode,doctypecode,noofitems,sgst,cgst,totalAmount,totalsubamount,note1,note2,imgpath))

        for item in data.items:
            itemName=item.itemName
            quantity=item.quantity
            price=item.price
            gst=item.gst
            totalitemamount=item.totalAmount

            insert_query='''Insert into Items
                            (itemname,itemquantity,price,gst,itemtotalvalue,invoicenum) values (?,?,?,?,?,?)'''

            cursor.execute(insert_query,(itemName,quantity,price,gst,totalitemamount,invoiceno))
                
    except Exception as e:
        print(e)
    
    finally:
        connection.commit()
        cursor.close()
        connection.close()

def searchinvoice(data):
    invoiceno=data.invoiceno
    dop=data.dop
    connection=sqlite3.connect('example.db')
    cursor = connection.cursor()
    query="Select LocalImageURL from Invoices where InvoiceNum=? and CustomerDop=?"
    parameters=(invoiceno,dop)
    cursor.execute(query,parameters)

    rows=cursor.fetchone()

    print(rows)
    
    if rows:
        link=rows[0]
        if link!=None:
            response=link
            print(response)
            cursor.close()
            connection.close()
            return response
        else:
            response="null"
            print(response)
            cursor.close()
            connection.close()
            return response
    else:
        response="null"
        print(response)
        cursor.close()
        connection.close()
        return response

def checksignup(data):
    nameofuser=data.name_of_user
    mobileno=data.mobileno
    username=data.username
    emailid=data.emailid
    password=data.password
    accformdate=data.accformdate
    
    connection = sqlite3.connect('example.db')

    cursor = connection.cursor()

    query_check="Select count(*) from Users where (username=? or mobileno=? or emailid=?)"

    parameters=(username,mobileno,emailid)

    cursor.execute(query_check,parameters)
    rows=cursor.fetchone()

    if rows[0]!=0:
        response={}
        query="Select mobileno,emailid from Users where mobileno=? or emailid=?"
        parameters=(mobileno,emailid)
        cursor.execute(query,parameters)
        rows=cursor.fetchall()
        for row in rows:
            if row[0]==mobileno and row[1]==emailid:                
                response={"Status":"User already exists","MatchingData":"Same MobileNo and Email Exists"}
                cursor.close()
                connection.close()
                return response
            elif row[0]==mobileno:
                response={"Status":"User already exists","MatchingData":"Same MobileNo Exists"}
            elif row[1]==emailid:          
                response={"Status":"User already exists","MatchingData":"Same Email Exists"}
        cursor.close()
        connection.close()
        return response
    else:
        values=(nameofuser,mobileno,username,emailid,password,accformdate)
        insert_query="Insert into Users (name_of_user,mobileno,username,emailid,password,dateaccformation) values (?,?,?,?,?,?)"
        cursor.execute(insert_query,values)
        connection.commit()
        cursor.close()
        connection.close()
        response={"Status":"User already not exists"}
        return response
    
def checksignin(data):
    username=data.username
    password=data.password

    connection = sqlite3.connect('example.db')

    cursor = connection.cursor()

    query_check="Select count(*) from Users where username=? and password=?"
    values=(username,password)

    cursor.execute(query_check,values)
    
    rows=cursor.fetchone()
    if rows[0]!=0:
        cursor.close()
        connection.close()
        return "User already exists"
    else:
        return "User already not exists"

def checkforgotpass(data):
    username=data.username
    email=data.email
    mobileno=data.mobileno
    
    connection = sqlite3.connect('example.db')

    cursor = connection.cursor()

    if username=="":
        query_check="Select name_of_user from users where mobileno=? and emailid=?"
        values=(mobileno,email)
        cursor.execute(query_check,values)
        rows=cursor.fetchone()
        print(rows)
        if rows!=None:
            response={"Status":"User Exists","NameOfUser":rows[0]}
            cursor.close()
            connection.close()
            return response
        else:
            response={"Status":"User Not Exists","NameOfUser":rows}
            cursor.close()
            connection.close()
            return response

    elif email=="":
        query_check="Select name_of_user from users where username=? and mobileno=?"
        values=(username,mobileno)
        cursor.execute(query_check,values)
        rows=cursor.fetchone()
        if rows!=None:
            response={"Status":"User Exists","NameOfUser":rows[0]}
            cursor.close()
            connection.close()
            return response
        else:
            response={"Status":"User Not Exists","NameOfUser":rows}
            cursor.close()
            connection.close()
            return response       

    elif mobileno=="":
        query_check="Select name_of_user from users where username=? and emailid=?"
        values=(username,email)
        cursor.execute(query_check,values)
        rows=cursor.fetchone()
        if rows!=None:
            response={"Status":"User Exists","NameOfUser":rows[0]}
            cursor.close()
            connection.close()
            return response
        else:
            response={"Status":"User Not Exists","NameOfUser":rows}
            cursor.close()
            connection.close()
            return response

    else:
        query_check="Select name_of_user from users where mobileno=? and emailid=? and username=?"
        values=(mobileno,email,username)
        cursor.execute(query_check,values)
        rows=cursor.fetchone()
        if rows!=None:
            response={"Status":"User Exists","NameOfUser":rows[0]}
            cursor.close()
            connection.close()
            return response
        else:
            response={"Status":"User Not Exists","NameOfUser":rows}
            cursor.close()
            connection.close()
            return response

def changepassword(data):
    username=data.Username
    email=data.Email
    mobileno=data.Mobileno
    newpass=data.NewPassword
    extracted_username=""
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()

    if username=="":
        query_check="Select username from users where mobileno=? and emailid=?"
        values=(mobileno,email)
        cursor.execute(query_check,values)
        rows=cursor.fetchone()
        extracted_username=rows[0]
    elif mobileno=="" or email=="":
        extracted_username=username

    updatequery="Update Users set password=? where (username=?)"
    values=(newpass,extracted_username)

    cursor.execute(updatequery,values)
    connection.commit()
    cursor.close()
    connection.close()
    
    response={"Status":"Done"}

    return response