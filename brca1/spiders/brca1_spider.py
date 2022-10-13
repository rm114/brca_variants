import scrapy
import requests
import json
from nested_lookup import nested_lookup
from time import sleep

class Brca1Spider(scrapy.Spider):
    name = "brca1"
    start_urls = [
        'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num=0&search_term=&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3',
    ]
    
    page = 0

    HGVS_Nucleotide_list = []
    HGVS_Protein_list = []
    Protein_Abbrev_list = []
    BIC_des_list = []


    search_list = input('Input the search term:')
    search_term = search_list.split()


    #for i in search_term
    def parse(self, response):
        
        json_response = response.json()
        
        print('----------------------------------------------------------')

        print(self.page)
        print (self.search_list)
        print (self.search_term)
        print (self.search_term[0])
        sleep(3)
    
        self.page = self.page + 1
        print(self.page)
        new_url = f'https://brcaexchange.org/backend/data/?format=json&order_by=Gene_Symbol&direction=ascending&page_size=20&page_num={self.page}&search_term={self.search_term[0]}&include=Variant_in_ENIGMA&include=Variant_in_ClinVar&include=Variant_in_1000_Genomes&include=Variant_in_ExAC&include=Variant_in_LOVD&include=Variant_in_BIC&include=Variant_in_ESP&include=Variant_in_exLOVD&include=Variant_in_ENIGMA_BRCA12_Functional_Assays&include=Variant_in_GnomAD&include=Variant_in_GnomADv3'
        
        HGVS_Nucleotide = nested_lookup(
            key = "HGVS_cDNA",
            document = json_response,
        )

        HGVS_Protein = nested_lookup(
            key = "HGVS_Protein",
            document = json_response,
        )

        Protein_Abbrev = nested_lookup(
            key = "Protein_Change",
            document = json_response,
        )

        BIC_des = nested_lookup(
            key = "BIC_Nomenclature",
            document = json_response,
        )

        result_end = nested_lookup(
            key = "data",
            document = json_response,
        )

        if result_end[0] == []:
            print('Lists compiled.')
            return

        self.HGVS_Nucleotide_list.extend(HGVS_Nucleotide)
        self.HGVS_Protein_list.extend(HGVS_Protein)
        self.Protein_Abbrev_list.extend(Protein_Abbrev)
        self.BIC_des_list.extend(BIC_des)

        #self.list[:] = (elem[12:] for elem in self.list)

        # print(self.HGVS_Nucleotide_list)
        # print('~+~+~+~+~+~+~+~+~+~+~')
        # print(self.HGVS_Protein_list)
        # print('~+~+~+~+~+~+~+~+~+~+~')
        # print(self.Protein_Abbrev_list)
        # print('~+~+~+~+~+~+~+~+~+~+~')
        # print(self.BIC_des_list)
        yield scrapy.Request(new_url, callback = self.parse, dont_filter = True)
        
        print('----------------------------------------------------------')