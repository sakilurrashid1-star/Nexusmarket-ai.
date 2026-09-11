import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NexusMarket AI - Global Tech Trends",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM UI STYLING ---
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: 800;
        background: linear-gradient(135deg, #0072ff, #00c6ff, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 25px;
    }
    .metric-box {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        border-left: 6px solid #0072ff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA SIMULATION ---
@st.cache_data
def generate_market_data():
    np.random.seed(101)
    samples = 2000
    
    titles = ['Data Scientist', 'Machine Learning Engineer', 'Data Engineer', 'Data Analyst', 'Cloud AI Solutions Architect']
    hubs = ['Germany', 'United States', 'United Kingdom', 'Canada', 'Bangladesh', 'Remote']
    experience = ['Entry-Level', 'Mid-Level', 'Senior-Level', 'Principal/Lead']
    
    tech_stacks = {
        'Data Scientist': ['Python', 'SQL', 'Machine Learning', 'R', 'Tableau', 'Scikit-Learn'],
        'Machine Learning Engineer': ['Python', 'PyTorch', 'TensorFlow', 'Docker', 'MLOps', 'AWS', 'CUDA'],
        'Data Engineer': ['SQL', 'Python', 'Spark', 'Airflow', 'Snowflake', 'AWS', 'Databricks'],
        'Data Analyst': ['SQL', 'Excel', 'Power BI', 'Tableau', 'Python', 'Statistics'],
        'Cloud AI Solutions Architect': ['AWS', 'Azure', 'Python', 'Docker', 'Kubernetes', 'LLMs', 'LangChain']
    }
    
    dataset = []
    for _ in range(samples):
        role = np.random.choice(titles)
        loc = np.random.choice(hubs)
        exp = np.random.choice(experience)
        
        base_val = 90000 if 'Engineer' in role or 'Architect' in role or 'Scientist' in role else 65000
        multiplier_loc = 1.35 if loc == 'United States' else (1.15 if loc == 'Germany' else 0.85)
        multiplier_exp = 0.65 if exp == 'Entry-Level' else (1.10 if exp == 'Mid-Level' else 1.55)
        
        computed_salary = int(base_val * multiplier_loc * multiplier_exp + np.random.normal(0, 4500))
        if loc == 'Bangladesh':
            computed_salary = int(computed_salary * 0.28)
            
        selected_skills = np.random.choice(tech_stacks[role], size=np.random.randint(3, 5), replace=False)
        dataset.append([role, loc, exp, computed_salary, ", ".join(selected_skills)])
        
    return pd.DataFrame(dataset, columns=['Job Title', 'Market Hub', 'Experience Seniority', 'Salary (USD)', 'Core Stack Required'])

market_df = generate_market_data()

# --- SIDEBAR CONTROL ---
st.sidebar.markdown("### 🛠️ NexusMarket Control Tower")
filter_roles = st.sidebar.multiselect("Target Industry Roles", options=list(market_df['Job Title'].unique()), default=list(market_df['Job Title'].unique()))
filter_hubs = st.sidebar.multiselect("Geographical Target Hubs", options=list(market_df['Market Hub'].unique()), default=list(market_df['Market Hub'].unique()))

processed_df = market_df[(market_df['Job Title'].isin(filter_roles)) & (market_df['Market Hub'].isin(filter_hubs))]

# --- MAIN INTERFACE ---
st.markdown('<div class="main-title">NexusMarket AI: Technical Skills & Global Talent Analytics (2026)</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>An enterprise-grade data intelligence application mapping global software engineering metrics.</p>", unsafe_allow_html=True)
st.write("")

if not processed_df.empty:
    # KPI CARDS
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.markdown(f'<div class="metric-box"><h5>📊 Data Ingestion Vol</h5><h3>{len(processed_df):,} Records</h3></div>', unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f'<div class="metric-box"><h5>💰 Comp Median</h5><h3>${int(processed_df["Salary (USD)"].mean()):,} USD</h3></div>', unsafe_allow_html=True)
    with kpi_col3:
        mode_val = processed_df["Job Title"].mode()
        top_role = mode_val[0] if not mode_val.empty else "N/A"
        st.markdown(f'<div class="metric-box"><h5>🔥 High Growth Core</h5><h3>{top_role}</h3></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("---")

    # VISUALIZATIONS
    chart_left, chart_right = st.columns(2)

    with chart_left:
        st.markdown("#### 📈 Comp Matrix Distribution Matrix")
        fig_box, ax_box = plt.subplots(figsize=(10, 5))
        sns.boxplot(data=processed_df, x='Salary (USD)', y='Job Title', palette='viridis', ax=ax_box)
        st.pyplot(fig_box)
        plt.close(fig_box)

    with chart_right:
        st.markdown("#### 🌍 Market Share by Hub")
        fig_pie, ax_pie = plt.subplots(figsize=(10, 5))
        counts = processed_df['Market Hub'].value_counts()
        ax_pie.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Blues_r'))
        st.pyplot(fig_pie)
        plt.close(fig_pie)

    # WORDCLOUD
    st.write("")
    st.markdown("#### 🔮 Deep Keyword Extraction Engine (NLP Stack Heatmap)")
    skills_corpus = " ".join(processed_df['Core Stack Required'].dropna())

    if skills_corpus.strip():
        text_cloud = WordCloud(width=1400, height=450, background_color='#0e1117', colormap='cool', max_words=40).generate(skills_corpus)
        fig_cloud, ax_cloud = plt.subplots(figsize=(16, 5))
        ax_cloud.imshow(text_cloud, interpolation='bilinear')
        ax_cloud.axis('off')
        st.pyplot(fig_cloud)
        plt.close(fig_cloud)

    # DATA EXPLORER
    st.markdown("#### 🔍 Real-Time Raw Ledger Explorer")
    st.dataframe(processed_df, use_container_width=True)
else:
    st.warning("Please select at least one Role and one Target Hub from the sidebar control tower.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 13px; color: #555;'>Engineered by <b> Alkamah Sakilur Rashid</b> | Data Science Portfolio Ecosystem 2026</p>", unsafe_allow_html=True)
