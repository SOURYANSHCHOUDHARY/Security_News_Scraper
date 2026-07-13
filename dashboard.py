import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database import get_articles, get_iocs

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp{
    background:#0F172A;
}

/* Hide default footer */
footer{
    visibility:hidden;
}

/* Main Container */
.block-container{
    padding-top:1.5rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* Title */

.main-title{

    font-size:42px;

    color:white;

    font-weight:800;

    margin-bottom:0px;

}

.sub-title{

    color:#94A3B8;

    font-size:18px;

}

/* Sidebar */

[data-testid="stSidebar"]{

    background:#111827;

}

[data-testid="stSidebar"] *{

    color:white;

}

/* Metric Cards */

div[data-testid="metric-container"]{

    background:#1E293B;

    border:1px solid #334155;

    border-radius:15px;

    padding:20px;

}

div[data-testid="metric-container"]:hover{

    border:1px solid #38BDF8;

}

/* Buttons */

.stButton>button{

    background:#0EA5E9;

    color:white;

    border:none;

    border-radius:10px;

    font-weight:bold;

}

.stButton>button:hover{

    background:#0284C7;

}

/* Tables */

[data-testid="stDataFrame"]{

    border-radius:15px;

    overflow:hidden;

}

/* Article Card */

.article-card{

    background:#1E293B;

    padding:22px;

    border-radius:15px;

    border:1px solid #334155;

    margin-bottom:18px;

    transition:.3s;

}

.article-card:hover{

    border:1px solid #38BDF8;

    transform:translateY(-4px);

}

.article-title{

    color:white;

    font-size:24px;

    font-weight:bold;

}

.article-meta{

    color:#94A3B8;

    font-size:14px;

}

.source-badge{

    display:inline-block;

    color:white;

    padding:5px 12px;

    border-radius:20px;

    font-size:13px;

}

</style>

""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""

<h1 class="main-title">

🛡️ Threat Intelligence Dashboard

</h1>

<p class="sub-title">

Real-time Cyber Threat Intelligence Platform

</p>

""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

articles = get_articles()

iocs = get_iocs()

article_df = pd.DataFrame(

    articles,

    columns=[
        "ID",
        "Source",
        "Title",
        "Published",
        "Link"
    ]

)

ioc_df = pd.DataFrame(

    iocs,

    columns=[
        "ID",
        "Source",
        "Article",
        "IOC Type",
        "IOC Value"
    ]

)

# ============================================================
# DATE CONVERSION
# ============================================================

article_df["Published"] = pd.to_datetime(

    article_df["Published"],

    errors="coerce"

)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("# 🛡 Threat Intel")

st.sidebar.markdown("### Security Operations Center")

st.sidebar.markdown("---")

page = st.sidebar.radio(

    "Navigation",

    [

        "Dashboard",

        "Articles",

        "Indicators of Compromise"

    ]

)

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Refresh Dashboard"):

    st.rerun()

st.sidebar.markdown("---")

st.sidebar.info(

"""

Version **1.0**

Python • SQLite • Streamlit • Plotly

"""

)
# ============================================================
# DASHBOARD PAGE
# ============================================================

if page == "Dashboard":

    st.header("📊 Dashboard Overview")

    # -----------------------------
    # KPI CALCULATIONS
    # -----------------------------

    total_articles = len(article_df)
    total_iocs = len(ioc_df)

    domains = len(ioc_df[ioc_df["IOC Type"] == "Domains"])
    urls = len(ioc_df[ioc_df["IOC Type"] == "URLs"])
    ips = len(ioc_df[ioc_df["IOC Type"] == "IPs"])

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("📰 Articles", total_articles)
    c2.metric("🚨 IOCs", total_iocs)
    c3.metric("🌐 Domains", domains)
    c4.metric("🔗 URLs", urls)
    c5.metric("🖥 IPs", ips)

    st.divider()

    # -----------------------------
    # IOC DISTRIBUTION
    # -----------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("IOC Distribution")

        if not ioc_df.empty:

            chart = (
                ioc_df["IOC Type"]
                .value_counts()
                .reset_index()
            )

            chart.columns = ["IOC Type", "Count"]

            fig = px.bar(
                chart,
                x="IOC Type",
                y="Count",
                text="Count",
                color="IOC Type",
                template="plotly_dark"
            )

            fig.update_layout(
                paper_bgcolor="#1E293B",
                plot_bgcolor="#1E293B",
                font_color="white",
                height=430,
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No IOC data available.")

    with right:

        st.subheader("IOC Percentage")

        if not ioc_df.empty:

            pie = px.pie(
                chart,
                names="IOC Type",
                values="Count",
                hole=.55,
                template="plotly_dark"
            )

            pie.update_layout(
                paper_bgcolor="#1E293B",
                plot_bgcolor="#1E293B",
                font_color="white",
                height=430
            )

            st.plotly_chart(
                pie,
                use_container_width=True
            )

        else:

            st.info("No IOC data available.")

    st.divider()

    # -----------------------------
    # ARTICLES BY SOURCE
    # -----------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("📰 Articles by Source")

        if not article_df.empty:

            source_chart = (
                article_df["Source"]
                .value_counts()
                .reset_index()
            )

            source_chart.columns = [
                "Source",
                "Articles"
            ]

            fig = px.bar(
                source_chart,
                x="Source",
                y="Articles",
                color="Source",
                text="Articles",
                template="plotly_dark"
            )

            fig.update_layout(
                paper_bgcolor="#1E293B",
                plot_bgcolor="#1E293B",
                font_color="white",
                showlegend=False,
                height=430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No article data available.")

    with right:

        st.subheader("📅 Articles Timeline")

        if not article_df.empty:

            timeline = article_df.copy()

            timeline["Date"] = timeline["Published"].dt.date

            timeline = (
                timeline.groupby("Date")
                .size()
                .reset_index(name="Articles")
            )

            fig = px.line(
                timeline,
                x="Date",
                y="Articles",
                markers=True,
                template="plotly_dark"
            )

            fig.update_layout(
                paper_bgcolor="#1E293B",
                plot_bgcolor="#1E293B",
                font_color="white",
                height=430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No timeline available.")

    st.divider()
    # ============================================================
    # TOP DOMAINS
    # ============================================================

    st.subheader("🌐 Top 10 Domains")

    domains_df = ioc_df[
        ioc_df["IOC Type"] == "Domains"
    ]

    if not domains_df.empty:

        top_domains = (
            domains_df["IOC Value"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_domains.columns = [
            "Domain",
            "Occurrences"
        ]

        left, right = st.columns([2, 3])

        with left:

            st.dataframe(
                top_domains,
                use_container_width=True,
                hide_index=True
            )

        with right:

            fig = px.bar(
                top_domains,
                x="Occurrences",
                y="Domain",
                orientation="h",
                text="Occurrences",
                template="plotly_dark"
            )

            fig.update_layout(
                paper_bgcolor="#1E293B",
                plot_bgcolor="#1E293B",
                font_color="white",
                showlegend=False,
                height=420
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:

        st.info("No domains extracted yet.")

    st.divider()

    # ============================================================
    # LATEST THREATS
    # ============================================================

    st.subheader("🔥 Latest Threats")

    latest_articles = (
        article_df
        .sort_values(
            "Published",
            ascending=False
        )
        .head(8)
    )

    if latest_articles.empty:

        st.warning("No articles available.")

    else:

        for _, row in latest_articles.iterrows():

            color = "#2563EB"

            if row["Source"] == "The Hacker News":
                color = "#16A34A"

            elif row["Source"] == "BleepingComputer":
                color = "#EA580C"

            elif row["Source"] == "SecurityWeek":
                color = "#7C3AED"

            elif row["Source"] == "Dark Reading":
                color = "#DC2626"

            st.markdown(
                f"""
<div class="article-card">

<div class="article-title">

{row['Title']}

</div>

<br>

<span
style="
background:{color};
padding:6px 12px;
border-radius:20px;
color:white;
font-size:13px;
">

{row['Source']}

</span>

<span class="article-meta">

&nbsp;&nbsp;📅 {row['Published']}

</span>

<br><br>

<a
href="{row['Link']}"
target="_blank">

🔗 Read Full Article

</a>

</div>
""",
                unsafe_allow_html=True
            )

    st.divider()

    # ============================================================
    # QUICK DATABASE SUMMARY
    # ============================================================

    st.subheader("📌 Database Summary")

    c1, c2, c3 = st.columns(3)

    c1.success(f"Articles Stored: **{len(article_df)}**")

    c2.info(f"IOCs Stored: **{len(ioc_df)}**")

    unique_sources = (
        article_df["Source"].nunique()
        if not article_df.empty
        else 0
    )

    c3.warning(
        f"RSS Sources: **{unique_sources}**"
    )

    st.divider()

# ============================================================
# ARTICLES PAGE
# ============================================================

elif page == "Articles":

    st.header("📰 Security News")

    st.markdown(
        "Browse all collected cybersecurity articles."
    )

    st.divider()

    # ---------------------------------------------------------
    # ARTICLE STATISTICS
    # ---------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📰 Total Articles",
        len(article_df)
    )

    col2.metric(
        "🌍 Sources",
        article_df["Source"].nunique()
        if not article_df.empty else 0
    )

    col3.metric(
        "📅 Latest Articles",
        min(10, len(article_df))
    )

    st.divider()

    # ---------------------------------------------------------
    # FILTERS
    # ---------------------------------------------------------

    left, right = st.columns(2)

    with left:

        sources = ["All Sources"] + sorted(
            article_df["Source"].dropna().unique().tolist()
        )

        selected_source = st.selectbox(
            "Select Source",
            sources
        )

    with right:

        search = st.text_input(
            "🔍 Search Article"
        )

    filtered = article_df.copy()

    if selected_source != "All Sources":

        filtered = filtered[
            filtered["Source"] == selected_source
        ]

    if search:

        filtered = filtered[
            filtered["Title"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.divider()

    # ---------------------------------------------------------
    # DATE FILTER
    # ---------------------------------------------------------

    if not filtered.empty:

        min_date = filtered["Published"].min().date()

        max_date = filtered["Published"].max().date()

        start_date, end_date = st.date_input(

            "Publication Date",

            value=(min_date, max_date)

        )

        filtered = filtered[

            (
                filtered["Published"].dt.date >= start_date
            )

            &

            (
                filtered["Published"].dt.date <= end_date
            )

        ]

    st.divider()

    st.subheader("Latest Articles")

    # ---------------------------------------------------------
    # ARTICLE CARDS
    # ---------------------------------------------------------

    if filtered.empty:

        st.warning("No articles found.")

    else:

        for _, row in filtered.iterrows():

            badge_color = "#2563EB"

            if row["Source"] == "The Hacker News":
                badge_color = "#16A34A"

            elif row["Source"] == "BleepingComputer":
                badge_color = "#EA580C"

            elif row["Source"] == "SecurityWeek":
                badge_color = "#7C3AED"

            elif row["Source"] == "Dark Reading":
                badge_color = "#DC2626"

            st.markdown(

                f"""

<div class="article-card">

<div class="article-title">

{row["Title"]}

</div>

<br>

<span
style="
background:{badge_color};
padding:6px 12px;
border-radius:20px;
color:white;
font-size:13px;
">

{row["Source"]}

</span>

<span class="article-meta">

&nbsp;&nbsp;📅 {row["Published"].strftime("%d %b %Y %H:%M")}

</span>

<br><br>

<a
href="{row['Link']}"
target="_blank">

🔗 Read Full Article

</a>

</div>

""",

                unsafe_allow_html=True

            )

# ============================================================
# IOC PAGE
# ============================================================

elif page == "Indicators of Compromise":

    st.header("🚨 Indicators of Compromise")

    st.markdown(
        "Search, filter and analyze extracted Indicators of Compromise."
    )

    st.divider()

    # ============================================================
    # KPI CARDS
    # ============================================================

    total_iocs = len(ioc_df)

    total_domains = len(
        ioc_df[ioc_df["IOC Type"] == "Domains"]
    )

    total_urls = len(
        ioc_df[ioc_df["IOC Type"] == "URLs"]
    )

    total_ips = len(
        ioc_df[ioc_df["IOC Type"] == "IPs"]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🚨 Total IOCs", total_iocs)
    c2.metric("🌐 Domains", total_domains)
    c3.metric("🔗 URLs", total_urls)
    c4.metric("🖥 IPs", total_ips)

    st.divider()

    # ============================================================
    # FILTERS
    # ============================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        sources = ["All Sources"] + sorted(
            ioc_df["Source"].dropna().unique().tolist()
        )

        selected_source = st.selectbox(
            "Source",
            sources
        )

    with col2:

        types = ["All Types"] + sorted(
            ioc_df["IOC Type"].dropna().unique().tolist()
        )

        selected_type = st.selectbox(
            "IOC Type",
            types
        )

    with col3:

        search = st.text_input(
            "🔍 Search IOC"
        )

    filtered = ioc_df.copy()

    if selected_source != "All Sources":

        filtered = filtered[
            filtered["Source"] == selected_source
        ]

    if selected_type != "All Types":

        filtered = filtered[
            filtered["IOC Type"] == selected_type
        ]

    if search:

        filtered = filtered[
            filtered["IOC Value"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.divider()

    # ============================================================
    # IOC TYPE CHART
    # ============================================================

    left, right = st.columns(2)

    with left:

        st.subheader("IOC Type Distribution")

        if not filtered.empty:

            chart = (
                filtered["IOC Type"]
                .value_counts()
                .reset_index()
            )

            chart.columns = [
                "IOC Type",
                "Count"
            ]

            fig = px.bar(

                chart,

                x="IOC Type",

                y="Count",

                text="Count",

                color="IOC Type",

                template="plotly_dark"

            )

            fig.update_layout(

                paper_bgcolor="#1E293B",

                plot_bgcolor="#1E293B",

                font_color="white",

                showlegend=False,

                height=420

            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No IOC data available.")

    with right:

        st.subheader("IOC Percentage")

        if not filtered.empty:

            pie = px.pie(

                chart,

                names="IOC Type",

                values="Count",

                hole=.55,

                template="plotly_dark"

            )

            pie.update_layout(

                paper_bgcolor="#1E293B",

                plot_bgcolor="#1E293B",

                font_color="white",

                height=420

            )

            st.plotly_chart(
                pie,
                use_container_width=True
            )

        else:

            st.info("No IOC data available.")

    st.divider()

    # ============================================================
    # TOP IOC VALUES
    # ============================================================

    st.subheader("🔥 Top IOC Values")

    if not filtered.empty:

        common = (

            filtered["IOC Value"]

            .value_counts()

            .head(10)

            .reset_index()

        )

        common.columns = [

            "IOC",

            "Count"

        ]

        fig = px.bar(

            common,

            x="Count",

            y="IOC",

            orientation="h",

            text="Count",

            template="plotly_dark"

        )

        fig.update_layout(

            paper_bgcolor="#1E293B",

            plot_bgcolor="#1E293B",

            font_color="white",

            showlegend=False,

            height=500

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    else:

        st.info("No IOC values available.")

    st.divider()

    # ============================================================
    # IOC TABLE
    # ============================================================

    st.subheader("IOC Database")

    st.dataframe(

        filtered,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ============================================================
    # DOWNLOAD CSV
    # ============================================================

    csv = filtered.to_csv(index=False)

    st.download_button(

        "📥 Download IOC Report",

        csv,

        file_name="ioc_report.csv",

        mime="text/csv"

    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

from datetime import datetime

current_time = datetime.now().strftime("%d %b %Y  %H:%M:%S")

left, center, right = st.columns([2, 2, 2])

with left:

    st.caption(
        "🛡 Threat Intelligence Dashboard"
    )

with center:

    st.caption(
        f"Last Updated: {current_time}"
    )

with right:

    st.caption(
        "Version 1.0"
    )

st.markdown(
"""
---
<center>

Built using

**Python | SQLite | Streamlit | Plotly | BeautifulSoup | Feedparser**

</center>
""",
unsafe_allow_html=True
)

# ============================================================
# SIDEBAR INFORMATION
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("📊 Database Statistics")

st.sidebar.write(f"📰 Articles : {len(article_df)}")

st.sidebar.write(f"🚨 IOCs : {len(ioc_df)}")

st.sidebar.write(
    f"🌍 Sources : {article_df['Source'].nunique()}"
)

st.sidebar.markdown("---")

st.sidebar.subheader("📌 IOC Summary")

try:

    st.sidebar.write(
        f"🌐 Domains : {len(ioc_df[ioc_df['IOC Type']=='Domains'])}"
    )

    st.sidebar.write(
        f"🔗 URLs : {len(ioc_df[ioc_df['IOC Type']=='URLs'])}"
    )

    st.sidebar.write(
        f"🖥 IPs : {len(ioc_df[ioc_df['IOC Type']=='IPs'])}"
    )

except:

    pass

st.sidebar.markdown("---")

st.sidebar.success("Dashboard Running Successfully")

# ============================================================
# EMPTY DATABASE MESSAGE
# ============================================================

if article_df.empty:

    st.warning(
        """
No articles found in the database.

Run:

python app.py

to scrape the latest cybersecurity news.
"""
    )

# ============================================================
# END
# ============================================================