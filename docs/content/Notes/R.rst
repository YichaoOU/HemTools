R for python people
==================


Summary
^^^^^^^

When I was just started my Ph.D, I was using Perl, then I moved to python and started to learn some R as well as other languages such as Matlab. Then I decided to use just one programming language (python) because it just feels too inconvenient to remember and use the same thing but in many different ways. And now, as job needed, I have to pick up some R.

Just like how I moved from Perl to Python, the key is to get familiar with the syntax for common logic and packages. In this post, I will gradually list them here:


A unique command in R is ``%>%``, which is similar to the pipe function in Linux ``|``.


R plots
^^^^^^^^

I'm not a good R user. Some of the following plots took me hours to figure out.

In this barplot, I have made clusters for WT and KO cells, I then want to make a barplot showing the "normalized value", basically cluster size divided by the corresponding WT or KO size. The key here is to use ``aes( y=..count../..Total_cell..)`` and a custom column in the ``aes`` mapping function.

::

  a=cell_data %>%
      group_by(orig.ident) %>%
      summarise(Total_cell = n()) 
  cell_data2 = merge(cell_data,a,by=c("orig.ident"))
  ggplot(cell_data2, aes(x = manual_label, fill = orig.ident,Total_cell=Total_cell)) +
      geom_bar(aes( y=..count../..Total_cell..),position=position_dodge2(reverse = TRUE),size=0.6,alpha=0.5,color="black") +
      scale_x_discrete(limits =new_level)+
  scale_fill_manual(values = c("#0073C2FF","#EFC000FF"))+theme(axis.text.x = element_text(angle = 45, vjust =1, hjust=1),
                                                               text = element_text(size=12))





simple command differences
^^^^^^^^^^^^^^^^^^^^^^^^^^

::

	length(x)		len(x)

	glue("xxx{asd}")		f"xxx{asd}"


logic flow differences
^^^^^^^^^^^^^^^^^^^^^

1. for loop R

::

	n=10
	s=c(1,2,3)
	for (i in 1:n){
		
		current_s = s[i]

	}





common package differences
^^^^^^^^^^^^^^^^^^^^


Ref:

https://shiring.github.io/r_vs_python/2017/01/22/R_vs_Py_post


data frame operation
^^^^^^^^^^^^^^


Replace a column value using values from another column
-------------------------------

https://stackoverflow.com/questions/40177132/replace-values-from-another-dataframe-by-ids

::

	library("dplyr")

	as1 <- data.frame(ID = c(1,2,3,4,5,6), pid = c(21,22,23,24,25,26),Values = c(435,33,45,NA, NA,12))
	as2 <- data.frame(ID = c(4,5),pid = c(24,25), Values = c(544, 676))

	left_join(as1, as2, by = c("ID", "pid")) %>% 
	    mutate(Values = ifelse(is.na(Values.x), Values.y, Values.x)) %>% 
	    select(ID, pid, Values)

For my data, the ``left_join`` command produced NA values in the new columns, I have to do this:

::

	label = read.csv("info.tsv",sep="\t",header=F,stringsAsFactors=F)


https://towardsdatascience.com/cheat-sheet-for-python-dataframe-r-dataframe-syntax-conversions-450f656b44ca

Python ↔R basics
# Python ⇔ R: object types
type(a)  ⇔ typeof(a)
# Python ⇔ R: variable assignment
a=5      ⇔ a<-5    # a=5 also works for R
# Python list ⇔ R vector:
a = [1,3,5,7]                ⇔  a <- c(1,3,5,7)
a = [i for i in range(3,9)]  ⇔  a <- c(3:9)
# Python 'for loop':
for val in [1,3,5]:
    print(val)
# R 'for loop':
for (val in c(1,3,5)){
    print(val)
}
# Python function:
def new_function(a, b=5):
    return a+b
