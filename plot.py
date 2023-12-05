import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Assuming df is your DataFrame with CSV data

def plot_monitor_synthesis_time(df):
    fig = px.line(
        data_frame=df.groupby(['model_size']).mean().reset_index(), 
        x="model_size", 
        y="monitor_synthesis_time [sec]",
        title="Monitor synthesis time"
    )
    # Update layout with improved settings
    fig.update_layout(
        xaxis_title="Model size [number of states/transitions/labels]",
        yaxis_title="Time [seconds]",
        title="Monitor Synthesis Time",
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="right", x=1.25),  # Legend on the right
        template="plotly_white",  # Use a white background template
        font=dict(size=18)
    )
    fig.write_image('./experiments/monitor_synthesis_time.png')

def plot_monitor_time_per_trace(df):
    fig = go.Figure()

    # Simplifying the loop using Plotly Express
    for c in df['trace_length'].unique():

        if c % 100 != 0:
            continue
        
        # Filter DataFrame for the current trace_length
        df_model = df[df['trace_length'] == c]
        
        # Plotting Prism data
        fig.add_trace(go.Scatter(
            x=df_model['model_size'],
            y=df_model['monitor_time_prism [sec]'],
            mode='lines',
            name=f'{c} prism',
            line=dict(color=f'rgb({int(c*255/500)}, 0, 0)'),
        ))
    for c in df['trace_length'].unique():

        if c % 100 != 0:
            continue
        
        # Filter DataFrame for the current trace_length
        df_model = df[df['trace_length'] == c]    
        # Plotting Storm data
        fig.add_trace(go.Scatter(
            x=df_model['model_size'],
            y=df_model['monitor_time_storm [sec]'],
            mode='lines',
            name=f'{c} storm',
            line=dict(color=f'rgb(0, 0, {int(c*255/500)})'),
        ))

    # Update layout with improved settings
    fig.update_layout(
        xaxis_title="Model size [number of states/transitions/labels]",
        yaxis_title="Time [seconds]",
        title="Monitor Execution Time (per event)",
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="right", x=1.25),  # Legend on the right
        template="plotly_white",  # Use a white background template
        font=dict(size=18)
    )

    # Save plot to file
    fig.write_image('./experiments/monitor_execution_time_per_trace_all.png')

def plot_monitor_time_per_event_per_trace(df):
    fig = go.Figure()

    # Simplifying the loop using Plotly Express
    for c in df['trace_length'].unique():

        if c % 100 != 0:
            continue
        
        # Filter DataFrame for the current trace_length
        df_model = df[df['trace_length'] == c]
        
        # Plotting Prism data
        fig.add_trace(go.Scatter(
            x=df_model['model_size'],
            y=df_model['monitor_time_per_event_prism [sec]'],
            mode='lines',
            name=f'{c} prism',
            line=dict(color=f'rgb({int(c*255/500)}, 0, 0)'),
        ))
    # Simplifying the loop using Plotly Express
    for c in df['trace_length'].unique():

        if c % 100 != 0:
            continue    

        # Filter DataFrame for the current trace_length
        df_model = df[df['trace_length'] == c]
        # Plotting Storm data
        fig.add_trace(go.Scatter(
            x=df_model['model_size'],
            y=df_model['monitor_time_per_event_storm [sec]'],
            mode='lines',
            name=f'{c} storm',
            line=dict(color=f'rgb(0, 0, {int(c*255/500)})'),
        ))

    # Update layout with improved settings
    fig.update_layout(
        xaxis_title="Model size [number of states/transitions/labels]",
        yaxis_title="Time [seconds]",
        title="Monitor Execution Time (per event)",
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="right", x=1.25),  # Legend on the right
        template="plotly_white",  # Use a white background template
        font=dict(size=18)
    )

    # Save plot to file
    fig.write_image('./experiments/monitor_execution_time_per_trace_per_event_all.png')

def plot_monitor_execution_time(df):
    fig = go.Figure()

    # Simplifying the loop using Plotly Express
    for c in df['model_size'].unique():
        if c % 500 != 0:
            continue
        
        # Filter DataFrame for the current model_size
        df_model = df[df['model_size'] == c]
        
        # Plotting Prism data
        fig.add_trace(go.Scatter(
            x=df_model['trace_length'],
            y=df_model['monitor_time_prism [sec]'],
            mode='lines',
            name=f'{c} prism',
            line=dict(color=f'rgb({int(c*255/3000)}, 0, 0)'),
        ))
    # Simplifying the loop using Plotly Express
    for c in df['model_size'].unique():
        if c % 500 != 0:
            continue    

        # Filter DataFrame for the current model_size
        df_model = df[df['model_size'] == c]

        # Plotting Storm data
        fig.add_trace(go.Scatter(
            x=df_model['trace_length'],
            y=df_model['monitor_time_storm [sec]'],
            mode='lines',
            name=f'{c} storm',
            line=dict(color=f'rgb(0, 0, {int(c*255/3000)})'),
        ))

    # Update layout with improved settings
    fig.update_layout(
        xaxis_title="Trace length [number of events]",
        yaxis_title="Time [seconds]",
        title="Monitor Execution Time",
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="right", x=1.25),  # Legend on the right
        template="plotly_white",  # Use a white background template
        font=dict(size=18)
    )

    # Save plot to file
    fig.write_image('./experiments/monitor_execution_time_all.png')

def plot_monitor_execution_time_per_event(df):
    fig = go.Figure()

    # Simplifying the loop using Plotly Express
    for c in df['model_size'].unique():
        if c % 500 != 0:
            continue
        
        # Filter DataFrame for the current model_size
        df_model = df[df['model_size'] == c]
        
        # Plotting Prism data
        fig.add_trace(go.Scatter(
            x=df_model['trace_length'],
            y=df_model['monitor_time_per_event_prism [sec]'],
            mode='lines',
            name=f'{c} prism',
            line=dict(color=f'rgb({int(c*255/3000)}, 0, 0)'),
        ))
    # Simplifying the loop using Plotly Express
    for c in df['model_size'].unique():
        if c % 500 != 0:
            continue    

        # Filter DataFrame for the current model_size
        df_model = df[df['model_size'] == c]

        # Plotting Storm data
        fig.add_trace(go.Scatter(
            x=df_model['trace_length'],
            y=df_model['monitor_time_per_event_storm [sec]'],
            mode='lines',
            name=f'{c} storm',
            line=dict(color=f'rgb(0, 0, {int(c*255/3000)})'),
        ))

    # Update layout with improved settings
    fig.update_layout(
        xaxis_title="Trace length [number of events]",
        yaxis_title="Time [seconds]",
        title="Monitor Execution Time (per event)",
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="right", x=1.25),  # Legend on the right
        template="plotly_white",  # Use a white background template
        font=dict(size=18)
    )

    # Save plot to file
    fig.write_image('./experiments/monitor_execution_time_per_event_all.png')
