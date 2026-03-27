Literature Search and paper download
====================

::

    usage: ncbi_paper_download.py [-h] --query QUERY [--author AUTHOR] [--api_key API_KEY] [--max_results MAX_RESULTS] [--outdir OUTDIR] [--email EMAIL]
                                  [--sort {relevance,pub_date}] [--no_pdf] [--pubmed_only]

    Retrieve papers from PubMed/PMC and download open-access PDFs.

    optional arguments:
      -h, --help            show this help message and exit
      --query QUERY         Search query (e.g. 'crispr deep learning')
      --author AUTHOR       Author name filter (e.g. 'Yichao Li')
      --api_key API_KEY     NCBI API key
      --max_results MAX_RESULTS
                            Max papers to retrieve (default: 100)
      --outdir OUTDIR       Output directory (default: ncbi_results)
      --email EMAIL         Your email (recommended by NCBI)
      --sort {relevance,pub_date}
                            Sort order: relevance or pub_date (default: relevance)
      --no_pdf              Skip PDF download
      --pubmed_only         Search PubMed only (skip OpenAlex)



Summary
-------

This is intented to be used by the literature review skill in HemAgent, but the code can also be usefully as a standalone.


Usage
-----

Basic topic search with PDF download::

    ncbi_paper_download.py --query "crispr deep learning" --max_results 20

Search by author and topic::

    ncbi_paper_download.py --author "Yichao Li" --query "bioinformatics" --max_results 50

Metadata only (no PDF download)::

    ncbi_paper_download.py --query "single-cell RNA-seq" --no_pdf

PubMed only (skip OpenAlex)::

    ncbi_paper_download.py --query "epigenetics" --pubmed_only --max_results 30

Outputs
-------

All output files are written to the directory specified by ``--outdir`` (default: ``ncbi_results/``).

``papers_metadata.csv``
    CSV file containing metadata for all papers found. Columns:

    - **PMID** -- PubMed identifier (empty for OpenAlex-only papers).
    - **Title** -- Paper title.
    - **Authors** -- Semicolon-separated author list.
    - **Journal** -- Journal name.
    - **Year** -- Publication year.
    - **Abstract** -- Paper abstract (PubMed papers only).
    - **DOI** -- Digital Object Identifier.
    - **PMCID** -- PubMed Central identifier (if available).
    - **PDF_Status** -- Download result (e.g., ``downloaded_PMC-tgz``, ``downloaded_unpaywall``, ``downloaded_publisher``, ``not_open_access``).
    - **PDF_Filename** -- Name of the downloaded PDF file.
    - **Source** -- Which database found this paper (``pubmed`` or ``openalex``).

``download_summary.txt``
    Plain-text summary of download results including per-paper status.

``pdfs/``
    Directory containing downloaded PDF files. Files are named as::

        FirstAuthor_ShortTitle_Year.pdf

    For example::

        Li_AcrNET_predicting_antiCRISPR_with_deep_learning_2023.pdf
        Zhang_Benchmarking_deep_learning_methods_for_predicting_2023.pdf

Output directory structure::

    ncbi_results/
    ├── papers_metadata.csv
    ├── download_summary.txt
    └── pdfs/
        ├── Li_AcrNET_predicting_antiCRISPR_with_deep_learning_2023.pdf
        ├── Zhang_Benchmarking_deep_learning_methods_for_predicting_2023.pdf
        └── ...
