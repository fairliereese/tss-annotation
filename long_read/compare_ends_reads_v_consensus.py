import pandas as pd
import argparse
import os
from matplotlib_venn import venn2
import seaborn as sns
import matplotlib.pyplot as plt

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-merged_ends', dest='merged_ends',
		help='merged ends from dataset')
	parser.add_argument('-read_ends', dest='read_ends',
		help='single bp read ends from dataset')
	parser.add_argument('-annot', dest='annot',
		help='read annotation file from which read_ends was derived')
	parser.add_argument('-type', dest='end_type',
		help='type of end. choose "TES" or "TSS"')
	parser.add_argument('-sample', dest='sample',
		help='sample name ie ONT GM12878')
	parser.add_argument('-o', dest='oprefix',
		help='output file prefix')
	args = parser.parse_args()
	return args

def main():
	args = get_args()
	merged = args.merged_ends
	reads = args.read_ends
	end_type = args.end_type
	annot = args.annot
	oprefix = args.oprefix
	sample = args.sample

	fname = '{}_{}_reads_v_merged.bed'.format(oprefix, end_type)
	bedtools_cmd = 'bedtools intersect -a {} -b {} -loj -s > {}'.format(reads, merged, fname)
	os.system(bedtools_cmd)
	int_df = pd.read_csv(fname, header=None, sep='\t',
		usecols=[6,7,8,11], names=['chrom_1', 'start_1', 'stop_1', 'strand_1'])
	print(int_df.head())
	print(len(int_df.index))

	# sort read df
	read_df = pd.read_csv(annot, sep='\t')
	read_df['name'] = '.'
	read_df['score'] = '.'
	if end_type == 'TSS':
		read_df = read_df[['chrom', 'read_start', 'read_start', 'gene_ID', 'transcript_ID',
			'strand']]
	elif end_type == 'TES':
		read_df = read_df[['chrom', 'read_end', 'read_end', 'gene_ID', 'transcript_ID',
			'strand']]
	read_df.to_csv('temp.bed', sep='\t', index=False, header=False)
	# beep = read_df.chrom.str.split('r', n=1, expand=True)
	# read_df['chrom_num'] = beep[1]
	# read_df.sort_values(by=['chrom_num', 'read_start'], inplace=True)
	# print(len(read_df.index))

	bedtools_cmd = 'bedtools sort -i temp.bed > temp_sorted.bed'
	os.system(bedtools_cmd)
	read_df = pd.read_csv('temp_sorted.bed', sep='\t', header=None,
		names=['chrom', 'read_start', 'read_end', 'gene_ID', 'transcript_ID', 'strand'])

	# concatenate the guys
	df = pd.concat([read_df, int_df], axis=1)
	
	# remove read ends that didn't merge with anything
	df = df.loc[df.start_1 != -1]
	df.to_csv('hello', index=False)


	# first, see how many unique ends there are for each transcript
	cols = ['gene_ID', 'transcript_ID', 'chrom_1', 'start_1', 'stop_1', 'strand_1']
	t_df = df.loc[~df[cols].duplicated()]
	t_df = t_df[['gene_ID', 'transcript_ID','strand']].groupby(['gene_ID', 'transcript_ID']).count()
	t_df.rename({'strand': 'counts'}, axis=1, inplace=True)
	t_df.reset_index(inplace=True)
	# t_df.to_csv('hello', index=False)

	ax = sns.distplot(t_df.counts, bins=t_df.counts.max(), kde=False)
	ax.set_xlim(0,25)
	plt.title('{} unique {}s per transcript isoform'.format(sample, end_type))
	plt.savefig('{}_unique_{}s_transcript.png'.format(oprefix, end_type))
	plt.clf()

	# now, for gene
	cols = ['gene_ID', 'transcript_ID', 'chrom_1', 'start_1', 'stop_1', 'strand_1']
	g_df = df.loc[~df[cols].duplicated()]
	g_df = g_df[['gene_ID', 'transcript_ID']].groupby(['gene_ID']).count()
	g_df.rename({'transcript_ID': 'counts'}, axis=1, inplace=True)
	g_df.reset_index(inplace=True)

	ax = sns.distplot(g_df.counts, bins=g_df.counts.max(), kde=False)
	ax.set_xlim(0,25)
	plt.title('{} unique {}s per gene'.format(sample, end_type))
	plt.savefig('{}_unique_{}s_gene.png'.format(oprefix, end_type))


if __name__ == '__main__': main()