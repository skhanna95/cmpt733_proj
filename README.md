# MEASURING OBSERVABLE INFLUENCE AND IMPACT OF SCIENTIFIC RESEARCH BEYOND ACADEMIA

> TEAM: ABRACA-DATA (HONGHUI WANG, CHHAVI VERMA, SHRAY KHANNA)

## EDA

Firstly, we conducted EDA on `Genome BC publication export Feb 2019.xlsx`
which is offered by Gnome BC listing the academic papers they funded.

### Clean the Genome BC data

we opened the 'Genome BC publication export Feb 2019.xlsx' file, fixed some anomaly lines,
such as line 3088, manually and stored the file as `gbc.csv`

Then we split `gbc.csv` into `gbc_doi_issn_ibsn.csv`, `gbc_nopmid_nodoi.csv` and `gbc_pmid.csv`
based on whether the entity has PMID value or DOI value.

Then we divided `gbc_nopmid_nodoi.csv` into two files `gbcnn_hastitle.csv` and `gbcnn_notitle.csv`
based on whether the entity has title.

For the 170 entities that has no title, we explored manually and determined to
discard them as they have no useful information.
For those that have titles, we used offline dataset `PMC-ids.csv` and APIs
offered by NCBI to get its PMID.
For running this code, you should down load `PMC-ids.csv` using this [link](ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/PMC-ids.csv.gz).

For entities in `gbc_doi_issn_ibsn.csv`, we used offline database `PMC-ids.csv` and APIs
offered by NCBI to get its PMID.

In the end, we droped dupliates and generated `gbc_ff.csv` listing all the unique 





es that have PMID values from `Genome BC publication export Feb 2019.xlsx`.
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
This step will take around 12 hours.

## Parsing pdf files

### pdf to XML ...
...

### XML to `reference.csv`
open pdfparsing.
To process the pdfs and parsing the references:
make sure that `config.py` has the correct path for pdf2xml.exe. You can download it from here or from sourceforge.
run `extract_references.ipynb` 
change the `directory` to the directory of pdfs.
change the `dir_name` to start of parent folder till the folder where pdfs are. 
Example: if pdfs are in /home/user_name/xyz/abc/mno/pqr then 
change `directory` to `directory='/home/user_name/xyz/abc/mno/pqr'` and
`dir_name` to `dir_name='xyz/abc/mno/pqr/'`

##After updating these
run all the cells in order and make sure all python scripts are in the same directory as of notebook


From 4739 pdf files, we extract 5383 refernce lines.

### `reference.csv` to `pdf_title_pmid.csv`
Run `extractTitleThenGetPMID.ipynb` will extract the title from `reference.csv`
and query NBCI api to get the corresponding pmid. 

From 5383 reference lines, we extract 1246 titles using regular expression
combined with NCBI APIs.
We set the regular expression rule like this: every title is between two
periods, and the number of words in the title should greater than 4.
Then we verify this title by quering NCBI API.
If we can find a paper the title of whom has an edit distance less than 4 to
the title, then we can be sure that the title is indeed a valid paper title.
In the meantime, we get the corresponding PMID of this paper.


## Data cleaning and data integration

We put all the results in `data/5entrise_ppd`.
Goto `4_DataIntegration/5entrise_ppd`. 
Run `cadth/txt2pmids.csv.ipynb`, `cpic/txt2pmids.csv.ipynb` and
`pgkb/txt2pmids.csv.ipynb`. 
Run `combine_pmids.csv.ipynb`.
Run `pmids.csvTOpmids_titles.csv.ipynb`
Then we will get `pmids_titles.csv`

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
