"""
Info: fileProcessor é especializada em fazer o processamento de arquivos. Foi concebida para realizar processamentos
      de arquivos.
      Nesta versão, estamos trabalhando com arquivos .zip, .xml e colocamos as funcionalidades para:

      1. processZipWithSummarize
         Como o próprio nome já diz, fará o processamento do arquivo .zip. Este processamento analiza se dentro do
         arquivo .zip contem um ou N arquivos .xml (config. no .env através das chaves: TYPE_OF_ARCHIVE e
         CONTEXT_DESCRIBE).

         Se encontrar, entrará no arquivo e fará buscas pelo contexto CONTEXT_DESCRIBE que neste caso, buscamos por:
         "<flow name=" Se identificado o contexto, então o processamento registrará:
          1.1 nome do projeto mule-app;
          1.2 data e hora de extração destes dados (header);
          1.3 nome do arquivo xml;
          1.4 a quantidade de vezes que foi encontrado o context dentro do arquivo;
          1.5 os números das linhas onde cada context foi encontrado;
          1.6 o context que ele buscou dentro do arquivo;
          1.7 o path da pasta onde ele encontrou o arquivo
          1.8 path do arquivo .xml (body)
          1.9 o total de linhas lidas dentro do projeto com o contexto (footer)

      2. processZip
         Ele faz quase a mesma coisa, com a diferença que não tem um header nem um footer. Ele irá percorrer o arquivo,
         pegar os dados e entregar uma lista e portanto irá criar mais linhas... (particularmente prefiro a primeira
         operação). Mas aqui não é preferencia e sim a necessidade.

Autor: Everton Martins
Dt. 2023-09-27
version 1.0.0
"""

import zipfile
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('../config/.env')

# Variáveis Globais
TYPE_OF_ARCHIVE = os.getenv('TYPE_OF_ARCHIVE')
CONTEXT_DESCRIBE = os.getenv('CONTEXT_DESCRIBE')

dt_extraction = datetime.now().strftime('%Y-%m-%d')
hr_extraction = datetime.now().strftime('%H:%M:%S')


def processZipWithSummarize(zip_path, zip_name, val_body_sum, val_header, val_footer):
    print(f"Variável  CONTEXT_DESCRIBE: {CONTEXT_DESCRIBE} Carregada com sucesso!")
    print(f"Variável  TYPE_OF_ARCHIVE: {TYPE_OF_ARCHIVE} Carregada com sucesso!")
    header_dictionary = {}
    data_list = []
    footer_dictionary = {}

    with zipfile.ZipFile(os.path.join(zip_path, zip_name.upper()), 'r') as zp:
        icount_total_incidence = 0
        for file in zp.namelist():
            if file.endswith(TYPE_OF_ARCHIVE):
                with zp.open(file) as fl:
                    lines = fl.readlines()
                    icount = 0
                    lines_with_flow = []
                    lines_with_flow_str = ""
                    is_flow_name = 0

                    header_dictionary = {
                        val_header[0]: zip_name.upper(),    # nome do projeto
                        val_header[1]: dt_extraction,       # data em que foi extraído a informação
                        val_header[2]: hr_extraction        # hora em que foi extraído a informação
                    }

                    for idx, line in enumerate(lines):
                        if b'<flow name="' in line:
                            icount += 1                                         # qt de contexto encontrado no arquivo
                            icount_total_incidence += 1                         # total lines flow name in archive
                            lines_with_flow.append(str(idx + 1))                # line with flow name
                            lines_with_flow_str = ", ".join(lines_with_flow)    # lines with flow name
                            is_flow_name = 1

                    if is_flow_name:
                        body_dictionary = {
                            val_body_sum[0]: file,                         # XMLFile
                            val_body_sum[1]: str(icount),                  # FlowNameCount
                            val_body_sum[2]: lines_with_flow_str,          # Lines with flow name=
                            val_body_sum[3]: CONTEXT_DESCRIBE,             # Context search in arq .xml
                            val_body_sum[4]: os.path.dirname(file),        # FolderPath
                            val_body_sum[5]: os.path.join(zip_path, file)  # FilePath
                        }
                        data_list.append(body_dictionary)

                    footer_dictionary = {
                        val_footer[0]: icount_total_incidence,  # Total in lines read in project.
                    }

    return {"header": header_dictionary, "body": data_list, "footer": footer_dictionary}


def processZip(zip_path, zip_name, val_names):
    print(f"Variável  CONTEXT_DESCRIBE: {CONTEXT_DESCRIBE} Carregada com sucesso!")
    print(f"Variável  TYPE_OF_ARCHIVE: {TYPE_OF_ARCHIVE} Carregada com sucesso!")
    results = []
    with zipfile.ZipFile(os.path.join(zip_path, zip_name), 'r') as zp:
        for file in zp.namelist():
            if file.endswith(TYPE_OF_ARCHIVE):
                with zp.open(file) as fl:
                    lines = fl.readlines()
                    icount = 0
                    for idx, line in enumerate(lines):
                        if b'<flow name="' in line:
                            icount += 1
                            datadictionary = {
                                val_names[0]: zip_name,                     # Project
                                val_names[1]: file,                         # XMLFile
                                val_names[2]: str(idx + 1),                 # Line
                                val_names[3]: str(icount),                  # FlowNameCount
                                val_names[4]: CONTEXT_DESCRIBE,             # Contexto que buscamos nos arquivos .xml
                                val_names[5]: os.path.dirname(file),        # FolderPath
                                val_names[6]: os.path.join(zip_path, file)  # FilePath
                            }
                            results.append(datadictionary)
    return results
