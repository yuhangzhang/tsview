


class TSWaveTree(QStandardItemModel):
    def __init__(ASDFdataset):
        super(TSWaveTree, self).__init__()

        self.wavenames = ASDFdataset.waveforms.list()

        self.waves = [ASDFdataset.waveforms[i] for i in self.wavenames]





