import sys
import requests
import time
import logging
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

import AliveDataTools_v105 as AliveDataTools
from django.utils import timezone
from privatelabel.models import Order, Customer, Product
from datetime import datetime
import os
from django.core.mail import send_mail

email_user = os.environ.get('EMAIL_USER')
email_password = os.environ.get('EMAIL_PASS')
author_email = 'lrichards@westridgelabs.com'
recipients = ['lrichards@westridgelabs.com' ]

VERSION = '101'

def main():
    BackorderSync('TAG')

def BackorderSync(entity):
    

    print(f'BackorderSync v{VERSION} for {entity} started.')
    inventory_items = getInventoryData()  
    # inventory_items_refined = []
    # for i in inventory_items:
    #     InventoryID = i[0]
    #     skip_it = False
    #     if len(InventoryID) != 10:   skip_it = True
    #     elif InventoryID[0] == 'X':  skip_it = True
    #     if not skip_it:
    #         inventory_items_refined.append(i)

    # #class used to convert list into json
    # class item:payload = {}

    # #Back order app url to update individual variants (bulk updated url doesn't work)    
    # url = "https://api.grit.software/polar-bear/external/v0/variants"

    # #Bearer token is in the TAG's Back order app
    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": "Bearer YZRHNJHKNTGTMWRKMS0ZYMI3LTG0ODYTNZHINTUXNTLLZGY3"
    # }

    # post the back-in-stock dates to the backorder app api
    # only print 

      

def getInventoryData():
    """
    Get the sku and backorder til date from Acumatica for desired SKUs.
    """
    
    # query Acumatica inventory data
    #
    print('Working on Acumatica data...')
    rs = AliveDataTools.RestQuery(debug=True)
    # print all in the rs object
    
    # result = rs.query(
    #     table  ='StockItem',
    #     filter ="InventoryID eq 'XLDXRX03'",
    #     expand ='Attributes',
    #     fields ='InventoryID,Attributes/AttributeID,Attributes/ValueDescription'
    # )

    # result = rs.query(
    #     table  ='StockItem',
    #     filter ="InventoryID eq 'XLDXRX03' or InventoryID eq 'XLDXCX11' or InventoryID eq 'XLDXCZ50' or InventoryID eq 'XLDXNX05' or InventoryID eq 'XLDXLX78' or InventoryID eq 'XLDXCZ52'",
    #     expand ='Attributes,WarehouseDetails',
    #     fields ='InventoryID,Attributes/AttributeID,Attributes/ValueDescription,WarehouseDetails/WarehouseID,WarehouseDetails/QtyOnHand'
    # )
    
    # for row in result:
    #     InventoryID = row['InventoryID']['value']
    #     for warehouse in row['WarehouseDetails']:
    #         WarehouseID = warehouse['WarehouseID']['value']
    #         QtyOnHand = warehouse['QtyOnHand']['value']
    #         print(f'InventoryID: {InventoryID}, QtyOnHand: {QtyOnHand}')
    customername = {
        'LC02125': 'Body Action',
        'LC02143': 'Skins Sexual Health Ltd.- Private Label',
        'LC00200': 'Lovehoney, Ltd. - Private Label',
        'LC02053': 'Landco Import  International, Inc.- Private Label',
        'LC01984': 'Atlantic Innovations',
        'LC02177': 'Mayer Laboratories, Inc',
        'LC02043': 'NCO Ventures, Inc. Private Label',
        'LC00047': 'Import Master',
    }
    
    result = rs.query(
        table  ='SalesOrder',
        filter ="startswith(OrderNbr, 'L')",
        expand ='Details',
        fields ='OrderNbr,Date,RequestedOn,Status,CustomerID,Details/InventoryID,Details/UOM,Details/OrderQty,Details/SalespersonID'
    )
    
    for row in result:
        OrderNbr = row['OrderNbr']['value']
        CustomerID = row['CustomerID']['value']
        Status = row['Status']['value']
        Date = datetime.strptime(row['Date']['value'], '%Y-%m-%dT%H:%M:%S%z').date()
        RequestedOn = datetime.strptime(row['RequestedOn']['value'], '%Y-%m-%dT%H:%M:%S%z').date()
        
        for detail in row['Details']:
            InventoryID = detail.get('InventoryID', {}).get('value')
            SalespersonID = detail.get('SalespersonID', {}).get('value')
            Uom = detail.get('UOM', {}).get('value')
            if SalespersonID and SalespersonID in ['L006A', 'L020K', 'L020X']:
                print(f'{OrderNbr}, {CustomerID}, {Status}, {InventoryID}, {Uom} SalespersonID: {SalespersonID}, {Date}, {RequestedOn}')
   
    # add this sales orders into the database
    created_list = []
    for row in result:
        OrderNbr = row['OrderNbr']['value']
        CustomerID = row['CustomerID']['value']
        Status = row['Status']['value']
        Date = datetime.strptime(row['Date']['value'], '%Y-%m-%dT%H:%M:%S%z').date()
        RequestedOn = datetime.strptime(row['RequestedOn']['value'], '%Y-%m-%dT%H:%M:%S%z').date()
        for detail in row['Details']:
            InventoryID = detail.get('InventoryID', {}).get('value')
            Uom = detail.get('UOM', {}).get('value')
            OrderQty = detail.get('OrderQty', {}).get('value')
            SalespersonID = detail.get('SalespersonID', {}).get('value')

            if SalespersonID and SalespersonID in ['L006A', 'L020K', 'L020X']:
                if Status in ['Complete', 'Canceled','']:
                    order = Order.objects.filter(number=OrderNbr, product=InventoryID, uom=Uom).first()
                    if order:
                        order.customer = customername.get(CustomerID, '')
                        order.customerid = CustomerID
                        order.uom = Uom
                        order.date_received = Date
                        order.desired_date = RequestedOn
                        order.qty = OrderQty
                        order.date_entered = timezone.now()
                        order.status = Status
                        order.salesperson = SalespersonID
                        order.save()
                        print(f'Order {OrderNbr} updated successfully.')
                    
                else:
                    order, created = Order.objects.update_or_create(
                        number=OrderNbr,
                        product=InventoryID,
                        uom=Uom,
                        defaults={
                            'customer': customername.get(CustomerID, ''),
                            'customerid': CustomerID,
                            'uom': Uom,
                            'date_received': Date,
                            'qty': OrderQty,
                            'date_entered': timezone.now(),
                            'status': Status,
                            'salesperson': SalespersonID
                        }
                    )
                    if created:
                        created_list.append(OrderNbr)
                        print(f'Order {OrderNbr} created successfully.')

                    else:
                        print(f'Order {OrderNbr} updated successfully.')
                    
    if created_list.count > 0:
        send_mail(f'Orders have been created', '', email_user, recipients, 
                  html_message=f'Orders {created_list} have been created.',
                  auth_user=email_user, auth_password=email_password)


    # create list of inventory and back-in-stock dates
    # back-in-stock date = None if blank in Acumatica
    #
    # backorder_list = []
    # for row in result:
    #     InventoryID = row['InventoryID']['value']
    #     back_order_til = None
    #     for attribute in row['Attributes']:
    #         if attribute['AttributeID']['value'] == 'A1006':
    #             back_order_til = attribute['ValueDescription']['value']
    #             back_order_til = back_order_til[0:10]
    #     backorder_list.append((InventoryID, back_order_til))
    # return backorder_list

if __name__=='__main__':main()


        




