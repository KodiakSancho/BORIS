"""
module for testing time budget analysis

pytest -s -vv test_irr.py
"""

import pytest
import sys
import json
import os
sys.path.append("../src")

import irr
import db_functions
from config import *
import decimal


class Test_irr(object):

    def test_same_observation(self):

        pj = json.loads(open("files/test.boris").read())

        ethogram = pj[ETHOGRAM]
        selected_observations = ["observation #1", "observation #1"]
        selected_subjects = ["subject1", "subject2"]

        r, s, db = cursor = db_functions.load_aggregated_events_in_db(pj,
                                              selected_subjects,
                                              selected_observations,
                                              ["s", "p"])
        assert r == True

        cursor = db.cursor()
        K, msg = irr.cohen_kappa(cursor,
                               obsid1 = selected_observations[0],
                               obsid2 = selected_observations[1],
                               interval = decimal.Decimal("1.0"),
                               selected_subjects = selected_subjects,
                               include_modifiers = False)


        assert K == 1



    def test_very_different_obs(self):

        pj = json.loads(open("files/test.boris").read())

        ethogram = pj[ETHOGRAM]
        selected_observations = ["observation #1", "observation #2"]
        selected_subjects = ["subject1", "subject2"]

        r, s, db = cursor = db_functions.load_aggregated_events_in_db(pj,
                                              selected_subjects,
                                              selected_observations,
                                              ["s"])

        cursor = db.cursor()
        K, msg = irr.cohen_kappa(cursor,
                               obsid1 = selected_observations[0],
                               obsid2 = selected_observations[1],
                               interval = decimal.Decimal("1.0"),
                               selected_subjects = selected_subjects,
                               include_modifiers = False)


        assert K == -0.036


    def test_very_similar_obs_interval_state_1s(self):

        pj = json.loads(open("files/test.boris").read())

        ethogram = pj[ETHOGRAM]
        selected_observations = ["observation #2", "observation #2 (copy)"]
        selected_subjects = ["No focal subject", "subject1", "subject2"]

        r, s, db = cursor = db_functions.load_aggregated_events_in_db(pj,
                                              selected_subjects,
                                              selected_observations,
                                              ["s"])

        cursor = db.cursor()
        K, _ = irr.cohen_kappa(cursor,
                               obsid1 = selected_observations[0],
                               obsid2 = selected_observations[1],
                               interval = decimal.Decimal("1.0"),
                               selected_subjects = selected_subjects,
                               include_modifiers = False)

        assert K == 0.988


    def test_very_similar_obs_interval_state_3s(self):

        pj = json.loads(open("files/test.boris").read())

        ethogram = pj[ETHOGRAM]
        selected_observations = ["observation #2", "observation #2 (copy)"]
        selected_subjects = ["No focal subject", "subject1", "subject2"]

        r, s, db = cursor = db_functions.load_aggregated_events_in_db(pj,
                                              selected_subjects,
                                              selected_observations,
                                              ["s"])

        cursor = db.cursor()
        K, _ = irr.cohen_kappa(cursor,
                               obsid1 = selected_observations[0],
                               obsid2 = selected_observations[1],
                               interval = decimal.Decimal("3"),
                               selected_subjects = selected_subjects,
                               include_modifiers = False)

        print(K)
        assert K == 1


    def test_very_similar_obs_interval_point_1s(self):

        pj = json.loads(open("files/test.boris").read())

        ethogram = pj[ETHOGRAM]
        selected_observations = ["observation #2", "observation #2 (copy)"]
        selected_subjects = ["No focal subject", "subject1", "subject2"]

        r, s, db = cursor = db_functions.load_aggregated_events_in_db(pj,
                                              selected_subjects,
                                              selected_observations,
                                              ["p"])

        cursor = db.cursor()
        K, _ = irr.cohen_kappa(cursor,
                               obsid1 = selected_observations[0],
                               obsid2 = selected_observations[1],
                               interval = decimal.Decimal("1.0"),
                               selected_subjects = selected_subjects,
                               include_modifiers = False)

        assert K == 0.866


    def test_very_similar_obs_interval_point_3s(self):

        pj = json.loads(open("files/test.boris").read())

        ethogram = pj[ETHOGRAM]
        selected_observations = ["observation #2", "observation #2 (copy)"]
        selected_subjects = ["No focal subject", "subject1", "subject2"]

        r, s, db = cursor = db_functions.load_aggregated_events_in_db(pj,
                                              selected_subjects,
                                              selected_observations,
                                              ["p"])

        cursor = db.cursor()
        K, _ = irr.cohen_kappa(cursor,
                               obsid1 = selected_observations[0],
                               obsid2 = selected_observations[1],
                               interval = decimal.Decimal("3.0"),
                               selected_subjects = selected_subjects,
                               include_modifiers = False)

        assert K == 0.798



    def test_obs_without_events(self):

        pj = json.loads(open("files/test.boris").read())

        ethogram = pj[ETHOGRAM]
        selected_observations = ["observation #2", "observation without events"]
        selected_subjects = ["No focal subject", "subject1", "subject2"]

        r, s, db = cursor = db_functions.load_aggregated_events_in_db(pj,
                                              selected_subjects,
                                              selected_observations,
                                              ["s"])

        cursor = db.cursor()
        K, _ = irr.cohen_kappa(cursor,
                               obsid1 = selected_observations[0],
                               obsid2 = selected_observations[1],
                               interval = decimal.Decimal("1"),
                               selected_subjects = selected_subjects,
                               include_modifiers = False)

        assert K == -100
