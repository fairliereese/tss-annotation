import pandas as pd
import argparse
import os


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-annot', dest='annot',
		help='talon read_annot file')
	parser.add_argument('-datasets', dest='datasets',
		help='comma separated list of datasets to include',
		default='all')
	# parser.add_argument('-chrom_sizes', dest='chrom_sizes',
	# 	help='chromosome sizes for each chromosome in the reference')
	# parser.add_argument('-tss_dist', dest='tss_dist',
	# 	help='range away from the read start to extend the tss')
	# parser.add_argument('-tes_dist', dest='tes_dist')
	# parser.add_argument('-filter_type', dest='ftype',
	# 	help="'known' or 'talon'")
	# parser.add_argument('-min_tpm', dest='min_tpm',
	# 	help="minimum tpm to call tss/tes")
	parser.add_argument('-o', dest='oprefix',
		help='prefix to save output files')
	args = parser.parse_args()
	return args

def main():
	args = get_args()
	oprefix = args.oprefix
	annot_file = args.annot
	datasets = args.datasets
	if datasets != 'all':
		datasets = datasets.split(',')
	
	# chrom_sizes = args.chrom_sizes
	# chr_sizes = pd.read_csv(chrom_sizes, sep='\t', header=None,
	# 	names=['chrom', 'chrom_length'])

	df = pd.read_csv(annot_file, sep='\t')

	# remove sirvs and erccs and EBV
	df = df.loc[~df.chrom.str.contains('SIRV')]
	df = df.loc[~df.chrom.str.contains('ERCC')]
	df = df.loc[~df.chrom.str.contains('EBV')]
	df = df.loc[~df.chrom.str.contains('chrM')]

	# filter out datasets we don't want
	if datasets != 'all':
		df = df.loc[df.dataset.isin(datasets)]

	# # merge the remaining entries with chrom sizes
	# df = df.merge(chr_sizes, how='left', on='chrom')
	# df['start_valid'] = df.read_start <= df.chrom_length
	# df['end_valid'] = df.read_end <= df.chrom_length

	# tss bed
	tss = df[['chrom', 'read_start', 'strand', 'read_name']].groupby(['chrom', 'read_start', 'strand']).count()
	tss.reset_index(inplace=True)
	tss.rename({'read_name':'counts'}, axis=1, inplace=True)
	tss['read_start'] = tss.read_start - 1 # decrement to fit bigwig 0-based indexing convention
	tss['read_start_2'] = tss.read_start 
	tss['name'] = '.'
	tss = tss[['chrom', 'read_start', 'read_start_2', 'name', 'counts', 'strand']]
	fname = '{}_tss.bed'.format(oprefix)
	tss.to_csv(fname, sep='\t', header=None, index=False)

	# and bedgraph, make one for the fwd and one for the rev strand
	fwd = tss.loc[tss.strand == '+', ['chrom', 'read_start', 'read_start_2', 'counts']]
	rev = tss.loc[tss.strand == '-', ['chrom', 'read_start', 'read_start_2', 'counts']]
	fwd.sort_values(by=['chrom', 'read_start'], inplace=True)
	rev.sort_values(by=['chrom', 'read_start'], inplace=True)
	fname = '{}_fwd_tss.bedgraph'.format(oprefix)
	fwd.to_csv(fname, sep='\t', header=None, index=False)
	fname = '{}_rev_tss.bedgraph'.format(oprefix)
	rev.to_csv(fname, sep='\t', header=None, index=False)

	# tes bed
	tes = df[['chrom', 'read_end', 'strand', 'read_name']].groupby(['chrom', 'read_end', 'strand']).count()
	tes.reset_index(inplace=True)
	tes.rename({'read_name':'counts'}, axis=1, inplace=True)
	tes['read_end'] = tes.read_end - 1 # decrement to fit bigwig 0-based indexing convention
	tes['read_end_2'] = tes.read_end 
	tes['name'] = '.'
	tes = tes[['chrom', 'read_end', 'read_end_2', 'name', 'counts', 'strand']]
	fname = '{}_tes.bed'.format(oprefix)
	tes.to_csv(fname, sep='\t', header=None, index=False)

	# and bedgraph, make one for the fwd and one for the rev strand
	fwd = tes.loc[tes.strand == '+', ['chrom', 'read_end', 'read_end_2', 'counts']]
	rev = tes.loc[tes.strand == '-', ['chrom', 'read_end', 'read_end_2', 'counts']]
	fwd.sort_values(by=['chrom', 'read_end'], inplace=True)
	rev.sort_values(by=['chrom', 'read_end'], inplace=True)
	fname = '{}_fwd_tes.bedgraph'.format(oprefix)
	fwd.to_csv(fname, sep='\t', header=None, index=False)
	fname = '{}_rev_tes.bedgraph'.format(oprefix)
	rev.to_csv(fname, sep='\t', header=None, index=False)

if __name__ == '__main__': main()