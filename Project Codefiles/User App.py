import customtkinter
from PIL  import  Image 
import datetime
import os
import secrets
import hashlib


## A fuction that updates the data being used in the program ##
def read_database():
    global data
    data = {"Products" : {} , "Users" : {} , "Last Logged" : 0}

    # Reading Last Logged
    with open("Database\\Last Logged.txt") as f :
        last = f.read()
        if last != '0' :
            data["Last Logged"] = last
        else :
            data["Last Logged"] = 0

    # Reading Product list
    with open("Database\\Products.txt") as f :
        products = f.read().split('\n')
        products = [i  for i in products if i != '']

    for product in range( 0 , len(products) , 7 ) : 

        data["Products"][products[product]] = { "Name": products[product + 1], "Cost": int(products[product + 2]), "Stock": int(products[product + 3]),"Type": products[product + 4],"Rating": float(products[product + 5]),"Sales": int(products[product + 6])}

    # Reading the Users data
    with open("Database\\Users.txt") as f :
        users = f.read().split('\n')
        users = [i  for i in users if i != '']

    # For each user, loading his/her cart, history, and wishlist
    for user in range( 0 , len(users) , 9 ) : 

        data["Users"][users[user]] = { "Password": [ users[user + 1],users[user + 2]], "Name": users[user + 3], "Email Address": users[user + 4], "Phone Number" : users[user + 5] , "Delivery Address": users[user + 6],  "Appearance": users[user + 7], "Color Theme": users[user + 8] , "Cart" : {} , "Wishlist" : [] , "Shopping History" : []}

        with open(f"Database\\Userdata\\{users[user]}\\Cart.txt") as s :
            cartitems = s.read().split('\n')
            cartitems = [i  for i in cartitems if i != '']
            
            for itemid in range( 0 , len(cartitems) ,2  ) : 
                data["Users"][users[user]]["Cart"][cartitems[itemid]] =  int(cartitems[itemid + 1])


        with open(f"Database\\Userdata\\{users[user]}\\Wishlist.txt") as s :
            wishes = s.read().split('\n')
            wishes = [i  for i in wishes if i != '']
            data["Users"][users[user]]["Wishlist"].extend(wishes)

        with open(f"Database\\Userdata\\{users[user]}\\Shopping History.txt") as s :
            past = s.read().split('\n')
            past = [i  for i in past if i != '']

            for historyid in range( 0 , len(past) , 7 ) : 
                data["Users"][users[user]]["Shopping History"].append({ "Name" : past[historyid ] , "Cost" : int(past[historyid + 1]) , "Type" : past[historyid + 2] , "Quantity": int(past[historyid + 3]), "Form of Payment": past[historyid + 4] ,"Given Rating": float(past[historyid + 5]) ,"Date" : past[historyid + 6]})


## Secure password ##
def hash_password(password, salt=None):

    if salt is None:
        salt = secrets.token_hex(16)  # Generate a random salt

    # Combine password and salt, and hash the result
    hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    
    return (hashed_password, salt)


## Updating all users data in the database ##
def update_user_data():
    with open("Database\\Users.txt" , "w") as f :

        for username in data["Users"] :
            f.write(username + '\n')

            for attribute in data["Users"][username] :

                if attribute not in ["Cart" , "Wishlist" , "Shopping History" , "Password"] :
                    f.write(str(data["Users"][username][attribute]) + '\n')
                elif attribute == "Password" :
                    f.write(str(data["Users"][username][attribute][0]) + '\n')
                    f.write(str(data["Users"][username][attribute][1]) + '\n')

            f.write('\n')

            with open(f"Database\\Userdata\\{username}\\Cart.txt" , "w") as s :
                for itemid in data["Users"][username]["Cart"] :
                    s.write(itemid + '\n')
                    s.write(str(data["Users"][username]["Cart"][itemid]) + '\n')
                    s.write('\n')

            with open(f"Database\\Userdata\\{username}\\Wishlist.txt" , "w") as s :
                for itemid in data["Users"][username]["Wishlist"] :
                    s.write(itemid + '\n')
                    s.write('\n')

            with open(f"Database\\Userdata\\{username}\\Shopping History.txt" , "w") as s :
                for item in range(len(data["Users"][username]["Shopping History"])) :

                    for attribute in data["Users"][username]["Shopping History"][item]:
                        s.write(str(data["Users"][username]["Shopping History"][item][attribute]) + '\n')

                    s.write('\n')


## For the ease of displaying a message ##
def GUI_Wrapper(text, time = 2 ,font_size = 40 , font_style = "roman"):
    label = customtkinter.CTkLabel(master= root, text=text, font=("arial" ,font_size , font_style))
    label.place(rely=0.5 , relx = 0.5 ,anchor = "center"  )
    root.after(time*1000 , lambda : label.destroy())


## Changing frames ### Warning without parameters ##
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


