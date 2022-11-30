import urllib.request
import urllib
import os
import hashlib

class RemoteFile(object):
    '''
    remote file
    '''
    def __init__(self, remote, target):
        self.remote = remote
        self.target = os.path.join(target, remote.split('/')[-1])
        return

    def check_version(self, length=32):
        # read from local
        try:
            with open(self.target,'rb') as fh:
                localversion = fh.read(length)
        except Exception:
            return

        # read remote
        with urllib.request.urlopen(self.remote) as f:
            remoteversion = f.read(length)

        # compare
        if localversion == remoteversion:
            return localversion

    def download(self):
        '''
        returns local file path
        '''
        return urllib.request.urlretrieve(self.remote, self.target)

    def md5sum(self):
        '''
        returns md5sum of self.target
        '''
        md5 = hashlib.md5()
        with open(self.target, 'rb') as fh:
            for chunk in iter(lambda: fh.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()


class Fetcher:
    '''
    Data fetching class
    '''
    def __init__(self, configs):
        self.configs = configs
        self.vcfs = {}
        # add listener here (update VCF reader when job has run)
        for cfg in configs:
            
            # check if target directory exists
            if not os.path.exists(cfg['directory']):
                os.mkdir(cfg['directory'])

            # read version from remote
            md5_file = RemoteFile(cfg['source']['md5'], cfg['directory'])
            vcf_file = RemoteFile(cfg['source']['vcf'], cfg['directory'])
            tbi_file = RemoteFile(cfg['source']['tbi'], cfg['directory'])
            current_version = md5_file.check_version()
            if not current_version or not vcf_file.check_version() or not tbi_file.check_version():
                md5_file.download()
                vcf_file.download()
                tbi_file.download()
                current_version = md5_file.check_version()

            # MD5 check
            vcf_md5 = vcf_file.md5sum()
            assert vcf_md5 == current_version.decode('utf-8')

