import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# sphinx_gallery_thumbnail_number = 2

class heatmap(object):
    def __init__(self):
        self.vegetables = np.zeros[10]
        self.farmers = np.zeros[10]
        self.harvest = np.zeros[10,10]
    
    def plot_test(self, subframe):
        self.harvest = subframe
               
        self.vegetables = self.harvest.shape[0]
        self.farmers = self.harvest.shape[1]

        fig, ax = plt.subplots()
        im = ax.imshow(harvest)
        '''
        # We want to show all ticks...
        ax.set_xticks(np.arange(len(farmers)))
        ax.set_yticks(np.arange(len(vegetables)))
        # ... and label them with the respective list entries
        ax.set_xticklabels(farmers)
        ax.set_yticklabels(vegetables)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        for i in range(len(vegetables)):
        for j in range(len(farmers)):
                text = ax.text(j, i, harvest[i, j],
                        ha="center", va="center", color="w")
        '''
        ax.set_title("Harvest of local farmers (in tons/year)")
        fig.tight_layout()
        plt.show()