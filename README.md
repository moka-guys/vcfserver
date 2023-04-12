# VCF server

Returns INFO/FORMAT Field data via simple HTTP API with automatic setup and source data updates.

It is configured to automatically download and serve the current ClinVar VCF files. 

The current use case it to serve the most up-to-date ClinVar classification to the ESMO germline focussed tumour analysis pipeline.


## Configuration

The `config.yaml` file defines a list of VCF resources (download link) that will automatically be downloaded/updated on server/worker startup.

## API

- `GET /kill` - kills the worker and triggers respawn and redownload of VCF resources
- `GET /vcf` - get list of available VCF resource names (e.g. clinvar_grch38)
- `GET /vcf/:resource/info` - Get resource INFO
- `GET /vcf/:resource?variant=1:1234:A:T` - fetch a VCF record from resource
- `GET /vcf/:resource?variant=1:1234:A:T;format=cellbase_clinvar` - fetch a VCF record from resource as cellbase compatible data model

Responses are JSON encoded and contain all fields from the VCF v4.3 specification
