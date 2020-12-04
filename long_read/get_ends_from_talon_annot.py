import pandas as pd
import pybedtools
import argparse
import os


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-annot', dest='annot',
		help='talon read_annot file')
	parser.add_argument('-datasets', dest='datasets',
		help='comma separated list of datasets to include',
		default='all')
	parser.add_argument('-filter_type', dest='ftype',
		help="'known' or 'talon'")
	parser.add_argument('-min_tpm', dest='min_tpm',
		help="minimum tpm to call tss/tes")
	parser.add_argument('-o', dest='oprefix',
		help='prefix to save output files')
	parser.add_argument('-index', dest='index_type',
		help='What number to start at, 0 or 1', 
		default='1')
	args = parser.parse_args()
	return args

def main():
	args = get_args()
	fname = args.annot
	datasets = args.datasets
	ftype = args.ftype
	oprefix = args.oprefix
	min_tpm = float(args.min_tpm)
	index_type = int(args.index_type)

	if datasets != 'all':
		datasets = datasets.split(',')

	df = pd.read_csv(fname, sep='\t')
	cols = ['dataset', 'chrom', 'read_start', 'read_end', 'strand', 'gene_ID',
		'transcript_ID', 'gene_novelty', 'transcript_novelty','ISM_subtype']
	df = df[cols]

	# choose from input datasets
	if datasets != 'all':
		df = df.loc[df.dataset.isin(datasets)]

	# remove spike-ins
	df = df.loc[~df.chrom.str.contains('ERCC')]
	df = df.loc[~df.chrom.str.contains('SIRV')]

	# remove novel genes
	df = df.loc[df.gene_novelty == 'Known']

	# if we're 0-indexing, decrement everything first
	if index_type == 0:
		df.read_start = df.read_start - 1
		df.read_end = df.read_end -1


	# filter transcript models by novelty
	if ftype == 'known':
		nov = ['Known']
	elif ftype == 'talon':
		tss_df = df.loc[(df.transcript_novelty!='ISM')|(df.ISM_subtype=='Prefix')].copy(deep=True)
		tes_df = df.loc[(df.transcript_novelty!='ISM')|(df.ISM_subtype=='Suffix')].copy(deep=True)
		nov = ['Known', 'NNC', 'NIC', 'ISM']
	tss_df = tss_df.loc[tss_df.transcript_novelty.isin(nov)]
	tes_df = tes_df.loc[tes_df.transcript_novelty.isin(nov)]

	fname = oprefix+'_read_annot_TSS.tsv'
	tss_df.to_csv(fname, sep='\t', index=False)

	fname = oprefix+'_read_annot_TES.tsv'
	tes_df.to_csv(fname, sep='\t', index=False)

	print('Generating read_annot bed files...')
	# starts
	tss_file = oprefix+'_TSS.bed'
	tss_df = tss_df[['chrom', 'read_start', 'strand']]
	tss_df['read_start_2'] = tss_df['read_start']
	tss_df['name'] = '.'
	tss_df['score'] = '.'
	tss_df = tss_df[['chrom', 'read_start', 'read_start_2', 'name', 'score', 'strand']]
	tss_df.to_csv(tss_file, sep='\t', index=False, header=False)

	# ends
	tes_file = oprefix+'_TES.bed'
	tes_df = tes_df[['chrom', 'read_end', 'strand']]
	tes_df['read_end_2'] = tes_df['read_end']
	tes_df['name'] = '.'
	tes_df['score'] = '.'
	tes_df = tes_df[['chrom', 'read_end', 'read_end_2', 'name', 'score', 'strand']]
	tes_df.to_csv(tes_file, sep='\t', index=False, header=False)

	print('Sorting and merging bed files...')

	# bedtools merge both sets of files
	tss_sorted_file = '{}_TSS_sorted.bed'.format(oprefix)
	b = 'bedtools sort -i {} > {}'.format(tss_file, tss_sorted_file)
	os.system(b)
	tss_sorted_merged_file = '{}_TSS_merged.bed'.format(oprefix)
	b = 'bedtools merge -i {} -s -d 50 -c 4,5,6 -o distinct,count,distinct > {}'.format(tss_sorted_file, tss_sorted_merged_file)
	os.system(b)

	tes_sorted_file = '{}_TES_sorted.bed'.format(oprefix)
	b = 'bedtools sort -i {} > {}'.format(tes_file, tes_sorted_file)
	os.system(b)
	tes_sorted_merged_file = '{}_TES_merged.bed'.format(oprefix)
	b = 'bedtools merge -i {} -s -d 50 -c 4,5,6 -o distinct,count,distinct > {}'.format(tes_sorted_file, tes_sorted_merged_file)
	os.system(b)

	print('Filtering for ends above {} TPM'.format(min_tpm))

	# TPM filter
	tss_df = pd.read_csv(tss_sorted_merged_file, sep='\t', header=None,
		names=['chrom', 'start', 'stop', 'name', 'counts', 'strand'])
	total_count = tss_df.counts.sum()
	tss_df['tpm'] = (tss_df.counts*1000000)/total_count

	tes_df = pd.read_csv(tes_sorted_merged_file, sep='\t', header=None,
		names=['chrom', 'start', 'stop', 'name', 'counts', 'strand'])
	total_count = tes_df.counts.sum()
	tes_df['tpm'] = (tes_df.counts*1000000)/total_count

	tss_df = tss_df.loc[tss_df.tpm >= min_tpm]
	tes_df = tes_df.loc[tes_df.tpm >= min_tpm]

	tss_df = tss_df[['chrom','start','stop','name','tpm','strand']]
	tes_df = tes_df[['chrom','start','stop','name','tpm','strand']]

	tss_filt = '{}_TSS_{}_tpm_filt.bed'.format(oprefix, min_tpm)
	tes_filt = '{}_TES_{}_tpm_filt.bed'.format(oprefix, min_tpm)

	print('{} TSSs'.format(len(tss_df.index)))
	print('{} TESs'.format(len(tes_df.index)))
	tss_df.to_csv(tss_filt, sep='\t', index=False, header=False)
	tes_df.to_csv(tes_filt, sep='\t', index=False, header=False)

if __name__ == '__main__': main()
