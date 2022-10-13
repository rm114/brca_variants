# import scrapy
# import requests
# import json
# from nested_lookup import nested_lookup



# class Brca1Spider(scrapy.Spider):
#     name = "brca1"
    
#     #this will eventually be user input
#     start_urls = [
#         'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num=0&search_term=&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3',
#     ]
#     search_term = input('Input the search term:')
#     page = 0
#     id_list = []

    

#     def parse(self, response):
#         json_response = response.json()
#         #json_dump = json.dumps(json_response, indent=4)
        
#         print('----------------------------------------------------------')

#         print(self.page)
    
#         #print(json_response.keys())
#         #print(json_dump) converts dict to str?
#         #print(json_response["deletedCount"])

#         #creates a readable JSON file
#         #jsonFile = open("site_json2.json", "w")
#         #jsonFile.write(json_dump)
#         #jsonFile.close()
#         #print('JSON filed saved!')

#         #User input of a list of variant names
#         #input_variants = {}

#         #print(nested_lookup('34394', json_response))



# # #this is original page

# #         results = nested_lookup(
# #             key = "id",
# #             document = json_response,
# #         )

# #         id_list = []
# #         id_list.extend(results)
        

# #this is each next page
#         self.page = self.page + 1
#         print(self.page)
#         new_url = f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={self.page}&search_term={self.search_term}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3'
        
#         results = nested_lookup(
#             key = "id",
#             document = json_response,
#         )

#         self.id_list.extend(results)

#         print(self.id_list)

#         yield scrapy.Request(new_url, callback = self.parse, dont_filter = True)
#         #print('variant 646226:', list(json_response.keys("data"))[list(json_response.values()).index('646226')])
        
#         print('----------------------------------------------------------')
#     #print(r.json())

# #r = requests.get("https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num=0&search_term=brca1&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3", verify=True)
# #print(r.json())