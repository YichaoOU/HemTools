Motif notes
===========



FIMO
^^^^


5-mer exact match p-value cutoff: 0.001
10-mer allows two mismatches: 1e-4 (default cutoff)

+--------+------------------------+
| AGATAA | 0.000352               |
+--------+------------------------+
| AGATAG | 0.00028900000000000003 |
+--------+------------------------+
| CCAAT  | 0.00105                |
+--------+------------------------+
| TGACCA | 0.00023700000000000001 |
+--------+------------------------+
| TGATAA | 0.000352               |
+--------+------------------------+
| TGATAG | 0.00028900000000000003 |
+--------+------------------------+

p_value
------

https://groups.google.com/forum/#!topic/meme-suite/xD2Z3EUw2BQ

the default 1e-4 p-value is not likely to report any matches for motif length=5,6

Motif mapping bed file is generated using FIMO. For motif length <= 7, p-value cutoff is 1e-3. For motif length >=8, default cutoff 1e-4 is used.


+--------------+----------------+
| motif length | p_value cutoff |
+--------------+----------------+
| 5-7          | 1e-3           |
+--------------+----------------+
| 8+           | 1e-4 (default) |
+--------------+----------------+


bedtools
^^^^^^^^

http://quinlanlab.org/tutorials/bedtools/bedtools.html#intersecting-multiple-files-at-once.


