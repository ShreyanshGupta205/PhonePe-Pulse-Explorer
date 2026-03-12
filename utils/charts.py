import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# PhonePe brand colors approximation
PRIMARY_COLOR = "#5f259f" 
SECONDARY_COLOR = "#e1ecf0"
ACCENT_COLOR = "#00d09c"
TEXT_COLOR = "#333333"

def apply_fintech_theme(fig):
    fig.update_layout(
        font_family="Inter, sans-serif",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title_font_color=PRIMARY_COLOR,
        title_font_size=18,
        title_text='',  # Explicitly clear string
        margin=dict(l=40, r=40, t=40, b=40), # Reduced top margin since no titles
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Inter, sans-serif",
            bordercolor="#e0e0e0"
        )
    )
    fig.update_xaxes(showgrid=False, linecolor="#e0e0e0", gridcolor="#f0f0f0")
    fig.update_yaxes(showgrid=True, linecolor="#e0e0e0", gridcolor="#f0f0f0")
    return fig

def create_line_chart(df, x_col, y_col, title, color_col=None):
    if color_col:
        fig = px.line(df, x=x_col, y=y_col, color=color_col)
    else:
        fig = px.line(df, x=x_col, y=y_col)
        fig.update_traces(line_color=PRIMARY_COLOR)
        
    fig.update_traces(line_width=3, mode='lines+markers')
    return apply_fintech_theme(fig)

def create_bar_chart(df, x_col, y_col, title, orientation='v', color_col=None):
    if orientation == 'h':
        df = df.sort_values(by=x_col, ascending=True)
    
    if color_col:
        fig = px.bar(df, x=x_col, y=y_col, color=color_col, orientation=orientation, text_auto='.2s')
    else:
        fig = px.bar(df, x=x_col, y=y_col, orientation=orientation, text_auto='.2s')
        fig.update_traces(marker_color=PRIMARY_COLOR, textposition='outside')
    return apply_fintech_theme(fig)

def create_pie_chart(df, names_col, values_col, title):
    fig = px.pie(df, names=names_col, values=values_col, hole=0.5,
                 color_discrete_sequence=["#5f259f", "#00d09c", "#ff9f43", "#ff6b6b", "#48dbfb"])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig = apply_fintech_theme(fig)
    fig.update_layout(showlegend=False)
    return fig

def create_india_choropleth(df_in, state_col, value_col, title):
    """
    Creates a high-quality bubble map over India since custom geojson for states
    can sometimes be tricky without an external file.
    """
    df = df_in.copy()
    # Rough coordinates for Indian states to plot bubbles
    state_coords = {
        "Andaman & Nicobar Islands": (11.7401, 92.6586),
        "Andhra Pradesh": (15.9129, 79.7400),
        "Arunachal Pradesh": (28.2180, 94.7278),
        "Assam": (26.2006, 92.9376),
        "Bihar": (25.0961, 85.3131),
        "Chandigarh": (30.7333, 76.7794),
        "Chhattisgarh": (21.2787, 81.8661),
        "Dadra and Nagar Haveli and Daman and Diu": (20.1809, 73.0169),
        "Delhi": (28.7041, 77.1025),
        "Goa": (15.2993, 74.1240),
        "Gujarat": (22.2587, 71.1924),
        "Haryana": (29.0588, 76.0856),
        "Himachal Pradesh": (31.1048, 77.1734),
        "Jammu & Kashmir": (33.7782, 76.5762),
        "Jharkhand": (23.6102, 85.2799),
        "Karnataka": (15.3173, 75.7139),
        "Kerala": (10.8505, 76.2711),
        "Ladakh": (34.1526, 77.5771),
        "Lakshadweep": (10.5667, 72.6417),
        "Madhya Pradesh": (22.9734, 78.6569),
        "Maharashtra": (19.7515, 75.7139),
        "Manipur": (24.6637, 93.9063),
        "Meghalaya": (25.4670, 91.3662),
        "Mizoram": (23.1645, 92.9376),
        "Nagaland": (26.1584, 94.5624),
        "Odisha": (20.9517, 85.0985),
        "Puducherry": (11.9416, 79.8083),
        "Punjab": (31.1471, 75.3412),
        "Rajasthan": (27.0238, 74.2179),
        "Sikkim": (27.5330, 88.5122),
        "Tamil Nadu": (11.1271, 78.6569),
        "Telangana": (18.1124, 79.0193),
        "Tripura": (23.9408, 91.9882),
        "Uttar Pradesh": (26.8467, 80.9462),
        "Uttarakhand": (30.0668, 79.0193),
        "West Bengal": (22.9868, 87.8550)
    }
    
    # Map coordinates onto dataframe
    df['lat'] = df[state_col].map(lambda x: state_coords.get(x, (0,0))[0])
    df['lon'] = df[state_col].map(lambda x: state_coords.get(x, (0,0))[1])
    
    df = df[df['lat'] != 0] # remove unbound
    
    fig = px.scatter_geo(
        df,
        lat='lat',
        lon='lon',
        color=value_col,
        size=value_col,
        hover_name=state_col,
        title=title,
        color_continuous_scale=[SECONDARY_COLOR, PRIMARY_COLOR]
    )
    
    fig.update_geos(
        fitbounds="locations",
        visible=False, # Hide the base map, we just want boundaries
        showcountries=True,
        countrycolor="LightGrey",
        resolution=50,
        scope="asia" 
    )
    fig.update_layout(
        geo=dict(
            center=dict(lat=22, lon=82),    # India center
            projection_scale=3              # Zoom level
        )
    )
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    return apply_fintech_theme(fig)
