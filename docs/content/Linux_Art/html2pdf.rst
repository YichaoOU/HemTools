Convert html file to PDF or PNG
=========================================================


Summary
^^^^^^^

There is no perfect solution. I compared pandoc vs weasyprint. I found pandoc is better.

Usage
^^^^^


.. code:: bash

    module load conda3

    module load texlive/20190410

    source activate /home/yli11/.conda/envs/pandoc

    pandoc my.html -t latex -o test.pdf

    


