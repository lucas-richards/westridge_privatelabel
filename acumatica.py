import sys
import requests
import time
import logging

import AliveDataTools_v105 as AliveDataTools

VERSION = '101'

def main():
    BackorderSync('TAG')

def BackorderSync(entity):
    

    print(f'BackorderSync v{VERSION} for {entity} started.')
    inventory_items = getInventoryData()  
    inventory_items_refined = []
    for i in inventory_items:
        InventoryID = i[0]
        skip_it = False
        if len(InventoryID) != 10:   skip_it = True
        elif InventoryID[0] == 'X':  skip_it = True
        if not skip_it:
            inventory_items_refined.append(i)

    #class used to convert list into json
    class item:payload = {}

    #Back order app url to update individual variants (bulk updated url doesn't work)    
    url = "https://api.grit.software/polar-bear/external/v0/variants"

    #Bearer token is in the TAG's Back order app
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YZRHNJHKNTGTMWRKMS0ZYMI3LTG0ODYTNZHINTUXNTLLZGY3"
    }

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

    result = rs.query(
        table  ='StockItem',
        filter ="InventoryID eq 'XLDXRX03' or InventoryID eq 'XLDXCX11' or InventoryID eq 'XLDXCZ50' or InventoryID eq 'XLDXNX05' or InventoryID eq 'XLDXLX78' or InventoryID eq 'XLDXCZ52'",
        expand ='Attributes,WarehouseDetails',
        fields ='InventoryID,Attributes/AttributeID,Attributes/ValueDescription,WarehouseDetails/WarehouseID,WarehouseDetails/QtyOnHand'
    )
    
    for row in result:
        InventoryID = row['InventoryID']['value']
        for warehouse in row['WarehouseDetails']:
            WarehouseID = warehouse['WarehouseID']['value']
            QtyOnHand = warehouse['QtyOnHand']['value']
            print(f'InventoryID: {InventoryID}, QtyOnHand: {QtyOnHand}')

    # create list of inventory and back-in-stock dates
    # back-in-stock date = None if blank in Acumatica
    #
    backorder_list = []
    for row in result:
        InventoryID = row['InventoryID']['value']
        back_order_til = None
        for attribute in row['Attributes']:
            if attribute['AttributeID']['value'] == 'A1006':
                back_order_til = attribute['ValueDescription']['value']
                back_order_til = back_order_til[0:10]
        backorder_list.append((InventoryID, back_order_til))
    return backorder_list

if __name__=='__main__':main()


        




