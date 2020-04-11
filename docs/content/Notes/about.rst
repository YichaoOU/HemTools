Thoughts on HemTools
===================



Packaging
^^^^^^^^^

HemTools is specifically designed for St. Jude HPC and LSF system. To make it universal, we can try nextflow and add ``--interactive`` option. 

When I started hemtools, I tried nextflow and I'm not satisfied with the way it handles dependecies. So I started to write my own syntax, in a bash-like way.


Resources
^^^^^^^^^

loading hg19 bwa index needs about 5G 

