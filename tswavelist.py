

class TSWaveList(QListView):
    def __init__(self):
        super(TSWaveList, self).__init__()

    def selectionChanged(self, selected, deselected):