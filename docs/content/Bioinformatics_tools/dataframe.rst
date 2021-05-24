


I was having trouble with the not (~) symbol as well, so here's another way from another StackOverflow thread:

df[df["col"].str.contains('this|that')==False]
shareimprove this answer
edited Oct 16 '18 at 7:07

Shaido
14.1k123045
answered Dec 15 '16 at 21:10

nanselm2
603510
Can it be combined like this? df[df["col1"].str.contains('this'|'that')==False and df["col2"].str.contains('foo'|'bar')==True]? Thanks! – tommy.carstensen May 24 '17 at 10:54
Yes, you can. The syntax is explained here: stackoverflow.com/questions/22086116/… – tommy.carstensen May 24 '17 at 11:26

https://stackoverflow.com/questions/17097643/search-for-does-not-contain-on-a-dataframe-in-pandas
