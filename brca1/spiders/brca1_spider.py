import scrapy
from time import sleep
import json
import re
from .functions import *

#Syapse variant validation script
#Started 10/13/2022
#Written in Python 3.10.7
class Brca1Spider(scrapy.Spider):
    #To execute: scrapy crawl variants
    name = "variants"
    #results page #
    page = 0
   
    gene = input('Input which gene you want to query (BRCA1, BRCA2, or both):')
    search_list = input('Input the variant(s):')
    #first, splits by comma
    search_term = search_list.split()
    #index # of current search term
    current_search_term = 0


    ignore_list = ["variant", "not", "found", "match", "matched", "report", "reported", "NM_007294.2", "NP_009225.1", "p", "brca1", "brca2", "stated", "positive", "dup", "del", "truncation", "intron", "exon", "introns", "exons", "ivs", "intronic", "deletion"]

    print("------------------------------------------")
   
    matched = ""
    number_match = 0
    number_no_match = 0
    number_no_results = 0
    number_excluded = 0

    start_urls = [f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={page}&search_term={search_term[current_search_term]}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3']
    match_table = {
        "Match_Results": []
    }
    no_match_table = {
        "No_Match_Results": []
    }
    misc_table = {
        "Misc_Results": []
    }

    def parse(self, response):

        #get the data drom database
        json_response = response.json()
        
        print('----------------------------------------------------------')

        print(f'Current search term: {self.search_term[self.current_search_term]}')
        print(f'Results page #: {self.page}')

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

                jsonFile = open("misc_table.json", "w")
                jsonFile.write(json.dumps(self.misc_table, indent=4))
                jsonFile.close()
                print('JSON Misc Table saved!')

                print(f'Variants matched: {self.number_match}/{(self.number_match + self.number_no_match + self.number_no_results)}')

                print('----------------------------------------------------------')

                return
    
        else:
          
            print(f'Still within array...{self.current_search_term + 1}/{len(self.search_term)}')
                
            #total number of results for single search term
            print (f'Total result count: {json_response["count"]}')

            #if small string (<4) or ignored word or only letters
            if len(str(self.search_term[self.current_search_term])) < 4  or self.search_term[self.current_search_term].lower() in self.ignore_list or re.search('[a-zA-Z]', self.search_term[self.current_search_term]) == None:
                misc_results_id_table = {

                    "Variant_id": [],
                    "Variant": [],
                    "Page": [],
                    "Note": [],
                    "Attempted_matches": []
                }
                misc_results_id_table['Variant_id'] = self.current_search_term + 1
                misc_results_id_table['Variant'] = self.search_term[self.current_search_term]
                misc_results_id_table['Page'] = self.page + 1
                misc_results_id_table['Attempted_matches'] = json_response['count']
                misc_results_id_table['Note'] = 'Invalid search term/variant'
                self.misc_table['Misc_Results'].append(misc_results_id_table)
                self.number_excluded = self.number_excluded + 1
                
                print(f'ERR: Invalid variant parsed: "{self.search_term[self.current_search_term]}", searching for the next variant...')

                #still more variants to be searched
                if len(self.search_term) - int(self.current_search_term) != 1:
                    self.current_search_term = self.current_search_term + 1
                    self.page = 0
    
                #if its the last variant in the array then end
                else:
                    print('>>> Database fully searched.')

                    jsonFile = open("match_table.json", "w")
                    jsonFile.write(json.dumps(self.match_table, indent=4))
                    jsonFile.close()
                    print('JSON Match Table saved!')

                    jsonFile = open("no_match_table.json", "w")
                    jsonFile.write(json.dumps(self.no_match_table, indent=4))
                    jsonFile.close()
                    print('JSON No Match Table saved!')

                    jsonFile = open("misc_table.json", "w")
                    jsonFile.write(json.dumps(self.misc_table, indent=4))
                    jsonFile.close()
                    print('JSON Misc Table saved!')

                    print(f'Variants matched: {self.number_match}/{(self.number_match + self.number_no_match + self.number_no_results)}')

                    print('----------------------------------------------------------')
                    
                    return
            
                new_url = f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={self.page}&search_term={self.search_term[self.current_search_term]}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3'
        
                return scrapy.Request(new_url, callback = self.parse, dont_filter = True)
           
            #if no results in BRCA exchange database
            if json_response["count"] < 1 and self.page == 0:
                no_results_id_table = {

                    "Variant_id": [],
                    "Variant": [],
                    "Page": [],
                    "Note": [],
                    "Attempted_matches": [],
                    "Gene_query(BRCA1/BRCA2)": [],
                    "Pathogenicity_all": [],
                    "Pathogenicity_expert": [],
                    "Protein_Change": [],
                    "HGVS_cDNA": [],
                    "HGVS_Protein": []
                }
                no_results_id_table['Variant_id'] = self.current_search_term + 1
                no_results_id_table['Variant'] = self.search_term[self.current_search_term]
                no_results_id_table['Page'] = self.page + 1
                no_results_id_table['Note'] = 'No results for this variant in BRCA Exchange database'
                no_results_id_table['Gene_query(BRCA1/BRCA2)'] = self.gene
                no_results_id_table['Attempted_matches'] = json_response['count']
                self.no_match_table['No_Match_Results'].append(no_results_id_table)
                self.number_no_results = self.number_no_results + 1
                
                print('ERR: No results found for this variant...')

            #checks for last results page (data is null)
            if json_response["data"] == []:

                self.current_search_term = self.current_search_term + 1
                self.page = 0
                self.matched = ""
                
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

                    jsonFile = open("misc_table.json", "w")
                    jsonFile.write(json.dumps(self.misc_table, indent=4))
                    jsonFile.close()
                    print('JSON Misc Table saved!')

                    print(f'Variants matched: {self.number_match}, variants not matched: {self.number_no_match}, variants not in the database: {self.number_no_results}, variants excluded: {self.number_excluded}')
                    print(f'Total variants searched: {(self.number_match + self.number_no_match + self.number_no_results)}')

                    print('----------------------------------------------------------')
                    
                    return

                new_url = f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={self.page}&search_term={self.search_term[self.current_search_term]}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3'
    
                print ('ERR: No further results, searching for the next variant...')

                return scrapy.Request(new_url, callback = self.parse, dont_filter = True)
            
            #not last page, continues on
            else:
                match_id_table = {

                    "Variant_id": [],
                    "Variant": [],
                    "Page": [],
                    "Note": [],
                    "Gene_query(BRCA1/BRCA2)": [],
                    "Pathogenicity_all": [],
                    "Pathogenicity_expert": [],
                    "Protein_Change": [],
                    "HGVS_cDNA": [],
                    "HGVS_Protein": []
                }

                no_match_id_table = {

                    "Variant_id": [],
                    "Variant": [],
                    "Page": [],
                    "Note": [],
                    "Attempted_matches": [],
                    "Gene_query(BRCA1/BRCA2)": [],
                    "Pathogenicity_all": [],
                    "Pathogenicity_expert": [],
                    "Protein_Change": [],
                    "HGVS_cDNA": [],
                    "HGVS_Protein": []
                }

                for result in json_response["data"]:

                        i = str(self.search_term[self.current_search_term].lower())
                        cut_parenth_i = remove_parenthesis(i)
                        cut_x = remove_x(cut_parenth_i)
                        cut_ast = remove_ast(cut_x)
                        cut_p = remove_p(cut_ast)
                        cut_c = remove_c(cut_p)
                        cut_ivs = remove_ivs(cut_c)
                        final_input = str(cut_ivs)
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
                            match_id_table['Variant_id'] = self.current_search_term + 1
                            match_id_table['Variant'] = self.search_term[self.current_search_term]
                            match_id_table['Page'] = self.page + 1
                            match_id_table['Gene_query(BRCA1/BRCA2)'] = self.gene
                            
                            if Protein_Change_search == "-":
                                None
                            elif Protein_Change_search == "?":
                                None
                            else:
                                match_id_table['Protein_Change'].append(result['Protein_Change'] + "[" + result["Gene_Symbol"] + "]")
                                match_id_table['Note'] = 'Variant data populated by protein match'
                            
                            if HGVS_cDNA_search == "-":
                                None
                            else:
                                match_id_table['Note'] = 'Variant data populated by HGVS cDNA match'
                                match_id_table['HGVS_cDNA'].append(result['HGVS_cDNA'] + "[" + result["Gene_Symbol"] + "]")

                            if "?" in HGVS_Protein_search:
                                None
                            else:
                                match_id_table['Note'] = 'Variant data populated by HGVS protein match'
                                match_id_table['HGVS_Protein'].append(result ['HGVS_Protein'] + "[" + result["Gene_Symbol"] + "]")

                            match_id_table['Pathogenicity_all'].append(result ['Pathogenicity_all'] + "[" + result["Gene_Symbol"] + "]")
                            match_id_table['Pathogenicity_expert'].append(result ['Pathogenicity_expert'] + "[" + result["Gene_Symbol"] + "]")
                            

                        def no_match_table_update():
                            no_match_id_table['Variant_id'] = self.current_search_term + 1
                            no_match_id_table['Variant'] = self.search_term[self.current_search_term]
                            no_match_id_table['Page'] = self.page + 1
                            no_match_id_table['Attempted_matches'] = json_response['count']
                            no_match_id_table['Gene_query(BRCA1/BRCA2)'] = self.gene

                            if Protein_Change_search == "-":
                                None
                            elif Protein_Change_search == "?":
                                None
                            else:
                                no_match_id_table['Note'] = 'No match found for this variant'
                                no_match_id_table['Protein_Change'].append(result ['Protein_Change'] + "[" + result["Gene_Symbol"] + "]")
                            
                            if HGVS_cDNA_search == "?":
                                None
                            else:
                                no_match_id_table['Note'] = 'No match found for this variant'
                                no_match_id_table['HGVS_cDNA'].append(result ['HGVS_cDNA'] + "[" + result["Gene_Symbol"] + "]")
                            
                            if "?" in HGVS_Protein_search:
                                None
                            else:
                                no_match_id_table['Note'] = 'No match found for this variant'
                                no_match_id_table['HGVS_Protein'].append(result ['HGVS_Protein'] + "[" + result["Gene_Symbol"] + "]")
                            
                            no_match_id_table['Pathogenicity_all'].append(result ['Pathogenicity_all'] + "[" + result["Gene_Symbol"] + "]")
                            no_match_id_table['Pathogenicity_expert'].append(result ['Pathogenicity_expert'] + "[" + result["Gene_Symbol"] + "]")
                            
                            
                        gene_symbol = str(result["Gene_Symbol"])
                        if gene_symbol.lower() == self.gene.lower() or self.gene.lower() == "both":
                            if re.search(input_search, Protein_Change_search) is not None or re.search(input_search, Protein_Change_search):
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
                        else:
                            print(f"Result not in {self.gene}, moving to next result...")
                    
                if self.matched == "YES":
                    self.number_match = self.number_match + 1
                    self.match_table['Match_Results'].append(match_id_table)
                else:
                    None

                if self.matched == "NO":
                    self.number_no_match = self.number_no_match + 1
                    self.no_match_table['No_Match_Results'].append(no_match_id_table)
                else:
                    None

                #set results page limit to X
                if self.page < 3:
                    self.page = self.page + 1
                else:
                    self.page = 100000000000
                    
                new_url = f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={self.page}&search_term={self.search_term[self.current_search_term]}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3'
        
                return scrapy.Request(new_url, callback = self.parse, dont_filter = True)
                
            #Control variants:
            #18-2delA, c.1405G>A, p.M1173V, E1210fs
            #18-2delA c.1405G>A p.M1173V E1210fs