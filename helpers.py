import geopandas as gpd
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from config import app_config


def avg_price_map_fig(selected_region, selected_year):
    # load csv
    csv_file_path = f'processed_data/average_price_by_year/region_data_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # filter data to selected region
    data = data[data['region'] == selected_region]

    # load geojson for selected region
    region_geojson_path = f'GeoJSON/regions/{selected_region}_postcode_sectors.geojson'
    region_geojson = gpd.read_file(region_geojson_path)

    # fetch the center and zoom for selected region
    region_config = app_config['regions'][selected_region]

    # define percentiles for key
    key_min = np.percentile(data.avg_price, 5)
    key_max = np.percentile(data.avg_price, 95)

    # create the figure
    fig = px.choropleth_mapbox(
        data,
        geojson=region_geojson,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='avg_price',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'avg_price': 'Average Price £'},
        title=f'Average price by postcode sector for {selected_region} in {selected_year}',
        hover_data = {'volume': True},
        range_color= [key_min, key_max],
    )

    fig.update_layout(
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Legend Title'), orientation='h', x=1, y=1.02),
    )

    return fig

def avg_price_bar_fig(selected_region, selected_year):
    # load data from csv
    csv_file_path = 'processed_data/region_avg_price/region_avg_prices.csv'
    data = pd.read_csv(csv_file_path)

    # filter data for selected region
    data = data[data['region'] == selected_region]

    # aggregate volume by year
    aggregated_data = data.groupby('year')['volume'].sum().reset_index()

    # Create stacked bar plot
    fig = px.bar(
        data,
        x = 'year',
        y = 'avg_price',
        color = 'property_type',
        title= f'Average price and sales volume for {selected_region} in {selected_year}',
        barmode='stack'
    )

    # add a line plot for the aggregated volume
    fig.add_trace(
        go.Scatter(x=aggregated_data['year'], y=aggregated_data['volume'], name='Volume', yaxis='y2', mode='lines+markers')
    )

    # Update legend names
    legend_names = {'D': 'Detached', 'S': 'Semi-Detached', 'T': 'Terraced', 'F': 'Flat'}
    fig.for_each_trace(lambda t: t.update(name=legend_names.get(t.name, t.name)))

    # update layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Average Price £',
        yaxis2 = dict(title='Volume', overlaying='y', showgrid=False, side='right'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Property Type'), orientation='h', yanchor='bottom', y = 1.02, xanchor='right', x=1),
    )



    return fig

def delta_box_plot_figure(selected_region, selected_year):
    start_year = int(selected_year) - 2
    end_year = int(selected_year) + 1

    # create empty list to store year data
    all_data = []

    for year in range(start_year, end_year):
        # load csv for current year
        csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{year}.csv'
        year_data = pd.read_csv(csv_file_path)

        # append data to list
        all_data.append(year_data)

    # concat all data
    data = pd.concat(all_data, ignore_index=True)

    # filter for selected region
    data = data[data['region'] == selected_region]

    # set y min and max values
    y_min = np.percentile(data.delta, 1)
    y_max = np.percentile(data.delta, 99)

    # create figure
    fig = px.box(
        data,
        x='year',
        y='delta',
        title=f'Year-on-year sector average price change for {selected_region} between {start_year} and {selected_year}',
        labels={'delta': 'Price Change %'},
        color='year',
        range_y=[y_min, y_max],
    )

        # Update layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Price Change %',
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def delta_map_figure(selected_region, selected_year):
    # load the csv
    csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # filter for selected region
    data = data[data['region'] == selected_region]

    # load relevant geojson
    region_geojson_path = f'GeoJSON/regions/{selected_region}_postcode_sectors.geojson'
    region_geojson = gpd.read_file(region_geojson_path)

    # fetch config for selected region
    region_config = app_config['regions'][selected_region]

    # define key min and max
    key_min = np.percentile(data.delta, 5)
    key_max = np.percentile(data.delta, 95)

    # create figure
    fig = px.choropleth_mapbox(
        data,
        geojson=region_geojson,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='delta',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'delta': 'Price Chanhe %'},
        title=f'Year-on-year price change for {selected_region} in {selected_year}',
        range_color=[key_min,key_max],
    )

    # Update layout attributes
    fig.update_layout(
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def fastest_growing_map_figure(selected_region, selected_year, slider_value):
    # load the csv
    csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # filter for selected region
    data = data[data['region'] == selected_region]

    # sort by delta in decending order
    data = data.sort_values('delta', ascending=False)

    # select top X rows
    top_x_data = data.head(slider_value)

    # fetch region config
    region_config = app_config['regions'][selected_region]

    # load relevant geojson
    region_geojson_path = f'GeoJSON/regions/{selected_region}_postcode_sectors.geojson'
    region_geojson = gpd.read_file(region_geojson_path)

    # create figure
    fig = px.choropleth_mapbox(
        top_x_data,
        geojson=region_geojson,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='delta',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'delta': 'Price Change %'},
        title=f'Top {slider_value} fastest growing sectors in {selected_region} in {selected_year}',
    )

    fig.update_layout(
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white',
    )

    return fig

def fastest_declining_map_figure(selected_region, selected_year, slider_value):
    # load the csv
    csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # filter for selected region
    data = data[data['region'] == selected_region]

    # sort by delta in decending order
    data = data.sort_values('delta', ascending=False)

    # select top X rows
    top_x_data = data.tail(slider_value)

    # fetch region config
    region_config = app_config['regions'][selected_region]

    # load relevant geojson
    region_geojson_path = f'GeoJSON/regions/{selected_region}_postcode_sectors.geojson'
    region_geojson = gpd.read_file(region_geojson_path)

    # create figure
    fig = px.choropleth_mapbox(
        top_x_data,
        geojson=region_geojson,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='delta',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'delta': 'Price Change %'},
        title=f'Top {slider_value} fastest declining sectors in {selected_region} in {selected_year}',
    )

    fig.update_layout(
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white',
    )

    return fig


