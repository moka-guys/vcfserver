


.PHONY: all clinvar annotations


# building
push: build
	docker push seglh/vcfserver

build:
	docker buildx build --platform linux/amd64 -t seglh/vcfserver .


# annotations
annotations: clinvar

clinvar: clinvar.vcf.gz clinvar.vcf.gz.tbi

clinvar.vcf.gz:
	wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz

clinvar.vcf.gz.tbi:
	wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz.tbi
