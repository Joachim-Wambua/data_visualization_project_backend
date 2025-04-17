from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/interactive-emissions", response_class=HTMLResponse)
def interactive_emissions_chart():
    df = pd.read_csv("data/countries_emissions.csv")
    top = df.sort_values("emissions", ascending=False).head(10)

    fig = px.bar(
        top,
        x="name",
        y="emissions",
        title="Top 10 Emitting Countries (2023)",
        labels={
            "name": "Country",
            "emissions": "Emissions (Million Tonnes)"
        },
        text="emissions"
    )

    # Format layout and labels
    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    fig.update_layout(
        yaxis_tickformat=",",  # Format large numbers with commas
        xaxis_tickangle=-45,   # Rotate x-axis labels
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(t=60, l=40, r=20, b=100)
    )

    return fig.to_html(include_plotlyjs="cdn")

@app.get("/api/emissions-map", response_class=HTMLResponse)
def emissions_choropleth():
    import pandas as pd
    import plotly.express as px

    # Load your emissions data
    df = pd.read_csv("data/countries_emissions.csv")

    # Define a custom monotone turquoise scale based on #009b9d
    custom_scale = [
        [0, "#e0fafa"],     # Lightest shade
        [0.25, "#66d1d3"],
        [0.5, "#33b8ba"],
        [0.75, "#00a0a1"],
        [1, "#009b9d"]      # Strongest shade
    ]

    # Create a choropleth map with the custom scale
    fig = px.choropleth(
        df,
        locations="name",
        locationmode="country names",
        color="emissions",
        hover_name="name",
        color_continuous_scale=custom_scale,
        title="Global Emissions by Country (2023)",
        labels={"emissions": "Emissions (Mt)"}
    )

    # Map styling
    fig.update_geos(
        showframe=False,
        showcoastlines=False,
        showcountries=True,
        countrycolor="#ffffff",
        projection_type="natural earth"
    )

    # Legend and layout
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        geo_bgcolor="white",
        coloraxis_colorbar=dict(
            title="Emissions (Mt)",
            tickprefix="",
            ticks="outside",
            len=0.75,
            thickness=10,
            tickfont=dict(color="#333", size=12),
        )
    )

    return fig.to_html(include_plotlyjs="cdn")

@app.get("/api/steel-bar-chart", response_class=HTMLResponse)
def steel_bar_chart():
    df = pd.read_csv("data/steelwatch_top_companies_2023.csv")

    fig = px.bar(
        df.sort_values("Production_Mt", ascending=True),
        x="Production_Mt",
        y="Company",
        title="Top Steel Producing Companies (2023)",
        labels={"Production_Mt": "Production (Mt)", "Company": "Company"},
        orientation="h",
        color_discrete_sequence=["#009b9d"]
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig.to_html(include_plotlyjs="cdn")

@app.get("/api/steel-map-chart", response_class=HTMLResponse)
def steel_map_chart():
    df = pd.read_csv("data/steelwatch_top_companies_2023.csv")

    fig = px.scatter_geo(
        df,
        locations="Country",
        locationmode="country names",
        hover_name="Company",
        hover_data={"Country": True, "Production_Mt": True},
        size="Production_Mt",             # Use actual production to scale
        size_max=60,                      # Increased for better visibility
        projection="natural earth",
        title="Steel Company Locations & Production (2023)"
    )

    # Set a consistent color
    fig.update_traces(marker=dict(color="#009b9d"))

    # Update layout for clean map visuals
    fig.update_geos(showframe=False, showcoastlines=True)
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Production (Mt)",
            ticks="outside"
        )
    )

    return fig.to_html(include_plotlyjs="cdn")


@app.get("/api/steel-companies-table", response_class=HTMLResponse)
def steel_companies_table():
    df = pd.read_csv("data/steelwatch_top_companies_2023.csv")

    fig = go.Figure(
        data=[go.Table(
            header=dict(
                values=["<b>Company</b>", "<b>Country</b>", "<b>Production (Mt)</b>"],
                fill_color="#009b9d",
                font=dict(color="white", size=14),
                align="left"
            ),
            cells=dict(
                values=[df.Company, df.Country, df.Production_Mt],
                fill_color="#f3f3f3",
                align="left"
            )
        )]
    )
    fig.update_layout(title="Steel Companies Production Table (2023)")
    return fig.to_html(include_plotlyjs="cdn")