## Making a sleeker frame ##
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

    label = customtkinter.CTkLabel(master=frame , text="Login system" ,font= ("arial" , 50))
    label.pack(pady=20 , padx = 40  )

    username = customtkinter.CTkEntry(master=frame  ,placeholder_text="Enter your username")
    username.pack(pady=20 , padx = 40  )
    
    password = customtkinter.CTkEntry(master=frame , placeholder_text="Password" , show = "*")
    password.pack(pady=20 , padx = 40  )

    rem = customtkinter.CTkSwitch(frame , text = "Remember Me")
    rem.pack(pady=20 , padx = 40 )

    button1 = customtkinter.CTkButton(master =frame , text = "Login" , command = lambda : login(username.get() , password.get()  , rem.get()) )
    button1.pack(pady=20 , padx = 40  )

    button2= customtkinter.CTkButton(master =frame ,width=70 , text = "Sign up" , command = lambda : change_frame(sign_up_page) )
    button2.pack(pady=20 , padx = 40  )


## Sign up page ##
def sign_up_page():

    make_fit_frame()

    label = customtkinter.CTkLabel(master=frame , text="Sign up system" ,font= ("arial" , 50))
    label.pack(pady=20 , padx = 40  )

    username = customtkinter.CTkEntry(master=frame  ,placeholder_text="Enter a Username")
    username.pack(pady=20 , padx = 40 )

    password = customtkinter.CTkEntry(master=frame , placeholder_text="Enter a Password" )
    password.pack(pady=(20, 1) , padx = 40)

    label1 = customtkinter.CTkLabel(master=frame , text="Password must contain a combination of alphabets and digits with no spaces" ,font= ("arial" , 10))
    label1.pack(pady=(1,1) , padx = 40  )

    name = customtkinter.CTkEntry(master=frame , placeholder_text="Enter your Name" )
    name.pack(pady=20 , padx = 40  )

    email = customtkinter.CTkEntry(master=frame , placeholder_text="Enter your Email" )
    email.pack(pady=20 , padx = 40  )

    number = customtkinter.CTkEntry(master=frame , placeholder_text="Enter your Phone Number" )
    number.pack(pady=(20, 1) , padx = 40  )

    label1 = customtkinter.CTkLabel(master=frame , text="Phone number must be of 11 digits" ,font= ("arial" , 10))
    label1.pack(pady=(1,1) , padx = 40  )

    delivery = customtkinter.CTkEntry(master=frame , placeholder_text="Enter your delivery address" )
    delivery.pack(pady=20 , padx = 40  )

    button1 = customtkinter.CTkButton(master =frame , text = "Confirm" , command = lambda : sign_up(username.get() , password.get() , name.get() , email.get() , number.get() , delivery.get() ) )
    button1.pack(pady=20 , padx = 40  )

    button2= customtkinter.CTkButton(master =frame , text = "Have an account ? Login" , command = lambda : change_frame(login_page) )
    button2.pack(pady=20 , padx = 40  )


## Sign up logic ##
def sign_up(a , b, c, d, e , f) :


    # Making sure there is no shitty info
    if e.isdigit() and len(e) == 11  and b.isalnum() and all( i.isalpha() for i in c.split()) and a != ''  and d != '' and ' ' not in a :

        # Making sure no duplicate user is being made

        if data["Users"].get(a , None) :
            GUI_Wrapper("User already in database")
            change_frame(sign_up_page)
                
        else :
            password , key = hash_password(b)
            data["Users"][a] = { "Password" : [password , key],"Name" : c ,"Email Address" : d , "Phone Number" : e ,"Delivery Address" : f ,"Cart" : {},"Wishlist" : {},"Shopping History" : [] , "Appearance" : customtkinter.get_appearance_mode() , "Color Theme" : customtkinter.ThemeManager._currently_loaded_theme}
            os.mkdir(f"Database\\Userdata\\{a}")


            # Adding the modified user list back to the database
            update_user_data()

            # Make sure the username can be accessed by the whole program
            global username
            username = a

            # Login the new user
            GUI_Wrapper( 'User added' )
            root.after(2000 , GUI_Wrapper , f'Welcome {data["Users"][username]["Name"]}')
            change_frame(show_tabs , 4)
    else :
        GUI_Wrapper( 'Invalid format of information')
        change_frame(sign_up_page)


## Login logic ##
def login(x ,y , z):

    global username 
    for username in data["Users"] :

        # Hashing the inserted password
        password_key_pair = hash_password(y , data["Users"][username]["Password"][1])

        if username  == x and data["Users"][username]["Password"] == list(password_key_pair) :

                # Load appearance as user had last set
                customtkinter.set_appearance_mode(data["Users"][username]["Appearance"])
                customtkinter.set_default_color_theme(data["Users"][username]["Color Theme"])

                # If remember me was ticked, it will record that
                if z ==1 :
                    data["Last Logged"] = username
                    with open("Database\\Last Logged.txt" , "w") as f :
                        f.write(str(data["Last Logged"]))


                GUI_Wrapper('Welcome ' + data["Users"][username]["Name"])
                change_frame(show_tabs)
                break

    # Incase of invalid entry
    else : 
        GUI_Wrapper('Invalid ID or Password')
        change_frame(login_page)


