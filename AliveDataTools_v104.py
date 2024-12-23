import requests
#import json
# import xmltodict

# Copyright 2022, Westridge Laboratories, Inc., All rights reserved.
# Tools for accessing Acumatica Alive data over odata and the rest API.
#
# 2020.12.25 Version 100
#
# 2021.01.09 Version 101
#   added 'grid' and 'schema' object returns to Odata
#
# 2021.03.15 Version 101
#   for ODATA 
#   1. made the query a function instead of a Class
#   2. changed so by default only a grid is returned with the query result
#      an empty grid is returned if there is an error or no data returned.
#   3. add feature, if returned error code is not 200, debug changes to True if it
#      was not set by calling program (='maybe')
#      if debug = True, additional debug information is printed to the console.
#
# 2021.05.16 Version 102
#   changed Acumatica endpoint to 20.200.001
#   added commented print lines to rest query, print indented json for debug
#
# 2021.06.04 Version 102
#   added def get_inventory()
#
# 2022.08.12 Version 103
#   added tennant functionality for login
#   added testing (if __main__)
#
# 2022.12.31 Version 104
#   added scc14_full attribute A1010 to get_inventory() for workorders with eCommerce

VERSION = 104

alive_username = "APIread"
alive_password = "12345678"

#tenant = 'Test'
tenant = 'Westridge Laboratories Inc.'

# base_url  = "https://westridgelabs-sandbox-22-1.acumatica.com"
base_url  = "https://westridgelabs.acumatica.com"
# base_url  = "http://10.1.1.22/alive"

endpoint  = "/entity/Default/20.200.001/"
login     = "/entity/auth/login"
logout    = "/entity/auth/logout"

class RestQuery:
    
    def __init__(self, debug=False):

        self.debug = debug
        self.endpoint_url = base_url + endpoint

        # Acumatica login parameters
        #
        payload = {
            "name"     : alive_username,
            "password" : alive_password,
            "company"  : tenant,
            "branch"   : "WLI",
            "locale"   : "en-US"
        }

        # login to Acumatica
        #
        with requests.Session() as self.s:
            response = self.s.post(base_url + login, payload, timeout=100)
            if self.debug: print ('login', response)

    def __del__(self):
        with requests.Session() as s:
            response = s.post(base_url + logout, timeout=10)
            if self.debug: print ('logout', response)

    def query(self, table='', id='', id_field='', fields='', filter='', expand='', top=0, parameter='', html=''):
    # ******************************************************************************************************************
    #
    # 2 types of queries. "grid" and "detail". Both types return the data in json. 
    # grid: returns muliple rows and columns in json format. Cannot be used for attributes.
    # detail: Returns one record, with details such as attributes, based on ID in request (i.e. InventoryID)
    #
    # The detail query is actually two queries. One to get the Acumatica ID (GUID) of the item and a second
    # query to return the detail data.
    #
    # If the 'id=' field is populated, a detail query will be returned. 
    #
    # Input Variables:
    #   table: The Acumatica data table of interest exposed in the restAPI. 
    #   id: For detail queries only, the id of the item of interest. ie. 'IDDGLD08'. If this field is populated, a detail query will be returned.
    #   id_field: The data table field of the id used for the detail queriry. i.e. for 'IDDGLD08', the id_field is 'InventoryID'.
    #   fields: list of fields to return, odata format i.e. 'TaxID,Description,TaxSchedule'. Uses the odata select parameter.
    #   filter: return records filter parameter, odata format i.e. "startswith(Customer,'LC')"
    #   expand: odata instruction to expand record detail data. i.e. '$expand=TaxSchedule' 
    #   top: limit the number of records to return. If 0, top is ignored. Default is 0.
    #   parameter: odata format parameter that can be added to the html request. Can replace the other fields above manually.
    #   html: raw html that bypasses all other variable to send in the request. 
    #
    # ******************************************************************************************************************

        # determine query type - detail (by key) or grid
        # and set api parameters
        #
        type = 'detail'
        if id == '': type = 'grid'
        parameters = parameter_build(table=table, id=id, id_field=id_field, fields=fields, filter=filter, expand=expand, top=top, parameter=parameter, html=html)

        # query Acumatica
        #
        if type == 'grid':
            if html == '':
                rest_query = self.endpoint_url + table + '?' + parameters
            else:
                rest_query = html
            if self.debug: print (rest_query)
            response = self.s.get(rest_query, timeout=100)
            json_query_result = response.json()

        elif type == 'detail':
            # first, get the GUID for the item of interest from Acumatica
            #
            id_query = self.endpoint_url + table + "?$select=" + id_field + "&$filter=" + id_field + " eq '" + id + "'" 
            if self.debug: print(id_query)            
            response = self.s.get(id_query, timeout=100)
            id = (response.json()[0]['id'])

            # then, return a key based query for all the item data using the id as the key
            #
            rest_query = self.endpoint_url + table + """/""" + id + """?""" + parameters
            if self.debug: print (rest_query)
            response = self.s.get(rest_query, timeout=100)
            json_query_result = response.json()
            
        # print(json.dumps(json_query_result, indent=2))
        return json_query_result
        

