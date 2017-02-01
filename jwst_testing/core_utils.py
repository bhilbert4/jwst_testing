"""
Utilities that are used for a number of different steps
"""

import numpy as np

dq_dict = {
'DO_NOT_USE' : 0,
'SATURATED' : 1,
'JUMP_DET' : 2,
'DROPOUT' : 3,
'RESERVED' : 4,     
'RESERVED' : 5,     
'RESERVED' : 6,     
'RESERVED' : 7,     
'UNRELIABLE_ERROR' : 8,
'NON_SCIENCE' : 9,
'DEAD' : 10,
'HOT' : 11,
'WARM' : 12,
'LOW_QE' : 13,
'RC' : 14,
'TELEGRAPH' : 15,
'NONLINEAR' : 16,
'BAD_REF_PIXEL' : 17,
'NO_FLAT_FIELD' : 18,
'NO_GAIN_VALUE' : 19,
'NO_LIN_CORR' : 20,
'NO_SAT_CHECK' : 21,
'UNRELIABLE_BIAS' : 22,
'UNRELIABLE_DARK' : 23,
'UNRELIABLE_SLOPE' : 24,
'UNRELIABLE_FLAT' : 25,
'OPEN' : 26,
'ADJ_OPEN' : 27,
'UNRELIABLE_RESET' : 28,
'MSA_FAILED_OPEN' : 29,
'OTHER_BAD_PIXEL' : 30,
}

def get_pixeldq_bit(name):
    if name in dq_dict:
        return dq_dict[name]
    else:
        return 'N/A'

def bitwise_propagate(refhdu, pixeldq):
    for row in refhdu['DQ_DEF'].data:
        try:
            # find which pixels have the bit set
            flagged = (np.bitwise_and(1, np.right_shift(refhdu['DQ'].data.astype(np.uint32), row['BIT'])))
            # shift them to the correct bit for PIXELDQ
            flagged = np.left_shift(flagged, dq_dict[row['NAME']])
            # propagate into the PIXELDQ extension
            pixeldq = np.bitwise_or(pixeldq, flagged)
        except KeyError:
            print("No DQ mnemonic "+row['NAME'])
    return pixeldq