## A functiom that establishes the main interface ##
def show_tabs():
        
    # For frequently updating the data base
    update_user_data()

    # To make sure any all information is up-to-data
    read_database()

    global frame

    # Incase of multiple clicks, make sure no multiple frames are made
    try :
        if frame :
            frame.destroy()
    except :
        pass

    frame = customtkinter.CTkTabview(master=root)
    frame.pack(pady=60 , padx = 60 , fill ="both" , expand =True)

    product_tab = frame.add("Products")
    cart_tab = frame.add("Cart")
    wishlist_tab = frame.add("Wish List")
    history_tab = frame.add("History")
    settings_tab = frame.add("Settings")
    frame.set("Products")

    ## Products tab ##
    productlist = customtkinter.CTkScrollableFrame(master = product_tab ,label_text = "Product list")
    productlist.pack( pady=60 , padx = 60 , fill ="both" , expand =True )
    productlist.columnconfigure([0,1,2,3,4,5], weight = 1)



    colnum = 0
    rownum = 0
    for productID in data["Products"]   :
        product = data["Products"][productID]

        if colnum % 6 == 0:
            rownum +=1
            colnum = 0


        # if image is present, display it
        try:
            img = customtkinter.CTkImage(light_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(200 , 200))
        except :
            img = None

        choice = customtkinter.CTkButton(productlist ,image=img,compound = "top" ,font = ("arial" ,20) ,text = f'Name : {product["Name"]} \nCost : Rs. {product["Cost"]}/- \nStock : {product["Stock"]} left \nType : {product["Type"]}\n Rating : {"*"*round(product["Rating"])} \nSales : {product["Sales"]}', text_color= ('white','black')  , command= lambda f = productID :  change_frame(select_product , 2 ,[f]))
        choice.grid(column  =colnum , row = rownum, sticky = 'nsew' , padx = 10 , pady = 10)
        colnum += 1
    
    psearchcase = customtkinter.CTkEntry(master=product_tab , placeholder_text="Search case")
    psearchcase.pack(pady=20 , padx = 40)

    pbutton = customtkinter.CTkButton(master =product_tab , text = "Search" , command= lambda :  narrow_search(productlist , psearchcase.get() , data["Products"]  ))
    pbutton.pack(pady=20 , padx = 20  )

    ## Cart tab ##
    cartlist = customtkinter.CTkScrollableFrame(master = cart_tab ,label_text = "Cart")
    cartlist.pack( pady=60 , padx = 60 , fill ="both" , expand =True )
    cartlist.columnconfigure([0,1,2,3,4,5], weight = 1)

    colnum = 0
    rownum = 0
    for cartitem , quantity in data["Users"][username]["Cart"].items()  :
        product = data["Products"][cartitem]

        if colnum % 6 == 0:
            rownum +=1
            colnum = 0


        # if image is present, display it
        try:
            img = customtkinter.CTkImage(light_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(200,200))
        except :
            img = None

        choice = customtkinter.CTkButton(cartlist ,image=img,compound = "top", font = ("arial" ,20) ,text_color= ('white','black')  ,text = f'Name : {product["Name"]} \nCost : Rs. {product["Cost"]}/- \nStock : {product["Stock"]} left \nType : {product["Type"]} \nRating : {"*"*round(product["Rating"])} \nSales : {product["Sales"]} \nQuantity : {quantity}'  , command= lambda  f = cartitem : change_frame(select_product , 2 ,[f] ))
        choice.grid(column  =colnum , row = rownum, sticky = 'nsew' , padx = 10 , pady = 10)
        colnum += 1

        if data["Products"].get(cartitem)["Stock"] < data["Users"][username]["Cart"][cartitem]:
            choice.configure(fg_color = 'grey')              

    cost = 0
    for item in data["Users"][username]["Cart"]:
        if data["Products"].get(item)["Stock"] > data["Users"][username]["Cart"][item]:
            cost += (data["Products"].get(item)["Cost"] * data["Users"][username]["Cart"][item] )

    label = customtkinter.CTkLabel(master=cart_tab, text= f"Total Cost of purchasable products : Rs. {cost}/-", font=("arial" ,20 , "italic"))
    label.pack(pady=20 , padx = 20 )

    csearchcase = customtkinter.CTkEntry(master=cart_tab , placeholder_text="Search case")
    csearchcase.pack(pady=20 , padx = 40)

    cbutton = customtkinter.CTkButton(master =cart_tab , text = "Search" , command= lambda :  narrow_search_in_cart(cartlist , csearchcase.get() , data["Users"][username]["Cart"] ))
    cbutton.pack(pady=20 , padx = 20  )

    cbutton2 = customtkinter.CTkButton(master =cart_tab , text = "Check Out" , command= lambda : check_out(cost))
    cbutton2.pack(pady=20 , padx = 20  )

    ## Wishlist tab ##

    wishlist = customtkinter.CTkScrollableFrame(master = wishlist_tab ,label_text = "Wish list")
    wishlist.pack( pady=60 , padx = 60 , fill ="both" , expand =True )
    wishlist.columnconfigure([0,1,2,3,4,5], weight = 1)

    colnum = 0
    rownum = 0

    for wish in data["Users"][username]["Wishlist"] :

        product = data["Products"][wish]

        if colnum % 6 == 0:
            rownum +=1
            colnum = 0


        # if image is present, display it
        try:
            img = customtkinter.CTkImage(light_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(200,200))
        except :
            img = None

        choice = customtkinter.CTkButton(wishlist ,image=img ,compound = "top", font = ("arial" ,20) ,text_color= ('white','black')  ,text = f'Name : {product["Name"]} \nCost : Rs. {product["Cost"]}/- \nStock : {product["Stock"]} left \nType : {product["Type"]} \nRating : {"*"*round(product["Rating"])} \nSales : {product["Sales"]}' , command= lambda f = wish :select_product(f) )
        choice.grid(column  =colnum , row = rownum, sticky = 'nsew' , padx = 10 , pady = 10)
        colnum += 1

    wsearchcase = customtkinter.CTkEntry(master = wishlist_tab , placeholder_text="Search case")
    wsearchcase.pack(pady=20 , padx = 40)

    wbutton = customtkinter.CTkButton(master = wishlist_tab , text = "Search" , command= lambda : narrow_search(wishlist , wsearchcase.get() ,data["Users"][username]["Wishlist"] )  )
    wbutton.pack(pady=20 , padx = 20  )

    ## History tab ##

    history = customtkinter.CTkScrollableFrame(master = history_tab ,label_text = "Shopping History")
    history.pack( pady=60 , padx = 60 , fill ="both" , expand =True )
    history.columnconfigure([0,1,2,3,4,5], weight = 1)

    colnum = 0
    rownum = 0
    for purchase in range(len(data["Users"][username]["Shopping History"])):
            
            product = data["Users"][username]["Shopping History"][purchase]
            
            if colnum % 6 == 0:
                rownum +=1
                colnum = 0


            # if image is present, display it
            try:
                img = customtkinter.CTkImage(dark_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(200,200))
            except :
                img = None

            choice = customtkinter.CTkButton(master = history,compound = "top", image=img , font = ("arial" ,20) ,text_color= ('white','black')  ,text =  f'Name : {product["Name"]} \nCost : Rs. {product["Cost"]}/- \nType  : {product["Type"]} \nQuantity : {product["Quantity"]} \nDate : {product["Date"]} \nGiven Rating : {"*"*round(product["Given Rating"])} \nForm of Payment : {product["Form of Payment"]}'  )
            choice.grid(column  =colnum , row = rownum, sticky = 'nsew' , padx = 10 , pady = 10)
            colnum += 1

    hsearchcase = customtkinter.CTkEntry(master=history_tab , placeholder_text="Search case")
    hsearchcase.pack(pady=20 , padx = 40)

    hbutton = customtkinter.CTkButton(master =history_tab , text = "Search" , command= lambda : search_in_history(history , hsearchcase.get())  )
    hbutton.pack(pady=20 , padx = 20  )

    ## Setting Tab ##

    miniframe = customtkinter.CTkFrame(settings_tab, fg_color = ['gray92', 'gray14'])
    miniframe.place(rely=0.5 , relx = 0.5 ,anchor = "center" ) 

    # Show user pic if it exists
    try :
        img = customtkinter.CTkImage(dark_image=Image.open(f'Pictures\\{username}.jpg')  ,size=(200,200) )
        
    except Exception:
        img = customtkinter.CTkImage(dark_image=Image.open(f'Pictures\\Default pic.png')  ,size=(200,200) )
        
    label1= customtkinter.CTkLabel(master=miniframe , image = img , text = '' )
    label1.pack(pady=20 , padx = 20 )
    
    label = customtkinter.CTkLabel(master=miniframe, text= data["Users"][username]["Name"] ,  font = ("arial" ,30, "italic"))
    label.pack(pady=20 , padx = 20 )

    label = customtkinter.CTkLabel(master=miniframe, text= "Appearance Mode",  font = ("arial" ,20))
    label.pack(pady=20 , padx = 20 )

    appear = customtkinter.CTkSegmentedButton(master=miniframe , values = ["system" , "light" , "dark"] )
    appear.pack(pady=(10 ,20) , padx = 20)

    appear.set(data["Users"][username]["Appearance"])
    appear.configure(command = lambda f =  appear.get() : update_appearance(f))

    label = customtkinter.CTkLabel(master=miniframe, text= "Color Theme",  font = ("arial" ,20))
    label.pack(pady=(20 , 1) , padx = 20 )

    label = customtkinter.CTkLabel(master=miniframe, text= "Will cause to exit out of settings",  font = ("arial" ,15 , "italic"))
    label.pack(pady= (1 ,20), padx = 20)

    color = customtkinter.CTkSegmentedButton(master=miniframe , values = ["blue" , "green" , "dark-blue"] )
    color.pack(pady=(10 ,20) , padx = 20)

    color.set(data["Users"][username]["Color Theme"])
    color.configure(command = lambda f = color.get() : update_color(f))

    sbutton = customtkinter.CTkButton(master =miniframe , text = "Change Password" , command =lambda :change_frame(change_password)  )
    sbutton.pack(pady=20 , padx = 20 )

    mainbutton = customtkinter.CTkButton(master =miniframe , text = "Log Out" , fg_color= "red"  , hover_color= "grey", command =lambda :change_frame(log_out)  )
    mainbutton.pack(pady=20 , padx = 20 )
    

