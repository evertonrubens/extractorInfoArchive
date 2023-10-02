
"""
Info: Este é ponto de entrada do sistema batch. O main vai cadenciar as orquestrações das operações contidas nas
      outras classes que compõe este sistema batch.
      O que o sistema faz?
        Com base nas configurações contidas no arquivo .env, fica ouvindo uma pasta que foi definida pelo usuário
        do sistema. Na estrutura do sistema, deixei o IN, mas pode ser qualquer pasta que você (usuário) definir no
        /config/.env
        Aliá, nesta estrutura, adicionei o .env (arquivo de configuração) justamente para facilitar nossa lógica no
        sistema. Além disso, criamos com isso uma parametrização do sistema.
        Depois, veja o arquivo .env localizado no /config. Da para ser feito muita coisa muito em função destas
        parametrizações. Deixei previamente fácil para:
        IN_FOLDER, OUT_FOLDER, REPORT_FOLDER, TYPE_OF_ARCHIVE, CONTEXT_DESCRIBE, HEADER_REPORT, BODY_REPORT_SUM,
        FOOTER_REPORT, FIELD_NAMES_REPORT e TYPE_REPORT.
        Então o sistema fica ouvindo o path do conteúdo da chave IN_FOLDER e qualquer arquivo .zip que cair nele,
        será processado, de forma a abrir, procurar por arquivos [.xml].
        Se encontrar arquivos [.xml], então dentro de cada arquivo, o sistema deverá buscar pela palavra chave
        CONTEXT_DESCRIBE.
        Este context é para buscar qualquer tipo de informação... No nosso caso, estamos procurando arquivos de
        projetos mule-apps que tenham mais de um <flow name=. Se encontrado, então ele irá obter uma série de
        informações e no final do seu processamento vai criar um relatório .csv sumarizado contextualizando e
        informando ao usuário, nome do projeto, nome de arquivos e endereço destes arquivos que contenham o
        CONTEXT_DESCRIBE procurado, em que linha de cada arquivo encontra este contexto e quantos contexto por
        arquivo foram encontrados e em footer o total de contextos encontrados em um ou mais arquivos.

      Todas informações parametrizaveis, deverão estar dentro do arquivo .env localizado na pasta config.
      Também estou oferecendo dois tipos de saídas de relatórios em .csv.
      São eles:
        1 = REPORT LIST (mais simples)
        2 = REPORT SUMMARY (mais complexo, com header, body e footer)
        se a chave: TYPE_REPORT="2", então o sistema irá criar um .csv com header, body e footer.
        se a chave: TYPE_REPORT="1", então o sistema irá criar um .csv com uma lista completa repetindo algumas
        informaçoes (lista).

      Tudo aqui pode ser incrementado e ele  não foi  feito  pensando  apenas em mule-app. Veja no arquivo .env,
      Você entenderá.

      Podemos informar qual é o caminho das pastas que ele ficará ouvindo, para qual past irá mover o arquivo
      do IN após o processamento e por fim onde o relatório .csv será armazenado.
      Também é possivel informar  qual tipo de arquivo desejamos pesquisar e o que queremos pesquisar.

      O sistema está desocoplado, de forma que temos um gerenciador (main) e fileManager.py, xmlProcessor.py que são
      especialistas no que foram fundamentado. Assim, se precisarmos ter outras classes especialistas, bastará criarmos
      e adicionar uma lógica no main.

Autor: Everton Martins
Dt. 2023-09-27
version 1.0.0
"""

# Declaração de bibliotecas que faremos uso
import os
from dotenv import load_dotenv
from fileManager import getZipFiles, moveFile, saveToCSV, saveToCSVSummarize
from fileProcessor import processZip, processZipWithSummarize
from datetime import datetime

# Declaração da operação que faramos uso para ler o arquivo environment em /config/.env
load_dotenv('../config/.env')

IN_FOLDER = os.getenv('IN_FOLDER')
OUT_FOLDER = os.getenv('OUT_FOLDER')
REPORT_FOLDER = os.getenv('REPORT_FOLDER')
FIELD_NAMES_REPORT = os.getenv('FIELD_NAMES_REPORT')
TYPE_REPORT = os.getenv('TYPE_REPORT')
HEADER_REPORT = os.getenv('HEADER_REPORT')
FOOTER_REPORT = os.getenv('FOOTER_REPORT')
BODY_REPORT_SUM = os.getenv('BODY_REPORT_SUM')

