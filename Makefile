


.PHONY: devbuild build push clinvar annotations test

# building
push: build
	docker push seglh/vcfserver

build:
	docker buildx build --platform linux/amd64 -t seglh/vcfserver .


# test docker container
test: devbuild
	docker stop test_vcfserver || echo "no container to stop"
	sleep 3
	docker run --rm -d -p 3003:5000 -v `pwd`/data:/app/data --name test_vcfserver seglh/vcfserver:develop
	sleep 5
	docker exec test_vcfserver tail -f /logs/vcfserver_error.log

# quick native build for testing
devbuild:
	docker build -t seglh/vcfserver:develop .

# annotations
annotations: clinvar

# ClinVar
clinvar: clinvar_grch37 clinvar_grch38
	mkdir -p data/clinvar_grch37

clinvar_grch37:  data/clinvar_grch37/clinvar.vcf.gz data/clinvar_grch37/clinvar.vcf.gz.tbi data/clinvar_grch37/clinvar.vcf.gz.md5

clinvar_grch38:  data/clinvar_grch38/clinvar.vcf.gz data/clinvar_grch38/clinvar.vcf.gz.tbi data/clinvar_grch38/clinvar.vcf.gz.md5

# GRCh37
data/clinvar_grch37:
	mkdir -p data/clinvar_grch37

data/clinvar_grch37/clinvar.vcf.gz: data/clinvar_grch37
	cd data/clinvar_grch37 && \
	wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz

data/clinvar_grch37/clinvar.vcf.gz.tbi: data/clinvar_grch37
	cd data/clinvar_grch37 && \
	wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz.tbi

data/clinvar_grch37/clinvar.vcf.gz.md5: data/clinvar_grch37
	cd data/clinvar_grch37 && \
	wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz.md5


# GRCh38
data/clinvar_grch38:
	mkdir -p data/clinvar_grch38

data/clinvar_grch38/clinvar.vcf.gz: data/clinvar_grch38
	cd data/clinvar_grch38 && \
	wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz

data/clinvar_grch38/clinvar.vcf.gz.tbi: data/clinvar_grch38
	cd data/clinvar_grch38 && \
	wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi

data/clinvar_grch38/clinvar.vcf.gz.md5: data/clinvar_grch38
	cd data/clinvar_grch38 && \
	wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.md5