## Function called to change the appearance ##
def update_appearance(x) :
    data["Users"][username]["Appearance"] = x
    customtkinter.set_appearance_mode(x)
    update_user_data()


## Function called to change the color theme ##
def update_color(x):
    data["Users"][username]["Color Theme"] = x
    customtkinter.set_default_color_theme(x)
    update_user_data()
    change_frame(show_tabs)


## A frame that helps to change the password ##
def change_password():
    make_fit_frame()

    label = customtkinter.CTkLabel(master=frame, text= "Change password" ,  font = ("arial" ,30, "italic"))
    label.pack(pady=20 , padx = 20 )

    oldp = customtkinter.CTkEntry(master=frame , placeholder_text="Old password")
    oldp.pack(pady=20 , padx = 20)

    newp = customtkinter.CTkEntry(master=frame , placeholder_text="New password")
    newp.pack(pady=20 , padx = 20)

    button1 = customtkinter.CTkButton(master =frame , text = "Confirm" , command =lambda :confirm_password_change(oldp.get() , newp.get())  )
    button1.pack(pady=20 , padx = 20 )

    button2 = customtkinter.CTkButton(master =frame , text = "Go back" , command =lambda :change_frame(show_tabs)  )
    button2.pack(pady=20 , padx = 20 )


## Logic behind password change ##
def confirm_password_change(x , y):
    password_key_pair = hash_password(x , data["Users"][username]["Password"][1])


    if data["Users"][username]["Password"] == list(password_key_pair) :

        password_key_pair = hash_password(y )
        data["Users"][username]["Password"] = list(password_key_pair)
        GUI_Wrapper("Password Changed")
        change_frame(show_tabs)

    else :
        GUI_Wrapper("Invalid password")
        change_frame(change_password)


