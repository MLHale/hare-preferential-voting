# @Author: Matthew Hale <matthale>
# @Date:   2018-04-23T18:25:12-05:00
# @Email:  mlhale@unomaha.edu
# @Filename: hare-pref-voting.py
# @Last modified by:   matthale
# @Last modified time: 2018-04-24T01:24:58-05:00
# @Copyright: Copyright (C) 2018 Matthew L. Hale
import os
import sys
import getopt
import csv
import operator
import random

import argparse

parser = argparse.ArgumentParser(description='Tabulate winners for elections conducted with HARE Preferential voting.')
parser.add_argument('ballots', metavar='c',
                    help='The CSV file containing a list of rank-order preferenced ballots of the form: candidate_a,candidate_c,candidate_b,...and so on by preference')

args = parser.parse_args()
print args.ballots
# print(args.accumulate(args.ballots))

num_candidates = 0
slots = 0
candidates = []
results = {}
current_election = ""
hare_quota = 0
ballots_current = []
with open(args.ballots) as ballotfile:
    for line in csv.reader(ballotfile, delimiter=','):
        if line[0] == "start":
            current_election = line[1]
            slots = int(line[2])
            for token in line[3:]:
                candidates.append(token)
            num_candidates = len(candidates)
            print "Electing %d members from %d candidates in the %s election." % (slots, num_candidates, current_election)
            results[current_election] = []
        elif line[0] == "end":
            # All ballots for this election have been parsed, perform HARE tabulation
            ranked_losers = [] # list of losers as they are eliminated
            hare_quota = (len(ballots_current)+1)/(slots+1) # the bar for becoming elected
            ranked_winners = []
            print "Hare quota (AKA number of votes to win) is %d" % hare_quota

            while len(ranked_winners) < slots:
                # print ranked_winners
                # print "starting round"
                top_ranked_votes = []
                tally = {}
                for ballot in ballots_current:
                    top_ranked_votes.append(ballot[0])

                # Selection step of HARE
                potential_winners = []
                for candidate in candidates:
                    if top_ranked_votes.count(candidate) > hare_quota:
                        print "%s has been elected" % candidate
                        potential_winners.append(candidate)

                    tally[candidate] = top_ranked_votes.count(candidate)

                # Count votes for each candidate and order them by total
                round_tally = sorted(tally.items(), key=operator.itemgetter(1), reverse=True)

                ranked_winners = ranked_winners + potential_winners
                # Ensure that only the number of slots are filled
                if len(ranked_winners) > slots:
                    raise Exception("There were more winners than slots available")
                elif len(ranked_winners) == slots:
                    break # we're done
                else:
                    # Remove winner from the candidate pool and continue
                    for winner in potential_winners:
                        candidates.remove(winner)

                        # Update ballots by transfering surplus votes from winner to next in list
                        # find ballots where the winner was selected first

                        potential_transfer_ballots = filter(lambda (index,ballot): ballot[0]==winner,enumerate(ballots_current))
                        # print potential_transfer_ballots
                        transfer_num = len(potential_transfer_ballots) - hare_quota
                        random_transfer_ballots = [ potential_transfer_ballots[i] for i in sorted(random.sample(xrange(len(potential_transfer_ballots)), transfer_num)) ]

                        # print "transfer-ballots", random_transfer_ballots
                        for index, ballot in random_transfer_ballots:
                            ballot.remove(winner)

                            ballots_current[index] = ballot
                            # ballots_current[index] = ballot



                # Elimination Step of HARE
                # Find the candidates with the lowest number of votes
                lowest_votes = filter(lambda (name,count): count == round_tally[len(round_tally)-1][1], round_tally)

                # Randomly pick one of the lowest candidates for removal
                lowest_candidate = lowest_votes[random.randint(0, len(lowest_votes)-1)][0]
                print "Lowest candidate this round is %s" % lowest_candidate
                ranked_losers.append(lowest_candidate)

                # Update ballots by removing the lowest candidate
                for index, ballot in enumerate(ballots_current):
                    # print ballot
                    ballot.remove(lowest_candidate)
                    ballots_current[index] = ballot

                # Now remove them from the candidate pool
                candidates.remove(lowest_candidate)

                # print "Lowest candidate this round is %s" % lowest_candidate
                # break
            ranked_losers.reverse()
            results[current_election] = { "winners" : ranked_winners, "ranking": ranked_winners + ranked_losers}
            print "The winners for the %s election are %s" % (current_election, results[current_election]["winners"])
            current_election=""
        else:
            ballots_current.append(line)