# R function:
new_function <- function(a, b=5) {
    return (a+b)
}
Inspecting dataframe
# Python ⇔ R
df.head()       ⇔  head(df)
df.head(3)      ⇔  head(df,3)
df.tail(3)      ⇔  tail(df,3)
df.shape[0]     ⇔  nrow(df)
df.shape[1]     ⇔  ncol(df)
df.shape        ⇔  dim(df)
df.info()       ⇔  NO EQUIVALENT
df.describe()   ⇔  summary(df)     # similar, not exactly the same
NO EQUIVALENT   ⇔  str(df)
File I/O
# Python  
import pandas as pd
df = pd.read_csv("input.csv",
                 sep    = ",",
                 header = 0)
df.to_csv("output.csv", index = False)
# R 
df <- read.csv("input.csv", 
               header = TRUE,
               na.strings=c("","NA"),    
               sep = ",")
write.csv(df, "output.csv", row.names = FALSE)
# na.strings: make sure NAs are not read as empty strings
Create a new dataframe
# Python
import pandas as pd
df = pd.DataFrame(dict(col_a=['a','b','c'], col_b=[1,2,3]))
# R
col_a <- c('a','b','c')
col_b <- c(1,2,3)
df <- data.frame(col_a, col_b)
Column / row filtering
# Python: row filtering  
df[(df['column_1'] > 3) &    
   (df['column_2'].isnull())]
# R: row filtering  
df[(df$column_1 > 3) &    
   (is.na(df$column_2)), ] 
OR
library(dplyr)
df %>% filter((column_1 > 3) & (is.na(column_2)))
# Python ⇔ R: column filtering (keep columns) 
df[['c1', 'c2']] ⇔  df[c('c1', 'c2')]   # OR: df[,c('c1', 'c2')]
# Python ⇔ R(with dplyr): column filtering (drop columns)
df.drop(['c1', 'c2'], axis=1)  ⇔  df %>% select(-c('c1', 'c2'))
# Python ⇔ R: select columns by position
df.iloc[:,2:5]  ⇔  df[c(3:5)]           # Note the indexing
# Python: check if a column contains specific values
df[df['c1'].isin(['a','b'])]
OR
df.query('c1 in ("a", "b")')
# R: check if a column contains specific values
df[df$c1 %in% c('a', 'b'), ]
OR
library(dplyr)
df %>% filter(c1 %in% c('a', 'b'))
Missing value handling / count
# Python: missing value imputation 
df['c1'] = df['c1'].fillna(0)  
OR
df.fillna(value={'c1': 0})
# R: missing value imputation
df$c1[is.na(df$c1)] <- 0
OR 
df$c1 = ifelse(is.na(df$c1) == TRUE, 0, df$c1)
OR
library(dplyr)
library(tidyr)
df %>% mutate(c1 = replace_na(c1, 0))
# Python ⇔ R: number of missing values in a column
df['c1'].isnull().sum()  ⇔  sum(is.na(df$c1))
Statistics for a single column
# Python ⇔ R: count value frequency (Similar)
df['c1'].value_counts()              ⇔ table(df$c1)
df['c1'].value_counts(dropna=False)  ⇔ table(df$c1, useNA='always')
df['c1'].value_counts(ascending=False) 
⇔ sort(table(df$c1), decreasing = TRUE)
# Python ⇔ R: unique columns (including missing values) 
df['c1'].unique()      ⇔  unique(df$c1)
len(df['c1'].unique()) ⇔  length(unique(df$c1))
# Python ⇔ R: column max / min / mean
df['c1'].max()         ⇔  max(df$c1,  na.rm = TRUE)
df['c1'].min()         ⇔  min(df$c1,  na.rm = TRUE)
df['c1'].mean()        ⇔  mean(df$c1, na.rm = TRUE)
grouping and aggregations
# Python: max / min / sum / mean / count
tbl = df.groupby('c1').agg({'c2':['max', 'min', 'sum'],
                            'c3':['mean'],
                            'c1':['count']}).reset_index()
tbl.columns = ['c1', 'c2_max', 'c2_min', 'c2_sum', 
               'c3_mean', 'count']
