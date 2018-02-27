import os

try:
    from tests import IntegronTest
except ImportError as err:
    msg = "Cannot import integron_finder: {0!s}".format(err)
    raise ImportError(msg)

from integron_finder import utils


class TestUtils(IntegronTest):

    def test_read_single_dna_fasta(self):
        replicon_name = 'acba.007.p01.13'
        replicon_path = self.find_data(os.path.join('Replicons', replicon_name + '.fst'))
        replicon = utils.read_single_dna_fasta(replicon_path)
        self.assertEqual(replicon.id, 'ACBA.007.P01_13')
        self.assertEqual(replicon.name, replicon.name)
        self.assertEqual(len(replicon), 20301)
        self.assertTrue(replicon.seq.startswith('TGCTGCTTGGATGCCCGAGGCATAGACTGTACAAAAAAACAGTCATAACAAGCCATGAAA'))
        self.assertTrue(replicon.seq.endswith('CGACCCACGGCGTAACGCGCT'))

    def test_read_multi_prot_fasta(self):
        replicon_name = 'acba.007.p01.13'
        replicon_path = self.find_data(os.path.join('Proteins', replicon_name + '.prt'))
        replicon = utils.read_multi_prot_fasta(replicon_path)
        expected_seq_id = ['ACBA.007.P01_13_{}'.format(i) for i in range(1, 24)]
        received_seq_id = [seq.id for seq in replicon]
        self.assertListEqual(expected_seq_id, received_seq_id)


    def test_model_len(self):
        model_path = self.find_data(os.path.join('Models', 'attc_4.cm'))
        self.assertEqual(utils.model_len(model_path), 47)
        bad_path = 'nimportnaoik'
        with self.assertRaises(IOError) as ctx:
            utils.model_len(bad_path)
        self.assertEqual(str(ctx.exception),
                         "Path to model_attc '{}' does not exists".format(bad_path))
        bad_path = self.find_data(os.path.join('Models', 'phage-int.hmm'))
        with self.assertRaises(RuntimeError) as ctx:
            utils.model_len(bad_path)
        self.assertEqual(str(ctx.exception),
                         "CLEN not found in '{}', maybe it's not infernal model file".format(bad_path))


    def test_get_name_from_path(self):
        self.assertEqual(utils.get_name_from_path('/foo/bar.baz'), 'bar')
        self.assertEqual(utils.get_name_from_path('bar.baz'), 'bar')
        self.assertEqual(utils.get_name_from_path('../foo/bar.baz'), 'bar')
        self.assertEqual(utils.get_name_from_path('../foo/bar'), 'bar')


    def test_non_gembase_parser(self):
        desc = 'ACBA.007.P01_13_1 # 55 # 1014 # 1 # ID=1_1;partial=00;start_type=ATG;rbs_motif=None;' \
               'rbs_spacer=None;gc_cont=0.585'
        prot_attr = utils.non_gembase_parser(desc)

        expected = utils.ProtDesc('ACBA.007.P01_13_1', 1, 55, 1014)
        self.assertTupleEqual(expected, prot_attr)

    def test_gembase_parser(self):
        desc = 'OBAL001.B.00005.C001_00003 C ATG TAA 3317 4294 Valid AKN90_RS00015 978 ' \
               '@WP_053105352.1@ AKN90_RS00015 1 3317 4294 | alpha-L-glutamate ligase-like protein  (translation)'
        prot_attr = utils.gembase_parser(desc)

        expected = utils.ProtDesc('OBAL001.B.00005.C001_00003', -1, 3317, 4294)
        self.assertTupleEqual(expected, prot_attr)