## Logic behind log out ##
def log_out():

    data["Last Logged"] = 0
    # Adding the modified product list back to the database and logging the user out of the terminal
    with open("Database\\Last Logged.txt" , "w") as f :
        f.write(str(data["Last Logged"]))

    
    GUI_Wrapper('Logging out')
    change_frame(login_page)


## Further action to be taken on an individual product ##
def select_product(x):

    make_fit_frame()

    product = data["Products"][x]

    try:
        img = customtkinter.CTkImage(light_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(100,100))
    except :
        img =None

    label = customtkinter.CTkLabel(master=frame , image = img ,compound= "left", text= f'Name : {product["Name"]} Cost : Rs. {product["Cost"]}/- Stock : {product["Stock"]} left Type : {product["Type"]} Rating : {"*"*round(product["Rating"])}', font=("arial" ,20 , "italic"))
    label.pack(pady=20 , padx = 20 ) 

    quantity = customtkinter.CTkEntry(frame , placeholder_text="Enter a valid quantity")
    quantity.pack(pady=20 , padx = 40)

    button1 = customtkinter.CTkButton(master =frame , text = "Buy" , command= lambda : direct_purchase(x , quantity.get()) )
    button1.pack(pady=20 , padx = 20  )

    if data["Users"][username]["Cart"].get(x , None) : 
        button2 = customtkinter.CTkButton(master =frame , text = "Remove from cart" , command = lambda :  [data["Users"][username]["Cart"].pop(x) , select_product(x)]  )
        button2.pack(pady=20 , padx = 20  )

    else : 
        button2 = customtkinter.CTkButton(master =frame , text = "Add to cart" , command = lambda :  add_to_cart(x  ,quantity.get()) )
        button2.pack(pady=20 , padx = 20  )

    if x in data["Users"][username]["Wishlist"] :
        button3 = customtkinter.CTkButton(master =frame , text = "Remove from Wishlist" , command = lambda : [data["Users"][username]["Wishlist"].remove(x) , select_product(x)]  )
        button3.pack(pady=20 , padx = 20  )

    else :
        button3 = customtkinter.CTkButton(master =frame , text = "Add to Wishlist" , command = lambda : [ frame.destroy() , add_to_wishlist(x )]  )
        button3.pack(pady=20 , padx = 20  )

    button4 = customtkinter.CTkButton(master =frame , text = "Go back" ,command = lambda : change_frame(show_tabs) )
    button4.pack(pady=20 , padx = 20  )