def OdataQuery(gi='', fields='', filter='', top=0, html='', debug='maybe'):
    # ******************************************************************************************************************
    #
    # oData query of Acumatica exposed Generic Inquiry returns data as XML. The data is returned to the caller
    # in a grid (list of lists). When debug is on, the following entities print:
    #   code: odata response code
    #   result: a list of dictionaries. One list item for each row of data returned. 
    #   text: the raw XML returned by the odata query. 
    #   schema: a list, one item per field name
    #
    # Input Variables:
    #   gi: The Acumatica generic inquiry where the data of interest exists. 
    #   fields: list of fields to return, odata format i.e. 'TaxID,Description,TaxSchedule'. Uses the odata select parameter.
    #   filter: return records filter parameter, odata format i.e. "startswith(Customer,'LC')"
    #   top: limit the number of records to return. If 0, top is ignored. Default is 0.
    #   html: raw html that bypasses all other variable to send in the request. 
    #
    # ******************************************************************************************************************
    parameters = parameter_build(fields=fields, filter=filter, html=html, top=top)
    session = requests.Session()
    session.auth = (alive_username,alive_password)
    #odata_endpoint = base_url + '/odata/' + gi
    #odata_endpoint = base_url + '/odata/Westridge Laboratories Inc./' + gi
    odata_endpoint = f'{base_url}/odata/{tenant}/{gi}'
    with requests.Session():
        # query Acumatica with Odata
        #
        session.auth = (alive_username,alive_password)
        if html == '':
            odata_query = odata_endpoint + '?' + parameters
        else:
            odata_query = html        
        odata_response = session.get(odata_query)

        #print ("debug:" + debug)
        if odata_response.status_code != 200 and debug == 'maybe':           
            debug = True

        if debug == True: # debug output
            print('DEBUG')
            print('text:{}'.format(odata_response.text))            
            print('code:{}'.format(odata_response.status_code))
            print('odata query:' + odata_query)
            print('url:{}'.format(odata_response.url))


        # convert the XML return data into an array of lists
        # the XML has only one return from the generic inquiry, handle
        # special. 
        #
        schema = []
        rows = []
        entries = []
        #multi_row = False
        d = xmltodict.parse(odata_response.text)

        if False:  #testing data structure
            for key in d.keys():
                print (key)
            for key in d['feed'].keys():
                print ('  ' + key)
            for key in d['feed']['entry'].keys():
                print ('    ' + key)
            for key in d['feed']['entry']['content'].keys():
                print ('      ' + key)
            for key in d['feed']['entry']['content']['m:properties'].keys():
                print ('        ' + key)

        # if the query returns nothing, there will be no 'entry' key
        #              
        if odata_response.status_code == 200 and 'entry' in d['feed'].keys():

            # get the schema and entries for the feed. multi row returns need to be
            # treated differently than single row returns
            #
            if isinstance(d['feed']['entry'], list):
                #multi_row = True
                schema = [e for e in d['feed']['entry'][0]['content']['m:properties']]
                entries = [e for e in d['feed']['entry']]
            else:
                #multi_row = False
                schema = [e for e in d['feed']['entry']['content']['m:properties']]
                entries.append(d['feed']['entry'])
            
            # get the field values from the entries using the schemea and populate the 
            # output row data
            #
            for row in entries:
                row_data = []
                for field in schema:
                    field_value = ''
                    field_object = row['content']['m:properties'][field]
                    if isinstance(field_object, dict):
                        txt = field_object.get('#text')
                        if txt != None:
                            field_value = row['content']['m:properties'][field]['#text']
                    else:
                        field_value = (row['content']['m:properties'][field])
                    row_data.append(field_value)
                if row_data != None:
                    rows.append(row_data)
            if debug == True: print('schema:{}'.format(schema))
        else:
            if debug == True: print ('ADT no query rows returned or return code <> 200')

        rows.sort()
        return rows

