import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import plotly.express as px
import pandas as pd

# marker_color='rgb(55, 83, 109)'
# marker_color='rgb(26, 118, 255)'

# template: ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]


def AddQpsLatencyTrace(fig, df, barName, lineName):
    XAxis = df['Threads']

    # Draw Bar
    fig.add_trace(go.Bar(
        x=XAxis,
        y=df['millicore'],
        name=barName,
    ),
        secondary_y=False,
    )

    # Draw Line
    fig.add_trace(go.Scatter(
        x=XAxis,
        y=df['AvgLatency'],
        mode='lines+markers',
        name=lineName,
        marker=dict(size=10),
    ),
        secondary_y=True,
    )

    # fig.add_trace(go.Scatter(
    #     x=XAxis,
    #     y=df['PctLatency'],
    #     mode='lines+markers',
    #     name='PctLatency',
    # ),
    #     secondary_y=True,
    # )


def Draw(figureTitle, configs):
    # Create figure with secondary y-axis
    filename = configs["filename"]
    data = pd.read_csv(filename, index_col=0)

    df_transposed = data.T
    df_melted = df_transposed.reset_index().melt(id_vars='index', var_name='TestBench', value_name='Value')
    # Create the bar chart using plotly.express
    fig = px.histogram(df_melted,
                       x='index',  # 'index' now holds 'cpu' or 'memory'
                       y='Value',
                       color='TestBench',  # Color by the directory name
                       barmode='group',
                       title='Comparison of CPU and Memory Usage',
                       labels={'index': 'Resource'})
    fig.update_layout(bargap=0.5,  # Gap between bars of the same group
                      bargroupgap=0.00)  # Gap between bars of different groups

    # Set x-axis title
    fig.update_xaxes(title_text="<b>Resource</b>")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>CPU-USAGE(milli-cores)<br>MEM-USAGE(MB)</b>", secondary_y=False)

    # Set figure title
    fig.update_layout(
        template="plotly_white",
        title={
            'text': figureTitle,
            'x': 0.5,
            'font': dict(
                family="Arial",  # figure title font
                size=24,  # figure title size
                color="#000000"  # figure title color
            )
        })
    # display
    fig.show()