## Fuction called to add a product to wishlist ##
def add_to_wishlist(x ):

    data["Users"][username]["Wishlist"].append(x)
    GUI_Wrapper("Added to Wishlist")
    change_frame(select_product , 2 ,[x] )


## Fuction called to add a product to cart ##
def add_to_cart(x , y ) :

    product = data["Products"][x]

    try :
        quantity = int(y)
        if quantity > product["Stock"] or quantity <= 0:
            raise Exception("Dummy")
    except :
        GUI_Wrapper("Invalid Quantity")
        change_frame(select_product , 2 ,[x] )

    else :
        
        data["Users"][username]["Cart"][x] =  quantity
        GUI_Wrapper("Added to Cart")
        change_frame(select_product , 2 ,[x] )


## Should the buyer choose to purchase the product directly ##
def direct_purchase(x ,y):
    
    product = data["Products"][x]

    # Checking for valid quantity
    try :
        quantity = int(y)
        if quantity > product["Stock"] or quantity <= 0:
            raise Exception("Dummy")
    except :
        GUI_Wrapper("Invalid Quantity")
        change_frame(select_product , 2 ,[x] )

    else :

        make_fit_frame()

        try:
            img = customtkinter.CTkImage(light_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(100,100))
        except :
            img =None

        label = customtkinter.CTkLabel(frame , image = img ,compound= "left", text= f'Name : {product["Name"]} Cost : Rs. {product["Cost"]}/- Stock : {product["Stock"]} left Type : {product["Type"]} Rating : {"*"*round(product["Rating"])}' , font=("arial" ,20 , "italic"))
        label.pack(pady=20 , padx = 20 )
        
        label = customtkinter.CTkLabel(frame , text= f'Total Cost : Rs. {product["Cost"]*quantity}/-', font=("arial" ,20 , "italic"))
        label.pack(pady=20 , padx = 20 )

        payment_options = [ "Credit Card" , "Debit Card" , "Cash on Delivery"]
        combo = customtkinter.CTkComboBox(master = frame , values = payment_options  ,width = 200, height = 40 , font =("arial" ,20) )
        combo.pack( pady=40 , padx = 40 )

        label = customtkinter.CTkLabel(frame , text= f'Product will be delivered to {data["Users"][username]["Delivery Address"]}', font=("arial" ,20 ))
        label.pack(pady=20 , padx = 20 )

        label = customtkinter.CTkLabel(frame , text= f'Receipt will be forwarded to {data["Users"][username]["Email Address"]}', font=("arial" ,20 ))
        label.pack(pady=20 , padx = 20 )

        button1 = customtkinter.CTkButton(frame , text = "Confirm" , command= lambda :  rating(x  , quantity, combo.get() ) )
        button1.pack(pady=20 , padx = 20  )

        button2 = customtkinter.CTkButton(frame , text = "Go back" , command= lambda : change_frame(select_product , 2 ,[x] ) )
        button2.pack(pady=20 , padx = 20  )


## Get a rating before the customer gets his product hehe ##
def rating(x,y,z):
    make_fit_frame()

    label = customtkinter.CTkLabel(frame , text= f"Please rate the product on recieving", font=("arial" ,20 ))
    label.pack(pady=20 , padx = 20 )

    slider = customtkinter.CTkSlider(frame , from_=0 , to=5 , number_of_steps= 51 , )
    slider.pack()

    button = customtkinter.CTkButton(frame , text = "Confirm" , command= lambda :  confirm_purchase(x  , y, z , slider.get()))
    button.pack(pady=20 , padx = 20  )


## Logic on confirming purchase of individual product ##
def confirm_purchase( a , b ,c ,d) :
    
    product = data["Products"][a]

    data["Products"][a]["Rating"] = (product["Rating"]*product["Sales"] + b*d) / (product["Sales"]+ b)
    data["Products"][a]["Stock"] -= b
    data["Products"][a]["Sales"] += b

    data["Users"][username]["Shopping History"].insert( 0 ,{ "Name" : product["Name"] , "Cost" : product["Cost"] , "Type" : product["Type"] , "Quantity": b, "Form of Payment": c ,"Given Rating": d ,"Date" : datetime.datetime.now().strftime("%x")})

    # Update the product list with change in stock, rating, and sales
    with open("Database\\Products.txt" , "w") as f :

        for productid in data["Products"] :
            f.write(productid + '\n')

            for attribute in data["Products"][productid] :
                f.write(str(data["Products"][productid][attribute]) + '\n')

            f.write('\n')

    GUI_Wrapper("Thank you for shopping with us" , 3, 80)
    change_frame(show_tabs ,3)


