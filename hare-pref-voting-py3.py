# @Author: Matthew Hale <matthale>
# @Date:   2018-04-23T18:25:12-05:00
# @Email:  mlhale@unomaha.edu
# @Filename: hare-pref-voting.py
# @Last modified by:   matthale
# @Last modified time: 2024-05-15T00:50:20-05:00
# @Copyright: Copyright (C) 2018 Matthew L. Hale

"""
Simple Hare preferential voting in python
Copyright (C) 2018, Matt Hale, updated for Python 3 in 2024

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import csv
import operator
import random
import argparse

parser = argparse.ArgumentParser(description='Tabulate winners for elections conducted with HARE Preferential voting.')
parser.add_argument('ballots', metavar='c',
                    help='The CSV file containing a list of rank-order preferenced ballots of the form: candidate_a,candidate_c,candidate_b,...and so on by preference')
parser.add_argument('--show_steps', help="Shows each step of the hare choice algorithm (Default: False)", 
                    choices=['True', 'False'])
parser.add_argument('--random_seed', help="Set the random seed (Default: 1)")

args = parser.parse_args()
print(f"Parsing Ballot data from {args.ballots}...")

def compute_election(election_name, slots, candidates, ballots, verbose=False):
    num_candidates = len(candidates)
    print(f"Electing {slots} members from {num_candidates} candidates in the {election_name} election.")
    # All ballots for this election have been parsed, perform HARE tabulation
    ranked_losers = [] # list of losers as they are eliminated
    hare_quota = (len(ballots) + 1) // (slots + 1) # the bar for becoming elected
    ranked_winners = []
    if verbose: 
        print(f"Hare quota (AKA number of votes to win) is {hare_quota}")

    while len(ranked_winners) < slots:
        top_ranked_votes = []
        tally = {}
        for ballot in ballots:
            top_ranked_votes.append(ballot[0])

        # Selection step of HARE
        potential_winners = []
        for candidate in candidates:
            if top_ranked_votes.count(candidate) > hare_quota:
                if verbose: 
                    print(f"{candidate} has been elected")
                potential_winners.append(candidate)

            tally[candidate] = top_ranked_votes.count(candidate)

        # Count votes for each candidate and order them by total
        round_tally = sorted(tally.items(), key=operator.itemgetter(1), reverse=True)

        ranked_winners += potential_winners
        # Ensure that only the number of slots are filled
        if len(ranked_winners) > slots:
            raise Exception("There were more winners than slots available")
        elif len(ranked_winners) == slots:
            for winner in potential_winners:
                candidates.remove(winner)
            break # we're done
        else:
            # Remove winner from the candidate pool and continue
            for winner in potential_winners:
                candidates.remove(winner)

                # Update ballots by transferring surplus votes from winner to next in list
                # find ballots where the winner was selected first
                potential_transfer_ballots = list(filter(lambda index_ballot: index_ballot[1][0] == winner, enumerate(ballots)))
                transfer_num = len(potential_transfer_ballots) - hare_quota
                random_transfer_ballots = [potential_transfer_ballots[i] for i in sorted(random.sample(range(len(potential_transfer_ballots)), transfer_num))]

                for index, ballot in random_transfer_ballots:
                    ballot.remove(winner)
                    ballots[index] = ballot

        # Elimination Step of HARE
        # Find the candidates with the lowest number of votes
        lowest_votes = list(filter(lambda name_count: name_count[1] == round_tally[-1][1], round_tally))

        # Randomly pick one of the lowest candidates for removal
        randomly_removed_candidate_index = random.randint(0, len(lowest_votes) - 1)
        lowest_candidate = lowest_votes[randomly_removed_candidate_index][0]
        ranked_losers.append(lowest_candidate)

        # Update ballots by removing the lowest candidate
        for index, ballot in enumerate(ballots):
            ballot.remove(lowest_candidate)
            ballots[index] = ballot

        # Now remove them from the candidate pool
        candidates.remove(lowest_candidate)

        if verbose: 
            print(f"Computing lowest candidate this round ... it is {lowest_candidate} with {lowest_votes[randomly_removed_candidate_index][1]} votes")
        # break

    ranked_losers.reverse()
    # print len(candidates)
    results = {"winners": ranked_winners, "ranking": ranked_winners + candidates + ranked_losers}
    print(f"The winners for the {election_name} election are {results['winners']}")
    return results

num_candidates = 0
slots = 0
candidates = []
results = {}
election_name = ""
ballots = []
seed_value = 1
if args.random_seed is not None:
    seed_value = int(args.random_seed)
random.seed(seed_value)
with open(args.ballots) as ballotfile:
    for line in csv.reader(ballotfile, delimiter=','):
        if line[0] == "start":
            # Gather relevant election meta data
            election_name = line[1]
            slots = int(line[2])
            for token in line[3:]:
                candidates.append(token)
        elif line[0] == "end":
            results[election_name] = compute_election(election_name, slots, candidates, ballots, args.show_steps == 'True')

            # Reset for next election (if it exists)
            election_name = ""
            slots = 0
            ballots = []
            candidates = []
        else:
            # Parse a ballot line
            ballots.append([token for token in line if token != ''])

with open('results.txt', 'w') as f:
    f.write(f"Election results computed from: {str(args.ballots)}\nRandom seed value used in the computation: {str(seed_value)}\n\n\n")
    for key in sorted(results):
        f.write(f"{key}\n")
        f.write(f"Winner(s): {str(results[key]['winners'])}\n")
        f.write(f"Full rankings: {str(results[key]['ranking'])}\n")
        f.write('\n')
