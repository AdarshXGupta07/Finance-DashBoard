import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from PIL import Image
import io
import streamlit as st

def create_er_diagram():
    """Create ER Diagram for Personal Finance Dashboard Database"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Define colors
    table_color = '#E3F2FD'
    header_color = '#1976D2'
    text_color = '#263238'
    line_color = '#546E7A'
    
    # Raw Transactions Table
    raw_table = FancyBboxPatch((0.5, 5), 3.5, 2, 
                              boxstyle="round,pad=0.1", 
                              facecolor=table_color, 
                              edgecolor=line_color, 
                              linewidth=2)
    ax.add_patch(raw_table)
    
    # Raw Transactions content
    ax.text(2.25, 6.5, 'raw_transactions', 
            fontsize=14, fontweight='bold', 
            ha='center', va='center', color=header_color)
    
    raw_fields = [
        'Type (VARCHAR)',
        'Date (DATETIME)', 
        'Name (VARCHAR)',
        'Amount (DECIMAL)',
        'Currency (VARCHAR)',
        'Category (VARCHAR)',
        'Account (VARCHAR)',
        'Status (VARCHAR)'
    ]
    
    for i, field in enumerate(raw_fields):
        ax.text(2.25, 6.2 - i*0.25, field, 
                fontsize=9, ha='center', va='center', color=text_color)
    
    # Cleaned Transactions Table
    clean_table = FancyBboxPatch((5.5, 5), 3.5, 2, 
                               boxstyle="round,pad=0.1", 
                               facecolor=table_color, 
                               edgecolor=line_color, 
                               linewidth=2)
    ax.add_patch(clean_table)
    
    ax.text(7.25, 6.5, 'transactions', 
            fontsize=14, fontweight='bold', 
            ha='center', va='center', color=header_color)
    
    clean_fields = [
        'type (VARCHAR)',
        'date (DATETIME)', 
        'item (VARCHAR)',
        'amount (DECIMAL)',
        'currency (VARCHAR)',
        'category (VARCHAR)',
        'account (VARCHAR)',
        'status (VARCHAR)'
    ]
    
    for i, field in enumerate(clean_fields):
        ax.text(7.25, 6.2 - i*0.25, field, 
                fontsize=9, ha='center', va='center', color=text_color)
    
    # Relationship Arrow
    ax.annotate('', xy=(5.4, 6), xytext=(4.1, 6),
                arrowprops=dict(arrowstyle='->', lw=2, color=line_color))
    ax.text(4.75, 6.3, 'ETL Process', 
            fontsize=10, ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor=line_color))
    
    # Data Flow Indicators
    ax.text(2.25, 4.2, 'CSV Upload', 
            fontsize=11, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#FFF3E0', edgecolor='#FF9800'))
    
    ax.text(7.25, 4.2, 'Analytics & Dashboard', 
            fontsize=11, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#E8F5E8', edgecolor='#4CAF50'))
    
    # Add title
    ax.text(5, 7.5, 'Personal Finance Dashboard - Database Schema', 
            fontsize=16, fontweight='bold', ha='center', va='center', color=text_color)
    
    # Add legend
    legend_y = 2.5
    ax.text(1, legend_y, 'Legend:', fontsize=12, fontweight='bold', color=text_color)
    ax.text(1, legend_y-0.3, '• Raw data from CSV upload', fontsize=10, color=text_color)
    ax.text(1, legend_y-0.6, '• Cleaned/processed data', fontsize=10, color=text_color)
    ax.text(1, legend_y-0.9, '• ETL: Extract, Transform, Load', fontsize=10, color=text_color)
    
    # Database type indicators
    ax.text(8.5, legend_y, 'Database Types:', fontsize=12, fontweight='bold', color=text_color)
    ax.text(8.5, legend_y-0.3, '• SQLite: Local file-based', fontsize=10, color=text_color)
    ax.text(8.5, legend_y-0.6, '• MySQL: Server-based', fontsize=10, color=text_color)
    ax.text(8.5, legend_y-0.9, '• PostgreSQL: Docker container', fontsize=10, color=text_color)
    
    plt.tight_layout()
    return fig

def create_data_flow_diagram():
    """Create Data Flow Diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Define colors
    colors = {
        'input': '#E1F5FE',
        'process': '#F3E5F5',
        'storage': '#E8F5E8',
        'output': '#FFF3E0'
    }
    
    # Input: CSV File
    csv_box = FancyBboxPatch((0.5, 4), 2, 1, 
                          boxstyle="round,pad=0.1", 
                          facecolor=colors['input'], 
                          edgecolor='#0288D1', linewidth=2)
    ax.add_patch(csv_box)
    ax.text(1.5, 4.5, 'CSV File\n(Bluecoins Export)', 
            fontsize=11, ha='center', va='center', fontweight='bold')
    
    # Process: Extract
    extract_box = FancyBboxPatch((3.5, 4), 2, 1, 
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['process'], 
                             edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(extract_box)
    ax.text(4.5, 4.5, 'Extract\n(pandas.read_csv)', 
            fontsize=11, ha='center', va='center', fontweight='bold')
    
    # Process: Transform
    transform_box = FancyBboxPatch((6.5, 4), 2, 1, 
                                boxstyle="round,pad=0.1", 
                                facecolor=colors['process'], 
                                edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(transform_box)
    ax.text(7.5, 4.5, 'Transform\n(Clean & Filter)', 
            fontsize=11, ha='center', va='center', fontweight='bold')
    
    # Storage: Database
    db_box = FancyBboxPatch((3.5, 2), 4, 1.5, 
                          boxstyle="round,pad=0.1", 
                          facecolor=colors['storage'], 
                          edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(db_box)
    ax.text(5.5, 2.75, 'Database\n(SQLite/MySQL/PostgreSQL)', 
            fontsize=12, ha='center', va='center', fontweight='bold')
    
    # Output: Dashboard
    dashboard_box = FancyBboxPatch((8.5, 2), 1.5, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor=colors['output'], 
                               edgecolor='#F57C00', linewidth=2)
    ax.add_patch(dashboard_box)
    ax.text(9.25, 2.75, 'Streamlit\nDashboard', 
            fontsize=11, ha='center', va='center', fontweight='bold')
    
    # Arrows
    arrows = [
        ((2.5, 4.5), (3.4, 4.5)),
        ((5.5, 4.5), (6.4, 4.5)),
        ((5.5, 4), (5.5, 3.6)),
        ((7.6, 2.75), (8.4, 2.75))
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color='#546E7A'))
    
    # Labels for arrows
    ax.text(2.95, 4.8, '1', fontsize=10, fontweight='bold', 
            bbox=dict(boxstyle="circle,pad=0.2", facecolor='white', edgecolor='#546E7A'))
    ax.text(5.95, 4.8, '2', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle="circle,pad=0.2", facecolor='white', edgecolor='#546E7A'))
    ax.text(5.2, 3.8, '3', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle="circle,pad=0.2", facecolor='white', edgecolor='#546E7A'))
    ax.text(8, 3.2, '4', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle="circle,pad=0.2", facecolor='white', edgecolor='#546E7A'))
    
    # Title
    ax.text(5, 5.5, 'Personal Finance Dashboard - Data Flow', 
            fontsize=16, fontweight='bold', ha='center', va='center')
    
    plt.tight_layout()
    return fig

