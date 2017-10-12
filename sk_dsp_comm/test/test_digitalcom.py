from unittest import TestCase

import numpy as np
from .. import digitalcom as dc
from numpy import testing as npt
from scipy import signal


class TestDigitalcom(TestCase):
    _multiprocess_can_split_ = True

    def setUp(self):
        np.random.seed(100)

    def test_farrow_example(self):
        x = np.arange(0, 10)
        self.skipTest("Test not implemented yet.")

    def test_bit_errors_no_errors(self):
        bits = 10
        transmit = np.zeros(bits)
        receive = np.zeros(bits)
        bit_count, bit_errors = dc.bit_errors(transmit, receive)
        self.assertEqual(bit_count, bits)
        self.assertEqual(bit_errors, 0)

    def test_bit_errors_five_errors(self):
        """
        Test for 5 bit errors. Uses ones for data alignment.
        :return:
        """
        bits = 100
        transmit = np.ones(bits)
        receive = np.ones(bits)
        rand_bits = [80, 75, 59, 3, 7]
        for rand_bit in rand_bits:
            receive[rand_bit] -= 1
        bit_count, bit_errors = dc.bit_errors(transmit, receive)
        self.assertEqual(bit_count, bits)
        self.assertEqual(bit_errors, len(rand_bits))

    def test_CIC_4(self):
        """
        4 taps, 7 sections
        :return:
        """
        b_test = np.array([  6.10351562e-05,   4.27246094e-04,   1.70898438e-03,
         5.12695312e-03,   1.23901367e-02,   2.52075195e-02,
         4.44335938e-02,   6.88476562e-02,   9.48486328e-02,
         1.17065430e-01,   1.29882812e-01,   1.29882812e-01,
         1.17065430e-01,   9.48486328e-02,   6.88476562e-02,
         4.44335938e-02,   2.52075195e-02,   1.23901367e-02,
         5.12695312e-03,   1.70898438e-03,   4.27246094e-04,
         6.10351562e-05])
        b = dc.CIC(4, 7)
        npt.assert_almost_equal(b_test, b)

    def test_CIC_1(self):
        """
        4 taps, 1 section
        :return:
        """
        b_test = np.ones(4) / 4
        b = dc.CIC(4, 1)
        npt.assert_almost_equal(b_test, b)

    def test_QAM_bb_qpsk_src(self):
        np.random.seed(100)
        x_test, b_test, t_test = (np.array([ 0.00585723+0.00585723j, -0.00275016-0.00275016j,
       -0.00164540-0.01335987j,  0.00887646+0.01437677j,
       -0.01540288+0.01131686j,  0.00480440-0.02394915j,
        0.02505607+0.02585128j, -0.04406383-0.00716616j,
       -0.02797722-0.08626139j,  0.11024504+0.1600832j ,
        0.00580570+0.16357483j, -0.44629859-0.76924864j,
       -0.96387506-1.22739262j, -1.32990076+0.11435352j,
       -1.06357060+1.2446656j ,  0.04406383+0.22076409j,
        1.06649175-1.18402117j,  1.21485132-1.24832839j,
        0.97347224-0.94165619j,  0.88372072-0.89875699j]),
                                  np.array([-0.00293625,  0.00137866,  0.00376109, -0.00582846,  0.00102417,
        0.00479866, -0.01276   ,  0.01284087,  0.02863407, -0.06775815,
       -0.04245547,  0.30467864,  0.54924435,  0.30467864, -0.04245547,
       -0.06775815,  0.02863407,  0.01284087, -0.01276   ,  0.00479866,
        0.00102417, -0.00582846,  0.00376109,  0.00137866, -0.00293625]),
                                  np.array([-1.-1.j, -1.+1.j,  1.-1.j,  1.-1.j,  1.-1.j,  1.-1.j, -1.+1.j,
       -1.-1.j, -1.-1.j, -1.+1.j]))
        x, b, t = dc.QAM_bb(10, 2, mod_type='qpsk', pulse='src')
        npt.assert_almost_equal(x, x_test)
        npt.assert_almost_equal(b, b_test)
        npt.assert_almost_equal(t, t_test)

    def test_QAM_bb_qpsk_rc(self):
        x_test, b_test, t_test = (np.array([ -2.22799382e-18 -2.22799382e-18j,
        -4.07129297e-03 -4.07129297e-03j,
         2.22160609e-19 +4.67814826e-18j,
        -2.22059175e-03 +5.92199418e-03j,
         6.43926133e-18 -2.91703518e-18j,
         1.97462099e-02 +7.90222150e-03j,
        -9.75189466e-18 -1.28297996e-17j,
        -4.09888874e-02 -7.30785022e-02j,
         1.05934616e-17 +3.71417032e-17j,
         9.37971907e-02 +2.31071828e-01j,
        -1.52549076e-18 -6.78758025e-17j,
        -4.10719565e-01 -8.26448725e-01j,
        -1.00000000e+00 -1.00000000e+00j,
        -1.36231531e+00 +1.25147025e-01j,
        -1.00000000e+00 +1.00000000e+00j,
         4.09888874e-02 +2.75737546e-01j,
         1.00000000e+00 -1.00000000e+00j,
         1.24877191e+00 -1.36728049e+00j,
         1.00000000e+00 -1.00000000e+00j,   8.23659721e-01 -7.64661456e-01j]),
                                  np.array([  1.11223990e-18,   2.03243583e-03,  -1.22314501e-18,
        -9.23891131e-04,  -8.79167710e-19,  -6.90120596e-03,
         5.63651951e-18,   2.84718702e-02,  -1.19149691e-17,
        -8.10891577e-02,   1.73229581e-17,   3.08804252e-01,
         4.99211393e-01,   3.08804252e-01,   1.73229581e-17,
        -8.10891577e-02,  -1.19149691e-17,   2.84718702e-02,
         5.63651951e-18,  -6.90120596e-03,  -8.79167710e-19,
        -9.23891131e-04,  -1.22314501e-18,   2.03243583e-03,
         1.11223990e-18]), np.array([-1.-1.j, -1.+1.j,  1.-1.j,  1.-1.j,  1.-1.j,  1.-1.j, -1.+1.j,
        -1.-1.j, -1.-1.j, -1.+1.j]))
        x, b, t = dc.QAM_bb(10, 2, mod_type='qpsk', pulse='rc')
        npt.assert_almost_equal(x, x_test)
        npt.assert_almost_equal(b, b_test)
        npt.assert_almost_equal(t, t_test)

    def test_QAM_bb_qpsk_rect(self):
        np.random.seed(100)
        x_test, b_test, t_test = (np.array([-1.-1.j, -1.-1.j, -1.+1.j, -1.+1.j,  1.-1.j,  1.-1.j,  1.-1.j,
        1.-1.j,  1.-1.j,  1.-1.j,  1.-1.j,  1.-1.j, -1.+1.j, -1.+1.j,
       -1.-1.j, -1.-1.j, -1.-1.j, -1.-1.j, -1.+1.j, -1.+1.j]), np.array([ 0.5,  0.5]),
                                  np.array([-1.-1.j, -1.+1.j,  1.-1.j,  1.-1.j,  1.-1.j,  1.-1.j, -1.+1.j,
       -1.-1.j, -1.-1.j, -1.+1.j]))
        x, b, t = dc.QAM_bb(10, 2, mod_type='qpsk', pulse='rect')
        npt.assert_almost_equal(x, x_test)
        npt.assert_almost_equal(b, b_test)
        npt.assert_almost_equal(t, t_test)

    def test_QAM_bb_pulse_error(self):
        with self.assertRaisesRegexp(ValueError, 'pulse shape must be src, rc, or rect'):
            dc.QAM_bb(10, 2, pulse='value')

    def test_ODFM_tx(self):
        x_out_test = np.array([ 0.00000000+0.125j,      -0.10185331+0.27369942j, -0.10291586+0.12529202j,
                               -0.05485981-0.1015143j,  -0.02143872-0.09787268j, -0.06906044+0.05231368j,
                               -0.18815224+0.050888j,   -0.26164122-0.15836327j, -0.21940048-0.36048543j,
                               -0.14486054-0.38169759j, -0.11830476-0.25561157j, -0.07250935-0.12760226j,
                                0.05301567-0.08413918j,  0.14316564-0.07020723j,  0.07590886+0.01736066j,
                               -0.04551924+0.15686941j, -0.03125000+0.21875j,     0.09755018+0.17168517j,
                                0.15431728+0.10974492j,  0.08889087+0.04259743j,  0.04284671-0.1107734j,
                                0.10071736-0.25986197j,  0.15582045-0.17226253j,  0.06652251+0.12312402j,
                               -0.15245874+0.29798543j, -0.32346606+0.23845079j, -0.25311017+0.21460293j,
                                0.07831717+0.3396657j,   0.43085592+0.30360811j,  0.48116320-0.0505655j,
                                0.16656460-0.32765262j, -0.20071609-0.16142259j, -0.25000000+0.1875j,
                                0.04290155+0.25900306j,  0.33313987+0.08484705j,  0.28478134-0.00986648j,
                               -0.05936711+0.00190181j, -0.30195965-0.0628197j,  -0.12280721-0.1651266j,
                                0.31807654-0.16252886j,  0.53190048-0.13951457j,  0.31342228-0.20065005j,
                                0.00806130-0.17969398j, -0.00105255+0.03378639j,  0.15279016+0.16494501j,
                                0.09844557-0.009236j,   -0.11589986-0.20597693j, -0.10438721-0.09983656j,
                                0.15625000+0.09375j,     0.22805837+0.03951473j,])
        x1, b1, IQ_data1 = dc.QAM_bb(50000, 1, '16qam')
        x_out = dc.OFDM_tx(IQ_data1, 32, 64, 0, True, 0)
        npt.assert_almost_equal(x_out[:50], x_out_test)

    def test_OFDM_rx(self):
        z_out_test, H_test = (np.array([-3.11740028 - 0.90748269j, -3.11628187 - 0.88948888j,
                                        2.88565859 + 1.13255112j, 2.89076997 + 3.16052588j,
                                        2.90396853 + 1.19595053j, 2.93439648 + 1.23703401j,
                                        -3.00724063 - 0.72880083j, 1.07519281 + 1.27075039j,
                                        1.14472192 + 3.22099905j, -2.82962216 + 1.15148633j,
                                        1.16245397 + 3.09533441j, -0.85799363 - 0.94063529j,
                                        1.12036257 + 1.03825793j, 1.10109739 + 1.02622557j,
                                        1.08488052 - 2.98041713j, 1.07132873 + 1.01625511j,
                                        -0.92119499 + 3.01872286j, -2.91683903 - 0.9906338j,
                                        -2.91213253 - 3.00295552j, 3.09229992 - 3.01974828j]),
                              np.array([1.42289223 - 1.43696423e-01j, 1.34580486 - 2.66705232e-01j,
                                        1.23071709 - 3.51736667e-01j, 1.09530096 - 3.87688911e-01j,
                                        0.95992898 - 3.71339473e-01j, 0.84428862 - 3.07656711e-01j,
                                        0.76421410 - 2.08710707e-01j, 0.72928932 - 9.14213562e-02j,
                                        0.74161551 + 2.54124114e-02j, 0.79590656 + 1.24244087e-01j,
                                        0.88082345 + 1.91510354e-01j, 0.98123573 + 2.19504072e-01j,
                                        1.08094630 + 2.07118520e-01j, 1.16536231 + 1.59418930e-01j,
                                        1.22364402 + 8.62177170e-02j, 1.25000000 - 2.77555756e-17j,
                                        1.25000000 + 2.77555756e-17j, 1.22364402 - 8.62177170e-02j,
                                        1.16536231 - 1.59418930e-01j, 1.08094630 - 2.07118520e-01j,
                                        0.98123573 - 2.19504072e-01j, 0.88082345 - 1.91510354e-01j,
                                        0.79590656 - 1.24244087e-01j, 0.74161551 - 2.54124114e-02j,
                                        0.72928932 + 9.14213562e-02j, 0.76421410 + 2.08710707e-01j,
                                        0.84428862 + 3.07656711e-01j, 0.95992898 + 3.71339473e-01j,
                                        1.09530096 + 3.87688911e-01j, 1.23071709 + 3.51736667e-01j,
                                        1.34580486 + 2.66705232e-01j, 1.42289223 + 1.43696423e-01j]))
        hc = np.array([1.0, 0.1, -0.05, 0.15, 0.2, 0.05])
        x1, b1, IQ_data1 = dc.QAM_bb(50000, 1, '16qam')
        x_out = dc.OFDM_tx(IQ_data1, 32, 64, 0, True, 0)
        c_out = signal.lfilter(hc, 1, x_out)  # Apply channel distortion
        r_out = dc.cpx_AWGN(c_out, 100, 64 / 32)  # Es/N0 = 100 dB
        z_out, H = dc.OFDM_rx(r_out, 32, 64, -1, True, 0, alpha=0.95, ht=hc);
        npt.assert_almost_equal(z_out[:20], z_out_test)
        npt.assert_almost_equal(H, H_test)

    def test_OFDM_rx_channel_estimate(self):
        z_out_test, H_out_test = (np.array([-2.91356233-0.93854058j, -3.03083561-1.01177886j,
                                             3.10687062+1.09962706j,  2.91679784+2.79392693j,
                                             2.95621370+0.87789714j,  2.93521287+1.12869418j,
                                            -3.17675560-1.0834705j ,  1.25700626+1.19497994j,
                                             1.16433902+2.62068101j, -3.10408334+1.08514004j,
                                             1.02623864+3.01672402j, -0.98366297-1.21602375j,
                                             0.89577012+1.07687508j,  1.05852406+1.05134363j,
                                             0.93287609-3.11042385j,  0.99965390+0.88124784j,
                                            -1.16293758+3.08562314j, -2.84891079-1.07199168j,
                                            -3.22236927-2.90425199j,  3.07028549-2.88413491j,
                                            -3.12192058+2.89625467j,  3.18017151-1.09375776j,
                                            -2.78212772+3.05087219j,  1.13471595-2.89218144j,
                                            -3.17092453-1.11298847j,  3.10927184+0.86801524j,
                                            -0.76520964-3.32101721j, -0.94935570+2.86081052j,
                                             0.93535950+1.10545223j,  1.09394518-1.17966519j,
                                             3.10748055+1.12377382j, -3.12337017-0.89848715j,
                                            -2.95725651+0.97491592j,  3.14041238-3.01998896j,
                                            -1.05440640+3.04843936j, -0.94130790-0.82179287j,
                                            -0.79049810-1.04083796j,  2.96004080+1.01692442j,
                                            -3.13063510+1.32083138j, -2.58084447-3.28171534j,
                                             3.09664605+0.82140179j,  2.87565015-1.17002378j,
                                             2.82351021+2.83242155j,  2.99238994+3.06883778j,
                                            -0.83601519-2.8886988j ,  3.05383614+1.22402533j,
                                            -0.92550302+0.92366226j, -0.97707573+3.08608891j,
                                             0.73489228-2.99163649j,  2.89544691+2.76671634j]),
                                  np.array([ 1.49261307-0.12886832j,  1.36399692-0.24831791j,
                                             1.24438887-0.41524198j,  1.15276504-0.47480443j,
                                             1.09981815-0.35438673j,  0.86684483-0.31710329j,
                                             0.75885865-0.23542562j,  0.76309583-0.19374055j,
                                             0.61556098+0.09731796j,  0.77281595+0.07096727j,
                                             0.87593303+0.15642133j,  1.06728467+0.29788462j,
                                             1.08613086+0.23650714j,  1.12082635+0.09129381j,
                                             1.31026672+0.17419224j,  1.19459330+0.01027668j,
                                             1.19745209+0.11471611j,  1.36689249-0.07997548j,
                                             1.26471663-0.07505238j,  1.14356226-0.19961235j,
                                             0.84149706-0.21609579j,  0.85489994-0.18101042j,
                                             0.79502365-0.17155484j,  0.71666634-0.02650505j,
                                             0.82384118+0.0565963j ,  0.74313589+0.28403893j,
                                             0.88570493+0.29345603j,  0.95203301+0.37888469j,
                                             0.98676887+0.4108844j ,  1.26869289+0.35672436j,
                                             1.44594176+0.3296819j ,  1.48817425+0.07577518j]))
        hc = np.array([1.0, 0.1, -0.05, 0.15, 0.2, 0.05])
        x1, b1, IQ_data1 = dc.QAM_bb(50000, 1, '16qam')
        x_out = dc.OFDM_tx(IQ_data1, 32, 64, 100, True, 10)
        c_out = signal.lfilter(hc, 1, x_out)  # Apply channel distortion
        r_out = dc.cpx_AWGN(c_out, 25, 64 / 32)  # Es/N0 = 25 dB
        z_out, H = dc.OFDM_rx(r_out, 32, 64, 100, True, 10, alpha=0.95, ht=hc)
        npt.assert_almost_equal(z_out[:50], z_out_test)
        npt.assert_almost_equal(H[:50], H_out_test)