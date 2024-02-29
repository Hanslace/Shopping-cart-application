import customtkinter
from PIL  import  Image
import uuid
import secrets
import hashlib


## For a Secure password ##
def hash_password(password, salt=None):

    if salt is None:
        salt = secrets.token_hex(16)  # Generate a random salt

    # Combine password and salt, and hash the result
    hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    
    return (hashed_password, salt)


## For the ease of displaying a message ##
def GUI_Wrapper(text, time = 2 ,font_size = 40 , font_style = "roman"):

    wraplabel = customtkinter.CTkLabel(master= root, text=text, font=("arial" ,font_size , font_style))
    wraplabel.place(rely=0.5 , relx = 0.5 ,anchor = "center"  )
    root.after(time*1000 , lambda : wraplabel.destroy())


## Changing frames ##
def change_frame(function , time =2 , x =[]):

    global frame
    frame.destroy()
    root.after(time*1000 , function , *x)


## Making a frame ##
def make_frame() :

    global frame

    # Incase of multiple clicks, make sure no multiple frames are made
    try:
        if frame :
            frame.destroy()
    except:
        pass
    
    frame= customtkinter.CTkFrame(master= root)
    frame.pack(pady=60 , padx = 60 , fill ="both" , expand =True)


## Make a sleeker frame ##
def make_fit_frame():
    
    global frame

    # Incase of multiple clicks, make sure no multiple frames are made
    try:
        if frame :
            frame.destroy()
    except:
        pass

    frame= customtkinter.CTkFrame(master= root)
    frame.place(rely=0.5 , relx = 0.5 ,anchor = "center" ) 


## Login page ##
def login_page():

    make_fit_frame()

    label = customtkinter.CTkLabel(master=frame , text="Login Information" ,font= ("arial" , 50))
    label.pack(pady=20 , padx = 40  )

    id = customtkinter.CTkEntry(master=frame  ,placeholder_text="Manager ID")
    id.pack(pady=20 , padx = 40  )
    
    password = customtkinter.CTkEntry(master=frame , placeholder_text="Password" , show = "*")
    password.pack(pady=20 , padx = 40  )

    button = customtkinter.CTkButton(master =frame , text = "Login" , command = lambda : login(id.get() , password.get()) )
    button.pack(pady=20 , padx = 40  )


## Verification ##
def login(x, y):

    manager = data["Managers"].get(x, None)

    # Check if manager exists
    if manager :

        # Hash the inserted password
        password_key_pair = hash_password(y , manager["Password"][1])

        # Match with stored password
        if manager["Password"] == list(password_key_pair) :
            GUI_Wrapper('Welcome back ' + manager["Name"])
            change_frame(show_menu)
        else : 
            GUI_Wrapper('Invalid ID or Password')
            change_frame(login_page)

    else :
        GUI_Wrapper('Invalid ID or Password')
        change_frame(login_page)
        

## Menu ##
def show_menu ():

    # For frequently updating the product list
    with open("Database\\Products.txt" , "w") as f :

        for productid in data["Products"] :
            f.write(productid + '\n')

            for attribute in data["Products"][productid] :
                f.write(str(data["Products"][productid][attribute]) + '\n')

            f.write('\n')

    make_frame()
               
    scroll = customtkinter.CTkScrollableFrame(frame ,label_text = "Select any product")
    scroll.pack( pady=60 , padx = 60 , fill ="both" , expand =True )
    scroll.columnconfigure([0,1,2,3,4,5], weight = 1)

 
    # To arrange the products in grids
    colnum = 0
    rownum = 0
    for productID in data["Products"]  :

        product = data["Products"][productID]

        if colnum % 6 == 0:
            rownum +=1
            colnum = 0
        
        # if image is present, display it
        try:
            img = customtkinter.CTkImage(dark_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(200,200))
        except :
            img =None

        choice = customtkinter.CTkButton(scroll ,image=img,compound = "top" ,font = ("arial" ,20) ,text = f'Name : {product["Name"]} \nCost : Rs. {product["Cost"]}/- \nStock : {product["Stock"]} left \nType : {product["Type"]}\n Rating : {"*"*round(product["Rating"])} \nSales : {product["Sales"]}', text_color= ('white','black')  , command= lambda f = productID :  change_frame(select_product , 2 ,[f]))
        choice.grid(column  =colnum , row = rownum, sticky = 'nsew' , padx = 10 , pady = 10)
        colnum += 1

    searchcase = customtkinter.CTkEntry(master=frame , placeholder_text="Search case")
    searchcase.pack(pady=20 , padx = 40)

    button1 = customtkinter.CTkButton(master =frame , text = "Search" , command= lambda :  search_in_products(scroll , searchcase.get())  )
    button1.pack(pady=20 , padx = 20  )  

    button2 = customtkinter.CTkButton(master =frame , text = "Add a product" , command= lambda : change_frame(new_product)  )
    button2.pack(pady=20 , padx = 20  )

    button3 = customtkinter.CTkButton(master =frame , text = "Log Out" , command= logout)
    button3.pack(pady=20 , padx = 20  )    
 