def create_query_diagram():
    """Create Query Processing Diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Database
    db_box = FancyBboxPatch((0.5, 3), 2.5, 2, 
                          boxstyle="round,pad=0.1", 
                          facecolor='#E8F5E8', 
                          edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(db_box)
    ax.text(1.75, 4, 'Database\n(Transactions)', 
            fontsize=12, ha='center', va='center', fontweight='bold')
    
    # Query Engine
    query_box = FancyBboxPatch((4, 3.5), 2, 1.5, 
                             boxstyle="round,pad=0.1", 
                             facecolor='#F3E5F5', 
                             edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(query_box)
    ax.text(5, 4.25, 'Query\nEngine', 
            fontsize=12, ha='center', va='center', fontweight='bold')
    
    # Analytics Modules
    analytics_boxes = [
        ((7, 5), 'Account\nBalance'),
        ((7, 3.5), 'Payment\nMethods'),
        ((9, 5), 'Expense\nCategories'),
        ((9, 3.5), 'Income\nSources'),
        ((7, 2), 'Time\nSeries')
    ]
    
    for (x, y), label in analytics_boxes:
        box = FancyBboxPatch((x, y), 1.2, 0.8, 
                           boxstyle="round,pad=0.1", 
                           facecolor='#E3F2FD', 
                           edgecolor='#1976D2', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 0.6, y + 0.4, label, 
                fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Arrows from Database to Query Engine
    ax.annotate('', xy=(3.9, 4), xytext=(3.1, 4),
               arrowprops=dict(arrowstyle='->', lw=2, color='#546E7A'))
    
    # Arrows from Query Engine to Analytics
    analytics_positions = [(7.6, 4.8), (7.6, 3.8), (8.8, 4.8), (8.8, 3.8), (7.6, 2.4)]
    for pos in analytics_positions:
        ax.annotate('', xy=pos, xytext=(6.1, 4.25),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='#546E7A'))
    
    # Title
    ax.text(5, 5.5, 'Query Processing & Analytics Pipeline', 
            fontsize=16, fontweight='bold', ha='center', va='center')
    
    plt.tight_layout()
    return fig

def main():
    st.set_page_config(page_title='Database ER Diagrams', layout='wide')
    st.title('🗄️ Personal Finance Dashboard - Database Diagrams')
    
    tab1, tab2, tab3 = st.tabs(['Database Schema', 'Data Flow', 'Query Processing'])
    
    with tab1:
        st.subheader('Entity Relationship Diagram')
        fig_er = create_er_diagram()
        st.pyplot(fig_er)
        
        st.markdown("""
        ### Database Schema Explanation:
        
        **Tables:**
        - `raw_transactions`: Original CSV data as uploaded
        - `transactions`: Cleaned and processed data
        
        **Key Fields:**
        - `type`: Income/Expense classification
        - `date`: Transaction timestamp
        - `amount`: Monetary value
        - `category`: Spending/earning category
        - `account`: Source account
        - `status`: Transaction status (filtered for "Reconciled")
        """)
    
    with tab2:
        st.subheader('Data Flow Architecture')
        fig_flow = create_data_flow_diagram()
        st.pyplot(fig_flow)
        
        st.markdown("""
        ### Data Processing Pipeline:
        
        **1. Extract**: Read CSV from Bluecoins export
        **2. Transform**: Clean data, filter reconciled transactions
        **3. Load**: Store in database (SQLite/MySQL/PostgreSQL)
        **4. Visualize**: Create interactive dashboard
        """)
    
    with tab3:
        st.subheader('Query Processing System')
        fig_query = create_query_diagram()
        st.pyplot(fig_query)
        
        st.markdown("""
        ### Query Architecture:
        
        **Database Layer**: Stores transaction data
        **Query Engine**: Executes SQL queries for analytics
        **Analytics Modules**: Generate specific insights:
        - Account balance tracking
        - Payment method analysis
        - Category-wise expenses
        - Income source tracking
        - Time series analysis
        """)

if __name__ == '__main__':
    main()
