import yaml
import pandas as pd
import plotly.graph_objs as go
import yaml
import os
import plotly.express as px

# Load or create default settings
def load_settings(config_filepath):
    try:
        with open(config_filepath, 'r') as file:
            settings = yaml.safe_load(file)
    except FileNotFoundError:
        # Default settings
        settings = {
            'income_color': '#1f77b4',  # blue
            'spending_color': '#d62728',  # red
            'plot_height': 300
        }
    return settings

def save_settings(settings):
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(settings, file)



def get_main_category(x):
    if isinstance(x, str):
        return x.split('/')[0]
    else:
        return 'unknown'  # or np.nan if you prefer
    

def plot_income_spending(monthly_balance_df, net_balance_df, settings):
    # Copy and ensure 'month' is a string
    df = monthly_balance_df.copy()
    df['month'] = df['month'].astype(str)

    #calculate net balance:
    # Separate income and spending
    income_df = df[df['is_income_category'] == 1]
    spending_df = df[df['is_income_category'] == 0]
    
    # Create figure
    fig = go.Figure()

    # Add income trace
    fig.add_trace(go.Bar(
        x=income_df['month'],
        y=income_df['amount'],
        name='income',
        marker = dict(color=settings['income_color']),
    ))

    # Add spending trace
    fig.add_trace(go.Bar(
        x=spending_df['month'],
        y=spending_df['amount'],
        name='spending',
        marker=dict(color=settings['spending_color']),
    ))

    # fig.add_trace(go.Bar(
    #     x=spending_df['month'],
    #     y=spending_df['amount'],
    #     name='spending',
    #     marker=dict(color=settings['spending_color']),
    # ))
    fig.update_layout(
        barmode = 'stack',
        
    )
    if settings['show_net_balance']:
        fig.add_trace(go.Scatter(
            x=net_balance_df['month'].astype(str),
            y=net_balance_df['amount'],
            line=dict(color=settings['net_balance_color']),
            name='net balance',
        ))

    # Layout customization
    months = monthly_balance_df['month'].astype(str).unique().tolist()
    fig.update_layout(
        width=settings['width'],
        height=settings['height'],
        bargap=settings['bargap'],
        barmode = 'overlay',
        template = settings['template'],
        xaxis=dict(
                    # tickmode='linear',  # force linear ticks
                    tickmode = 'array',
                    tickvals=months,
                    tickangle=-60,            # show every tick
                )
    )

    return fig

def make_directories(paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)


def plot_monthly_spend_percentage(df, 
                                  settings,
                                  date_col='month', 
                                  category_col='main_tag', 
                                  spend_col='amount'):
    """
    Plots a stacked bar chart showing percentage of total spend per category by month.

    Parameters:
    - df: pandas DataFrame with the data
    - date_col: name of the column containing dates (default 'date')
    - category_col: name of the column containing category names (default 'category')
    - spend_col: name of the column containing spend amounts (default 'spend')
    """
    df['month'] = df[date_col].astype(str)

    # Get unique categories and months
    categories = df[category_col].unique()
    mean_category_percentage_df = df.groupby([category_col], as_index = False)['percent'].mean()
    sorted_categories = mean_category_percentage_df.sort_values('percent', ascending = False)[category_col].values
    months = df['month'].unique()

    # Build the color map: user-supplied colors override defaults
    # Get default colors from plotly express palette
    default_colors = px.colors.qualitative.Plotly
    if len(sorted_categories) > len(default_colors):
        default_colors = default_colors * (len(sorted_categories) // len(default_colors) + 1)
    
    # Build color map: use user colors if exist, else default colors
    color_map = {}
    for i, cat in enumerate(sorted_categories):
        color_map[cat] = settings.get(cat, default_colors[i])

    # Prepare the data for the stacked bar plot
    data = []
    for category in sorted_categories:
        cat_data = df[df[category_col] == category]
        percents = []
        for month in months:
            val = cat_data[cat_data['month'] == month]['percent']
            percents.append(val.values[0] if not val.empty else 0)
        data.append(go.Bar(name=category, 
                           x=months, 
                           y=percents,
                           marker_color=color_map[category]))

    # Create figure
    fig = go.Figure(data=data)

    # Update layout for stacked bar chart
    fig.update_layout(
        barmode='stack',
        title='Percentage Spend by Category per Month',
        xaxis_title='Month',
        yaxis_title='Percentage of Total Spend (%)',
        yaxis=dict(range=[0, 100]),
        height=settings['height'],
        bargap=settings['bargap'],
        template=settings['template']
    )

    return fig