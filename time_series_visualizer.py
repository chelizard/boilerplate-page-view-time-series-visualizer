import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True, index_col='date')

# # Note: this doesn't work with the stupid test cases
# df = df[df['value'] > df['value'].quantile(0.025)]
# df = df[df['value'] < df['value'].quantile(0.975)]

# Clean data – filter out days with page view in the top or bottom 2.5% of the dataset
lower_bound = df['value'].quantile(0.025).round(2)
upper_bound = df['value'].quantile(0.975).round(2)
df = df[df['value'] > lower_bound]
df = df[df['value'] < upper_bound]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(10, 5)) # Create a figure and an axes.

    # Plot the data
    ax.plot(df.index, df['value'], color='red')

    # Set the labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    # Order the months
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 
        'August', 'September', 'October', 'November', 'December'
        ]
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)
    df_bar = df_bar.sort_values(['year', 'month'])

    df_bar = df_bar.groupby(['year', 'month'])['value'].mean()
    df_bar = df_bar.unstack()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 5))
    df_bar.plot(kind='bar', ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Page Views per Year per Month')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    sns.boxplot(x='year', y='value', data=df_box, ax=ax1,
                flierprops={'marker': 'o', 'markersize': 1},
                palette=sns.color_palette(palette='magma', n_colors=len(df_box['year'].unique())))
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_title('Year-wise Box Plot (Trend)')

    sns.boxplot(x='month', y='value', data=df_box, ax=ax2,
                flierprops={'marker': 'o', 'markersize': 1}, 
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                palette=sns.color_palette(palette='hls', n_colors=12))
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    plt.tight_layout()
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
