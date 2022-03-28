from read_spreadsheet import read_spreadsheet_and_return_dna_symbol

import json

import pandas as pd

import requests

import urllib

write_list = []

gene_list = read_spreadsheet_and_return_dna_symbol("./arquivos/planilha.xlsx")

HEADERS = {
    'Accept': 'application/json',
}

BASE_URL = 'http://rest.genenames.org/fetch/'

result_table_lines = [
    ["index", "HGNC ID", "Atualizado para", "identificação do gene NCBI"]]


for index, gene in enumerate(gene_list):
    if not pd.isna(gene):
        gene = gene.strip()
        url = f'{BASE_URL}symbol/{gene}'

        print(f"URL: {url}")

        response = requests.get(url=url, headers=HEADERS)
        response_dict = response.json()
        results_amount = response_dict['response']['numFound']

        if results_amount:
            # lógica para resultado em symbol
            print(f'{gene} encontrado em symbol')
            result = response_dict['response']['docs'][0]
            hgnc_id = result['hgnc_id']
            symbol = None
            name = result['name']

            result_table_lines.append([index, hgnc_id, symbol, name])

        else:
            url = f'{BASE_URL}alias_symbol/{gene}'

            print(f"URL: {url}")

            response = requests.get(url=url, headers=HEADERS)
            response_dict = response.json()

            results_amount = response_dict['response']['numFound']

            if results_amount:
                # lógica para resultado em alias_symbol
                print(f'{gene} encontrado em alias_symbol')
                result = response_dict['response']['docs'][0]
                hgnc_id = result['hgnc_id']
                symbol = result['symbol']
                name = result['name']

                result_table_lines.append([index, hgnc_id, symbol, name])

            else:
                # lógica para nenhum resultado encontrado.
                print(f"{gene} nenhum resultado encontrado")
                result_table_lines.append(
                    [index, "Not Found", "Not Found", "Not Found"])

    else:
        # espaços em branco na planilha
        print("espaço em branco")
        result_table_lines.append([index, None, None, None])


df = pd.DataFrame(result_table_lines)

df.to_excel("./arquivos/resultados.xlsx")
