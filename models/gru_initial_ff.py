import sloika.module_tools as smt

def network(klen, sd, nfeature=4, winlen=3, size=64):
    """ GRU Nanonet with addition initial feed-forward layer

    :param klen: Length of kmer
    :param sd: Standard Deviation of initialisation noise
    :param nfeature: Number of features
    :param winlen: Length of window over data
    :param size: size of hidden recurrent layers

    :returns: a `class`:layer.Layer:
    """
    _prn = smt.partial(smt._rn, sd=sd)
    nstate = (smt._NBASE ** klen) + 1
    gru_act = smt.tanh
    ff_act = smt.tanh

    insize = nfeature * winlen

    inlayer = smt.Window(winlen)

    inlayerFF = smt.FeedForward(insize, size, has_bias=True, fun=ff_act)

    fwd1 = smt.Gru(size, size, init=_prn, has_bias=True, fun=gru_act)
    bwd1 = smt.Gru(size, size, init=_prn, has_bias=True, fun=gru_act)
    layer1 = smt.birnn(fwd1, bwd1)

    layer2 = smt.FeedForward(2 * size, size, has_bias=True, fun=ff_act)

    fwd3 = smt.Gru(size, size, init=_prn, has_bias=True, fun=gru_act)
    bwd3 = smt.Gru(size, size, init=_prn, has_bias=True, fun=gru_act)
    layer3 = smt.birnn(fwd3, bwd3)

    layer4 = smt.FeedForward(2 * size, size, init=_prn, has_bias=True, fun=ff_act)

    outlayer = smt.Softmax(size, nstate, init=_prn, has_bias=True)

    return smt.Serial([inlayer, inlayerFF, layer1, layer2, layer3, layer4, outlayer])
