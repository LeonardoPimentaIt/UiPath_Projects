Projeto

#RPA de Busca CNAE Seções A, B e C.

- RPA construído com o uso do REFramework

- Para a execução do RPA é necessário.

    1 - Criação da fila no orquestrador com o nome: Fila_Busca_CNAE_IBGE
    2 - Ajustar no arquivo Config o caminho do pythonPath da máquina.(este item corresponde ao caminho de instalação do python)

O arquivo config fica no caminho "\Busca_De_Dados_CNAE\Data\Config.xlsx"

O script Python fica no caminho "\Busca_De_Dados_CNAE\Data\pyScript.py"

Passo a passo do RPA

1 - No estado inicial do REFramework o RPA irá na primeira execução(First Run) alimentar a fila com os itens do arquivo "Arquivo_De_Secoes_Para_Leitura"
    que está localizado no caminho "\Busca_De_Dados_CNAE\Data\Arquivo_De_Secoes_Para_Leitura.xlsx"

    No arquivo já irão constar as seções A,B e C para extração.
#    

2 - Também no estado inicial o RPA irá acessar a URL do site do IBGE. Está etapa foi construída dentro do workflow "InitAllApplications". Ele possui um Retry Scope para
    tentar o acesso ao site por 3 vezes.
#

3 - Após alimentar a fila e acessar o site no estado inicial o RPA seguirá para o estado "Get Transaction Data" onde no workflow "GetTransactionData" irá pegar cada item 
    para que seja executado dentro do processo de extração para cada seção.
#

4 - Após obter o item a ser transacionado ele irá para o Estado "Process Transaction" onde irá processar o Item, ou seja, fará a extração dos dados daquela seção.
#
Agora irei detalhar o processo desenvolvido.
#
1 - No primeiro workflow(Build_CNAE_DataTable) será criado o DataTable do CNAE, com as colunas que serão preenchidas durante o processo.
#
2 - No segundo workflow(Reading_Specific_Item_Content) será extraido do transaction item a informação necessária ao processo que está na variável in_TransactionItem.
#
3 - No terceiro workflow(Reading_Sections) ele fará a leitura das seções do site do IBGE.
#
4 - No quarto workflow(Accessing_Specific_Section) ele irá acessar a código da seção relacionada ao item que está sendo transacionado.
    Caso o código não seja localizado o RPA irá gerar uma business exception para o item e esta informação irá constar na fila do orchestrator.
#
5 - Após acessar a seção, no workflow(Reading_Division_And_Generate_TrElements), o RPA irá realizar a leitura das divisões e carregar uma variável com a quantidade total de linhas.
#
6 - Na etapa posterior(Acessing_Specific_Division workflow) ele irá acessar a divisão, que terá sua contagem iniciada de 1.
#
7 - Após acessar a seção, no workflow(Reading_Groups_And_Generate_TrElements workflow), o RPA irá realizar a leitura das divisões e carregar uma variável com a quantidade total de linhas.
#
8 - Na etapa posterior(Acessing_Specific_Group) ele irá acessar a divisão, que terá sua contagem iniciada de 2.
#
9 - Após acessar a seção, no workflow(Reading_Classes_And_Generate_TrElements workflow), o RPA irá realizar a leitura das divisões e carregar uma variável com a quantidade total de linhas.
#
10 - Na etapa posterior(Acessing_Specific_Class) ele irá acessar a divisão, que terá sua contagem iniciada de 3.
#
11 - Após acessar a seção, no workflow(Reading_Subclass_And_Generate_TrElements), o RPA irá realizar a leitura das divisões e carregar uma variável com a quantidade total de linhas.
#
12 - Na etapa posterior(Acessing_Specific_Subclass) ele irá acessar a divisão, que terá sua contagem iniciada de 4.
#
13 - Na próxima etapa(Extracting_Data), o RPA fará a extração da da tabela com os dados que precisam ser salvos no data table.
#
14 - Na próxima etapa(Feeding_Busca_CNAE_DataTable workflow), o RPA irá alimentar o datatable com as informações extraídas do site.

OBS.: Foi desenvolvida uma lógica onde o RPA percorre toda a arvore com variaveis de controle para armazenar o total de linhas percorridas, quantos itens cada linha da arvore possui, e em qual
linha o RPA se encontra atualmente para que ele possa ir e voltar lendo todas as subclasses, classes, grupos e divisões.

Quando o RPA termina toda a extração da seção ele finaliza e vai para a etapa de ajuste de texto com python onde são feitos os ajustes necessários onde o script pytoh é carregado e são utilizados dois métodos, um para remover
os acentos e outro para manter somente os numeros.

Após isso na etapa seguinte todo o dado do datatable é armazenado em um arquivo .CSV

Em seguida o RPA retorna para a URL inicial para que possa ir para o próximo item.

Assim que finalizado todos os itens da fila o RPA seguirá para o estado End Process, fechará o chrome e irá gerar o arquivo excel com todos os dados do arquivo CSV.

No final da execução irão constar na pasta "\Busca_De_Dados_CNAE\Data\" dois arquivos com os dados extraidos, um será .CSV e outro .XLSX
 



