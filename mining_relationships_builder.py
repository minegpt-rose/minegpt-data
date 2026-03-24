#!/usr/bin/env python3
"""
Mining Relationships Builder

Creates ONLY meaningful mining relationships
No generic relationships, only specific mining context
"""

import csv

def load_variable_database():
    """Load the variable database"""
    variables = []
    
    try:
        with open('/dropbox/03. Knowledge Graph/accurate_database_final_FL_corrected.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                variables.append(row)
    except Exception as e:
        print(f"Error loading variable database: {e}")
        return []
    
    return variables

def create_mining_relationships(variables):
    """Create meaningful mining relationships"""
    relationships = []
    
    # Only create relationships that make mining sense
    
    # 1. Unit relationships (base variables -> their units)
    for variable in variables:
        table_name = variable['table_name']
        column_name = variable['column_name']
        
        if '_unit' in column_name.lower():
            base_var_name = column_name.replace('_unit', '')
            # Check if base variable exists in same table
            table_vars = [v for v in variables if v['table_name'] == table_name]
            base_exists = any(v['column_name'] == base_var_name for v in table_vars)
            
            if base_exists:
                relationships.append(create_relationship(
                    table_name, base_var_name,
                    table_name, column_name,
                    'has_unit', 'Has Unit'
                ))
    
    # 2. Cost relationships (cost components -> total costs)
    cost_table_vars = [v for v in variables if v['table_name'] == 'cost_table']
    cost_columns = [v['column_name'] for v in cost_table_vars]
    
    if 'total_initial_direct_capex' in cost_columns:
        for variable in cost_table_vars:
            col_name = variable['column_name']
            col_lower = col_name.lower()
            
            # Skip units and totals
            if '_unit' in col_lower or col_name == 'total_initial_direct_capex':
                continue
                
            # Cost components contribute to total
            if any(keyword in col_lower for keyword in ['mining', 'process', 'plant', 'tailings', 'infrastructure', 'closure']):
                relationships.append(create_relationship(
                    'cost_table', col_name,
                    'cost_table', 'total_initial_direct_capex',
                    'contributes_to', 'Contributes To'
                ))
    
    return relationships

def create_relationship(node1_table, node1_column, node2_table, node2_column, predicate, predicate_display):
    """Create a properly formatted relationship"""
    return {
        'node1_table': node1_table,
        'node1_column': node1_column,
        'node1_report_number': '',
        'node1_display': node1_column.replace('_', ' ').title(),
        'predicate': predicate,
        'predicate_display': predicate_display,
        'node2_table': node2_table,
        'node2_column': node2_column,
        'node1_report_number_copy': '',
        'node2_display': node2_column.replace('_', ' ').title(),
        'Example': f"{node1_column} — {predicate} → {node2_column}"
    }

def main():
    """Main function"""
    print("Loading variable database...")
    variables = load_variable_database()
    
    if not variables:
        print("Failed to load variables")
        return
    
    print(f"Loaded {len(variables)} variables")
    
    print("\nCreating mining relationships...")
    relationships = create_mining_relationships(variables)
    
    print(f"Generated {len(relationships)} relationships")
    
    # Remove duplicates
    unique_relationships = []
    seen = set()
    
    for rel in relationships:
        rel_key = f"{rel['node1_table']}.{rel['node1_column']}.{rel['node2_table']}.{rel['node2_column']}.{rel['predicate']}"
        if rel_key not in seen:
            seen.add(rel_key)
            unique_relationships.append(rel)
    
    print(f"Final unique relationships: {len(unique_relationships)}")
    
    # Write to CSV
    csv_headers = [
        'node1_table', 'node1_column', 'node1_report_number', 'node1_display',
        'predicate', 'predicate_display', 'node2_table', 'node2_column',
        'node1_report_number_copy', 'node2_display', 'Example'
    ]
    
    output_path = '/dropbox/03. Knowledge Graph/mining_relationships.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in unique_relationships:
            writer.writerow(rel)
    
    print(f"Saved mining relationships to: {output_path}")
    
    # Show relationship type breakdown
    print("\nRelationship type breakdown:")
    rel_counts = {}
    for rel in unique_relationships:
        rel_type = rel['predicate']
        rel_counts[rel_type] = rel_counts.get(rel_type, 0) + 1
    
    for rel_type, count in sorted(rel_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {rel_type}: {count}")
    
    print("\nSample relationships:")
    for i, rel in enumerate(unique_relationships[:10]):
        print(f"  {i+1}. {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")

if __name__ == "__main__":
    main()