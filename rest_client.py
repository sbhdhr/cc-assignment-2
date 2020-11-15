# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:02:58 2020

@author: Subhashis
"""
import requests
import json
import sys

url = "http://gateway1:5000/apiv1/"


def get_all_inventory_items():
    res = requests.get(url + "inventory/all")
    text = res.text
    # alert_list = json.loads(text)
    # # print(type(alert_list))
    # for i, v in enumerate(alert_list):
    #     t = (i + 1, v["desc"])
    #     alert_list[i] = t
    return text


def send_alert(n):
    res = requests.post(url + "alert/" + str(n))
    return res.text


if __name__ == "__main__":
    
    user = int(input("Enter userId: "))
    
    while True:
        print("\n------- Distributed Shopping Cart -------")
        print("1. List available items.")
        print("2. Show shopping cart.")
        print("3. Add item.")
        print("4. Delete item.")
        print("q. Exit")
      
        print()
        try:
            c = input("Enter your choice: ")
            if c == '1':
                print("Item list !!")
                print(get_all_inventory_items())
            elif c == 'q' or c == 'Q':
                break
            else:
                print("Invalid option!!")
        except:
            print("Error!", sys.exc_info()[0], " occured.")