## For the ease of displaying products ##
def search_in_products(x , y):

    for widgets in x.winfo_children() :
        widgets.destroy()
        
    # To arrange the products in grids
    colnum = 0
    rownum = 0
    for productID in data["Products"]  :

        product = data["Products"][productID]

        # Check the search term
        if y in product.values() or y.capitalize() in product.values() or y =='':

            if colnum % 6 == 0:
                rownum +=1
                colnum = 0

            # if image is present, display it
            try:
                img = customtkinter.CTkImage(dark_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(200,200))
            except :
                img =None

            choice = customtkinter.CTkButton(x ,image=img,compound = "top" ,font = ("arial" ,20) ,text = f'Name : {product["Name"]} \nCost : Rs. {product["Cost"]}/- \nStock : {product["Stock"]} left \nType : {product["Type"]}\n Rating : {"*"*round(product["Rating"])} \nSales : {product["Sales"]}', text_color= ('white','black')  , command= lambda f = productID :  change_frame(select_product , 2 ,[f]))
            choice.grid(column  =colnum , row = rownum, sticky = 'nsew' , padx = 10 , pady = 10)
            colnum += 1


## Log out ##
def logout():
    GUI_Wrapper('Logging out')
    change_frame(login_page)


## Making a new product ##
def new_product():

    make_fit_frame()
    
    label = customtkinter.CTkLabel(master=frame , text="Product Information" , font = ("arial" , 50))
    label.pack(pady=20 , padx = 40 , expand = True )

    name = customtkinter.CTkEntry(master=frame  ,placeholder_text="Product Name")
    name.pack(pady=20 , padx = 40  )
    
    cost = customtkinter.CTkEntry(master=frame  ,placeholder_text="Product Cost")
    cost.pack(pady=20 , padx = 40  )
    
    stock = customtkinter.CTkEntry(master=frame  ,placeholder_text="Product Stock")
    stock.pack(pady=20 , padx = 40  )
    
    type = customtkinter.CTkEntry(master=frame  ,placeholder_text="Product Type")
    type.pack(pady=20 , padx = 40  )

    button1 = customtkinter.CTkButton(master =frame , text = "Confirm" , command = lambda :checkinfo(name.get() , cost.get(), stock.get() , type.get()) )
    button1.pack(pady=20 , padx = 40  )

    button2 = customtkinter.CTkButton(master =frame , text = "Go back" , command =lambda : change_frame(show_menu) )
    button2.pack(pady=20 , padx = 40  )


##  Make sure the input info is valid ##
def checkinfo(x, y, z ,w):
    
    try :
        y = int(y)
        z = int(z)
        if (not(x.isalnum())) and (not(w.isalnum())) and y > 0 and z >=0 and x  != '' and w  != '':
            raise Exception('Dummy')
        
    except :
        GUI_Wrapper( 'Invalid format of information')
        change_frame(new_product)

    

    else :
        for product in data["Products"] : 

            # Make sure no duplicate products are being made
            if data["Products"][product]["Name"] == x :
                GUI_Wrapper( 'Product of same name already in database')
                change_frame( show_menu)
                break

        else :
            # Adding product to product list with a new id   
            data["Products"][str(uuid.uuid4())] = {"Name": x , "Cost": y , "Stock": z , "Type": w , "Rating" : 0.0 , "Sales" : 0}
            GUI_Wrapper( 'Product added')
            change_frame(show_menu)


