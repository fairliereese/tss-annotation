import pandas as pd
import argparse
import os
from matplotlib_venn import venn2
import matplotlib.pyplot as plt

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-bed_1', dest='bed_1',
		help='bedfile of 1st set of merged ends')
	parser.add_argument('-bed_1_type', dest='bed_1_type',
		help='datatype of bedfile 1')
	parser.add_argument('-bed_2', dest='bed_2',
		help='bedfile of 2nd set of merged ends')
	parser.add_argument('-bed_2_type', dest='bed_2_type',
		help='datatype of bedfile 2')
	parser.add_argument('-type', dest='end_type',
		help='type of end. choose "TES" or "TSS"')
	parser.add_argument('-celltype', dest='celltype',
		help='cell type')
	parser.add_argument('-o', dest='oprefix',
		help='output file prefix')
	args = parser.parse_args()
	return args

def format_subprocess_cmd(string):
	return string.split(' ')

def main():
	args = get_args()
	end_type = args.end_type
	bed_1 = args.bed_1
	bed_1_type = args.bed_1_type
	bed_2 = args.bed_2
	bed_2_type = args.bed_2_type
	celltype = args.celltype
	oprefix = args.oprefix

	df = pd.read_csv(bed_1, sep='\t', header=None, usecols=[0,1,2,5],
		names=['chrom','start','stop','strand'])
	bed_1_counts = len(df.index)
	print('{} total {}s'.format(bed_1_counts, bed_1_type))

	df = pd.read_csv(bed_2, sep='\t', header=None, usecols=[0,1,2,5],
		names=['chrom','start','stop','strand'])
	bed_2_counts = len(df.index)
	print('{} total {}s'.format(bed_2_counts, bed_2_type))

	fname = '{}_{}.bed'.format(oprefix, end_type)
	bedtools_cmd = 'bedtools intersect -a {} -b {} -s -u > {}'.format(bed_1, bed_2, fname)
	os.system(bedtools_cmd)

	# read in the resultant file
	df = pd.read_csv(fname, sep='\t', header=None, usecols=[0,1,2,5],
		names=['chr', 'start', 'stop', 'strand'])
	both_counts = len(df.index)
	print('{} overlapping {}s with {} to {}'.format(both_counts, end_type, bed_1_type, bed_2_type))

	# generate venn diagram of 1-->2
	counts_1 = bed_1_counts - both_counts
	counts_2 = bed_2_counts - both_counts 
	counts = (counts_1, counts_2, both_counts)

	plt.figure(figsize=(8.5,8.5))
	v = venn2(subsets=counts, set_labels=('A', 'B'))
	plt.title('Shared {} TSSs: {} to {}'.format(celltype, bed_1_type, bed_2_type), 
			  fontsize='xx-large')

	# messing with label text
	v.get_label_by_id('A').set_text(bed_1_type)
	v.get_label_by_id('B').set_text(bed_2_type)
	v.get_label_by_id('A').set_fontsize('x-large')
	v.get_label_by_id('B').set_fontsize('x-large')

	# messing with numerical text
	v.get_label_by_id('10').set_fontsize('x-large')
	v.get_label_by_id('01').set_fontsize('x-large')
	v.get_label_by_id('11').set_fontsize('x-large')

	plt.savefig('figures/{}_{}_{}.png'.format(celltype, bed_1_type, bed_2_type))

	fname = '{}_{}.bed'.format(oprefix, end_type)
	bedtools_cmd = 'bedtools intersect -a {} -b {} -s -u > {}'.format(bed_2, bed_1, fname)
	os.system(bedtools_cmd)

	# read in the resultant file
	df = pd.read_csv(fname, sep='\t', header=None, usecols=[0,1,2,5],
		names=['chr', 'start', 'stop', 'strand'])
	both_counts = len(df.index)
	print('{} overlapping {}s with {} to {}'.format(both_counts, end_type, bed_1_type, bed_2_type))

	# generate venn diagram of 2-->1
	counts_1 = bed_1_counts - both_counts
	counts_2 = bed_2_counts - both_counts 
	counts = (counts_1, counts_2, both_counts)

	plt.figure(figsize=(8.5,8.5))
	v = venn2(subsets=counts, set_labels=('A', 'B'))
	plt.title('Shared {} TSSs: {} to {}'.format(celltype, bed_2_type, bed_1_type), 
			  fontsize='xx-large')

	# messing with label text
	v.get_label_by_id('A').set_text(bed_1_type)
	v.get_label_by_id('B').set_text(bed_2_type)
	v.get_label_by_id('A').set_fontsize('x-large')
	v.get_label_by_id('B').set_fontsize('x-large')

	# messing with numerical text
	v.get_label_by_id('10').set_fontsize('x-large')
	v.get_label_by_id('01').set_fontsize('x-large')
	v.get_label_by_id('11').set_fontsize('x-large')

	plt.savefig('figures/{}_{}_{}.png'.format(celltype, bed_2_type, bed_1_type))

if __name__ == '__main__':
	main()