import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

logger = logging.getLogger('utils')

class Graph(object):
    """ tbd """

    def __init__(self):
        pass

    def plot(self, card, data):
        """ tbd """

        if card['type']=='bar':
            if data.shape[1]==2:
                plt.figure(figsize=[10,5])
                sns.barplot(x=data.columns[0],
                    y=data.columns[1],
                    data=data
                )
