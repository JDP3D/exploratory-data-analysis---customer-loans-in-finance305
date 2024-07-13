import missingno as msno
import seaborn as sns
import pandas as pd
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from collections import Counter

class Plotter:

    def plot_missingno(self, dataframe):
        '''This method produces a missingno plot
        
        Parameters:
            dataframe: The required dataframe for the plot.

        Returns:
            None
        
        '''
        msno.matrix(dataframe)
    
    def plot_missingno_heatmap(self, dataframe):
        msno.heatmap(dataframe)
    
    def histogram_grid(self, dataframe, font_scale=0.7, data=None, columns=3):
        '''This method plots a grid of histograms

        Parameters:
            dataframe: The required dataframe for the plot.
            font_scale: The font size.
            data: The required columns of the dataframe.
            columns: The number of plots on the horizontal axis

        Returns:
            None
        
        '''
        sns.set(font_scale=font_scale)
        f = pd.melt(dataframe, value_vars=data)
        g = sns.FacetGrid(f, col="variable",  col_wrap=columns, sharex=False, sharey=False)
        g = g.map(sns.histplot, "value", kde=True)
    
    def boxplot_grid(self, dataframe, font_scale=0.7, data=None, columns=3):
        '''This method plots a grid of box plots
        
         Parameters:
            dataframe: The required dataframe for the plot.
            font_scale: The font size.
            data: The required columns of the dataframe.
            columns: The number of plots on the horizontal axis.

        Returns:
            None
        
        '''
        sns.set(font_scale=font_scale)
        f = pd.melt(dataframe, value_vars=data)
        g = sns.FacetGrid(f, col="variable",  col_wrap=columns, sharex=False, sharey=False)
        g = g.map(sns.boxplot, "value", order=None)

    def plot_histogram(self, dataframe, column, kd=True, plot_title='', fig_size=(10,5), font_size=10):
        '''
        This method plots a histogram of the given data
        
        Parameters:
            dataframe: The required dataframe for the plot.
            column: The column of the dataframe to plot
            kd: whether to include a kernel density estimate in the plot.
            plot_title:Ttitle for the plot.
            fig_size: The figure size given as a tuple.
            font_size: The font size.

        Returns:
            None
        
        '''
        fig, ax = plt.subplots(1,1,figsize=fig_size)
        h = sns.histplot(dataframe[column],label="Skewness: %.2f"%(dataframe[column].skew()), kde=kd, ax=ax)
        h.set_title(plot_title, fontsize=font_size)
        h.legend(fontsize=font_size)
        plt.show()
    
    def plot_box(self, dataframe, column, orientation='h', fill=True, plot_title='', fig_size=(10,5), font_size=10):
        '''This method plots a boxplot of the given data.
        
        Parameters:
            dataframe: The required dataframe for the plot.
            column: The column(s) of the dataframe to plot.
            orientation: Plot horizontal or vertical plots.
            fill. Filled boxes or not.
            plot_title:Ttitle for the plot.
            fig_size: The figure size given as a tuple.
            font_size: The font size.


        Returns:
            None
        
        '''

        fig, ax = plt.subplots(1,1,figsize=fig_size)
        h = sns.boxplot(dataframe[column], orient=orientation, fill=fill, ax=ax) #type: ignore
        h.set_title(plot_title, fontsize=font_size)
        plt.show()

    def qq_plot(self, dataframe, scale=1, fig_size=(10,5), plot_title='', font_size=10):
        ''' This method plots a qq plo
        
        Parameters:
            dataframe: The required dataframe for the plot.
            scale: scale of the plot
            fig_size: The figure size given as a tuple.
            plot_title:Ttitle for the plot.
            font_size: The font size.

        Returns:
            None
        
        '''
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
    

    def plot_line2d(self, x, y, label='', marker='', color='green', fig_size=(6.4, 4.8),
                    xlabel='', ylabel='', title='', legend=False, grid=False, annotate=False, xy_text=(0,0)):
        
        '''This method plots a 2d line plot'''
        plt.figure(figsize=fig_size)
        plt.plot(x, y, label=label, marker=marker, color=color)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(title)
        if legend:
            plt.legend()
        plt.grid(grid)

        if annotate:
            for x,y in zip(x, y):
                label = "{:.2f}".format(y)
                plt.annotate(label,
                             (x, y),
                             textcoords="offset points",
                             xytext=xy_text,
                             ha='center') #type: ignore
        plt.show()


    def plot_bar_chart(self, x, y, width=0.8, color='green', title='', ylabel='', fig_size=(6.4, 4.8),
                       annotate=False, xy_text=(0,0)): #type: ignore
        '''This method plots a bar chart'''

        plt.figure(figsize=fig_size)
        xs = x
        ys = y
        plt.bar(xs, height=ys, width=width, color=color)
        plt.title(title)
        plt.ylabel(ylabel)

        #annotation
        if annotate:
            for x,y in zip(xs,ys):
                label = "{:.2f}".format(y)
                plt.annotate(label, 
                             (x,y), #type: ignore
                             textcoords = "offset points",
                             xytext = xy_text,
                             ha='center')

        plt.show()

    def plot_risk_comparison(self, data_1, data_2, y_1, y_2, plot_title='', title_1='', title_2='', title_3_cat = 'category',
                              ylabel_1='', ylabel_2='', order_ascending=False, stat='percent', fmt='%.2f',fig_size=(15,10), padding=3.0):
        '''This method plots to hprizontal bar charts, one below the other, for making comparisons'''

        sns.set_style("darkgrid")
        fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=fig_size)
        fig.suptitle(plot_title)
        fig.tight_layout(pad=padding)

        #plot 1
        sns.countplot(data=data_1, y = y_1, stat=stat, order=data_1[y_1].value_counts(ascending=order_ascending).index, ax=ax1)#type: ignore
        ax1.set_title(title_1)
        ax1.bar_label(ax1.containers[0], fmt=fmt, label_type='edge')#type: ignore
        ax1.set_ylabel(ylabel_1)

        #plot 2
        sns.countplot(data=data_2, y = y_2, stat=stat, order=data_2[y_2].value_counts(ascending=order_ascending).index, #type: ignore
                          color='orange', ax=ax2)
        ax2.set_title(title_2)
        ax2.bar_label(ax2.containers[0], fmt=fmt, label_type='edge') #type: ignore
        ax2.set_ylabel(ylabel_2)

        #plot 3
        #get percentage of category defaults
        # categories = data_1[y_1].unique()
        # percentages = {}

        # for name in categories:
        #     a = len(data_1[data_1[y_1]==name])
        #     b = len(data_2[data_2[y_2]==name])
        #     percent = (b/a) * 100
        #     percentages[name] = percent

        # descending = dict(Counter(percentages).most_common())
        
        # # for key, value in sorted(percentages.items(), key=lambda x: x[1]):
        # #             sorted_dict[key] = value

        # # percentages = dict(reversed(list(sorted_dict.items())))
    
        # sns.barplot(y=list(descending.keys()), x=list(descending.values()), orient = 'h', color= 'red',
        #               ax=ax3)
        a = data_2[y_2].value_counts()
        b = data_1[y_1].value_counts()


        percent = (a/b)*100
        percent = percent.sort_values(ascending = False)

        sns.barplot(y=percent.index, x=percent, orient = 'h', order=percent.index, color= 'red')
        ax3.set_title(f'Percentage of defaulted loans in each {title_3_cat} of {ylabel_2}' )
        ax3.bar_label(ax3.containers[0], fmt=fmt, label_type='edge') #type: ignore
        ax3.set_xlabel('percent')
        ax3.set_ylabel(ylabel_2)

        plt.show()

    def plot_charged_default_comparison(self, data_1, data_2, column, orientation='v', plot_title='', title_1='', title_2='',
                                        label_1='', label_2='', fmt='%.2f', fig_size=(10,5), padding=3.0):
        '''This method compares the distribtion of value counts as percentages of two dataframe columns'''

        if orientation == 'v':

            fig, axes = plt.subplots(1,2, figsize = fig_size)
            fig.suptitle(plot_title)
            fig.tight_layout(pad=padding)

            #plot 1
            sns.countplot(data_1, x=column, stat='percent',
                        order=data_1[column].value_counts(ascending=False).index,ax=axes[0])
            axes[0].set_title(title_1)
            axes[0].set_xlabel(label_1)
            axes[0].set_ylabel(label_2)
            axes[0].bar_label(axes[0].containers[0], fmt=fmt, label_type='edge') #type: ignore

            #plot 2
            sns.countplot(data_2, x=column, stat='percent',
                        order=data_2[column].value_counts(ascending=False).index ,ax=axes[1])
            axes[1].set_title(title_2)
            axes[1].set_xlabel(label_1)
            axes[1].set_ylabel(label_2)
            axes[1].bar_label(axes[1].containers[0], fmt=fmt, label_type='edge') #type: ignore
        
        elif orientation == 'h':

            fig, axes = plt.subplots(2,1, figsize = fig_size)
            fig.suptitle(plot_title)
            fig.tight_layout(pad=padding)

            #plot 1
            sns.countplot(data_1, y=column, stat='percent',
                        order=data_1[column].value_counts(ascending=False).index,ax=axes[0])
            axes[0].set_title(title_1)
            axes[0].set_xlabel(label_1)
            axes[0].set_ylabel(label_2)
            axes[0].bar_label(axes[0].containers[0], fmt=fmt, label_type='edge') #type: ignore

            #plot 2
            sns.countplot(data_2, y=column, stat='percent',
                        order=data_2[column].value_counts(ascending=False).index ,ax=axes[1])
            axes[1].set_title(title_2)
            axes[1].set_xlabel(label_1)
            axes[1].set_ylabel(label_2)
            axes[1].bar_label(axes[1].containers[0], fmt=fmt, label_type='edge') #type: igno

        plt.show()






# fig, axes = plt.subplots(2,1, figsize=(15,10))
# plt.title('Purpose (All loans)')
# t=sns.countplot(data=df, y ='purpose', stat='percent', order=df['purpose'].value_counts(ascending=False).index, ax=axes[0])
# t.set_title('Purpose (all loans)')
# t.bar_label(t.containers[0], fmt='%.2f', label_type='edge')

# g = sns.countplot(data=defaulted_subset, y ='purpose', stat='percent', color='orange', order=df['purpose'].value_counts(ascending=False).index,ax=axes[1])

# g.set_title('Purpose (Defaulted loans)')
# for label in g.containers:
#     g.bar_label(label, fmt='%.2f', label_type='edge')
# plt.show()
