import pandas as pd
import argparse
import os
from matplotlib_venn import venn2


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-bedfile', dest='bed',
		help='bedfile of merged ends')
	parser.add_argument('-ref', dest='ref',
		help='bedfile of reference ends')
	parser.add_argument('-type', dest='end_type',
		help='type of end. choose "TES" or "TSS"')
	parser.add_argument('-o', dest='oprefix',
		help='output file prefix')
	args = parser.parse_args()
	return args

def format_subprocess_cmd(string):
	return string.split(' ')

def main():
	args = get_args()
	end_type = args.end_type
	bed = args.bed
	ref = args.ref
	oprefix = args.oprefix

	fname = '{}_{}.bed'.format(oprefix, end_type)
	bedtools_cmd = 'bedtools intersect -a {} -b {} -u -s > {}'.format(bed, ref, fname)
	os.system(bedtools_cmd)

	df = pd.read_csv(fname, sep='\t', header=None, usecols=[0])
	known_count = len(df.index)
	print("Found {} known {}'s".format(known_count, end_type))


	fname = '{}_{}_v.bed'.format(oprefix, end_type)
	bedtools_cmd = 'bedtools intersect -a {} -b {} -v -s > {}'.format(bed, ref, fname)
	os.system(bedtools_cmd)

	df = pd.read_csv(fname, sep='\t', header=None, usecols=[0])
	novel_count = len(df.index)
	print("Found {} novel {}'s".format(novel_count, end_type))

if __name__ == '__main__':
	main()