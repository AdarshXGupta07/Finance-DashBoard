import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_comprehensive_er_static():
    """Create static Comprehensive ER Diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(20, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define colors
    colors = {
        'entity': '#E3F2FD',
        'header': '#1976D2',
        'text': '#263238',
        'line': '#546E7A',
        'relationship': '#FF6B6B'
    }
    
    # Entity 1: Users
    user_box = FancyBboxPatch((1, 6), 2.5, 2, 
                           boxstyle="round,pad=0.1", 
                           facecolor=colors['entity'], 
                           edgecolor=colors['line'], linewidth=2)
    ax.add_patch(user_box)
    ax.text(2.25, 7.5, 'Users', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    user_fields = ['user_id (PK)', 'username', 'email', 'created_at', 'is_active']
    for i, field in enumerate(user_fields):
        ax.text(2.25, 7.0 - i*0.35, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Entity 2: Accounts
    account_box = FancyBboxPatch((5, 6), 3, 2, 
                              boxstyle="round,pad=0.1", 
                              facecolor=colors['entity'], 
                              edgecolor=colors['line'], linewidth=2)
    ax.add_patch(account_box)
    ax.text(6.5, 7.5, 'Accounts', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    account_fields = ['account_id (PK)', 'user_id (FK)', 'account_name', 'account_type', 'balance', 'currency']
    for i, field in enumerate(account_fields):
        ax.text(6.5, 7.0 - i*0.28, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Entity 3: Categories
    category_box = FancyBboxPatch((9, 6), 2.5, 2, 
                               boxstyle="round,pad=0.1", 
                               facecolor=colors['entity'], 
                               edgecolor=colors['line'], linewidth=2)
    ax.add_patch(category_box)
    ax.text(10.25, 7.5, 'Categories', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    category_fields = ['category_id (PK)', 'category_name', 'category_type', 'description', 'icon']
    for i, field in enumerate(category_fields):
        ax.text(10.25, 7.0 - i*0.35, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Entity 4: Transactions
    transaction_box = FancyBboxPatch((12.5, 6), 3, 2.5, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor=colors['entity'], 
                                 edgecolor=colors['line'], linewidth=2)
    ax.add_patch(transaction_box)
    ax.text(14, 7.5, 'Transactions', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    transaction_fields = ['transaction_id (PK)', 'account_id (FK)', 'category_id (FK)', 'amount', 'transaction_type', 'date', 'description', 'status']
    for i, field in enumerate(transaction_fields):
        ax.text(14, 7.2 - i*0.28, field, 
                fontsize=8, ha='center', va='center', color=colors['text'])
    
    # Entity 5: Budgets
    budget_box = FancyBboxPatch((2, 2.5), 3, 2, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['entity'], 
                            edgecolor=colors['line'], linewidth=2)
    ax.add_patch(budget_box)
    ax.text(3.5, 4, 'Budgets', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    budget_fields = ['budget_id (PK)', 'user_id (FK)', 'category_id (FK)', 'amount_limit', 'period_type', 'start_date', 'end_date']
    for i, field in enumerate(budget_fields):
        ax.text(3.5, 3.5 - i*0.28, field, 
                fontsize=8, ha='center', va='center', color=colors['text'])
    
    # Entity 6: Tags
    tag_box = FancyBboxPatch((7, 2.5), 2.5, 2, 
                         boxstyle="round,pad=0.1", 
                         facecolor=colors['entity'], 
                         edgecolor=colors['line'], linewidth=2)
    ax.add_patch(tag_box)
    ax.text(8.25, 4, 'Tags', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    tag_fields = ['tag_id (PK)', 'tag_name', 'color', 'description']
    for i, field in enumerate(tag_fields):
        ax.text(8.25, 3.5 - i*0.4, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Entity 7: Transaction Tags (Junction)
    junction_box = FancyBboxPatch((11, 2.5), 3, 2, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#FFF3E0', 
                               edgecolor=colors['line'], linewidth=2)
    ax.add_patch(junction_box)
    ax.text(12.5, 4, 'Transaction_Tags', fontsize=14, fontweight='bold', 
            ha='center', va='center', color=colors['header'])
    
    junction_fields = ['transaction_id (FK)', 'tag_id (FK)', 'created_at']
    for i, field in enumerate(junction_fields):
        ax.text(12.5, 3.5 - i*0.5, field, 
                fontsize=9, ha='center', va='center', color=colors['text'])
    
    # Relationships with cardinality
    relationships = [
        ((3.5, 7), (5, 7), '1', 'N'),
        ((8, 7), (12.5, 7), '1', 'N'),
        ((11.5, 7), (12.5, 6.5), '1', 'N'),
        ((3.5, 6), (3.5, 4.5), '1', 'N'),
        ((10.25, 6), (5, 3), '1', 'N'),
        ((14, 6), (12.5, 4.5), 'N', 'M'),
        ((8.25, 2.5), (11, 2.5), '1', 'N')
    ]
    
    for start, end, card1, card2 in relationships:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color=colors['relationship']))
        
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x - 0.15, mid_y + 0.1, card1, 
                fontsize=9, fontweight='bold', color=colors['relationship'],
                bbox=dict(boxstyle="circle,pad=0.15", facecolor='white', edgecolor=colors['relationship']))
        ax.text(mid_x + 0.15, mid_y + 0.1, card2, 
                fontsize=9, fontweight='bold', color=colors['relationship'],
                bbox=dict(boxstyle="circle,pad=0.15", facecolor='white', edgecolor=colors['relationship']))
    
    # Title
    ax.text(8, 9, 'Personal Finance Dashboard - 7 Entity ER Diagram', 
            fontsize=18, fontweight='bold', ha='center', va='center', color=colors['text'])
    
    # Legend
    ax.text(1, 1, 'Legend: PK=Primary Key, FK=Foreign Key, 1:N=One-to-Many, N:M=Many-to-Many', 
            fontsize=10, color=colors['text'])
    
    plt.tight_layout()
    plt.savefig('comprehensive_er_diagram.png', dpi=300, bbox_inches='tight')
    plt.savefig('comprehensive_er_diagram.jpg', dpi=300, bbox_inches='tight')
    print("Comprehensive ER Diagram saved!")
    
    return fig

if __name__ == '__main__':
    create_comprehensive_er_static()
