from PIL import Image, ImageDraw, ImageFont
import inflect
import qrcode
from newdatabase import generate_random_code,insert_data
import os

def create_invoice_img(data):
    customer_name=data.customer_name    
    customer_no=data.customer_num    
    customer_addr=data.customer_addr    
    date_period=data.customer_dop    
    date_of_purchase=data.customer_dop    
    invoice_no=generate_random_code(6) #generating invoice code   
    placeofsupply=data.customer_pos    
    supplytypecode=data.supplycode    
    doctypecode=data.doctype
    note1=data.note1
    note2=data.note2
    irn='afgfgdsfsfafadafgdrhtehkvsrj\nasdfgasdfgasdfgasdfgasdfgasd\nasdfga'   

    img = Image.open('images\\invoice_template.jpg')
    draw = ImageDraw.Draw(img)
    text_color = (0, 0, 0)  # black color
    myFont = ImageFont.truetype('times new roman bold.ttf', 11)
    
    #adding invoice no
    text_position = (525, 220)
    text_to_add = str(invoice_no)
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding date_period
    text_position = (525, 236)
    text_to_add = date_period
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding placeofsupply
    text_position = (525, 252)
    text_to_add = placeofsupply
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding customer_name
    text_position = (430, 68)
    text_to_add = customer_name
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding customer_number
    text_position = (430, 88)
    text_to_add = customer_no
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding customer_addr
    text_to_add=customer_addr.split()
    if len(text_to_add)<=4:
        text_to_add=" ".join(text_to_add)
        text_position = (380, 106)
        draw.text(text_position, text_to_add,font=myFont,fill=text_color)
    else:
        text_position = (380, 106)
        text_to_add=" ".join(text_to_add[:4])+'\n'+' '.join(text_to_add[5:])
        draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding dateofpurchase
    text_position = (435, 145)
    text_to_add = str(date_of_purchase)
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding supplytypecode
    text_position = (532, 282)
    text_to_add = supplytypecode
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding documenttypecode
    text_position = (532, 298)
    text_to_add = doctypecode
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding irn
    text_position = (435, 340)
    text_to_add = irn
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding item details
    add_item(data,draw,myFont,text_color)

    #adding totalvalue
    text_to_add ='$'+ str(data.totalamount)
    Font = ImageFont.truetype('times new roman bold.ttf', 41)
    for i in range(1,11):
        if len(str(data.totalamount))==i:
            text_position = (520-15*i, 565)
            draw.text(text_position, text_to_add,font=Font,fill=text_color)
            break

    #adding no.tostr
    text_to_add=number_to_words(data.totalamount).split()
    if len(text_to_add)<=4:
        text_to_add=" ".join(text_to_add)+' only'
        text_position = (390, 610)
        draw.text(text_position, text_to_add,font=myFont,fill=text_color)
    else:
        text_position = (390, 610)
        text_to_add=" ".join(text_to_add[:4])+'\n'+' '.join(text_to_add[5:])+' only'
        draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding subtotal
    text_position = (493, 658)
    text_to_add='$'+str(data.totalsubamount)
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)

    #adding cgst and sgst
    text_position = (493, 678)
    text_to_add="$"+str(data.cgst)+"\n"+"$"+str(data.sgst)
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)    

    #adding signature
    sign = Image.open("images\\signature_image.jpg")
    sign = sign.resize((150, 65))  # Adjust the size as needed
    position = (80, 590)
    img.paste(sign, position)

    #adding qr code
    add_qr(img,data,invoice_no)
    
    #adding notes
    text_to_add=note1
    text_position=(87,652)
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)    

    text_to_add=note2
    text_position=(87,695)
    draw.text(text_position, text_to_add,font=myFont,fill=text_color)    

    img.save(f'Output_images/{invoice_no}.jpg')

    imgpath=f'Output_images\\{invoice_no}.jpg'    
    
    insert_data(data,invoice_no,imgpath)

    # os.system(imgpath)

    return imgpath,invoice_no

def add_item(data,draw,font,fill):

        i=1
        items=data.items
        no_of_items=len(data.items)
        if no_of_items>1:
            x=36
            y=440
            for item in items:                
                #adding item serial number
                text_position = (x, y)
                text_to_add=str(i)+'.'
                draw.text(text_position, text_to_add,font=font,fill=fill)
                i=i+1

                #adding item name
                item_name=item.itemName
                text_position=(x+30,y)
                draw.text(text_position, item_name,font=font,fill=fill)

                #adding item quantity
                item_quantity=item.quantity
                text_position=(x+270,y)
                draw.text(text_position, str(item_quantity),font=font,fill=fill)

                #adding item price
                item_price=item.price
                text_position=(x+340,y)
                draw.text(text_position, str(item_price),font=font,fill=fill)

                #adding amount details
                amount_2='$'+str(item.totalAmount)
                text_position=(x+480,y)
                draw.text(text_position, str(amount_2),font=font,fill=fill)

                #adding gst
                text_position=(x+400,y)
                gst_amount=float(item.totalAmount)*float(item.gst)/100
                text_to_add=str(gst_amount)+f" ({item.gst}%)"
                draw.text(text_position, text_to_add,font=font,fill=fill)

                y=y+20 # for going in next line

        else:
            x=36
            y=440
            text_position = (x, y)

            text_to_add = str(1) + '.'
            draw.text(text_position, text_to_add,font=font,fill=fill)

            #adding item name
            item_name=data.items[0].itemName
            text_position=(x+30,y)
            draw.text(text_position, item_name,font=font,fill=fill)

            #adding item quantity
            item_quantity=data.items[0].quantity
            text_position=(x+270,y)
            draw.text(text_position, str(item_quantity),font=font,fill=fill)

            #adding item price
            item_price=data.items[0].price
            text_position=(x+340,y)
            draw.text(text_position, str(item_price),font=font,fill=fill)

            #adding amount details
            amount=data.items[0].totalAmount
            amount_2='$'+str(amount)
            text_position=(x+480,y)
            draw.text(text_position, amount_2,font=font,fill=fill)

            #adding gst
            text_position=(x+400,y)
            gst_amount=float(amount)*float(data.items[0].gst)/100
            text_to_add=str(gst_amount)+f" ({data.items[0].gst}%)"
            draw.text(text_position,str(text_to_add),font=font,fill=fill)

    
def number_to_words(number):
    p = inflect.engine()
    return p.number_to_words(number).title()

def add_qr(img,data,invocieno):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
    text_to_add=str(invocieno)+" "+str(data)
    qr.add_data(text_to_add)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image =qr_image.resize((150, 150))
    position = (31, 250)
    img.paste(qr_image, position)
