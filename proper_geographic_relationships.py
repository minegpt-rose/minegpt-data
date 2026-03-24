#!/usr/bin/env python3
"""
Proper Geographic Relationships Builder

Creates meaningful geographic relationships for mining projects
Only uses actual geographic fields, not coordinates or file locations
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

def create_proper_geographic_relationships(variables):
    """Create meaningful geographic relationships"""
    relationships = []
    
    # Get all variables
    general_info_vars = [v for v in variables if v['table_name'] == 'general_information']
    
    # Project location relationships
    project_name_exists = any(v['column_name'] == 'project_name' for v in general_info_vars)
    
    if project_name_exists:
        # Only use actual geographic location fields (not coordinates or file paths)
        geographic_fields = ['country', 'province', 'state', 'region', 'district']
        
        for var in general_info_vars:
            col_name = var['column_name']
            
            if col_name in geographic_fields:
                relationships.append(create_relationship(
                    'general_information', 'project_name',
                    'general_information', col_name,
                    'is_located_at', 'Is Located At'
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
    
    print("\nCreating proper geographic relationships...")
    relationships = create_proper_geographic_relationships(variables)
    
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
    
    # Load existing mining relationships
    existing_relationships = []
    try:
        with open('/dropbox/03. Knowledge Graph/mining_relationships.csv', 'r') as f:
            reader = csv.DictReader(f)
            existing_relationships = list(reader)
    except:
        existing_relationships = []
    
    # Combine relationships
    all_relationships = existing_relationships + unique_relationships
    
    # Write to CSV
    csv_headers = [
        'node1_table', 'node1_column', 'node1_report_number', 'node1_display',
        'predicate', 'predicate_display', 'node2_table', 'node2_column',
        'node1_report_number_copy', 'node2_display', 'Example'
    ]
    
    output_path = '/dropbox/03. Knowledge Graph/proper_mining_relationships.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in all_relationships:
            writer.writerow(rel)
    
    print(f"Saved proper mining relationships to: {output_path}")
    
    print(f"Total relationships: {len(all_relationships)}")
    
    print("\nNew geographic relationships:")
    for i, rel in enumerate(unique_relationships):
        print(f"  {i+1}. {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")

if __name__ == "__main__":
    main()