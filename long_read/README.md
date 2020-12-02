## June 2020 Jamboree

Code to run stuff from last jamboree (June 2020) is in `intersect_tss_tes.sh`. This includes merging TSSs/TESs within 50 bp of each other, merging with Gencode and ONT data.

## December 2020 Jamboree

### Getting bigwig files for TSSs/TESs from PacBio Sequel II GM12878 data
```bash
infile=data/GM12878_talon_read_annot.tsv
datasets=PB_GM12878_R1,PB_GM12878_R2
oprefix=data/pb_gm12878_sequel2
chrom_sizes=~/mortazavi_lab/ref/hg38/hg38.chrom.sizes

bash get_bigwig_from_talon_ends.sh \
	-a ${infile} \
	-c ${chrom_sizes} \
	-o ${oprefix}
```

### Getting TSSs from C2C12 data
```bash
python get_ends_from_talon_annot.py \
    -annot data/C2C12_talon_read_annot.tsv \
    -datasets PB154,PB155 \
    -filter_type talon \
    -min_tpm 1 \
    -o data/c2c12_mb
```