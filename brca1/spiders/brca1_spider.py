import scrapy
from time import sleep
import json
import re

class Brca1Spider(scrapy.Spider):
    name = "brca1"
    page = 0
    match_found = "NO"

    search_list = input('Input the variant(s):')
    search_term = search_list.split()
    current_search_term = 0

    start_urls = [f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={page}&search_term={search_term[current_search_term]}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3']
  
    test_table = {
        "Variant": [],
        "Protein_Change": [],
        "HGVS_cDNA": [],
        "HGVS_Protein": [],
        "BIC_Nomenclature": []
    }

    def parse(self, response):
 
        #get the data drom database
        json_response = response.json()
        #print(json_response)
        
        print('----------------------------------------------------------')
      
        #checks if current index is within search array
        print (f'Current search index: {self.current_search_term}')
        print (f'Current search array length: {len(self.search_term)}')
        if self.current_search_term >= len(self.search_term):
                print('Database fully searched.')
                print(f'Match found: {self.match_found}')
                print('Test Table:')
                print (json.dumps(self.test_table, indent=4))
                return
        else:
          
            print(f'Still within array...{self.current_search_term}/{len(self.search_term)}')
                
            #total number of results for single search term
            print (f'Total result count: {json_response["count"]}')

            #checks for last results page (data null)
            if json_response["data"] == []:
                
                print(f'Length search term: {len(self.search_term)}')
                print(f'Current term index: {self.current_search_term}')
                print(f'Current page: {self.page}')


                self.current_search_term = self.current_search_term + 1
                self.page = 0

                if self.current_search_term >= len(self.search_term):
                    print('Database fully searched.')
                    print(f'Match found: {self.match_found}')
                    print('Test Table:')
                    print (json.dumps(self.test_table, indent=4))
                    return

                new_url = f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={self.page}&search_term={self.search_term[self.current_search_term]}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3'
    
                print(f'Updated term index: {self.current_search_term}')
                print(f'Updated page: {self.page}')

                return scrapy.Request(new_url, callback = self.parse, dont_filter = True)
        
            #not last page, continues on
            else:

                for result in json_response["data"]:
                    
                    def table_update():
                        self.test_table['Variant'].append(self.search_term[self.current_search_term])
                        self.test_table['Protein_Change'].append(result ['Protein_Change'])
                        self.test_table['HGVS_cDNA'].append(result ['HGVS_cDNA'])
                        self.test_table['HGVS_Protein'].append(result ['HGVS_Protein'])
                        self.test_table['BIC_Nomenclature'].append(result ['BIC_Nomenclature'])

                    input_search = r".*\b%s\b" %str(self.search_term[self.current_search_term].lower())
                    Protein_Change_search = str(result['Protein_Change']).lower()
                    HGVS_cDNA_search = str(result['HGVS_cDNA']).lower()
                    HGVS_Protein_search = str(result['HGVS_Protein']).lower()
                    BIC_Nomenclature_search = str(result['BIC_Nomenclature']).lower()

                    print(f'Input search: {input_search}')
                    print(f'Protein change search: {Protein_Change_search}')
                    print(f'HGVS cDNA search: {HGVS_cDNA_search}')
                    print(f'HGVS protein search: {HGVS_Protein_search}')
                    print(f'BIC nomenclature search: {BIC_Nomenclature_search}')

                    if re.search(input_search, Protein_Change_search) is not None:
                        self.match_found = "YES"
                        table_update()
                        print('Protein match found!')

                    elif re.search(input_search, HGVS_cDNA_search) is not None:
                        self.match_found = "YES"
                        table_update()
                        print('Nucleotide match found!')

                    elif re.search(input_search, HGVS_Protein_search) is not None:
                        self.match_found = "YES"
                        table_update()
                        print('HGVS protein match found!')

                    elif re.search(input_search, BIC_Nomenclature_search) is not None:
                        self.match_found = "YES"
                        table_update()
                        print('BIC des match found!')
                    
                    else:
                        None

                if self.page < 3:
                    #add a page, first results start on page 1
                    print(f'Previous page #:{self.page}')
                    self.page = self.page + 1
                    print(f'Current page #:{self.page}')
                else:
                    self.page = 100000000000
                    print(f'Current page #:{self.page}')
                    
                new_url = f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={self.page}&search_term={self.search_term[self.current_search_term]}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3'
        
                return scrapy.Request(new_url, callback = self.parse, dont_filter = True)
                
                
                print('----------------------------------------------------------')

    #import re

    # txt = "NP_009225.1:p.(Lys1667Ter)"

    # i = "p.(Lys1667Ter)"
    # #match = re.search(r".+\b6999A>G\b", txt)
    # #raw_match = re.search(r".+\b" + {i} + r"\b", txt)
    # raw_match = re.search(r".*\b%s\b" %i, txt)
    # #no_match = re.search(r".+\b6989A>G\b", txt)

    # #print(match)
    # print(raw_match)
    # #print(no_match)
