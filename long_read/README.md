## June 2020 Jamboree

Code to run stuff from last jamboree (June 2020) is in `intersect_tss_tes.sh`. This includes merging TSSs/TESs within 50 bp of each other, merging with Gencode and ONT data.

## December 2020 Jamboree

### Getting bigwig files for TSSs/TESs from different datasets
```bash
# human chrom sizes
chrom_sizes=~/mortazavi_lab/ref/hg38/hg38.chrom.sizes

# GM12878 - PacBio Sequel II
infile=data/GM12878_talon_read_annot.tsv
datasets=PB_GM12878_R1,PB_GM12878_R2
oprefix=data/pb_gm12878_sequel2
bash get_bigwig_from_talon_ends.sh \
	-a ${infile} \
	-c ${chrom_sizes} \
	-o ${oprefix}
```

### Getting TSSs from different datasets
```bash
# Mats Ljungman's HCT116 - PacBio Sequel II (ENCLB218VBB)
annot=data/PB215_talon_read_annot.tsv
datasets='all'
oprefix=data/mats_hct116
python get_ends_from_talon_annot.py \
    -annot ${annot} \
    -datasets ${datasets} \
    -filter_type talon \
    -min_tpm 1 \
    -o ${oprefix}

# Mats Ljungman's PC-3 - PacBio Sequel II (ENCLB542NGF)
annot=data/PB216_talon_read_annot.tsv
datasets='all'
oprefix=data/mats_pc3
python get_ends_from_talon_annot.py \
    -annot ${annot} \
    -datasets ${datasets} \
    -filter_type talon \
    -min_tpm 1 \
    -o ${oprefix}

# Mats Ljungman's Panc1 - PacBio Sequel II (ENCLB962HZB)
annot=data/PB217_talon_read_annot.tsv
datasets='all'
oprefix=data/mats_panc1
python get_ends_from_talon_annot.py \
    -annot ${annot} \
    -datasets ${datasets} \
    -filter_type talon \
    -min_tpm 1 \
    -o ${oprefix}

# Mats Ljungman's K562 - PacBio Sequel II (ENCLB214YWC)
annot=data/PB218_talon_read_annot.tsv
datasets='all'
oprefix=data/mats_k562
python get_ends_from_talon_annot.py \
    -annot ${annot} \
    -datasets ${datasets} \
    -filter_type talon \
    -min_tpm 1 \
    -o ${oprefix}

# Mats Ljungman's GM12878 - PacBio Sequel II (ENCLB784FMA)
annot=data/PB219_talon_read_annot.tsv
datasets='all'
oprefix=data/mats_gm12878
python get_ends_from_talon_annot.py \
    -annot ${annot} \
    -datasets ${datasets} \
    -filter_type talon \
    -min_tpm 1 \
    -o ${oprefix}

# Mats Ljungman's HepG2 - PacBio Sequel II (ENCLB798VOD)
annot=data/PB220_talon_read_annot.tsv
datasets='all'
oprefix=data/mats_hepg2
python get_ends_from_talon_annot.py \
    -annot ${annot} \
    -datasets ${datasets} \
    -filter_type talon \
    -min_tpm 1 \
    -o ${oprefix}

# Mats Ljungman's MCF-7 - PacBio Sequel II (ENCLB192AUL)
annot=data/PB221_talon_read_annot.tsv
datasets='all'
oprefix=data/mats_mcf7
python get_ends_from_talon_annot.py \
    -annot ${annot} \
    -datasets ${datasets} \
    -filter_type talon \
    -min_tpm 1 \
    -o ${oprefix}

# Mats Ljungman's IMR90 - PacBio Sequel II (ENCLB085UQI)
annot=data/PB222_talon_read_annot.tsv
datasets='all'
oprefix=data/mats_imr90
python get_ends_from_talon_annot.py \
    -annot ${annot} \
    -datasets ${datasets} \
    -filter_type talon \
    -min_tpm 1 \
    -o ${oprefix}

# C2C12 Myoblasts - PacBio Sequel II (ENCLB756XOV, ENCLB214KKF)
annot=data/C2C12_talon_read_annot.tsv
datasets='PB154,PB155'
oprefix=data/c2c12_mb
python get_ends_from_talon_annot.py \
    -annot ${annot} \
    -datasets ${datasets} \
    -filter_type talon \
    -min_tpm 1 \
    -o ${oprefix}

# C2C12 Myotubes - PacBio Sequel II (ENCLB959RPY, ENCLB627KIH)
annot=data/C2C12_talon_read_annot.tsv
datasets='PB213,PB214'
oprefix=data/c2c12_mt
python get_ends_from_talon_annot.py \
    -annot ${annot} \
    -datasets ${datasets} \
    -filter_type talon \
    -min_tpm 1 \
    -o ${oprefix}
```