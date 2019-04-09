#!/usr/bin/env python3

"""
Requires: https://github.com/PyGithub/PyGithub

Command line wrapper to make github assets

No download, just list assets:

make-release-assets.py -k -r ontodev/robot -v v1.1.0

"""

from github import Github
import click
import logging
logging.basicConfig(level=logging.INFO)

@click.command()
@click.option("-k", "--dry-run/--no-dry-run", default=False)
@click.option("-t", "--token")
@click.option("-o", "--org")
@click.option("-r", "--repo", default="mondo")
@click.option("-v", "--release", default="v2018-08-24")
@click.argument("paths", nargs=-1)
def make_assets(dry_run, token, org, repo, release, paths):
    if '/' in repo:
        [org,repo] = repo.split('/')
    if org == None:
        org = 'monarch-initiative'
    logging.info('org={} repo={} rel={}'.format(org, repo, release))
    if token == None:
        with open('.token') as f:
            logging.info("Reading token from file")
            token = f.read().rstrip().lstrip()
    G = Github(token)
    G_org = G.get_organization(org)
    G_repo = G_org.get_repo(repo)
    G_rel = G_repo.get_release(release)

    print('Existing assets:')
    for a in G_rel.get_assets():
        print('Asset: {} Size: {} Downloads: {}'.format(a.name, a.size, a.download_count))

    if (dry_run):
        print("DRY RUN")
    else:
        for path in paths:
            # TODO: if asset already exists, skip; add a --force option to explicitly overwrite
            print('Uploading: {}'.format(path))
            a = G_rel.upload_asset(path=path)
            print('Uploaded: {} {} from {}'.format(a.name, a.size, path))

    
if __name__ == "__main__":
    make_assets()
