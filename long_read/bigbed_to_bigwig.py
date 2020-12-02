import pyBigWig
import pandas as pd

chrom_sizes = '/Users/fairliereese/Documents/programming/mortazavi_lab/ref/hg38/hg38.chrom.sizes'
bigbed = 'data/pb_gm12878_tss_sorted.bedgraph'

ifile = open(chrom_sizes, 'r')
chr_lens = []
for line in ifile:
    line = line.strip().split('\t')
    chrom = line[0]
    length = int(line[1])
    chr_lens.append((chrom, length))
ifile.close()

df = pd.read_csv(bigbed, sep='\t',
	header=None, names=['chrom', 'start', 'stop', 'score'])

# separate bigwigs for + and - strands
fwd =

bw = pyBigWig.open("data/test.bw", "w")

# add the bigwig headers
bw.addHeader(chr_lens)

df = pd.read_csv(bigbed, sep='\t',
	header=None, names=['chrom', 'start', 'stop', 'score'])

# df = df.loc[df.chrom == 'chr1']

# df = df.head(100)

df = df.loc[df.chrom == 'chr22']

# df['stop'] = df['start']+20

# df['start'] = df.start.astype('float')
# df['stop'] = df.stop.astype('float')
# df['score'] = df.score.astype('float')

chrs = df.chrom.tolist()
starts = df.start.tolist()
stops = df.stop.tolist()
scores = df.score.tolist()

# print(df.dtypes)
# print(chrs[:10])
# print(starts[:10])
# print(stops[:10])
# print(scores[:10])
# print(type(chrs[0]))
# print(type(starts[0]))
# print(type(stops[0]))
# print(type(scores[0]))

# bw.addEntries(df.chrom.values, df.start.values, \
# 	ends=df.stop.values, values=df.score.values)
bw.addEntries(chrs, starts, ends=stops, values=scores)


bw.close()