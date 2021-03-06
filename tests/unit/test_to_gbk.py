#!/usr/bin/env python
# coding: utf-8

"""
Unit tests func_annot function of integron_finder
"""

import integron_finder
import unittest
import pandas as pd
import numpy as np
import os
from Bio import SeqIO
from Bio import Seq
from Bio import SeqFeature


class TestFunctions(unittest.TestCase):
    def setUp(self):
        """
        Define variables common to all tests
        """
        self.replicon_path = os.path.join("tests", "data", 'Replicons', "acba.007.p01.13.fst")
        self.seq = SeqIO.read(self.replicon_path, "fasta",
                              alphabet=Seq.IUPAC.unambiguous_dna)
        integron_finder.PROT_file = os.path.join("tests", "data",
                                                 "Results_Integron_Finder_acba.007.p01.13",
                                                 "acba.007.p01.13.prt")
        integron_finder.DISTANCE_THRESHOLD = 4000
        integron_finder.SIZE_REPLICON = len(self.seq)

    def tearDown(self):
        """
        To do after each test. remove output directory if it was generated
        """
        pass
    # def test_blabla(self):
    #     """
    #     Test blabla
    #     """
    #     # to_gbk(df, sequence)
    #     # sequence is     SEQUENCE = SeqIO.read(replicon_path, "fasta", alphabet=Seq.IUPAC.unambiguous_dna) -> sequence du replicon donné en entrée
    #     # df is :
    #     # pour chaque integron, tous les éléments de l'integron (integrase, attC, attI, promoteur, proteins)
    #     associate an integron number to each integron, sorted by start position of all proteins -> replace ID_integron
    #     reorder columns, and put evalue column to float type
    #     sort all elements by ID_integron, pos_beg, evalue

    #     first case : integron contains only 1 element

    def test_integron_1elem_prot(self):
        """
        Test to_gbk when the only element is an integron composed of 1 protein only.

        """
        infos = {"ID_replicon": "acba.007.p01.13",
                 "ID_integron": "integron_01",
                 "element": "ACBA.007.P01_13_20",
                 "pos_beg": 17375,
                 "pos_end": 17375,
                 "strand": -1,
                 "evalue": np.nan,
                 "type_elt": "protein",
                 "annotation": "protein",
                 "model": "NA",
                 "type": "complete",
                 "default": "Yes",
                 "distance_2attC": np.nan
                }

        df = pd.DataFrame(infos, index = [0])

        start_seq = self.seq.seq
        start_id = self.seq.id

        integron_finder.to_gbk(df, self.seq)

        # Translation should be protein ACBA.007.P01_13_20 in
        # tests/data/Results_Integron_Finder_acba.007.p01.13/acba.007.p01.13.prt
        translate = ("MKGWLFLVIAIVGEVIATSALKSSEGFTKLAPSAVVIIGYGIAFYFLSLVLKSIPVGVAY"
                     "AVWSGLGVVIITAIAWLLHGQKLDAWGFVGMGLIIAAFLLARSPSWKSLRRPTPW*")

        # Check that there are 2 features (integron and protein)
        self.assertEqual(len(self.seq.features), 2)
        # Check that initial sequence and id are not modified
        self.assertEqual(self.seq.seq, start_seq)
        self.assertEqual(self.seq.id, start_id)
        # Check first feature: integron
        self.assertEqual(self.seq.features[0].location.start, infos["pos_beg"] - 1)
        self.assertEqual(self.seq.features[0].location.end, infos["pos_end"])
        self.assertEqual(self.seq.features[0].strand, 0)
        self.assertEqual(self.seq.features[0].type, "integron")
        self.assertEqual(self.seq.features[0].qualifiers["integron_id"], infos["ID_integron"])
        self.assertEqual(self.seq.features[0].qualifiers["integron_type"], infos["type"])
        # Check second feature: protein
        self.assertEqual(self.seq.features[1].location.start, infos["pos_beg"] - 1)
        self.assertEqual(self.seq.features[1].location.end, infos["pos_end"])
        self.assertEqual(self.seq.features[1].strand, infos["strand"])
        self.assertEqual(self.seq.features[1].type, "CDS")
        self.assertEqual(self.seq.features[1].qualifiers["protein_id"], infos["element"])
        self.assertEqual(self.seq.features[1].qualifiers["gene"], infos["annotation"])
        self.assertEqual(self.seq.features[1].qualifiers["model"], infos["model"])
        self.assertEqual(self.seq.features[1].qualifiers["translation"].tostring(), translate)


    def test_integron_1elem_int(self):
        """
        Test to_gbk when the only element is an integron composed of 1 integrase only.

        """
        infos = {"ID_replicon": "acba.007.p01.13",
                 "ID_integron": "integron_01",
                 "element": "ACBA.007.P01_13_1",
                 "pos_beg": 55,
                 "pos_end": 1014,
                 "strand": 1,
                 "evalue": 1.9e-25,
                 "type_elt": "protein",
                 "annotation": "intI",
                 "model": "intersection_tyr_intI",
                 "type": "complete",
                 "default": "Yes",
                 "distance_2attC": np.nan
                }

        df = pd.DataFrame(infos, index = [0])

        start_seq = self.seq.seq
        start_id = self.seq.id

        integron_finder.to_gbk(df, self.seq)

        # Translation should be protein ACBA.007.P01_13_1 in
        # tests/data/Results_Integron_Finder_acba.007.p01.13/acba.007.p01.13.prt
        translate = ("MKTATAPLPPLRSVKVLDQLRERIRYLHYSLRTEQAYVNWVRAFIRFHGVRHPATLGSSE"
                     "VEAFLSWLANERKVSVSTHRQALAALLFFYGKVLCTDLPWLQEIGRPRPSRRLPVVLTPD"
                     "EVVRILGFLEGEHRLFAQLLYGTGMRISEGLQLRVKDLDFDHGTIIVREGKGSKDRALML"
                     "PESLAPSLREQLSRARAWWLKDQAEGRSGVALPDALERKYPRAGHSWPWFWVFAQHTHST"
                     "DPRSGVVRRHHMYDQTFQRAFKRAVEGTVAKLAMRQPFVLFKGLTFQKLCLPGAFRPGDH"
                     "HNKMLRPGLCVVHASPQYL*")

        # Check that there are 2 features (integron and protein)
        self.assertEqual(len(self.seq.features), 2)
        # Check that initial sequence and id are not modified
        self.assertEqual(self.seq.seq, start_seq)
        self.assertEqual(self.seq.id, start_id)
        # Check first feature: integron
        self.assertEqual(self.seq.features[0].location.start, infos["pos_beg"] - 1)
        self.assertEqual(self.seq.features[0].location.end, infos["pos_end"])
        self.assertEqual(self.seq.features[0].strand, 0)
        self.assertEqual(self.seq.features[0].type, "integron")
        self.assertEqual(self.seq.features[0].qualifiers["integron_id"], infos["ID_integron"])
        self.assertEqual(self.seq.features[0].qualifiers["integron_type"], infos["type"])
        # Check second feature: protein
        self.assertEqual(self.seq.features[1].location.start, infos["pos_beg"] - 1)
        self.assertEqual(self.seq.features[1].location.end, infos["pos_end"])
        self.assertEqual(self.seq.features[1].strand, infos["strand"])
        self.assertEqual(self.seq.features[1].type, "integrase")
        self.assertEqual(self.seq.features[1].qualifiers["protein_id"], infos["element"])
        self.assertEqual(self.seq.features[1].qualifiers["gene"], infos["annotation"])
        self.assertEqual(self.seq.features[1].qualifiers["model"], infos["model"])
        self.assertEqual(self.seq.features[1].qualifiers["translation"].tostring(), translate)


    def test_integron_1elem_prom(self):
        """
        Test to_gbk when the only element is an integron composed of 1 promoter only.

        """
        infos = {"ID_replicon": "acba.007.p01.13",
                 "ID_integron": "integron_01",
                 "element": "Pc_int1",
                 "pos_beg": 25,
                 "pos_end": 51,
                 "strand": -1,
                 "evalue": np.nan,
                 "type_elt": "Promoter",
                 "annotation": "Pc_1",
                 "model": "NA",
                 "type": "complete",
                 "default": "Yes",
                 "distance_2attC": np.nan
                }

        df = pd.DataFrame(infos, index = [0])

        start_seq = self.seq.seq
        start_id = self.seq.id

        integron_finder.to_gbk(df, self.seq)

        # Check that there are 2 features (integron and promoter)
        self.assertEqual(len(self.seq.features), 2)
        # Check that initial sequence and id are not modified
        self.assertEqual(self.seq.seq, start_seq)
        self.assertEqual(self.seq.id, start_id)
        # Check first feature: integron
        self.assertEqual(self.seq.features[0].location.start, infos["pos_beg"] - 1)
        self.assertEqual(self.seq.features[0].location.end, infos["pos_end"])
        self.assertEqual(self.seq.features[0].strand, 0)
        self.assertEqual(self.seq.features[0].type, "integron")
        self.assertEqual(self.seq.features[0].qualifiers["integron_id"], infos["ID_integron"])
        self.assertEqual(self.seq.features[0].qualifiers["integron_type"], infos["type"])
        # Check second feature: promotor
        self.assertEqual(self.seq.features[1].location.start, infos["pos_beg"] - 1)
        self.assertEqual(self.seq.features[1].location.end, infos["pos_end"])
        self.assertEqual(self.seq.features[1].strand, infos["strand"])
        self.assertEqual(self.seq.features[1].type, infos["type_elt"])
        self.assertEqual(self.seq.features[1].qualifiers["Promoter"], infos["element"])
        self.assertEqual(self.seq.features[1].qualifiers["model"], infos["model"])


    def test_integron_nelem(self):
        """
        Test to_gbk when there are several elements in the integron:
        protein, integrase, promotor, attC

        """
        # Integron is composed of: 1 promoter, 1 integrase, 1protein, 1attC
        # promoter and integrase are at the begining of the genome
        # others are at the end
        int_id = "integron_01"
        rep_id = "acba.007.p01.13"
        int_type = "complete"
        infos_prom = {"ID_replicon": rep_id,
                      "ID_integron": int_id,
                      "element": "Pc_int1",
                      "pos_beg": 25,
                      "pos_end": 51,
                      "strand": -1,
                      "evalue": np.nan,
                      "type_elt": "Promoter",
                      "annotation": "Pc_1",
                      "model": "NA",
                      "type": int_type,
                      "default": "Yes",
                      "distance_2attC": np.nan
                     }
        infos_int = {"ID_replicon": rep_id,
                     "ID_integron": int_id,
                     "element": "ACBA.007.P01_13_1",
                     "pos_beg": 55,
                     "pos_end": 1014,
                     "strand": 1,
                     "evalue": 1.9e-25,
                     "type_elt": "protein",
                     "annotation": "intI",
                     "model": "NA",
                     "type": int_type,
                     "default": "Yes",
                     "distance_2attC": np.nan
                    }
        infos_prot = {"ID_replicon": rep_id,
                      "ID_integron": int_id,
                      "element": "ACBA.007.P01_13_20",
                      "pos_beg": 17375,
                      "pos_end": 17375,
                      "strand": -1,
                      "evalue": np.nan,
                      "type_elt": "protein",
                      "annotation": "protein",
                      "model": "intersection_tyr_intI",
                      "type": int_type,
                      "default": "Yes",
                      "distance_2attC": np.nan
                     }
        infos_attC = {"ID_replicon": rep_id,
                      "ID_integron": int_id,
                      "element": "attc_001",
                      "pos_beg": 17825,
                      "pos_end": 17884,
                      "strand": -1,
                      "evalue": 1e-9,
                      "type_elt": "attC",
                      "annotation": "attC",
                      "model": "attc_4",
                      "type": int_type,
                      "default": "Yes",
                      "distance_2attC": np.nan
                     }


        df1 = pd.DataFrame(infos_prom, index = [0])
        df2 = pd.DataFrame(infos_int, index = [0])
        df3 = pd.DataFrame(infos_prot, index = [0])
        df4 = pd.DataFrame(infos_attC, index = [0])

        df = pd.concat([df1, df2, df3, df4])

        start_seq = self.seq.seq
        start_id = self.seq.id
        lenseq = len(self.seq)

        tr_int = ("MKTATAPLPPLRSVKVLDQLRERIRYLHYSLRTEQAYVNWVRAFIRFHGVRHPATLGSSE"
                  "VEAFLSWLANERKVSVSTHRQALAALLFFYGKVLCTDLPWLQEIGRPRPSRRLPVVLTPD"
                  "EVVRILGFLEGEHRLFAQLLYGTGMRISEGLQLRVKDLDFDHGTIIVREGKGSKDRALML"
                  "PESLAPSLREQLSRARAWWLKDQAEGRSGVALPDALERKYPRAGHSWPWFWVFAQHTHST"
                  "DPRSGVVRRHHMYDQTFQRAFKRAVEGTVAKLAMRQPFVLFKGLTFQKLCLPGAFRPGDH"
                  "HNKMLRPGLCVVHASPQYL*")
        tr_prot = ("MKGWLFLVIAIVGEVIATSALKSSEGFTKLAPSAVVIIGYGIAFYFLSLVLKSIPVGVAY"
                   "AVWSGLGVVIITAIAWLLHGQKLDAWGFVGMGLIIAAFLLARSPSWKSLRRPTPW*")

        integron_finder.to_gbk(df, self.seq)

        # Check that there are 5 features (integron, promoter, integrase, protein, attC)
        self.assertEqual(len(self.seq.features), 5)
        # Check that initial sequence and id are not modified
        self.assertEqual(self.seq.seq, start_seq)
        self.assertEqual(self.seq.id, start_id)
        # Check first feature: integron
        self.assertEqual(self.seq.features[0].location.parts[0].start, infos_prot["pos_beg"] - 1)
        self.assertEqual(self.seq.features[0].location.parts[0].end,  lenseq)
        self.assertEqual(self.seq.features[0].location.parts[1].start, 0)
        self.assertEqual(self.seq.features[0].location.parts[1].end, infos_int["pos_end"])
        self.assertEqual(self.seq.features[0].strand, 0)
        self.assertEqual(self.seq.features[0].type, "integron")
        self.assertEqual(self.seq.features[0].qualifiers["integron_id"], int_id)
        self.assertEqual(self.seq.features[0].qualifiers["integron_type"], int_type)
        # Check second feature: promoter
        self.assertEqual(self.seq.features[1].location.start, infos_prom["pos_beg"] - 1)
        self.assertEqual(self.seq.features[1].location.end, infos_prom["pos_end"])
        self.assertEqual(self.seq.features[1].strand, infos_prom["strand"])
        self.assertEqual(self.seq.features[1].type, "Promoter")
        self.assertEqual(self.seq.features[1].qualifiers["Promoter"], infos_prom["element"])
        self.assertEqual(self.seq.features[1].qualifiers["model"], infos_prom["model"])
        # Check second feature: integrase
        self.assertEqual(self.seq.features[2].location.start, infos_int["pos_beg"] - 1)
        self.assertEqual(self.seq.features[2].location.end, infos_int["pos_end"])
        self.assertEqual(self.seq.features[2].strand, infos_int["strand"])
        self.assertEqual(self.seq.features[2].type, "integrase")
        self.assertEqual(self.seq.features[2].qualifiers["protein_id"], infos_int["element"])
        self.assertEqual(self.seq.features[2].qualifiers["gene"], infos_int["annotation"])
        self.assertEqual(self.seq.features[2].qualifiers["model"], infos_int["model"])
        self.assertEqual(self.seq.features[2].qualifiers["translation"].tostring(), tr_int)
        # Check second feature: protein
        self.assertEqual(self.seq.features[3].location.start, infos_prot["pos_beg"] - 1)
        self.assertEqual(self.seq.features[3].location.end, infos_prot["pos_end"])
        self.assertEqual(self.seq.features[3].strand, infos_prot["strand"])
        self.assertEqual(self.seq.features[3].type, "CDS")
        self.assertEqual(self.seq.features[3].qualifiers["protein_id"], infos_prot["element"])
        self.assertEqual(self.seq.features[3].qualifiers["gene"], infos_prot["annotation"])
        self.assertEqual(self.seq.features[3].qualifiers["model"], infos_prot["model"])
        self.assertEqual(self.seq.features[3].qualifiers["translation"].tostring(), tr_prot)
        # Check second feature: attC
        self.assertEqual(self.seq.features[4].location.start, infos_attC["pos_beg"] - 1)
        self.assertEqual(self.seq.features[4].location.end, infos_attC["pos_end"])
        self.assertEqual(self.seq.features[4].strand, infos_attC["strand"])
        self.assertEqual(self.seq.features[4].type, "attC")
        self.assertEqual(self.seq.features[4].qualifiers["attC"], infos_attC["element"])
        self.assertEqual(self.seq.features[4].qualifiers["model"], infos_attC["model"])

    def test_integron_2int_nelem(self):
        """
        Test to_gbk when there are 2 integrons:
            integron 1 with several elements: protein, integrase, promoter
            integron 2 with only 1 attC site
        Integrons are not over the edge of sequence
        """
        # integron 1
        int_id = "integron_01"
        rep_id = "acba.007.p01.13"
        int_type = "complete"
        infos_prom = {"ID_replicon": rep_id,
                      "ID_integron": int_id,
                      "element": "Pc_int1",
                      "pos_beg": 25,
                      "pos_end": 51,
                      "strand": -1,
                      "evalue": np.nan,
                      "type_elt": "Promoter",
                      "annotation": "Pc_1",
                      "model": "NA",
                      "type": int_type,
                      "default": "Yes",
                      "distance_2attC": np.nan
                     }
        infos_int = {"ID_replicon": rep_id,
                     "ID_integron": int_id,
                     "element": "ACBA.007.P01_13_1",
                     "pos_beg": 55,
                     "pos_end": 1014,
                     "strand": 1,
                     "evalue": 1.9e-25,
                     "type_elt": "protein",
                     "annotation": "intI",
                     "model": "NA",
                     "type": int_type,
                     "default": "Yes",
                     "distance_2attC": np.nan
                    }
        infos_prot = {"ID_replicon": rep_id,
                      "ID_integron": int_id,
                      "element": "ACBA.007.P01_13_20",
                      "pos_beg": 2000,
                      "pos_end": 2056,
                      "strand": -1,
                      "evalue": np.nan,
                      "type_elt": "protein",
                      "annotation": "protein",
                      "model": "intersection_tyr_intI",
                      "type": int_type,
                      "default": "Yes",
                      "distance_2attC": np.nan
                     }
        # integron 2
        infos_attC = {"ID_replicon": rep_id,
                      "ID_integron": "integron_02",
                      "element": "attc_001",
                      "pos_beg": 17825,
                      "pos_end": 17884,
                      "strand": -1,
                      "evalue": 1e-9,
                      "type_elt": "attC",
                      "annotation": "attC",
                      "model": "attc_4",
                      "type": int_type,
                      "default": "Yes",
                      "distance_2attC": np.nan
                     }

        df1 = pd.DataFrame(infos_prom, index = [0])
        df2 = pd.DataFrame(infos_int, index = [0])
        df3 = pd.DataFrame(infos_prot, index = [0])
        df4 = pd.DataFrame(infos_attC, index = [0])

        df = pd.concat([df1, df2, df3, df4])

        start_seq = self.seq.seq
        start_id = self.seq.id
        lenseq = len(self.seq)

        tr_int = ("MKTATAPLPPLRSVKVLDQLRERIRYLHYSLRTEQAYVNWVRAFIRFHGVRHPATLGSSE"
                  "VEAFLSWLANERKVSVSTHRQALAALLFFYGKVLCTDLPWLQEIGRPRPSRRLPVVLTPD"
                  "EVVRILGFLEGEHRLFAQLLYGTGMRISEGLQLRVKDLDFDHGTIIVREGKGSKDRALML"
                  "PESLAPSLREQLSRARAWWLKDQAEGRSGVALPDALERKYPRAGHSWPWFWVFAQHTHST"
                  "DPRSGVVRRHHMYDQTFQRAFKRAVEGTVAKLAMRQPFVLFKGLTFQKLCLPGAFRPGDH"
                  "HNKMLRPGLCVVHASPQYL*")
        tr_prot = ("MKGWLFLVIAIVGEVIATSALKSSEGFTKLAPSAVVIIGYGIAFYFLSLVLKSIPVGVAY"
                   "AVWSGLGVVIITAIAWLLHGQKLDAWGFVGMGLIIAAFLLARSPSWKSLRRPTPW*")

        integron_finder.to_gbk(df, self.seq)

        # Check that there are 6 features (integron1, promoter, integrase, protein,
        #                                  integron2, attC)
        self.assertEqual(len(self.seq.features), 6)
        # Check that initial sequence and id are not modified
        self.assertEqual(self.seq.seq, start_seq)
        self.assertEqual(self.seq.id, start_id)
        # Check first feature: integron1
        self.assertEqual(self.seq.features[0].location.start, infos_prom["pos_beg"] - 1)
        self.assertEqual(self.seq.features[0].location.end, infos_prot["pos_end"])
        self.assertEqual(self.seq.features[0].strand, 0)
        self.assertEqual(self.seq.features[0].type, "integron")
        self.assertEqual(self.seq.features[0].qualifiers["integron_id"], int_id)
        self.assertEqual(self.seq.features[0].qualifiers["integron_type"], int_type)
        # Check feature 2: promoter
        self.assertEqual(self.seq.features[1].location.start, infos_prom["pos_beg"] - 1)
        self.assertEqual(self.seq.features[1].location.end, infos_prom["pos_end"])
        self.assertEqual(self.seq.features[1].strand, infos_prom["strand"])
        self.assertEqual(self.seq.features[1].type, "Promoter")
        self.assertEqual(self.seq.features[1].qualifiers["Promoter"], infos_prom["element"])
        self.assertEqual(self.seq.features[1].qualifiers["model"], infos_prom["model"])
        # Check feature 3: integrase
        self.assertEqual(self.seq.features[2].location.start, infos_int["pos_beg"] - 1)
        self.assertEqual(self.seq.features[2].location.end, infos_int["pos_end"])
        self.assertEqual(self.seq.features[2].strand, infos_int["strand"])
        self.assertEqual(self.seq.features[2].type, "integrase")
        self.assertEqual(self.seq.features[2].qualifiers["protein_id"], infos_int["element"])
        self.assertEqual(self.seq.features[2].qualifiers["gene"], infos_int["annotation"])
        self.assertEqual(self.seq.features[2].qualifiers["model"], infos_int["model"])
        self.assertEqual(self.seq.features[2].qualifiers["translation"].tostring(), tr_int)
        # Check feature 4: protein
        self.assertEqual(self.seq.features[3].location.start, infos_prot["pos_beg"] - 1)
        self.assertEqual(self.seq.features[3].location.end, infos_prot["pos_end"])
        self.assertEqual(self.seq.features[3].strand, infos_prot["strand"])
        self.assertEqual(self.seq.features[3].type, "CDS")
        self.assertEqual(self.seq.features[3].qualifiers["protein_id"], infos_prot["element"])
        self.assertEqual(self.seq.features[3].qualifiers["gene"], infos_prot["annotation"])
        self.assertEqual(self.seq.features[3].qualifiers["model"], infos_prot["model"])
        self.assertEqual(self.seq.features[3].qualifiers["translation"].tostring(), tr_prot)
        # Check feature 5: integron2
        self.assertEqual(self.seq.features[4].location.start, infos_attC["pos_beg"] - 1)
        self.assertEqual(self.seq.features[4].location.end, infos_attC["pos_end"])
        self.assertEqual(self.seq.features[4].strand, 0)
        self.assertEqual(self.seq.features[4].type, "integron")
        self.assertEqual(self.seq.features[4].qualifiers["integron_id"], "integron_02")
        self.assertEqual(self.seq.features[4].qualifiers["integron_type"], int_type)
        # Check feature 6: attC
        self.assertEqual(self.seq.features[5].location.start, infos_attC["pos_beg"] - 1)
        self.assertEqual(self.seq.features[5].location.end, infos_attC["pos_end"])
        self.assertEqual(self.seq.features[5].strand, infos_attC["strand"])
        self.assertEqual(self.seq.features[5].type, "attC")
        self.assertEqual(self.seq.features[5].qualifiers["attC"], infos_attC["element"])
        self.assertEqual(self.seq.features[5].qualifiers["model"], infos_attC["model"])

    def test_integron_long_seqname(self):
        """
        Test to_gbk when the only element is an integron composed of 1 protein only.

        """
        infos = {"ID_replicon": "acba.007.p01.13",
                 "ID_integron": "integron_01",
                 "element": "ACBA.007.P01_13_20",
                 "pos_beg": 17375,
                 "pos_end": 17375,
                 "strand": -1,
                 "evalue": np.nan,
                 "type_elt": "protein",
                 "annotation": "protein",
                 "model": "NA",
                 "type": "complete",
                 "default": "Yes",
                 "distance_2attC": np.nan
                }

        df = pd.DataFrame(infos, index = [0])

        start_seq = self.seq.seq
        start_id = self.seq.id
        seq_name = self.seq.name
        self.seq.name = "abcdefgh" + seq_name

        integron_finder.to_gbk(df, self.seq)

        # Translation should be protein ACBA.007.P01_13_20 in
        # tests/data/Results_Integron_Finder_acba.007.p01.13/acba.007.p01.13.prt
        translate = ("MKGWLFLVIAIVGEVIATSALKSSEGFTKLAPSAVVIIGYGIAFYFLSLVLKSIPVGVAY"
                     "AVWSGLGVVIITAIAWLLHGQKLDAWGFVGMGLIIAAFLLARSPSWKSLRRPTPW*")

        # Check that there are 2 features (integron and protein)
        self.assertEqual(len(self.seq.features), 2)
        # Check that initial sequence and id are not modified
        self.assertEqual(self.seq.seq, start_seq)
        self.assertEqual(self.seq.id, start_id)
        # Check that sequence name has been shortened
        self.assertEqual(self.seq.name, "h" + seq_name)
