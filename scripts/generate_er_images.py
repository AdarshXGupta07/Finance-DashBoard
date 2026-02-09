import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_er_diagram_static():
    """Create static ER Diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define colors
    table_color = '#E3F2FD'
    header_color = '#1976D2'
    text_color = '#263238'
    line_color = '#546E7A'
    
    # Raw Transactions Table
    raw_table = FancyBboxPatch((1, 6), 4, 2.5, 
                              boxstyle="round,pad=0.1", 
                              facecolor=table_color, 
                              edgecolor=line_color, 
                              linewidth=2)
    ax.add_patch(raw_table)
    
    ax.text(3, 7.5, 'raw_transactions', 
            fontsize=16, fontweight='bold', 
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
        ax.text(3, 7.1 - i*0.3, field, 
                fontsize=10, ha='center', va='center', color=text_color)
    
    # Cleaned Transactions Table
    clean_table = FancyBboxPatch((7, 6), 4, 2.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor=table_color, 
                               edgecolor=line_color, 
                               linewidth=2)
    ax.add_patch(clean_table)
    
    ax.text(9, 7.5, 'transactions', 
            fontsize=16, fontweight='bold', 
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
        ax.text(9, 7.1 - i*0.3, field, 
                fontsize=10, ha='center', va='center', color=text_color)
    
    # Relationship Arrow
    ax.annotate('', xy=(6.9, 7.25), xytext=(5.1, 7.25),
                arrowprops=dict(arrowstyle='->', lw=3, color=line_color))
    ax.text(6, 7.6, 'ETL Process', 
            fontsize=12, ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor=line_color))
    
    # Data Sources
    ax.text(3, 5, '📁 CSV Upload', 
            fontsize=14, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#FFF3E0', edgecolor='#FF9800'))
    
    ax.text(9, 5, '📊 Analytics Ready', 
            fontsize=14, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#E8F5E8', edgecolor='#4CAF50'))
    
    # Add title
    ax.text(6, 9, 'Personal Finance Dashboard - Entity Relationship Diagram', 
            fontsize=20, fontweight='bold', ha='center', va='center', color=text_color)
    
    # Add database comparison
    comparison_y = 3
    ax.text(2, comparison_y, 'Database Options:', fontsize=14, fontweight='bold', color=text_color)
    
    db_options = [
        ('SQLite', 'Local file-based', '🗄️'),
        ('MySQL', 'Server-based', '🐬'),
        ('PostgreSQL', 'Docker container', '🐘')
    ]
    
    for i, (db_type, desc, icon) in enumerate(db_options):
        ax.text(2, comparison_y - 0.5 - i*0.4, f'{icon} {db_type}: {desc}', 
                fontsize=11, ha='center', va='center', color=text_color)
    
    # Add field descriptions
    desc_y = 1
    ax.text(8, desc_y, 'Key Fields:', fontsize=14, fontweight='bold', color=text_color)
    
    field_descs = [
        'type: Income/Expense classification',
        'date: Transaction timestamp',
        'amount: Monetary value',
        'category: Spending/earning category',
        'account: Source/destination account',
        'status: Transaction processing status'
    ]
    
    for i, desc in enumerate(field_descs):
        ax.text(8, desc_y - 0.4 - i*0.3, f'• {desc}', 
                fontsize=10, ha='left', va='center', color=text_color)
    
    plt.tight_layout()
    plt.savefig('er_diagram.png', dpi=300, bbox_inches='tight')
    plt.savefig('er_diagram.jpg', dpi=300, bbox_inches='tight')
    print("ER Diagram saved as 'er_diagram.png' and 'er_diagram.jpg'")
    
    return fig

def create_data_flow_static():
    """Create static Data Flow Diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Define colors
    colors = {
        'input': '#E1F5FE',
        'process': '#F3E5F5',
        'storage': '#E8F5E8',
        'output': '#FFF3E0'
    }
    
    # Process boxes
    boxes = [
        ((1, 3.5), 2, 1.5, colors['input'], '#0288D1', '📁 CSV File\n(Bluecoins Export)'),
        ((4, 3.5), 2, 1.5, colors['process'], '#7B1FA2', '⚙️ Extract\n(pandas.read_csv)'),
        ((7, 3.5), 2, 1.5, colors['process'], '#7B1FA2', '🔄 Transform\n(Clean & Filter)'),
        ((10, 3.5), 2, 1.5, colors['storage'], '#2E7D32', '🗄️ Database\n(SQLite/MySQL/PostgreSQL)'),
        ((4, 1), 2, 1.5, colors['output'], '#F57C00', '📊 Streamlit\nDashboard'),
        ((7, 1), 2, 1.5, colors['output'], '#F57C00', '📈 Analytics\n& Charts')
    ]
    
    for (x, y), w, h, color, edge, label in boxes:
        box = FancyBboxPatch((x, y), w, h, 
                           boxstyle="round,pad=0.1", 
                           facecolor=color, 
                           edgecolor=edge, linewidth=2)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, label, 
                fontsize=11, ha='center', va='center', fontweight='bold')
    
    # Arrows
    arrows = [
        ((3, 4.25), (3.9, 4.25)),
        ((6, 4.25), (6.9, 4.25)),
        ((9, 4.25), (9.9, 4.25)),
        ((5, 3.4), (5, 2.6)),
        ((8, 3.4), (8, 2.6))
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color='#546E7A'))
    
    # Step numbers
    steps = [(3.5, 4.5), (6.5, 4.5), (9.5, 4.5), (5, 3), (8, 3)]
    for i, (x, y) in enumerate(steps):
        ax.text(x, y, str(i+1), fontsize=12, fontweight='bold', 
                bbox=dict(boxstyle="circle,pad=0.3", facecolor='white', edgecolor='#546E7A'))
    
    # Title
    ax.text(6, 5.5, 'Personal Finance Dashboard - Data Flow Architecture', 
            fontsize=18, fontweight='bold', ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig('data_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.savefig('data_flow_diagram.jpg', dpi=300, bbox_inches='tight')
    print("Data Flow Diagram saved as 'data_flow_diagram.png' and 'data_flow_diagram.jpg'")
    
    return fig

if __name__ == '__main__':
    print("Creating ER Diagrams...")
    create_er_diagram_static()
    print("\nCreating Data Flow Diagram...")
    create_data_flow_static()
    print("\n✅ All diagrams created successfully!")
    print("Files saved:")
    print("- er_diagram.png")
    print("- er_diagram.jpg") 
    print("- data_flow_diagram.png")
    print("- data_flow_diagram.jpg")