## Finalizing purchase of bulk prroduct ##
def check_out(x): 

    make_frame()

    cartlist = customtkinter.CTkScrollableFrame(master = frame ,label_text = "Cart")
    cartlist.pack( pady=20 , padx = 20 , fill ="both" , expand =True )
    cartlist.columnconfigure([0,1,2,3,4,5] , weight=1)

    # To arrange the products in grids
    colnum = 0
    rownum = 0
    for cartitem , quantity in data["Users"][username]["Cart"].items()  :

        product = data["Products"][cartitem]

        if colnum % 6 == 0:
            rownum +=1
            colnum = 0

        # if image is present, display it
        try:
            img = customtkinter.CTkImage(light_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(100,100))
        except :
            img = None

        if data["Products"].get(cartitem)["Stock"] >= quantity:
            choice = customtkinter.CTkButton(cartlist ,image=img , compound='top', font = ("arial" ,20) ,text = f'Name : {product["Name"]} \nCost : Rs. {product["Cost"]}/- \nStock : {product["Stock"]} left \nType : {product["Type"]} \nRating : {"*"*round(product["Rating"])} \nSales : {product["Sales"]} \nQuantity : {quantity}' , text_color=('white' , 'black') , command= lambda  f = cartitem : change_frame(select_product , 2 ,[f] ))
            choice.grid(column  =colnum , row = rownum, sticky = 'nsew' , padx = 10 , pady = 10)
            colnum += 1

    label = customtkinter.CTkLabel(frame , text= f'Total Cost : Rs. {x}/-', font=("arial" ,20 , "italic"))
    label.pack(pady=20 , padx = 20 )

    payment_options = [ "Credit Card" , "Debit Card" , "Cash on Delivery"]
    combo = customtkinter.CTkComboBox(master = frame , values = payment_options  ,width = 200, height = 40 , font =("arial" ,20) )
    combo.pack( pady=40 , padx = 40 )

    label = customtkinter.CTkLabel(frame , text= f'Products will be delivered to {data["Users"][username]["Delivery Address"]}', font=("arial" ,20 ))
    label.pack(pady=10 , padx = 20 )

    label = customtkinter.CTkLabel(frame , text=f'Receipt will be forwarded to {data["Users"][username]["Email Address"]}', font=("arial" ,20 ))
    label.pack(pady=10 , padx = 20 )

    button1 = customtkinter.CTkButton(frame , text = "Confirm" , command= lambda :  rating_for_cart( combo.get() ) )
    button1.pack(pady=20 , padx = 20  )

    button2 = customtkinter.CTkButton(master =frame , text = "Go back" ,command = lambda : change_frame(show_tabs) )
    button2.pack(pady=20 , padx = 20  )
    

## Get a rating before the customer gets his product hehe ##
def rating_for_cart(x ):

    make_fit_frame()


    label = customtkinter.CTkLabel(master = frame, text= f"Please rate the products on recieving", font=("arial" ,20))
    label.pack(pady=20, padx = 20 )

    slider = customtkinter.CTkSlider(frame , from_=0 , to=5 , number_of_steps= 51 , )
    slider.pack()

    button = customtkinter.CTkButton(frame , text = "Confirm" , command= lambda :  confirm_purchase_for_cart( x,slider.get()))
    button.pack(pady=20 , padx = 20  )


## Logic behind finalizing the cart ##
def confirm_purchase_for_cart( a , b ) :

    # We need store products bought and remove them from cart afterwards, if we do it simultaneusly, the program  breaks
    cartitems = []
    for cartitem  , quantity in data["Users"][username]["Cart"].items() :

        # Check if the product has enough stock for purchase
        if data["Products"].get(cartitem)["Stock"] >= quantity:

            product = data["Products"][cartitem]

            data["Products"][cartitem]["Rating"] = (((product["Rating"]*product["Sales"]) + (b*quantity)) / (product["Sales"]+ quantity))
            data["Products"][cartitem]["Stock"] -= quantity
            data["Products"][cartitem]["Sales"] += quantity

            data["Users"][username]["Shopping History"].insert( 0 ,{ "Name" : product["Name"] , "Cost" : product["Cost"] , "Type" : product["Type"] , "Quantity": quantity, "Form of Payment": a ,"Given Rating": b ,"Date" : datetime.datetime.now().strftime("%x")})
            cartitems.append(cartitem)
    
    # Update the product list with change in stock, rating, and sales
    with open("Database\\Products.txt" , "w") as f :

        for productid in data["Products"] :
            f.write(productid + '\n')

            for attribute in data["Products"][productid] :
                f.write(str(data["Products"][productid][attribute]) + '\n')

            f.write('\n')

    for item in cartitems :
        data["Users"][username]["Cart"].pop(item)


    GUI_Wrapper("Thank you for shopping with us" , 3 ,80 )
    change_frame(show_tabs ,3) 


