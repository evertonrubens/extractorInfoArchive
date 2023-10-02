# extractorInfoArchive
Sistema batch criado em python para buscar informações em estruturas de arquivos compactadas, procurando por arquivos com extensões e trechos de códigos pre configurados em um .env. Se encontrado ele irá extrair uma série de informações e irá gerar como saída um relatório com header, body e footer em .csv.
O que o sistema faz?
  Com base nas configurações contidas no arquivo .env, fica ouvindo uma pasta que foi definida pelo usuário do sistema. Na estrutura do sistema, deixei o IN, mas pode ser qualquer  pasta que você (usuário) definir no /config/.env. Aliás, nesta estrutura, adicionei o .env (arquivo de configuração) justamente 
  para facilitar nossa lógica no sistema. Além disso, criamos com isso uma parametrização do sistema.
        Depois, veja o arquivo .env localizado no /config. Da para ser feito muita coisa muito em função destas parametrizações. 
        
        Deixei previamente fácil para:
        IN_FOLDER;
        OUT_FOLDER; 
        REPORT_FOLDER; 
        TYPE_OF_ARCHIVE;
        CONTEXT_DESCRIBE;
        HEADER_REPORT;
        BODY_REPORT_SUM (summarize);
        FOOTER_REPORT;
        FIELD_NAMES_REPORT;
        TYPE_REPORT.
        
        Então o sistema fica ouvindo o path do conteúdo da chave IN_FOLDER e qualquer arquivo .zip que for colocado nesta pasta, 
        será processado, desta  forma, será aberto e o sistema  irá  procurar  por arquivos com  extensão  que estiver na chave: 
        TYPE_OF_ARCHIVE (no nosso caso,  ".xml".  Se encontrar  arquivos [.xml], então, dentro de  cada arquivo  .xml o  sistema 
        deverá buscar pela palavra que estiver na chave CONTEXT_DESCRIBE. O context  é  para buscar qualquer tipo de informação.
        No nosso caso, estamos procurando arquivos .xml de  projetos de mule-apps  (MuleSoft Anypoint Studio) que tenham mais de 
        um <flow name=. Se encontrado, então, irá obter várias informações e no final do seu  processamento  criará um relatório 
        .csv  sumarizado,  informando ao usuário, nome  do projeto, nome de  arquivos e endereço destes arquivos que contenham o 
        CONTEXT_DESCRIBE  procurado,  em que linha  de cada  arquivo encontra-se  este contexto e quantos contextos por arquivos 
        foram encontrados e em footer, o total de contextos encontrados em um ou mais arquivos.

        Todas informações parametrizaveis, deverão estar dentro do arquivo .env localizado na pasta config. Nesta versão, ofereço 
        dois tipos de saídas de relatórios em .csv
        
        São eles:
        1 = REPORT LIST (mais simples)
        2 = REPORT SUMMARY (mais complexo, com header, body e footer)
        se a chave: TYPE_REPORT="2", então o sistema irá criar um .csv com header, body e footer.
        se a chave: TYPE_REPORT="1", então o sistema irá criar um .csv com uma lista completa repetindo algumas
        informaçoes (lista).

O sistema não foi feito pensando apenas em mule-app. Veja no arquivo .env que você entenderá. Podemos informar qual é o caminho das pastas que ele ficará ouvindo, para qual pasta irá  mover  os arquivos do IN após o processamento e por fim onde os relatórios .csv serão armazenados. Também é possivel informar qual tipo de arquivo desejamos pesquisar e o que queremos pesquisar. O sistema está desocoplado, de forma que temos um gerenciador (main) e fileManager.py, fileProcessor.py que são especialistas no que  foram fundamentado.  Assim, se precisarmos ter  outras classes especialistas,  bastará criarmos e adicionar uma lógica no main.

##IMPORTANTE:
    1. Certifique-se de que você tem o python instalado em seu ambiente de trabalho, para isso execute:
          python --version  ou python3 --version
          se tiver algum python instalado, o terminal escreverá na sua saída
          Python 3.8.10 (minha versão até o dia 02/10/2023)

    2. Para executar o sistema, vá até a pasta src do projeto via command / terminal ou via terminal integrado do vscode.
          execute a instrução: python .\main.py
          exemplo: c:\pyton\extractorInfo\src> python .\main.py

          Se tiver tudo certinho, vc terá a seguinte saída:
              PS c:\python\extractorInfo\src> python .\main.py (enter)
                  
                  saída do processamento:
                  ----------------------------------------------
                  Processamento iniciado em: 2023-10-02-20:06:55 
                  ----------------------------------------------

                  Variável IN_FOLDER: D:/Workspace/desenvolvimento/python/extractorInfo/in Carregada com sucesso!
                  Variável  OUT_FOLDER: D:/Workspace/desenvolvimento/python/extractorInfo/out Carregada com sucesso!
                  Variável  REPORT_FOLDER: D:/Workspace/desenvolvimento/python/extractorInfo/report Carregada com sucesso!
                  Variável  FIELD_NAMES_REPORT: PROJECT,ARQUIVO_XML,QTD_INCID_ENCONTRA,LINHAS_POR_ARQ,CONTEXTO,CAMINHO_PASTA,CAMINHO_ARQUIVO Carregada com sucesso!
                  Variável  TYPE_REPORT: 2 Carregada com sucesso!
                  Variável  HEADER_REPORT: NOME_PROJETO,DATA_EXTRACAO,HORA_EXTRACAO Carregada com sucesso!
                  Variável  BODY_REPORT_SUM: ARQUIVO_XML,QTD_INCID_ENCONTRA,LINHAS_POR_ARQ,CONTEXTO,CAMINHO_PASTA,CAMINHO_ARQUIVO Carregada com sucesso!
                  Variável  FOOTER_REPORT: TOTAL_LINHAS_INCID_PROJETO Carregada com sucesso!
                  Variável  CONTEXT_DESCRIBE: <flow name= Carregada com sucesso!
                  Variável  TYPE_OF_ARCHIVE: .xml Carregada com sucesso!
                  Total de arquivos processados: 1 

                  ------------------------------------------------
                  Processamento finalizado em: 2023-10-02-20:06:55 
                  ------------------------------------------------

                  Neste exemplo, 
                  havia um arquivo de um projeto mule-app na pasta IN ele identificou, abriu varreu procurando arquivo .xml encontrou e processou buscando 
                  informações dentro deste arquivo que tivesse uma interseção com <flow name=

Até a proxima...

Everton Rubens
#JuntosSomosMaisFortes
#SEMPRE
