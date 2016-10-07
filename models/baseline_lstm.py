import sloika.module_tools as smt

def network(klen, sd, winlen=3, nfeature=4, size=64):
    """ Create standard Nanonet with LSTM recurrent units

    :param klen: Length of kmer
    :param sd: Standard Deviation of initialisation noise
    :param winlen: Length of window over data
    :param nfeature: Number of features
    :param size: size of hidden recurrent layers

    :returns: a `class`:layer.Layer:
    """

    _prn = smt.partial(smt._rn, sd=sd)
    nstate = (smt._NBASE ** klen) + 1
    rnn_act = smt.tanh
    ff_act = smt.tanh
    insize = nfeature * winlen

    inlayer = smt.Window(winlen)

    fwd1 = smt.Lstm(insize, size, init=_prn, has_bias=True,
                       has_peep=True, fun=rnn_act)
    bwd1 = smt.Lstm(insize, size, init=_prn, has_bias=True,
                       has_peep=True, fun=rnn_act)
    layer1 = smt.birnn(fwd1, bwd1)

    layer2 = smt.FeedForward(2 * size, size, has_bias=True, fun=ff_act)

    fwd3 = smt.Lstm(size, size, init=_prn, has_bias=True,
                       has_peep=True, fun=rnn_act)
    bwd3 = smt.Lstm(size, size, init=_prn, has_bias=True,
                       has_peep=True, fun=rnn_act)
    layer3 = smt.birnn(fwd3, bwd3)

    layer4 = smt.FeedForward(2 * size, size, init=_prn, has_bias=True, fun=ff_act)

    outlayer = smt.Softmax(size, nstate, init=_prn, has_bias=True)

    return smt.Serial([inlayer, layer1, layer2, layer3, layer4, outlayer])
