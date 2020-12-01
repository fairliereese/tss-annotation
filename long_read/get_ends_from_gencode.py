import pandas as pd

df = pd.read_csv('/Users/fairliereese/mortazavi_lab/ref/gencode.v29/gencode.v29.annotation.gtf', 
	sep='\t', usecols=[0, 2,3,4,6], comment='#',
	names=['chrom', 'feature_type', 'start', 'stop', 'strand'])
df = df.loc[df.feature_type == 'transcript']

rev_starts = df.loc[df.strand == '-', 'stop']
rev_stops = df.loc[df.strand == '-', 'start']

df.loc[df.strand == '-', 'stop'] = rev_stops
df.loc[df.strand == '-', 'start'] = rev_starts

df['name'] = '.'
df['score'] = '.'

tss_df = df[['chrom', 'start', 'start', 'name', 'score', 'strand']].copy(deep=True)
tes_df = df[['chrom', 'stop', 'stop', 'name', 'score', 'strand']].copy(deep=True)

tss_fname = '/Users/fairliereese/mortazavi_lab/ref/gencode.v29/gencode.v29.tss.bed'
tss_df.to_csv(tss_fname, index=False, header=False, sep='\t')
tes_fname = '/Users/fairliereese/mortazavi_lab/ref/gencode.v29/gencode.v29.tes.bed'
tes_df.to_csv(tes_fname, index=False, header=False, sep='\t')