def parameter_build(table='', id='', id_field='', fields='', filter='', expand='', top=0, parameter='', html=''):
    # gather user input parameters and format them for use in rest or odata queries
    #
    p = [] 

    if expand != '':
        rest_expand = '$expand={}'.format(expand)
        p.append(rest_expand)

    if fields != '':
        rest_select = '$select={}'.format(fields)
        p.append(rest_select)

    if filter != '':
        rest_filter = '$filter={}'.format(filter)
        p.append(rest_filter)

    if not isinstance(top, int): top = 0
    if top > 0:
        rest_top = '$top={}'.format(top)
        p.append(rest_top)
    # else:
    #     rest_top = ''

    if parameter != '':
        rest_parameter = parameter
        p.append(rest_parameter)

    return '&'.join(p)

def remove_namespace(element):
    # return the element tag passed without the namespace i.e. "http://schemas.microsoft.com/ado/2007/08/dataservices"
    #
    modified = element
    if '}' in element:
        modified = element.split('}')[1]
    return modified 


def get_inventory(query_filter=''):
    #********************************************************************************************
    # special query for just inventory (stock and non-stock)
    #
    # Input:
    #   query_filter: REST API compatible filter statement i.e. "ItemClass eq '{}'".format('LF')
    # 
    # Output:
    #   inventory dictionary of stock and non-stock items
    #   key is the sku.
    #   value is a list of inventory item properties:
    #     0 = sku
    #     1 = item status (Active or otherwise)
    #     2 = stock (true/false, stock/non-stock)
    #     3 = item class
    #     4 = description
    #     5 = kit (true/false, is a kit/not a kit)
    #     6 = sales uom conversion factor
    #     7 = wo_parameters 
    #     8 = upc, default = 'None'
    #     9 = scc14 (actual code, not the raw Acumatica entry)
    #     10= c_rev (valid lics number)
    #     11= item type
    #
    # Notes:
    #   Be carefult with the filter, it needs to work for both stock and nonstock tables.
    #********************************************************************************************

    # variable to hold the return dictionary
    #
    inventory = {}
    stock = False

    rs = RestQuery(debug=True)
    for inventory_type in ['stock','nonstock']:
        # run this loop twice, once for stock items and once for nonstock.
        # gets both sets of Acumatica data with one login
        #

        if inventory_type == 'stock': 
            stock = True
            result_stock = rs.query(
                table  ='StockItem',
                filter = query_filter, 
                expand = 'Attributes, UOMConversions',
                fields = 'InventoryID,ItemStatus,ItemClass,ItemType,Description,SalesUOM,UOMConversions/ConversionFactor,UOMConversions/FromUOM,IsAKit,Attributes/AttributeID,Attributes/ValueDescription'
            )
        elif inventory_type == 'nonstock':
            stock = False
            result_nonstock = rs.query(
                table  ='NonStockItem', 
                filter = query_filter, 
                expand = 'Attributes',
                fields = 'InventoryID,ItemStatus,ItemClass,ItemType,Description,IsKit,Attributes/AttributeID,Attributes/ValueDescription',
            )       
        #print(json.dumps(result_stock, indent=2))
        
    # logout of Acumatica
    #
    del rs

    for inventory_type in ['stock','nonstock']:
        # Extract properties from Acumatica data
        # Run the loop twice, once of stock and once for non-stock items.
        # both times add to the inventory dictionary
        #
        if inventory_type == 'stock':
            result = result_stock
            stock = True
        elif inventory_type == 'nonstock':
            result = result_nonstock
            stock = False

        for item in result: 
            #print(json.dumps(item, indent=2))        
            sku = item['InventoryID']['value']

            item_status = ''
            if 'ItemStatus' in item:
                item_status = item['ItemStatus'].get('value','')

            item_type = ''
            if 'ItemType' in item:
                item_type = item['ItemType'].get('value','')

            item_class = ''
            if 'ItemClass' in item:
                item_class = item['ItemClass'].get('value','')
            #if 'value' in item['ItemClass']: item_class = item['ItemClass']['value']

            description = ''
            if 'Description' in item:
                description = item['Description'].get('value','')

            kit = False
            if inventory_type == 'stock':
                #print('here')
                if 'IsAKit' in item:
                    #print('isakit')
                    kit = item['IsAKit'].get('value',False)
                    #print (item['IsAKit']['value'])
            else:
                if 'IsKit' in item:
                    kit = item['IsKit'].get('value',False)

            sales_uom = ''
            if 'SalesUOM' in item:
                sales_uom = item['SalesUOM']['value']

            uom = 1 #sales uom convertion factor
            if 'UOMConversions' in item:
                # if len(item['UOMConversions']) > 0:
                #     uom = item['UOMConversions'][0]['ConversionFactor'].get('value', 1)
                for unit in item['UOMConversions']:
                    if unit['FromUOM']['value'] == sales_uom:
                        uom = unit['ConversionFactor']['value']

            # item attributes
            #
            wo_parameters = ''
            upc = 'None'
            scc14_raw = ''
            scc14_full = ''
            c_rev = ''
            if 'Attributes' in item:
                for a in item['Attributes']:
                    if 'AttributeID' in a:
                        if 'value' in a['AttributeID']:
                            if a['AttributeID']['value'] == 'A1007': wo_parameters = a['ValueDescription']['value']
                            if a['AttributeID']['value'] == 'A1002': upc = a['ValueDescription']['value']
                            if a['AttributeID']['value'] == 'A1003': scc14_raw = a['ValueDescription']['value']
                            if a['AttributeID']['value'] == 'A1008': c_rev = a['ValueDescription']['value']
                            if a['AttributeID']['value'] == 'A1010': scc14_full = a['ValueDescription']['value']
            #scc14 = scc14_raw # no conversion done here
            scc14 = scc14_full # no conversion done here
            # add the item and parameters to the output dictionary
            #
            inventory[sku] = [
                sku, 
                item_status,
                stock, 
                item_class, 
                description, 
                kit, 
                uom, 
                wo_parameters, 
                upc, 
                scc14, 
                c_rev,
                item_type
                ]

    return inventory

