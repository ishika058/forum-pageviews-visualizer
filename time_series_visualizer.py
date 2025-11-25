import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Import data
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Clean data: remove top 2.5% and bottom 2.5%
lower_quantile = df['value'].quantile(0.025)
upper_quantile = df['value'].quantile(0.975)
df = df[(df['value'] >= lower_quantile) & (df['value'] <= upper_quantile)]


def draw_line_plot():
    
    data = df.copy()
    
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(data.index, data['value'], color='red')
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    # Save figure
    fig.savefig('line_plot.png')
    return fig



    
def draw_bar_plot():
    
    data = df.copy()
    
    # Make sure the index is a DatetimeIndex
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)
    
    # Prepare data for bar plot
    data['year'] = data.index.year
    data['month'] = data.index.month
    monthly_avg = data.groupby(['year','month'])['value'].mean().unstack()
    
    # Draw bar plot
    fig = monthly_avg.plot(kind='bar', figsize=(12,8)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title='Months', labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    
    # Save figure
    fig.savefig('bar_plot.png')
    return fig



def draw_box_plot():
    
    data = df.copy()
    data.reset_index(inplace=True)
    
    # Ensure 'date' column is datetime
    data['date'] = pd.to_datetime(data['date'])
    
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.strftime('%b')
    data['month_num'] = data['date'].dt.month
    
    # Sort months for proper order
    data = data.sort_values('month_num')
    
    # Draw box plots
    fig, axes = plt.subplots(1, 2, figsize=(20,8))
    
    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=data, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=data, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    
    # Save figure
    fig.savefig('box_plot.png')
    return fig