"""
 Declaração da definição da main() classe principal que irá orquestrar as todas as operações necessárias para o seu bom 
 funcionamento.
"""


def main():
    iarq_process = 0
    dt_exec = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    print("----------------------------------------------")
    print(f"Processamento iniciado em: {dt_exec} ")
    print("----------------------------------------------")
    print("")

    # logs informativos para logar que todas as variáveis necessárias para a execução das
    # funções dentro do main() estão ok.
    print(f"Variável IN_FOLDER: {IN_FOLDER} Carregada com sucesso!")
    print(f"Variável  OUT_FOLDER: {OUT_FOLDER} Carregada com sucesso!")
    print(f"Variável  REPORT_FOLDER: {REPORT_FOLDER} Carregada com sucesso!")
    print(f"Variável  FIELD_NAMES_REPORT: {FIELD_NAMES_REPORT} Carregada com sucesso!")
    print(f"Variável  TYPE_REPORT: {TYPE_REPORT} Carregada com sucesso!")
    print(f"Variável  HEADER_REPORT: {HEADER_REPORT} Carregada com sucesso!")
    print(f"Variável  BODY_REPORT_SUM: {BODY_REPORT_SUM} Carregada com sucesso!")
    print(f"Variável  FOOTER_REPORT: {FOOTER_REPORT} Carregada com sucesso!")

    # Variavel necessária para ouvirmos a pasta onde será incluída os arquivos .zip
    zip_files = getZipFiles(IN_FOLDER)

    header_names = HEADER_REPORT.strip("[]\n").split(',')
    body_names = FIELD_NAMES_REPORT.strip("[]\n").split(',')
    body_names_sum = BODY_REPORT_SUM.strip("[]\n").split(',')
    footer_names = FOOTER_REPORT.strip("[]\n").split(',')
    is_report_type = TYPE_REPORT == "1"

    """
    Comando Laço (FOR) para ficar ouvindo a pasta IN, se houver algum arquivo .zip ele inicilizará o processo
    abrindo o arquivo, procurando por arquivos .XML de forma recursiva (lendo todas as sub-pastas e pacotes). 
    Se encontrar  um  .XML, o sistema irá percorre-lo procurando pelo CONTEXT_DESCRIBE="<flow name=" que está
    dentro do .env, assim como outros parametros como o proprio tipo de arquivo que queremos pesquisar.
    """
    for zipFile in zip_files:

        # SE is_report_type = 1 ENTAO REPORT LIST (MAIS SIMPLES), SE = 2 É O REPORT SUMMARY
        if is_report_type:
            result_data = processZip(IN_FOLDER, zipFile, body_names)

            # SE result_data <> "" então teremos uma lista da dados em formato list para podermos
            # salva-lo em um arquivo .csv
            if result_data:
                project_name = zipFile.split(".")[0]
                saveToCSV(REPORT_FOLDER, result_data, project_name, body_names)
                moveFile(IN_FOLDER, OUT_FOLDER, zipFile)
                iarq_process += 1

        # Se não, o is_report_type <> 1 no caso é um 2 (conforme definido no .env), o  sistema irá
        # processar em forma summarize (mais completo).
        else:
            result_data = processZipWithSummarize(IN_FOLDER, zipFile, body_names_sum, header_names, footer_names)
            project_name = zipFile.split(".")[0]

            # SE result_data <> "" então teremos uma lista da dados em formato list para podermos
            # salva-lo em um arquivo .csv
            if result_data:
                saveToCSVSummarize(REPORT_FOLDER, result_data, project_name, body_names_sum, header_names, footer_names)
                moveFile(IN_FOLDER, OUT_FOLDER, zipFile)
                iarq_process += 1

    print(f"Total de arquivos processados: {iarq_process} ")
    print("")

    dt_exec = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    print("------------------------------------------------")
    print(f"Processamento finalizado em: {dt_exec} ")
    print("------------------------------------------------")


if __name__ == "__main__":
    main()
    