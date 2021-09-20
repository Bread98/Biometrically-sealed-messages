# In the reedsolo.py module, substitute the rs_encode_msg() function (line 508) with the following modified version.


def rs_encode_msg(msg_in, nsym, fcr=0, generator=2, gen=None):
    '''Reed-Solomon main encoding function, using polynomial division (Extended Synthetic Division, the fastest algorithm available to my knowledge), better explained at http://research.swtch.com/field'''
    global field_charac
    if (len(msg_in) + nsym) > field_charac: raise ValueError("Message is too long (%i when max is %i)" % (len(msg_in)+nsym, field_charac))
    if gen is None: gen = rs_generator_poly(nsym, fcr, generator)

    msg_in = _bytearray(msg_in)
    msg_out = _bytearray(msg_in) + _bytearray(len(gen)-1) # init msg_out with the values inside msg_in and pad with len(gen)-1 bytes (which is the number of ecc symbols).

    # Precompute the logarithm of every items in the generator
    lgen = _bytearray([gf_log[gen[j]] for j in xrange(len(gen))])

    # Extended synthetic division main loop
    # Fastest implementation with PyPy (but the Cython version in creedsolo.pyx is about 2x faster)
    for i in xrange(len(msg_in)):
        coef = msg_out[i] # Note that it's msg_out here, not msg_in. Thus, we reuse the updated value at each iteration (this is how Synthetic Division works: instead of storing in a temporary register the intermediate values, we directly commit them to the output).
        # coef = gf_mul(msg_out[i], gf_inverse(gen[0]))  # for general polynomial division (when polynomials are non-monic), the usual way of using synthetic division is to divide the divisor g(x) with its leading coefficient (call it a). In this implementation, this means:we need to compute: coef = msg_out[i] / gen[0]
        if coef != 0: # log(0) is undefined, so we need to manually check for this case. There's no need to check the divisor here because we know it can't be 0 since we generated it.
            lcoef = gf_log[coef] # precaching

            for j in xrange(1, len(gen)): # in synthetic division, we always skip the first coefficient of the divisior, because it's only used to normalize the dividend coefficient (which is here useless since the divisor, the generator polynomial, is always monic)
                #if gen[j] != 0: # log(0) is undefined so we need to check that, but it slow things down in fact and it's useless in our case (reed-solomon encoding) since we know that all coefficients in the generator are not 0
                msg_out[i + j] ^= gf_exp[lcoef + lgen[j]] # optimization, equivalent to gf_mul(gen[j], msg_out[i]) and we just substract it to msg_out[i+j] (but since we are in GF256, it's equivalent to an addition and to an XOR). In other words, this is simply a "multiply-accumulate operation"

    # Recopy the original message bytes (overwrites the part where the quotient was computed)
    msg_out[:len(msg_in)] = msg_in # equivalent to c = mprime - b, where mprime is msg_in padded with [0]*nsym
    pad_to_ret = msg_out[len(msg_in):]
    return msg_out, pad_to_ret