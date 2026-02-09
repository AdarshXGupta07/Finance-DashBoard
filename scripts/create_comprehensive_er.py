import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_comprehensive_er_diagram():
    """Create Comprehensive ER Diagram with 5+ entities"""
    
    fig, ax = plt.subplots(1, 1, figsize=(20, 14))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Define colors
    colors = {
        'entity': '#E3F2FD',
        'header': '#1976D2',
        'text': '#263238',
        'line': '#546E7A',
        'relationship': '#FF6B6B',
        'weak': '#FFA726'
    }
    
    # Entity 1: Users
    user_box = FancyBboxPatch((1, 8), 2.5, 2, 
                           boxstyle="round,pad=0.1", 
                           facecolor=colors['entity'], 
                           edgecolor=colors['line'], linewidth=2)
    ax.add_patch(user_box)
    ax.text(2.25, 9.5, 'Users', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    user_fields = [
        'user_id (PK)',
        'username',
        'email',
        'created_at',
        'is_active'
    ]
    
    for i, field in enumerate(user_fields):
        ax.text(2.25, 9.0 - i*0.35, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Entity 2: Accounts
    account_box = FancyBboxPatch((5, 8), 3, 2, 
                              boxstyle="round,pad=0.1", 
                              facecolor=colors['entity'], 
                              edgecolor=colors['line'], linewidth=2)
    ax.add_patch(account_box)
    ax.text(6.5, 9.5, 'Accounts', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    account_fields = [
        'account_id (PK)',
        'user_id (FK)',
        'account_name',
        'account_type',
        'balance',
        'currency'
    ]
    
    for i, field in enumerate(account_fields):
        ax.text(6.5, 9.0 - i*0.3, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Entity 3: Categories
    category_box = FancyBboxPatch((9, 8), 2.5, 2, 
                               boxstyle="round,pad=0.1", 
                               facecolor=colors['entity'], 
                               edgecolor=colors['line'], linewidth=2)
    ax.add_patch(category_box)
    ax.text(10.25, 9.5, 'Categories', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    category_fields = [
        'category_id (PK)',
        'category_name',
        'category_type',
        'description',
        'icon'
    ]
    
    for i, field in enumerate(category_fields):
        ax.text(10.25, 9.0 - i*0.35, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Entity 4: Transactions
    transaction_box = FancyBboxPatch((13, 8), 3, 2.5, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor=colors['entity'], 
                                 edgecolor=colors['line'], linewidth=2)
    ax.add_patch(transaction_box)
    ax.text(14.5, 9.75, 'Transactions', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    transaction_fields = [
        'transaction_id (PK)',
        'account_id (FK)',
        'category_id (FK)',
        'amount',
        'transaction_type',
        'date',
        'description',
        'status'
    ]
    
    for i, field in enumerate(transaction_fields):
        ax.text(14.5, 9.2 - i*0.28, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Entity 5: Budgets
    budget_box = FancyBboxPatch((2, 4), 3, 2, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['entity'], 
                            edgecolor=colors['line'], linewidth=2)
    ax.add_patch(budget_box)
    ax.text(3.5, 5.5, 'Budgets', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    budget_fields = [
        'budget_id (PK)',
        'user_id (FK)',
        'category_id (FK)',
        'amount_limit',
        'period_type',
        'start_date',
        'end_date'
    ]
    
    for i, field in enumerate(budget_fields):
        ax.text(3.5, 5.0 - i*0.28, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Entity 6: Tags
    tag_box = FancyBboxPatch((7, 4), 2.5, 2, 
                         boxstyle="round,pad=0.1", 
                         facecolor=colors['entity'], 
                         edgecolor=colors['line'], linewidth=2)
    ax.add_patch(tag_box)
    ax.text(8.25, 5.5, 'Tags', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    tag_fields = [
        'tag_id (PK)',
        'tag_name',
        'color',
        'description'
    ]
    
    for i, field in enumerate(tag_fields):
        ax.text(8.25, 5.0 - i*0.4, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Entity 7: Transaction Tags (Junction Table)
    transaction_tag_box = FancyBboxPatch((11, 4), 3, 2, 
                                     boxstyle="round,pad=0.1", 
                                     facecolor='#FFF3E0', 
                                     edgecolor=colors['line'], linewidth=2)
    ax.add_patch(transaction_tag_box)
    ax.text(12.5, 5.5, 'Transaction_Tags', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    transaction_tag_fields = [
        'transaction_id (FK)',
        'tag_id (FK)',
        'created_at'
    ]
    
    for i, field in enumerate(transaction_tag_fields):
        ax.text(12.5, 5.0 - i*0.5, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Relationships
    relationships = [
        # Users to Accounts (1:N)
        ((3.5, 9), (5, 9), '1', 'N'),
        # Accounts to Transactions (1:N)
        ((8, 9), (13, 9), '1', 'N'),
        # Categories to Transactions (1:N)
        ((11.5, 9), (13, 8.5), '1', 'N'),
        # Users to Budgets (1:N)
        ((3.5, 8), (3.5, 6), '1', 'N'),
        # Categories to Budgets (1:N)
        ((10.25, 8), (5, 5), '1', 'N'),
        # Transactions to Transaction_Tags (N:M)
        ((14.5, 8), (12.5, 6), 'N', 'M'),
        # Tags to Transaction_Tags (1:N)
        ((8.25, 4), (11, 4), '1', 'N')
    ]
    
    for start, end, card1, card2 in relationships:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color=colors['relationship']))
        
        # Add cardinality labels
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x - 0.1, mid_y + 0.1, card1, 
                fontsize=10, fontweight='bold', color=colors['relationship'],
                bbox=dict(boxstyle="circle,pad=0.2", facecolor='white', edgecolor=colors['relationship']))
        ax.text(mid_x + 0.1, mid_y + 0.1, card2, 
                fontsize=10, fontweight='bold', color=colors['relationship'],
                bbox=dict(boxstyle="circle,pad=0.2", facecolor='white', edgecolor=colors['relationship']))
    
    # Title
    ax.text(8, 11.5, 'Personal Finance Dashboard - Comprehensive ER Diagram', 
            fontsize=18, fontweight='bold', ha='center', va='center', color=colors['text'])
    
    # Legend
    legend_x = 1
    legend_y = 2
    ax.text(legend_x, legend_y, 'Legend:', fontsize=12, fontweight='bold', color=colors['text'])
    ax.text(legend_x, legend_y-0.4, 'PK = Primary Key', fontsize=10, color=colors['text'])
    ax.text(legend_x, legend_y-0.7, 'FK = Foreign Key', fontsize=10, color=colors['text'])
    ax.text(legend_x, legend_y-1.0, '1:N = One-to-Many', fontsize=10, color=colors['text'])
    ax.text(legend_x, legend_y-1.3, 'N:M = Many-to-Many', fontsize=10, color=colors['text'])
    
    # Entity descriptions
    desc_x = 13
    desc_y = 2
    ax.text(desc_x, desc_y, 'Entities:', fontsize=12, fontweight='bold', color=colors['text'])
    
    entity_descs = [
        'Users: System users',
        'Accounts: Financial accounts',
        'Categories: Transaction categories',
        'Transactions: Financial records',
        'Budgets: Spending limits',
        'Tags: Custom labels',
        'Transaction_Tags: Many-to-many link'
    ]
    
    for i, desc in enumerate(entity_descs):
        ax.text(desc_x, desc_y - 0.3 - i*0.25, f'• {desc}', 
                fontsize=9, ha='left', va='center', color=colors['text'])
    
    plt.tight_layout()
    return fig

def create_enhanced_data_flow():
    """Create Enhanced Data Flow Diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Define colors
    colors = {
        'source': '#E8F5E8',
        'process': '#F3E5F5',
        'storage': '#E3F2FD',
        'output': '#FFF3E0',
        'integration': '#FFEE58'
    }
    
    # Components
    components = [
        ((1, 5), 2.5, 1.5, colors['source'], '#4CAF50', '📁 Data Sources', ['CSV Upload', 'Bank APIs', 'Manual Entry']),
        ((5, 5), 2.5, 1.5, colors['process'], '#7B1FA2', '⚙️ Data Processing', ['Validation', 'Cleansing', 'Categorization']),
        ((8.5, 5), 2.5, 1.5, colors['storage'], '#2196F3', '🗄️ Storage Layer', ['Users', 'Accounts', 'Transactions', 'Categories']),
        ((11.5, 5), 2.5, 1.5, colors['process'], '#7B1FA2', '📊 Analytics Engine', ['Aggregation', 'Trend Analysis', 'Budget Tracking']),
        ((14, 5), 2, 1.5, colors['output'], '#FF9800', '📈 Visualization', ['Dashboard', 'Reports', 'Alerts'])
    ]
    
    for (x, y), w, h, color, edge, label, subitems in components:
        box = FancyBboxPatch((x, y), w, h, 
                           boxstyle="round,pad=0.1", 
                           facecolor=color, 
                           edgecolor=edge, linewidth=2)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2 + 0.3, label, 
                fontsize=12, ha='center', va='center', fontweight='bold')
        
        # Add subitems
        for i, item in enumerate(subitems):
            ax.text(x + w/2, y + h/2 - 0.2 - i*0.25, f'• {item}', 
                    fontsize=9, ha='center', va='center', color='#263238')
    
    # Arrows
    arrows = [
        ((3.5, 5.75), (4.9, 5.75)),
        ((7.5, 5.75), (8.4, 5.75)),
        ((11, 5.75), (11.4, 5.75)),
        ((14, 5.75), (13.9, 5.75))
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=3, color='#546E7A'))
    
    # Title
    ax.text(8, 7, 'Enhanced Data Flow Architecture', 
            fontsize=16, fontweight='bold', ha='center', va='center')
    
    # Data flow indicators
    flow_labels = ['Ingest', 'Process', 'Store', 'Analyze', 'Present']
    flow_positions = [2.25, 6.25, 10.25, 12.25, 15]
    
    for i, (label, pos) in enumerate(zip(flow_labels, flow_positions)):
        ax.text(pos, 6.5, label, fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='#546E7A'))
    
    plt.tight_layout()
    return fig

def main():
    import streamlit as st
    
    st.set_page_config(page_title='Comprehensive ER Diagrams', layout='wide')
    st.title('🗄️ Personal Finance Dashboard - Comprehensive Database Design')
    
    tab1, tab2, tab3 = st.tabs(['Enhanced ER Diagram', 'Data Flow Architecture', 'Schema Comparison'])
    
    with tab1:
        st.subheader('7-Entity Database Schema')
        fig_er = create_comprehensive_er_diagram()
        st.pyplot(fig_er)
        
        st.markdown("""
        ### Enhanced Database Design (7 Entities):
        
        **🔵 Core Entities:**
        1. **Users** - System user management
        2. **Accounts** - Financial accounts (wallets, banks, digital wallets)
        3. **Categories** - Transaction categorization system
        4. **Transactions** - Financial transaction records
        
        **🟢 Supporting Entities:**
        5. **Budgets** - Budget planning and tracking
        6. **Tags** - Flexible labeling system
        7. **Transaction_Tags** - Many-to-many relationship
        
        **🔗 Key Relationships:**
        - Users → Accounts (1:N)
        - Users → Budgets (1:N)
        - Accounts → Transactions (1:N)
        - Categories → Transactions (1:N)
        - Categories → Budgets (1:N)
        - Transactions ↔ Tags (N:M via Transaction_Tags)
        """)
    
    with tab2:
        st.subheader('Enhanced Data Processing Pipeline')
        fig_flow = create_enhanced_data_flow()
        st.pyplot(fig_flow)
        
        st.markdown("""
        ### Multi-Source Data Architecture:
        
        **📊 Data Sources:**
        - CSV Upload (Bluecoins export)
        - Bank APIs (direct integration)
        - Manual Entry (web interface)
        
        **⚙️ Processing Layer:**
        - Data validation and cleansing
        - Automatic categorization
        - Duplicate detection
        
        **🗄️ Storage Layer:**
        - Multi-entity relational database
        - Indexed for performance
        - ACID compliance
        
        **📈 Analytics Engine:**
        - Real-time aggregation
        - Trend analysis algorithms
        - Budget variance tracking
        
        **📈 Visualization Layer:**
        - Interactive dashboards
        - Automated reports
        - Smart alerts
        """)
    
    with tab3:
        st.subheader('Database Schema Evolution')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Original Design (2 Entities)
            **Pros:**
            - Simple implementation
            - Fast development
            - Easy migration
            
            **Cons:**
            - Limited functionality
            - Data redundancy
            - Poor scalability
            - No user management
            - No budget tracking
            """)
        
        with col2:
            st.markdown("""
            ### Enhanced Design (7 Entities)
            **Pros:**
            - Normalized structure
            - User management
            - Budget tracking
            - Flexible categorization
            - Tag system
            - Scalable architecture
            - Better performance
            
            **Cons:**
            - More complex queries
            - Development overhead
            - More storage space
            """)

if __name__ == '__main__':
    main()