OR (for chained operations)
tbl = df.groupby('c1').agg(c2_max=  ('c2', max),
                           c2_min=  ('c2', min),
                           c2_sum=  ('c2', sum),
                           c3_mean= ('c2', 'mean'),
                           count=   ('c1', 'count')).reset_index()
# R: max / min / sum / mean / count
library(dplyr)
df %>% group_by(c1) %>% 
       summarise(c2_max  = max(c2, na.rm = T),
                 c2_min  = min(c2, na.rm = T),
                 c2_sum  = sum(c2, na.rm = T),
                 c3_mean = mean(c3, na.rm = T),
                 count   = n())       
# Python: count distinct
df.groupby('c1')['c2'].nunique()\
                      .reset_index()\
                      .rename(columns={'c2':'c2_cnt_distinct'})
# R: count distinct
library(dplyr)
tbl <- df %>% group_by(c1) 
          %>% summarise(c2_cnt_distinct = n_distinct(c2))
creating new columns / altering existing columns
# Python: rename columns
df.rename(columns={'old_col': 'new_col'})         
# R: rename columns
library(dplyr)
df %>% rename(new_col = old_col)
# Python: value mapping
df['Sex'] = df['Sex'].map({'male':0, 'female':1})
# R: value mapping
library(dplyr)
df$Sex <- mapvalues(df$Sex, 
          from=c('male', 'female'), 
          to=c(0,1))
# Python ⇔ R: change data type
df['c1'] = df['c1'].astype(str)    ⇔  df$c1 <- as.character(df$c1)
df['c1'] = df['c1'].astype(int)    ⇔  df$c1 <- as.integer(df$c1)
df['c1'] = df['c1'].astype(float)  ⇔  df$c1 <- as.numeric(df$c1)
Updating column values by row filters
# Python ⇔ R: 
df.loc[df['c1']=='A', 'c2'] = 99  ⇔  df[df$c1=='A', 'c2'] <- 99
Joining / sorting
# Python: inner join / left join
import pandas as pd
merged_df1 = pd.merge(df1, df2, on='c1', how='inner')
merged_df2 = pd.merge(df1, df2, on='c1', how='left')
OR (for chained operations)
merged_df1 = df1.merge(df2, on='c1', how='inner')
merged_df2 = df1.merge(df2, on='c1', how='left')
# R: inner join / left join
merged_df1 <- merge(x=df1,y=df2,by='c1')
merged_df2 <- merge(x=df1,y=df2,by='c1',all.x=TRUE)
OR 
library(dplyr)
merged_df1 <- inner_join(x=df1,y=df2,by='c1')
merged_df2 <- left_join(x=df1,y=df2,by='c1')
# Python: sorting
df.sort_values(by=['c1','c2'], ascending = [True, False])
# R: sorting 
library(dplyr)
df %>% arrange(c1, desc(c2))
Concatenation / sampling
# Python (import pandas as pd) ⇔ R: concatenation
pd.concat([df1, df2, df3])     ⇔ rbind(df1, df2, df3)
pd.concat([df1, df2], axis=1)  ⇔ cbind(df1, df2)
# Python random sample
df.sample(n=3, random_state=42)
# R random sample
set.seed(42)
sample_n(df, 3)
An example of chained operations
# Python: chained operations with '.'
df.drop('c1', axis=1)\
  .sort_values(by='c2', ascending=False)\
  .assign(c3 = lambda x: x['c1']*3 + 2)\
  .fillna(value={'c2': 0, 'c4':-99})\
  .rename(columns={'total': 'TOT'})\
  .query('c3 > 10')
# R: chained operations with '%>%'
library(dplyr)
library(tidyr)
df %>% select(-c('c1')) %>%
       arrange(desc(c2)) %>%
       mutate(c3 = c1*3 + 2) %>%
       mutate(c2 = replace_na(c2, 0),
              c4 = replace_na(c4, -99)) %>%
       rename(TOT = total) %>%            
       filter(c3 > 10)