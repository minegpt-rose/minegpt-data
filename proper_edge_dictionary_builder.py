#!/usr/bin/env python3
"""
Proper Edge Dictionary Builder

Creates relationships using ONLY actual table and column names
No hallucination, no self-references, meaningful mining relationships
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

def get_actual_tables(variables):
    """Get actual table names"""
    return sorted(set(v['table_name'] for v in variables))

def get_columns_for_table(variables, table_name):
    """Get actual column names for a table"""
    return [v['column_name'] for v in variables if v['table_name'] == table_name]

def create_meaningful_relationships(variables):
    """Create meaningful mining relationships"""
    relationships = []
    
    # Get actual tables and columns
    tables = get_actual_tables(variables)
    
    for variable in variables:
        table_name = variable['table_name']
        column_name = variable['column_name']
        column_lower = column_name.lower()
        notes = variable.get('notes', '').lower()
        
        # Skip report_number columns
        if 'report_number' in column_lower:
            continue
        
        # 1. Unit relationships (only for actual _unit fields)
        if '_unit' in column_lower:
            base_var_name = column_name.replace('_unit', '')
            table_cols = get_columns_for_table(variables, table_name)
            if base_var_name in table_cols:
                relationships.append(create_relationship(
                    table_name, base_var_name,
                    table_name, column_name,
                    'has_unit', 'Has Unit'
                ))
        
        # 2. Cost relationships (only for cost_table)
        if table_name == 'cost_table':
            if any(keyword in column_lower for keyword in ['mining', 'process', 'tailings', 'infrastructure', 'closure']):
                if 'total_initial_direct_capex' in get_columns_for_table(variables, 'cost_table'):
                    relationships.append(create_relationship(
                        table_name, column_name,
                        'cost_table', 'total_initial_direct_capex',
                        'contributes_to', 'Contributes To'
                    ))
        
        # 3. Geographic relationships (only for actual location fields)
        location_fields = ['country', 'province', 'state', 'region', 'district', 'location']
        if any(field in column_lower for field in location_fields):
            if 'project_name' in get_columns_for_table(variables, 'general_information'):
                relationships.append(create_relationship(
                    'general_information', 'project_name',
                    table_name, column_name,
                    'located_in', 'Located In'
                ))
        
        # 4. Commodity relationships
        if 'commodity' in column_lower or 'mineral' in column_lower:
            if 'project_name' in get_columns_for_table(variables, 'general_information'):
                relationships.append(create_relationship(
                    'general_information', 'project_name',
                    table_name, column_name,
                    'produces', 'Produces'
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
    
    print("\nCreating meaningful relationships...")
    relationships = create_meaningful_relationships(variables)
    
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
    
    output_path = '/dropbox/03. Knowledge Graph/proper_edge_dictionary.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in unique_relationships:
            writer.writerow(rel)
    
    print(f"Saved proper edge dictionary to: {output_path}")
    
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