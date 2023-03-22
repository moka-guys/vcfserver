#!/usr/bin/env python
import re
import os
import flask
import signal
import yaml
from flask import request, jsonify, Response
from functools import lru_cache
from collections import defaultdict
from .vcfs import VCFs
from .fetcher import Fetcher

app = flask.Flask(__name__)

# load config
with open('config.yaml') as fh:
    try:
        cfg = yaml.safe_load(fh)
        app.config.update(cfg)
    except yaml.YAMLError as err:
        print(err)
        raise

# setup file fetcher
print('Starting VCF fetchers...')
fetcher = Fetcher(app.config['DATA'])

# setup VCF readers
print('Starting VCF request handlers...')
vcf_handlers = VCFs(app.config['DATA'])

''' kills the server (docker would restart it) '''
@app.route('/kill', methods=['GET'])
def kill():
    os.kill(os.getpid(), signal.SIGTERM)
    return 'Server shutting down...'

''' returns available VCFs '''
@app.route('/vcf', methods=['GET'])
def vcfs():
    search = request.args.get('search','')
    items = list(filter(lambda x: re.match(search, x['id']) if search else True, vcf_handlers.ids()))
    print(items)
    return jsonify(items)

''' returns vcf info'''
@app.route('/vcf/<string:id>/info', methods=['GET'])
def vcf_info(id):
    try:
        return jsonify(vcf_handlers.info(id))
    except Exception as err:
        return Response(status=404)


''' returns vcf record '''
@app.route('/vcf/<string:id>', methods=['GET'])
def vcf(id):
    variant = request.args.get('variant')
    format = request.args.get('format')
    print(variant)
    if vcf_handlers[id]:
        print(f'Query {id}')
        try:
            chrom, pos, ref, alt = variant.split(':')
        except ValueError:
            return None
        record = vcf_handlers.fetch_position(id, chrom, int(pos), ref, alt)
        if record is not None and record.chrom == chrom and record.pos == int(pos) and  record.ref == ref and record.alts[0] == alt:
            if format == 'cellbase_clinvar':
                return jsonify({
                    'accession': record.id,
                    'link': f'https://www.ncbi.nlm.nih.gov/clinvar/variation/{record.id}/',
                    'clinicalSignificance': ','.join(record.info['CLNSIG']),
                    'reviewStatus': '|'.join(record.info['CLNREVSTAT']),
                    'traits': '|'.join(record.info['CLNDN']),
                    'geneNames': '|'.join(record.info['GENEINFO']),
                })
            return jsonify({
                'chrom': record.chrom,
                'pos': record.pos,
                'id': record.id,
                'qual': record.qual,
                'filter': dict(record.filter),
                'ref': record.ref,
                'alt': record.alts,
                'info': dict(record.info),
                'format': dict(record.format),
            })
        return jsonify({})
    return Response(status=404)


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)


