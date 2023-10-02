"""
Info: fileManager é especializada em gerenciar arquivos. Foi concebido justamente para tratar quaisquer tipo de
      arquivos. Nesta v1, colocamos funcionalidades para:
      1. getZipFiles(path)
         dado um path de pasta,se encarregará de ler todos os arquivos com a extenção .zip e devolver uma lista

      2. moveFile(src_path, dest_path, file_name)
         Move um arquivo da pasta de origem para uma pasta de destino.

      3. saveToCSV
         Obtem o resultado do processamento e o grava em um arquivo .csv como um relatório formato lista.

      4. saveToCSVSummarize
         Obtem o resultado do processamento e o grava em um arquivo .csv como um relatório em formato Sumarizado,
         mais inteligênte com um header, um body e um footer.

      Importante: Qualquer tipo de arquivo novo que queiramos trabalhar, esta é a classe para especializar.

Autor: Everton Martins
Dt. 2023-09-27
version 1.0.0
"""

import csv
import os
import shutil
from datetime import datetime

# Variáveis Globais
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')


def getZipFiles(path):
    return [file for file in os.listdir(path) if file.endswith('.zip')]


def moveFile(src_path, dest_path, file_name):
    shutil.move(os.path.join(src_path, file_name), os.path.join(dest_path, file_name))


def saveToCSV(report_folder, data, project_name, field_names):
    file_name = f"{timestamp}_{project_name}.csv"

    with open(os.path.join(report_folder, file_name), mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=field_names, delimiter=';')
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def saveToCSVSummarize(report_folder, data, project_name, body_names, header_names, footer_names):
    file_name = f"{timestamp}_{project_name}_summarize.csv"

    with open(os.path.join(report_folder, file_name), mode='w', newline='', encoding='utf-8') as file:
        if header_names is not None:
            header_writer = csv.DictWriter(file, fieldnames=header_names, delimiter=';')
            header_writer.writeheader()
            header_writer.writerow(data["header"])

        if body_names is not None:
            body_writer = csv.DictWriter(file, fieldnames=body_names, delimiter=';')
            body_writer.writeheader()
            for row in data["body"]:
                body_writer.writerow(row)

        if footer_names is not None:
            footer_writer = csv.DictWriter(file, fieldnames=footer_names, delimiter=';')
            footer_writer.writeheader()
            footer_writer.writerow(data["footer"])
