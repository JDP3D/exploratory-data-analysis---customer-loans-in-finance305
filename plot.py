import missingno as msno
import seaborn as sns
import pandas as pd
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

class Plotter:

    def plot_missingno(self, dataframe):
        msno.matrix(dataframe)
    
    def plot_missingno_heatmap(self, dataframe):
        msno.heatmap(dataframe)
    
    def histogram_grid(self, dataframe, font_scale=0.7, data=None, columns=3):
        '''This method plots a grid of histograms'''

        sns.set(font_scale=font_scale)
        f = pd.melt(dataframe, value_vars=data)
        g = sns.FacetGrid(f, col="variable",  col_wrap=columns, sharex=False, sharey=False)
        g = g.map(sns.histplot, "value", kde=True)
    
    def boxplot_grid(self, dataframe, font_scale=0.7, data=None, columns=3):
        '''This method plots a grid of histograms'''

        sns.set(font_scale=font_scale)
        f = pd.melt(dataframe, value_vars=data)
        g = sns.FacetGrid(f, col="variable",  col_wrap=columns, sharex=False, sharey=False)
        g = g.map(sns.boxplot, "value", order=None)

    def plot_histogram(self, dataframe, column, kd=True, plot_title='', fig_size=(10,5), font_size=10):
        '''This method plots a histogram of the given data'''

        fig, ax = plt.subplots(1,1,figsize=fig_size)
        h = sns.histplot(dataframe[column],label="Skewness: %.2f"%(dataframe[column].skew()), kde=kd, ax=ax)
        h.set_title(plot_title, fontsize=font_size)
        h.legend(fontsize=font_size)
        plt.show()
    
    def plot_box(self, dataframe, column, orientation='h', fill=True, plot_title='', fig_size=(10,5), font_size=10):
        '''This method plots a histogram of the given data'''

        fig, ax = plt.subplots(1,1,figsize=fig_size)
        h = sns.boxplot(dataframe[column], orient=orientation, fill=fill, ax=ax) #type: ignore
        h.set_title(plot_title, fontsize=font_size)
        plt.show()

    def qq_plot(self, dataframe, scale=1, fig_size=(10,5), plot_title='', font_size=10):
        ''' This method plots a qq plot'''

        fig, ax = plt.subplots(1,1,figsize=fig_size)
        qqplot(dataframe, scale=scale ,line='q', fit=True, ax=ax)
        ax.set_title(plot_title, fontsize=font_size)
        plt.xlabel('Theoretical Quantities', fontsize=font_size)
        plt.ylabel('Sample Quantiles', fontsize=font_size)
        plt.show()

    def test_logtransform(self, dataframe, data, fig_size=(15,5)):
        '''This method applys a log transform  to the data and plots a histogram and qq plot'''

        log = dataframe[data].map(lambda i: np.log(i) if i > 0 else 0)

        fig, axes = plt.subplots(1,2,figsize=fig_size)
        t=sns.histplot(log,label="Skewness: %.2f"%(log.skew()), kde=True, ax=axes[0] )
        t.legend()
        qqplot(log , scale=1 ,line='q', fit=True, ax=axes[1])
        plt.show()
    
    
    def plot_transform_comparison(self, dataframe, data, fig_size=(15,8), title='', font_size=10):
        '''This method plots comparisons in data transformations as histograms and qq plots'''

        fig, axes = plt.subplots(2,4,figsize=fig_size)
        fig.suptitle(f'{title} transform comparison', fontsize=font_size+2)
        fig.tight_layout(pad=3.0)

        # Original
        orig = sns.histplot(dataframe[data], label="Skewness: %.2f"%(dataframe[data].skew()), kde=True, ax=axes[0,0])
        orig.legend(fontsize=font_size)
        orig.set_title('Original', fontsize=font_size)
        qqplot(dataframe[data], scale=1 ,line='q', fit=True, ax=axes[1,0])


        # log transform
        log = dataframe[data].map(lambda i: np.log(i) if i > 0 else 0)

        t = sns.histplot(log,label="Skewness: %.2f"%(log.skew()), kde=True, ax=axes[0,1])
        t.legend(fontsize=font_size)
        t.set_title('Log Transform', fontsize=font_size)
        qqplot(log, scale=1 ,line='q', fit=True, ax=axes[1,1])

        # Box-Cox
        if dataframe[data].min() <= 0:
            axes[0,2].text(0.5, 0.5, 'Box-Cox transform not applied \nas data is not strictly positive.', 
                           horizontalalignment='center', verticalalignment='center', transform=axes[0,2].transAxes)
        else:
            boxcox = dataframe[data]
            boxcox = stats.boxcox(boxcox)
            boxcox = pd.Series(boxcox[0])

            b=sns.histplot(boxcox,label="Skewness: %.2f"%(boxcox.skew()), kde=True, ax=axes[0,2]) #type: ignore
            b.legend(fontsize=font_size)
            b.set_title('Box-Cox', fontsize=font_size)
            b.set(xlabel=data)
            qqplot(boxcox, scale=1 ,line='q', fit=True, ax=axes[1,2])

        # Yeo-Johnson
        yeojohnson = dataframe[data]
        yeojohnson = stats.yeojohnson(yeojohnson)
        yeojohnson= pd.Series(yeojohnson[0])

        y=sns.histplot(yeojohnson,label="Skewness: %.2f"%(yeojohnson.skew()), kde=True, ax=axes[0,3] ) #type: ignore
        y.legend(fontsize=font_size)
        y.set_title('Yeo-Johnson', fontsize=font_size)
        y.set(xlabel=data)
        qqplot(yeojohnson, scale=1 ,line='q', fit=True, ax=axes[1,3])

        plt.show()

    
    def plot_outlier_removal_comparison(self, df1, df2, column, width=0.8, fig_size=(15,4), title='', font_size=12, padding=3.0):
        '''' This method plots boxplots and histograms before and after outlier removal from a dataframe column'''

        fig, axes = plt.subplots(1,2,figsize=fig_size)
        fig.suptitle(f'{title} before and after outlier removal', fontsize=font_size+2)
        fig.tight_layout(pad=padding)

        box_before = sns.boxplot(df1[column], orient='h', width=width, ax=axes[0]) #type: ignore
        box_before.set_title('Before outlier removal', fontsize=font_size)
        box_after = sns.boxplot(df2[column], orient='h', width=width, ax=axes[1]) #type: ignore
        box_after.set_title('After outlier removal', fontsize=font_size)

        # sns.histplot(df1[column], kde=True, ax=axes[1,0])
        # sns.histplot(df2[column], kde=True, ax=axes[1,1])

        plt.show()

    def correlation_heatmap(self, dataframe, column, fig_size=(14,12), title='', font_size=12):
            '''This method plots correlation heatmap'''

            fig,  ax = plt.subplots(figsize=(14, 12))
            corr_matrix = dataframe[column].corr()
            mask = np.triu(np.ones_like(corr_matrix))
            sns.heatmap(
                data=corr_matrix,
                square=True,
                annot=True,
                cmap="crest",
                fmt=".2f",
                linewidth=.5,
                cbar_kws={"shrink": 0.9},
                mask=mask,
                axes=ax
            )
            plt.title(title, fontsize=font_size)
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)
            plt.tight_layout()
            plt.show()





