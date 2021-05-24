How to download all files from a website
========================================

Use httrack


Example: download all gRNA libraries from addgene

.. code:: bash

	"c:\Program Files\WinHTTrack\httrack.exe" https://www.addgene.org/pooled-library/ +*.txt +*.pdf +*.xlsx +*.xls +*.zip +*.png +*.docs +*.doc .


