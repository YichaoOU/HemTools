import pandas as pd
import sys
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

filename = sys.argv[1]

df = pd.read_csv(str(filename), delimiter='\t')
df.drop(labels=['AllSubs','Frequency','gCoverage-q30','gMeanQ','gBaseCount[A,C,G,T]','gAllSubs','gFrequency'], axis=1, inplace=True)

#break up BaseCount[A,C,G,T] into individual columns
df['Reads_A'] = df.apply(lambda row: int(row['BaseCount[A,C,G,T]'].split(',')[0][1:]), axis=1)
df['Reads_C'] = df.apply(lambda row: int(row['BaseCount[A,C,G,T]'].split(',')[1][1:]), axis=1)
df['Reads_G'] = df.apply(lambda row: int(row['BaseCount[A,C,G,T]'].split(',')[2][1:]), axis=1)
df['Reads_T'] = df.apply(lambda row: int(row['BaseCount[A,C,G,T]'].split(',')[3][1:-1]), axis=1)

df.drop(labels='BaseCount[A,C,G,T]', axis=1, inplace=True)
#filter for coverage >= 10
df = df[df['Coverage-q30'] >= 10]
df.to_csv(str(filename)[:-4] + '_mod.csv')

#filter by plus or minus strands
df_plus = df[df['Strand'] == 1]
df_plus = df_plus[df_plus.Reference == 'A']

df_minus = df[df['Strand'] == 0]
df_minus = df_minus[df_minus.Reference == 'T']

plus_Reads_A = df_plus['Reads_A'].tolist()
plus_Reads_T = df_plus['Reads_T'].tolist()
plus_Reads_G = df_plus['Reads_G'].tolist()
plus_Reads_C = df_plus['Reads_C'].tolist()

minus_Reads_A = df_minus['Reads_A'].tolist()
minus_Reads_T = df_minus['Reads_T'].tolist()
minus_Reads_G = df_minus['Reads_G'].tolist()
minus_Reads_C = df_minus['Reads_C'].tolist()

with open(filename + '.out.txt', 'w') as f:
	f.write('Total plus-strand A reads = ' + str(sum(plus_Reads_A) + sum(plus_Reads_T) + sum(plus_Reads_G) + sum(plus_Reads_C)) + '\n')
	f.write('plus strand A-to-I reads = ' + str(sum(plus_Reads_G)) + '\n')
	f.write('Total minus-strand A reads = ' + str(sum(minus_Reads_A) + sum(minus_Reads_T) + sum(minus_Reads_G) + sum(minus_Reads_C)) + '\n')
	f.write('minus strand A-to-I reads = ' + str(sum(minus_Reads_C)))