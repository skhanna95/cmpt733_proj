# MEASURING OBSERVABLE INFLUENCE AND IMPACT OF SCIENTIFIC RESEARCH BEYOND ACADEMIA

> TEAM: ABRACA-DATA (HONGHUI WANG, CHHAVI VERMA, SHRAY KHANNA)

## EDA

Firstly, we conducted EDA on `Genome BC publication export Feb 2019.xlsx` which is offered by Gnome BC listing the academic papers they funded.

### Clean the Gnome BC data

we opened the 'Genome BC publication export Feb 2019.xlsx' file, fixed some anomaly lines,
such as line 3088, manully and stored the file as `gbc.csv`

Then we split `gbc.csv` into `gbc_doi_issn_ibsn.csv`, `gbc_nopmid_nodoi.csv` and `gbc_pmid.csv`
based on whether the entity has PMID value or DOI value.

Then we divided `gbc_nopmid_nodoi.csv` into two files `gbcnn_hastitle.csv` and `gbcnn_notitle.csv`
based on whether the entity has title.

For the 170 entitise that has no title, we explored manully and determined to
discard them as they has no useful information.
For those that have titles, we used offline dataset `PMC-ids.csv` and APIs
offered by NCBI to get its PMID.
For running this code, you should down load `PMC-ids.csv` using this [link](ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/PMC-ids.csv.gz).

For entitise in `gbc_doi_issn_ibsn.csv`, we used offline database `PMC-ids.csv` and APIs
offered by NCBI to get its PMID.

In the end, we droped dupliates and generated `gbc_ff.csv` listing all the unique entitise that have PMID values from `Genome BC publication export Feb 2019.xlsx`.
We get 2703 meaningful entities out of 3216 entities.

All the steps can be done by running `code/1GenomeBC_EDA/EDA.ipynb`

## scrape the downstream documentations

The five downstream documentations entries are: 

* BC Cancer clinical guidelines [website](http://www.bccancer.bc.ca/health-professionals) (Clinical Resources, Clinical Trials and Studies)

* BC Ministry of Health [Guidelines](https://www2.gov.bc.ca/gov/content/health/practitioner-professional-resources/bc-guidelines) 

* CADTH pan-Canadian Oncology Drug [Review](https://www.cadth.ca/pcodr)

* CPIC [Guidelines](https://cpicpgx.org/guidelines/)

* [PharmGKB](https://www.pharmgkb.org/)

We denotes them as bcc, bcm, cadth, cpic and pgkb.

### For bcm

It has a zip file that contains all the information the website
hosts. 
So we get all the pdf files by downloaded the [zip file](https://www2.gov.bc.ca/assets/download/1DEC4FCF66B04F218AB2F4BEF1E3BD71) and unziped it manully.

### For bcc, cadth and cpic
We uses scrappy to scrapy all the pdf files and extract
all the DOI, PMCID and PMID references.

Goto `2_scrapy` then go to `bbc`, `cadth` and `cpic` folder respectively, run command `scrapy crawl downloadPDFs` in terminal.

### For pgkb
pgkb is an js generated dynamic website, so we used scrappy and selenium to
scrapy the pdf files and extract all the DOI, PMCID and PMID references.
Goto `2_scrapy` then go to `pgkd`, run command `scrapy crawl downloadPDFs` in terminal.

## Parsing pdf files

...

pdf -> `titles_authors.csv`

`titles_authors.csv` -> `title_pmids.csv`

...

## Data cleaning and data integration

Put all the results in `data/5entrise_ppd`.
Goto `4_DataIntegration/5entrise_ppd`. 
Run `cadth/txt2pmids.csv.ipynb`, `cpic/txt2pmids.csv.ipynb` and
`pgkb/txt2pmids.csv.ipynb`. 
Run `combine_pmids.csv.ipynb`.
Run `pmids.csvTOpmids_titles.csv.ipynb`
Then we will get `pmids_titles.csv`

...
Then concatenate `title_pmids.csv` obtained from paring pdf files to
`pmids_titles.csv`.
...

## Data Analysis and Visulization

Run `gbc_relation_map.ipynb` to analysis the relationship between Genome BC funded papers,
and visulize the relationship.

Run `get_refer_graph.py` to get the downstream documentation refercen map with
`maxdepth=depth_constraint+1=4`.
This step will generate `depth3_nodes_visitedConstrain`.
This step will take about half an hour.

Then edit `get_refer_graph_break_and_continue.py`,
change `pre_depth_constrain` to 3, and change `depth_constraint` to 4. 
Run command `python get_reger_graph_break_and_continue.py` in terminal.
This step will generate `depth4_nodes_visitedConstrain`.
This step will take about 6 hours.


Then edit `get_refer_graph_break_and_continue.py`,
change `pre_depth_constrain` to 4, and change `depth_constraint` to 5. 
Run command `python get_reger_graph_break_and_continue.py` in terminal.
This step will generate `depth5_nodes_visitedConstrain`.
This step will take about 19 hours.

Run `get_entity_sixGroup.ipynb`.
This step will generate `depth5_nodes_visitedConstrain_entity_sixGroup`

Run command `python prepare_data_for_topx_visulization.py` in terminal.

Run command `python prepare_data_for_topxpapers_barchart.py` in terminal.

Run `Report.ipynb` to get the visulization result.