## Interface in which we can work on an individual product ##
def select_product(x):

    make_fit_frame()

    product = data["Products"][x]

    try:
        img = customtkinter.CTkImage(dark_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(100,100))
    except :
        img =None

    label = customtkinter.CTkLabel(master=frame , image = img ,compound= "left", text= f'Name : {product["Name"]} Cost : Rs. {product["Cost"]}/- Stock : {product["Stock"]} left Type : {product["Type"]} Rating : {"*"*round(product["Rating"])}', font=("arial" ,20 , "italic"))
    label.pack(pady=20 , padx = 20 ) 

    button1 = customtkinter.CTkButton(master =frame , text = "Change the product information" , command= lambda :change_product(x) )
    button1.pack(pady=20 , padx = 20  )

    button2 = customtkinter.CTkButton(master =frame , text = "Remove the product" , command = lambda :remove_product(x)  )
    button2.pack(pady=20 , padx = 20  )

    button3 = customtkinter.CTkButton(master =frame , text = "Go back" ,command = lambda : change_frame(show_menu) )
    button3.pack(pady=20 , padx = 20  )


## Logic behind removal of product from database ##
def remove_product(x):

    del data["Products"][x]
    GUI_Wrapper('Product removed')
    change_frame(show_menu)


## Interface showcasing change of product ##
def change_product(x):

    make_fit_frame()

    product = data["Products"][x]

    try:
        img = customtkinter.CTkImage(dark_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(100,100))
    except :
        img =None

    label = customtkinter.CTkLabel(master=frame ,compound= "left",image = img , text= f'Name : {product["Name"]} Cost : Rs. {product["Cost"]}/- Stock : {product["Stock"]} left Type : {product["Type"]} Rating : {"*"*round(product["Rating"])}', font=("arial" ,20 , "italic"))
    label.pack(pady=20 , padx = 20 ) 

    name = customtkinter.CTkEntry(master=frame  ,placeholder_text=product["Name"])
    name.pack(pady=20 , padx = 20  )
    
    cost = customtkinter.CTkEntry(master=frame  ,placeholder_text=product["Cost"])
    cost.pack(pady=20 , padx = 20  )
    
    stock = customtkinter.CTkEntry(master=frame  ,placeholder_text=product["Stock"])
    stock.pack(pady=20 , padx = 20  )
    
    type = customtkinter.CTkEntry(master=frame  ,placeholder_text=product["Type"])
    type.pack(pady=20 , padx = 20  )

    button1 = customtkinter.CTkButton(master =frame , text = "Confirm changes" , command = lambda :change_in_product_list(name.get() , cost.get() , stock.get() , type.get() , x) )
    button1.pack(pady=20 , padx = 20  )

    button2 = customtkinter.CTkButton(master =frame , text = "Go back" ,command = lambda : change_frame(show_menu) )
    button2.pack(pady=20 , padx = 20  )


## Logic behind changing product info ##
def change_in_product_list(x , y ,z ,w ,q):

    # Checking for valid info
    try :
        y = int(y)
        z = int(z)
        if (not(x.isalnum())) and (not(w.isalnum())) and y > 0 and z >=0 and x  != '' and w  != '':
            raise Exception('Dummy')

    except :
        GUI_Wrapper( 'Invalid format of information')
        change_frame(change_product , x =[q])

    else :
        data["Products"][q]["Name"] = x
        data["Products"][q]["Cost"] = y
        data["Products"][q]["Stock"] = z
        data["Products"][q]["Type"] = w

        GUI_Wrapper( 'Product changed')
        change_frame(show_menu)
    

## Loads database to memory ##
data = { "Managers" : {} , "Products" : {}}

with open("Database\\Managers.txt") as f :
    managers = f.readlines()
    managers = [manager.replace('\n' , '') for manager in managers]
        
for manager in range( 0 , len(managers) , 5 ) : 
    data["Managers"][managers[manager]] = { "Password"  : [ managers[manager+1] , managers[manager+2]] , "Name" : managers[manager+3]}

with open("Database\\Products.txt") as f :
    products = f.readlines()
    products = [product.replace('\n' , '') for product in products]

for product in range( 0 , len(products) , 8 ) : 
    if products[product] != '' :
        data["Products"][products[product]] = { "Name": products[product + 1], "Cost": int(products[product + 2]), "Stock": int(products[product + 3]),"Type": products[product + 4],"Rating": float(products[product + 5]),"Sales": int(products[product + 6])}



## Set appearance for GUI ##
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


## Initialize main window ##
root = customtkinter.CTk()
root.title("Nonpareil Emporium Manager")
root.geometry("1000x800")


# Show the app name
GUI_Wrapper('Nonpareil Emporium' , 5 , 80 , "italic")


# Show the login page
root.after(5000 , login_page)


root.mainloop()
