# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:02:58 2020

@author: Subhashis
"""
import requests
import json
import sys

LOCAL_FLAG = False


if LOCAL_FLAG:
    gateway = ["http://localhost:6001","http://localhost:6002"]
    
    
else:
    gateway = ["http://gateway1:6000","http://gateway2:6000"]
    

part=1

inv_dict = {}


def get_all_inventory_items(verbose):
    global part
    global user
    global inv_dict
    
    inv_dict = requests.get(gateway[part] + "/listallitems",params=({'id':user})).json()
    
    if verbose:
        for i,item in enumerate(inv_dict.keys()):
            #print(item)
            print(i+1,".",item,":",inv_dict[item]['quan'],": $",inv_dict[item]['price'],"/unit")

 

def get_shop_cart():
    global part
    global user
    global inv_dict
    
    total = 0
    
    cart = requests.get(gateway[part] + "/getcartfor",params=({'id':user})).json()
    
    for i,item in enumerate(cart.keys()):
        price = float(inv_dict[item]['price'])*int(cart[item])
        print(i+1,".",item,":",cart[item]," : $",str(round(price,2)))
        total=total+price
        
    print("\n\nTotal cart value: $ ",str(round(total,2)))
        
    return cart
    

def add_to_shop_cart():
    global part
    global user
    global inv_dict
    
    get_all_inventory_items(True)
    print()
    
    i = int(input("Enter your choice: "))
    
    item = list(inv_dict.keys())[i-1]
        
    q = input("Enter quantity for {} : ".format(item))
    
    res = requests.post(gateway[part]+"/additem",params={'id':user,
                                                            'item':item,
                                                            'quant':q}).text
    
    if res=='true':
        print("Added successfully !!")
    else:
        print(res)
        
        
def upd_shop_cart():
    global part
    global user
    
    print("Your cart !!")
    cart = get_shop_cart()
    print()
    
    i = int(input("Enter your choice: "))
    
    item = list(cart.keys())[i-1]

    q = input("Enter new quantity for {} : ".format(item))

    res = requests.put(gateway[part]+"/updateitem",params={'id':user,
                                                            'item':item,
                                                            'quant':q}).text
    
    if res=='true':
        print("Updated successfully !!")
    else:
        print(res)
        
        
def delete_item():
    global part
    global user
    
    print("Your cart !!")
    cart = get_shop_cart()
    print()
    
    i = int(input("Enter your choice: "))
    
    item = list(cart.keys())[i-1]

    res = requests.delete(gateway[part]+"/deleteitem",params={'id':user,
                                                            'item':item}).text
    
    if res=='true':
        print("Deleted successfully !!")
    else:
        print(res)
        
        
def get_all_shop_cart():
    global part
    carts = requests.get(gateway[part] + "/getallcarts",params=({'id':'0','pass':'pass'})).json()
    
    for i,item in enumerate(carts.keys()):
        print("User: ",i+1)
        print("----------")
        for j,item2 in enumerate(carts[item].keys()):
            print(j+1,".",item2,":",carts[item][item2])
        print()
            
    return carts


def get_shop_cart_for():
    global part
    global inv_dict
    
    get_all_inventory_items(True)
    print()
    
    i = int(input("Enter your choice: "))
    
    item = list(inv_dict.keys())[i-1]
        
    
    ids = requests.get(gateway[part] + "/getcartcontaining",params=({'id':'0','pass':'pass','item':item})).json()
    
    print(ids)
       
        
def admin_menu():
    global part
    
    
    while True:
        print("\n------- Distributed Shopping Cart :: ADMIN-------")
        print("1. List available items.")
        print("2. List all shopping cart.")
        print("3. List all shopping cart for item.")
        print("q. Exit")
      
        print()
        part=(part+1)%2
        #part=0
        try:
            c = input("Enter your choice: ")
            if c == '1':
                print("Item list !!")
                get_all_inventory_items(True)
                
            
            elif c == '2':
                print("Cart List!!")
                get_all_shop_cart()
                
            elif c == '3':
                print("Cart List!!")
                get_shop_cart_for()
            
            elif c == 'q' or c == 'Q':
                break
            else:
                print("Invalid option!!")
        except:
            print("Error!", sys.exc_info()[0], " occured.")
    
        
        
def normal_menu():
    global part
    
    while True:
        print("\n------- Distributed Shopping Cart -------")
        print("1. List available items.")
        print("2. Show shopping cart.")
        print("3. Add item.")
        print("4. Update item.")
        print("5. Delete item.")
        print("q. Exit")
      
        print()
        part=(part+1)%2
        #part=0
        try:
            c = input("Enter your choice: ")
            if c == '1':
                print("Item list !!")
                get_all_inventory_items(True)
                
            
            elif c == '2':
                print("Your cart !!")
                get_shop_cart()
                
            
            elif c == '3':
                print("Add item !!")
                add_to_shop_cart()
                
            elif c == '4':
                print("Update item !!")
                upd_shop_cart()
                
            elif c == '5':
                print("Delete item !!")
                delete_item()
                            
            
            elif c == 'q' or c == 'Q':
                break
            else:
                print("Invalid option!!")
        except Exception as e:
            print("Error!", str(e))
    

if __name__ == "__main__":
    
    
    user = int(input("Enter userId: "))
    get_all_inventory_items(False)
    if user==0:
        passwrd=input('Enter admin password:')
        if passwrd=='pass':
            admin_menu()
        else:
            print("Invalid Credentials, exiting...")
    else:
        normal_menu()
    
    