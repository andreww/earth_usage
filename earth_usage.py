#!/usr/env/bin python

import subprocess
from collections import defaultdict

def str_2_sec(timein):
    """
    Convert time in days / hrs / mins etc to total seconds used)
    """
    splitdays = timein.split('-')
    if len(splitdays) == 2:
        # Have list of days and time
        secs = 24*60*60*int(splitdays[0]) + str_2_sec(splitdays[1])
    elif len(splitdays) == 1:
        # Just have a time
        splittime = timein.split(':')
        assert len(splittime) == 3, 'not enough bits'
        secs = int(splittime[2]) + 60*int(splittime[1]) + 60*60*int(splittime[0])
    else:
        # Bust
        assert False, 'time conversion error'

    return secs


def extract_data():
    args = ['sacct', '-q','earth', '-a', '-S', '2021-01-01',
            '-o jobid,jobname,partition,account,alloccpus,start,elapsed,state,user']
    compproc = subprocess.run(args, capture_output=True, check=True, text=True)

    projects_tottime = defaultdict(int) # Default should be 0

    for line in compproc.stdout.splitlines():
        words = line.split()
        if words[0] == 'JobID' or words[0] == '------------':
            pass
        elif len(words) == 9:
            cores = int(words[4])
            secs = str_2_sec(words[6])
            # Has a 'user' and everything we need (probably)
            # (skip the tasks that are somehow automatic)
            projects_tottime[words[3]] += cores * secs

    return projects_tottime

def main():
    projects = extract_data()
    tot_time = 0
    for k, v in projects.items():
        tot_time = tot_time + v
        time = v / 60 / 60 / 24
        print(f"{k} used {time} cpu days")
    tot_time = tot_time / 60 / 60/ 24
    print(f"Total time used {tot_time}")

if __name__ == "__main__":
    main()
