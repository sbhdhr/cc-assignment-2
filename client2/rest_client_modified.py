# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:02:58 2020

@author: Subhashis
"""
import requests
import json
import sys
import time

time.sleep(5)

LOCAL_FLAG = False


if LOCAL_FLAG:
    gateway = ["http://localhost:6001","http://localhost:6002"]
    
    
else:
    gateway = ["http://gateway1:6000","http://gateway2:6000"]
    

part=1

inv_dict = {}

def get_all_inventory_items(verbose,user):
    global part
    global inv_dict
    
    inv_dict = requests.get(gateway[part] + "/listallitems",params=({'id':user})).json()
    
    if verbose:
        for i,item in enumerate(inv_dict.keys()):
            #print(item)
            print(i+1,".",item,":",inv_dict[item]['quan'],": $",inv_dict[item]['price'],"/unit")


def get_shop_cart(user):
    global part
    global inv_dict
    get_all_inventory_items(False,user)
    total = 0
    
    cart = requests.get(gateway[part] + "/getcartfor",params=({'id':user})).json()
    
    for i,item in enumerate(cart.keys()):
        price = float(inv_dict[item]['price'])*int(cart[item])
        print(i+1,".",item,":",cart[item]," : $",str(round(price,2)))
        total=total+price
        
    print("\n\nTotal cart value: $ ",str(round(total,2)))
        
    return cart
    

def add_to_shop_cart(user,item):
    global part
    res = requests.post(gateway[part]+"/additem",params={'id':user,
                                                            'item':item,
                                                            'quant':1}).text
    
    if res=='true':
        print("Added successfully !!")
    else:
        print(res)
        
        
def delete_item(user,item):
    global part
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


def get_shop_cart_for(item):
    global part    
    ids = requests.get(gateway[part] + "/getcartcontaining",params=({'id':'0','pass':'pass','item':item})).json()
    print(ids)

def admin_menu(c,user,item):
    global part
    c=str(c)
    part=(part+1)%2
    if c == '1':
        print("Item list !!")
        get_all_inventory_items(True,user)    
    elif c == '2':
        print("Cart List!!")
        get_all_shop_cart()  
    elif c == '3':
        print("Cart List containing item!!")
        get_shop_cart_for(item)
    else:
        print("Invalid option!!")  
        
def normal_menu(c,user,item):
    global part
    c=str(c)
    
    part=(part+1)%2
    #part=0
    if c == '1':
        print("Item list !!")
        get_all_inventory_items(True,user)
    elif c == '2':
        print("Your cart !!")
        get_shop_cart(user)
    elif c == '3':
        print("Add item !!")
        add_to_shop_cart(user,item)
    elif c == '5':
        print("Delete item !!")
        delete_item(user,item)
    else:
        print("Invalid option!!")
    

if __name__ == "__main__":
    filePtr = open('client2.json')
    operations = json.load(filePtr)
    for opId in operations:
        print(" {} -> {}".format(opId,operations[opId]))
        user = operations[opId]["UserID"]
        operation = operations[opId]["Operation"]
        item = operations[opId]["item"]
        if(user!=0):
            # 1>all items , 2>cart items, 3>Add, 4>Update, 5>Del
            if(operation=="ADD"):
                normal_menu(3,user,item)
            elif(operation=="DELETE"):
                normal_menu(5,user,item)
            elif(operation=="LISTALL"):
                normal_menu(1,user,item)
            elif(operation=="VIEWCART"):
                normal_menu(2,user,item)
        else:
            if(operation=="VIEWALL"):
                admin_menu(1,user,item)
            elif(operation=="LISTALL"):
                admin_menu(2,user,item)
            elif(operation=="TRACKITEM"):
                admin_menu(3,user,item)
    
    