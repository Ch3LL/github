# python imports
import csv
import os
import subprocess

# github project imports
import githubapi
from parser import args


def _write_to_csv(pr_commit):
    with open(os.path.join('/tmp', 'pr-commit.csv'), 'w', newline='') as csvfile:
        pr_csv = csv.writer(csvfile, delimiter='!', quotechar='|',
                              quoting=csv.QUOTE_MINIMAL)
        pr_csv.writerow(['pr', 'url',  'commits', 'author'])
        for pr,values in pr_commit.items():
            pr_csv.writerow([pr,
                             f'https://github.com/saltstack/salt/pull/{pr}',
                             values['commits'], values['author'][0]])

def associated_pr_commit(owner, repo, commit):
    '''
    find out which PRs are associated with a commit
    '''
    query = f'''
    query{{
    repository(owner: {owner}, name: {repo}) {{
      commit: object(expression: "{commit}") {{
        ... on Commit {{
          associatedPullRequests(first:3){{
            edges{{
              node{{
                title
                number
                body
                author {{
                  login
                }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    '''
    return githubapi.graphql_query(query)

def get_range_commits(commit1, commit2):
    '''
    query PRs for range of commits between two commits
    and write to a csv file the results
    '''
    ret = subprocess.check_output(
          ['git', '--git-dir=/home/ch3ll/git/salt/.git',
           '--work-tree=/home/ch3ll/git/salt/', 'rev-list',
           commit1 + '..' + commit2, '--no-merges']
    )
    pr_commit = {}
    for commit in ret.decode().split('\n'):
        ret = associated_pr_commit(owner='saltstack', repo='salt', commit=commit)
        for key,val in ret.items():
            try:
                node = val['repository']['commit']['associatedPullRequests']['edges'][0]['node']
                pr = node['number']
                author = node['author']['login']

                if not pr_commit.get(pr):
                    pr_commit[pr] = {}
                    for value in ['author', 'commits']:
                        pr_commit[pr][value] = []

                pr_commit[pr]['commits'].append(commit)
                if not pr_commit[pr]['author']:
                    pr_commit[pr]['author'].append(author)
            except (KeyError,TypeError,IndexError):
                pass
    _write_to_csv(pr_commit)

def get_one_commit(commit):
    '''
    query PR for individual commit
    '''
    ret = associated_pr_commit(owner='saltstack', repo='salt', commit=commit)
    print(ret)

def main():
    if args.commit:
        print(f'Querying PR information for { args.commit }')
        get_one_commit(args.commit)
    if args.range:
        get_range_commits(args.commit1, args.commit2)


if __name__ == '__main__':
    main()
