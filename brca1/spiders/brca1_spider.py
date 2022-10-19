from operator import ilshift
from types import NoneType
import scrapy
from time import sleep
import json
import re

class Brca1Spider(scrapy.Spider):
    name = "brca1"
    page = 0

    search_list = input('Input the variant(s):')
    search_term = search_list.split()
    current_search_term = 0
    print("------------------------------------------")
    # print (search_term)
    # sleep(100)
    matched = ""
    number_match = 0
    number_no_match = 0
    number_no_results = 0


    start_urls = [f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={page}&search_term={search_term[current_search_term]}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3']
    match_table = {
        "Match_Results": []
    }
    no_match_table = {
        "No_Match_Results": []
    }

    def parse(self, response):
        print(f'Current search term: {self.search_term[self.current_search_term]}')
        print(f'Page #: {self.page}')
        #get the data drom database
        json_response = response.json()
        #print(json_response)
        
        print('----------------------------------------------------------')

        #checks if current index is within search array
        if self.current_search_term >= len(self.search_term):
                print('>>> Database fully searched.')
                
                jsonFile = open("match_table.json", "w")
                jsonFile.write(json.dumps(self.match_table, indent=4))
                jsonFile.close()
                print('JSON Match Table saved!')

                jsonFile = open("no_match_table.json", "w")
                jsonFile.write(json.dumps(self.no_match_table, indent=4))
                jsonFile.close()
                print('JSON No Match Table saved!')

                print(f'Variants matched: {self.number_match}/{(self.number_match + self.number_no_match + self.number_no_results)}')

                print('----------------------------------------------------------')

                return
        elif self.search_term == "":
            self.current_search_term = self.current_search_term + 1
            self.page = 0
            return scrapy.Request(new_url, callback = self.parse, dont_filter = True)
        else:
          
            print(f'Still within array...{self.current_search_term}/{len(self.search_term)}')
                
            #total number of results for single search term
            print (f'Total result count: {json_response["count"]}')

            if json_response["count"] < 1 and self.page == 0:
                no_results_id_table = {

                    "Variant_id": [],
                    "Variant": [],
                    "Page": [],
                    "Attempted_matches": [],
                    "Protein_Change": [],
                    "HGVS_cDNA": [],
                    "HGVS_Protein": [],
                    "BIC_Nomenclature": []
                }
                no_results_id_table['Variant_id'] = self.current_search_term
                no_results_id_table['Variant'] = self.search_term[self.current_search_term]
                no_results_id_table['Page'] = self.page
                no_results_id_table['Attempted_matches'] = json_response['count']
                self.no_match_table['No_Match_Results'].append(no_results_id_table)
                self.number_no_results = self.number_no_results + 1

            #checks for last results page (data null)
            if json_response["data"] == []:
                
                # print(f'Length search term: {len(self.search_term)}')
                # print(f'Current term index: {self.current_search_term}')
                # print(f'Current page: {self.page}')

                self.current_search_term = self.current_search_term + 1
                self.page = 0
                self.matched = ""

                # def table_reset():
                #         self.id_table['id'].pop(0)
                #         self.id_table['Variant'].pop(0)
                #         self.id_table['Protein_Change'].pop(0)
                #         self.id_table['HGVS_cDNA'].pop(0)
                #         self.id_table['HGVS_Protein'].pop(0)
                #         self.id_table['BIC_Nomenclature'].pop(0)
                # table_reset()
                
                if self.current_search_term >= len(self.search_term):
                    print('>>> Database fully searched.')

                    jsonFile = open("match_table.json", "w")
                    jsonFile.write(json.dumps(self.match_table, indent=4))
                    jsonFile.close()
                    print('JSON Match Table saved!')

                    jsonFile = open("no_match_table.json", "w")
                    jsonFile.write(json.dumps(self.no_match_table, indent=4))
                    jsonFile.close()
                    print('JSON No Match Table saved!')

                    print(f'Variants matched: {self.number_match}/{(self.number_match + self.number_no_match + self.number_no_results)}')

                    print('----------------------------------------------------------')
                    return

                new_url = f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={self.page}&search_term={self.search_term[self.current_search_term]}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3'
    
                # print(f'Updated term index: {self.current_search_term}')
                # print(f'Updated page: {self.page}')
                print ('No further results, searching for the next variant...')

                return scrapy.Request(new_url, callback = self.parse, dont_filter = True)
            
                #not last page, continues on
            else:
                match_id_table = {

                    "Variant_id": [],
                    "Variant": [],
                    "Page": [],
                    "Protein_Change": [],
                    "HGVS_cDNA": [],
                    "HGVS_Protein": [],
                    "BIC_Nomenclature": []
                }

                no_match_id_table = {

                    "Variant_id": [],
                    "Variant": [],
                    "Page": [],
                    "Attempted_matches": [],
                    "Protein_Change": [],
                    "HGVS_cDNA": [],
                    "HGVS_Protein": [],
                    "BIC_Nomenclature": []
                }

                for result in json_response["data"]:
                    
                    def remove_parenthesis (i):
                        # if i == None:
                        #     return
                        start = i.find("(")
                        end = i.find(")")
                        if start != -1 and end != -1:
                            i = i[start+1:end]
                            return (i)
                        elif start == -1 and end != -1:
                            i = i[:end]
                            return (i)
                        elif start != -1 and end == -1:
                            i = i[start+1:]
                            return (i)
                        else:
                            return (i)
                    def remove_p(i):
                        # if i == None:
                        #    return
                        if "p." in i:
                            i = i.replace("p.", "")
                            return(i)
                        else:
                            return (i)
                    def remove_c(i):
                        # if i == None:
                        #    return
                        if "c." in i:
                            i = i.replace("c.", "")
                            return (i)
                        else:
                            return (i)

                    def remove_ast(i):
                        # if i == None:
                        #    return
                        if "*" in i:
                            i = i.replace("*", "ter")
                            return(i)
                        else:
                            return(i)
                    def remove_x(i):
                        # if i == None:
                        #    return
                        if "x" in i:
                            i = i.replace("x", "*")
                            return(i)
                        else:
                            return(i)
                    def remove_ivs(i):
                        # if i == None:
                        #    return
                        if "ivs" in i:
                            i = i.replace("ivs", "")
                            return(i)
                        else:
                            return(i)

                    i = str(self.search_term[self.current_search_term].lower())
                    cut_parenth_i = remove_parenthesis(i)
                    cut_x = remove_x(cut_parenth_i)
                    cut_ast = remove_ast(cut_x)
                    cut_p = remove_p(cut_ast)
                    cut_c = remove_c(cut_p)
                    cut_ivs = remove_ivs(cut_c)
                    final_input = str(cut_ivs)
                    # regex_input = re.escape(final_input)
                    input_search = r".*\b" + final_input + r"\b"

                    Change = str(result['Protein_Change']).lower()
                    Change_cut_parenth_i = remove_parenthesis(Change)
                    Change_cut_x = remove_x(Change_cut_parenth_i)
                    Protein_Change_search = str(Change_cut_x)

                    cDNA = str(result['HGVS_cDNA']).lower()
                    cDNA_cut_parenth_i = remove_parenthesis(cDNA)
                    cDNA_cut_c = remove_c(cDNA_cut_parenth_i)
                    HGVS_cDNA_search = str(cDNA_cut_c)

                    Protein = str(result['HGVS_Protein']).lower()
                    Protein_cut_parenth_i = remove_parenthesis(Protein)
                    Protein_cut_p = remove_p(Protein_cut_parenth_i)
                    Protein_cut_ast = remove_ast(Protein_cut_p)
                    HGVS_Protein_search = str(Protein_cut_ast)

                    BIC = str(result['BIC_Nomenclature']).lower()
                    BIC_cut_parenth_i = remove_parenthesis(BIC)
                    BIC_cut_ivs = remove_ivs(BIC_cut_parenth_i)
                    BIC_Nomenclature_search = str(BIC_cut_ivs)

                    def match_table_update():
                        match_id_table['Variant_id'] = self.current_search_term
                        match_id_table['Variant'] = self.search_term[self.current_search_term]
                        match_id_table['Page'] = self.page
                        
                        if Protein_Change_search == "-":
                            None
                        elif Protein_Change_search == "?":
                            None
                        else:
                            match_id_table['Protein_Change'].append(result ['Protein_Change'])
                        
                        if HGVS_cDNA_search == "-":
                            None
                        else:
                            match_id_table['HGVS_cDNA'].append(result ['HGVS_cDNA'])

                        if "?" in HGVS_Protein_search:
                            None
                        else:
                            match_id_table['HGVS_Protein'].append(result ['HGVS_Protein'])
                        
                        if BIC_Nomenclature_search == "-":
                            None
                        else:
                            match_id_table['BIC_Nomenclature'].append(result ['BIC_Nomenclature'])
                        

                    def no_match_table_update():
                        no_match_id_table['Variant_id'] = self.current_search_term
                        no_match_id_table['Variant'] = self.search_term[self.current_search_term]
                        no_match_id_table['Page'] = self.page
                        no_match_id_table['Attempted_matches'] = json_response['count']

                        if Protein_Change_search == "-":
                            None
                        elif Protein_Change_search == "?":
                            None
                        else:
                            no_match_id_table['Protein_Change'].append(result ['Protein_Change'])
                        
                        if HGVS_cDNA_search == "?":
                            None
                        else:
                            no_match_id_table['HGVS_cDNA'].append(result ['HGVS_cDNA'])
                        
                        if "?" in HGVS_Protein_search:
                            None
                        else:
                            no_match_id_table['HGVS_Protein'].append(result ['HGVS_Protein'])
                        
                        if BIC_Nomenclature_search == "-":
                            None
                        else:
                            no_match_id_table['BIC_Nomenclature'].append(result ['BIC_Nomenclature'])
                        

                    # print(f'Input search: {final_input}')
                    # print(f'Protein change search: {Protein_Change_search}')
                    # print(f'HGVS cDNA search: {HGVS_cDNA_search}')
                    # print(f'HGVS protein search: {HGVS_Protein_search}')
                    # print(f'BIC nomenclature search: {BIC_Nomenclature_search}')
                    print(f'Search term pre-cutting: {i}')
                    print(f'Search term post-cutting: {input_search}')
                    print(f'Page: {self.page}')
                    if re.search(input_search, Protein_Change_search) is not None:
                        self.matched = "YES"
                        match_table_update()
                        print('Protein match found!')

                    elif re.search(input_search, HGVS_cDNA_search) is not None:
                        self.matched = "YES"
                        match_table_update()
                        print('Nucleotide match found!')

                    elif re.search(input_search, HGVS_Protein_search) is not None:
                        self.matched = "YES"
                        match_table_update()
                        print('HGVS protein match found!')

                    elif re.search(input_search, BIC_Nomenclature_search) is not None:
                        self.matched = "YES"
                        match_table_update()
                        print('BIC des match found!')
                    
                    else:
                        self.matched = "NO"
                        no_match_table_update()
                        print('No match found...')
                    
                if self.matched == "YES":
                    self.number_match = self.number_match + 1
                    self.match_table['Match_Results'].append(match_id_table)
                elif self.matched == "NO":
                    self.number_no_match = self.number_no_match + 1
                    self.no_match_table['No_Match_Results'].append(no_match_id_table)
                else:
                    self.no_match_table['No_Match_Results'].append(no_match_id_table)
                    self.number_no_results = self.number_no_results + 1

                #set results page limit to X
                if self.page < 3:
                    self.page = self.page + 1
                else:
                    self.page = 100000000000
                    
                new_url = f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={self.page}&search_term={self.search_term[self.current_search_term]}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3'
        
                return scrapy.Request(new_url, callback = self.parse, dont_filter = True)
                
            #k1667x m1014l 1935d