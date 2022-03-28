import pandas as pd


def read_spreadsheet_and_return_dna_symbol(path):
    reader = pd.read_excel(path, header=2)

    dna_symbol = reader["ANALYZED/ PROTEIN"].tolist()

    return dna_symbol


# def is_field_nan(field):