## Narrow the search ##
def narrow_search( a ,b,c  ):
    for widgets in a.winfo_children() :
        widgets.destroy()
    
    # To arrange the products in grids
    colnum = 0
    rownum = 0
    for item in c:
        product = data["Products"][item]

        # Check the search term
        if b.capitalize() in product.values() or b == '':
            if colnum % 6 == 0:
                rownum +=1
                colnum = 0
                
            # if image is present, display it
            try:
                img = customtkinter.CTkImage(light_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(200 , 200))
            except :
                img = None

            choice = customtkinter.CTkButton(a ,image=img,compound = "top" ,font = ("arial" ,20) ,text = f'Name : {product["Name"]} \nCost : Rs. {product["Cost"]}/- \nStock : {product["Stock"]} left \nType : {product["Type"]}\n Rating : {"*"*round(product["Rating"])} \nSales : {product["Sales"]}', text_color= ('white','black')  , command= lambda f = item :  change_frame(select_product , 2 ,[f]))
            choice.grid(column  =colnum , row = rownum, sticky = 'nsew' , padx = 10 , pady = 10)
            colnum += 1


## Narrow the search in cart ##
def narrow_search_in_cart( a ,b,c  ):
    for widgets in a.winfo_children() :
        widgets.destroy()

    # To arrange the products in grids
    colnum = 0
    rownum = 0
    for item in c:

        product = data["Products"][item]
        quantity = c[item]["Quantity"]

        # Check the search term
        if b.capitalize() in product.values() or b == '':

            if colnum % 6 == 0:
                rownum +=1
                colnum = 0
                
            # if image is present, display it
            try:
                img = customtkinter.CTkImage(light_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(200,200))
            except :
                img = None


            choice = customtkinter.CTkButton(a ,image=img,compound = "top", font = ("arial" ,20) ,text_color= ('white','black')  ,text = f'Name : {product["Name"]} \nCost : Rs. {product["Cost"]}/- \nStock : {product["Stock"]} left \nType : {product["Type"]} \nRating : {"*"*round(product["Rating"])} \nSales : {product["Sales"]} \nQuantity : {quantity}'  , command= lambda  f = item : change_frame(select_product , 2 ,[f] ) )
            choice.grid(column  =colnum , row = rownum, sticky = 'nsew' , padx = 10 , pady = 10)
            
            colnum += 1

            if data["Products"].get(item)["Stock"] < data["Users"][username]["Cart"][item]:
                choice.configure(fg_color = 'grey')


## Narrow the search in history ##
def search_in_history(x , y):

    for widgets in x.winfo_children() :
        widgets.destroy()

    # To arrange the products in grids
    colnum = 0
    rownum = 0
    for purchases in range(len(data["Users"][username]["Shopping History"]))   :
        product = data["Users"][username]["Shopping History"][purchases]
        
        # Check the search term
        if y.capitalize() in product.values() or y == '':
            
            if colnum % 6 == 0:
                rownum +=1
                colnum = 0

            # if image is present, display it
            try:
                img = customtkinter.CTkImage(light_image = Image.open(f'Pictures\\{product["Name"]}.png') , size=(200,200) )
            except :
                img = None

            choice = customtkinter.CTkButton(master= x ,image=img ,compound = "top" , font = ("arial" ,20) ,text_color= ('white','black')  ,text =  f'Name : {product["Name"]} \nCost : Rs. {product["Cost"]}/- \nType  : {product["Type"]} \nQuantity : {product["Quantity"]} \nDate : {product["Date"]} \nGiven Rating : {"*"*round(product["Given Rating"])} \nForm of Payment : {product["Form of Payment"]}'  )
            choice.grid(column  =colnum , row = rownum, sticky = 'nsew' , padx = 10 , pady = 10)
            colnum += 1

## Loads database to memory ##
read_database()


## Set appearance for GUI ##
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")


## Initialize main window ##
root = customtkinter.CTk()
root.title("Nonpareil Emporium")
root.geometry("1000x800")


# Show the app name
GUI_Wrapper('Nonpareil Emporium' , 5 , 80 , "italic")


# If remembered, log back in
if data["Last Logged"] :
    global username
    username = data["Last Logged"]

    # Load appearance as user had last set
    customtkinter.set_appearance_mode(data["Users"][username]["Appearance"])
    customtkinter.set_default_color_theme(data["Users"][username]["Color Theme"])
    root.after(5000 ,GUI_Wrapper , 'Welcome back ' + data["Users"][username]["Name"])
    root.after(8000 , show_tabs)

# Else show login page 
else :
    
    root.after(5000 , login_page)


root.mainloop()