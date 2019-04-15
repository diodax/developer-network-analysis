# -*- coding: utf-8 -*-
import click
import logging
import itertools
from dotenv import find_dotenv, load_dotenv
from git import Repo
from collections import defaultdict


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """
    Runs data processing scripts to turn repository data from (../external) into
    cleaned edge list ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('Importing repo from ' + str(input_filepath))

    repo = Repo(input_filepath)
    committers_by_file = defaultdict(set)

    commits = repo.iter_commits()
    for commit in commits:
        # Iterate through all the files affected in this commit
        print("Checking commit by %s with SHA %s" % (commit.committer.name, commit.hexsha))

        for key, value in commit.stats.files.items():
            # Add them to the committers_by_file, if they don't exist already
            committers_by_file[key].add(commit.committer.email)

    # Print all unordered pairs of distinct authors of each file set
    logger.info('Generating list of author edge combinations...')
    graph_edges = set()
    for key, value in committers_by_file.items():
        # Get the set from each file and generate pairs from it
        for pair in itertools.combinations(value, 2):
            graph_edges.add(pair)

    logger.info('Saving results on ' + output_filepath)
    with open(output_filepath, 'w') as writer:
        # Further file processing goes here
        for edge in graph_edges:
            writer.write(str(edge[0]) + ":" + str(edge[1] + "\n"))


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    load_dotenv(find_dotenv())

    main()