if __name__ == "__main__":
    # test connections and data retrieval
    #
    verbose = True
    print(f'******************************************')
    print(f'*** Testing AliveDataTools version:{VERSION} ***')
    
    # ODATA Query to a GI with a filter
    #
    if False:
        odata_filter = "InventoryCD eq 'IDDGLD08EA'"
        odata_select = ''\
            'InventoryCD,'\
            'Description,'\
            'UnitRate,'\

        qr = OdataQuery(gi="Odata106", filter=odata_filter, fields=odata_select, debug=False)
        print('ODATA query done')
        print(f'ODATA Query Returned {len(qr)} rows and {len(qr[0])} columns')
        if verbose:
            for row in qr:
                print(row)

    # 2 REST API Queries with single REST Query Object
    #
    if True:
        #skus = ['IDDGLD08','IDDGLD04','ASRT1024']
        skus = ['IDDGLD08','IDDGLD08EA',]
        rs = RestQuery(debug=True)
        sku_data_list = []
        progress_counter = 1

        for sku in skus:
            error_code = 0
            error_report = ''

            # query sku data and attributes
            #
            result = rs.query(
                table  ='StockItem',
                filter = "InventoryID eq '{}'".format(sku),
                expand ='Attributes, UOMConversions',
                fields ='InventoryID,Description,SalesUOM,UOMConversions/ConversionFactor,UOMConversions/FromUOM,Attributes/AttributeID,Attributes/ValueDescription'
            )
            if verbose:
                print('result:')
                print(result)
                print()
            
            inventoryCD = result[0]['InventoryID']['value']
            description = result[0]['Description']['value']
            upc_code = ''
            scc14_code = ''
            wo_parameters = ''
            for a in result[0]['Attributes']:
                if a['AttributeID']['value'] == 'A1002': upc_code = a['ValueDescription']['value']
                if a['AttributeID']['value'] == 'A1003': scc14_code = a['ValueDescription']['value']
                if a['AttributeID']['value'] == 'A1007': wo_parameters = a['ValueDescription']['value']

            sales_uom = ''
            if 'SalesUOM' in result[0]:
                sales_uom = result[0]['SalesUOM']['value']

            uom = 0
            if 'UOMConversions' in result[0]:
                for unit in result[0]['UOMConversions']:
                    if unit['FromUOM']['value'] == sales_uom:
                        uom = unit['ConversionFactor']['value']

            print(f'{inventoryCD}, {description}, {upc_code}, {scc14_code}, {wo_parameters}, {uom}')
            if inventoryCD != sku:
                print(f'The returned inventoryCD did not match the original sku: {inventoryCD} vs {sku}')
        del rs

    # Inventory Query
    #
    if False:
        inventory_dict = get_inventory()
        print('Inventory query done')
        print(f"sample inventory item: {inventory_dict['IDD114G3']}")
        print(f'Inventory query returned {len(inventory_dict)} items')
        if verbose:
            for item in inventory_dict:
                print(item)

    print(f'*** Testing AliveDataTools version:{VERSION} complete ***')

# Copyright 2022, Westridge Laboratories, Inc., All rights reserved.