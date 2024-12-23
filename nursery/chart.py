import pandas as pd
import plotly.express as px
from django.db.models import (Case, CharField, Count, DateField, DateTimeField,
                              DecimalField, DurationField, ExpressionWrapper,
                              F, FloatField, Func, IntegerField, Model,
                              OuterRef, Prefetch, Q, Subquery, Sum, Value,
                              When)

from .models import CPVP
def funcFdrBarChart():
    data = (
        CPVP.objects.all().values("batch")
        .annotate(
            No_of_participant=Count(F("id")),
        )
    )

    df = pd.DataFrame(data)
    df.rename(
        columns={"batch": "Batch", "No_of_participant":"Nos. of Participant"},
        inplace=True,
    )

    fig = px.bar(
        df,
        x="Batch",
        y="Nos. of Participant",
        # Root, branches, leaves
        title="<b>Participant by SSC Batch Year</b>",
        color="Nos. of Participant",
        # color_continuous_scale=px.colors.sequential.G10,
        # color_discrete_sequence=px.colors.qualitative.plotly,
        template="seaborn",  # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        #                                   # 'plotly_white', 'plotly_dark', 'presentation',
        #                                   # 'xgridoff', 'ygridoff', 'gridon', 'none'
        hover_name="Batch",
        # height=450,
        # width=650,
        # text_auto="",
        text_auto=True,
        # hover_data={
        #     "Bank": "Bank",
        #     "Amount": "Amount"
        #     # "id": False,
        # },
    )
    fig.update_layout(
        # showlegend=False,
        margin=dict(t=50, l=0, r=0, b=100),
        
        legend=dict(
            title=None, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
        ),
        title={"font_size": 20, "xanchor": "right", "x": 0.5,},
        title_font_color="#CD6600",

    )
    fig.update_traces(
        textfont_size=14,
        textangle=-90,
        textposition="outside",
        cliponaxis=False,
        # textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
    )
    fig.update_coloraxes(showscale=False)
    # fig.update_traces(
    #     texttemplate="%{label}: %{value:.1f}Lac",  # Display values in millions with two decimal places
    # )

    chart = fig.to_html()
    return {"barchart": chart}