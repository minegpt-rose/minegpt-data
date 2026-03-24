#!/usr/bin/env python3
"""
Final Accurate Relationship Builder

Creates relationships using ONLY actual table and column names
Avoids self-references and ensures all relationships are meaningful
"""

import csv

def load_variable_database():
    """Load the variable database and organize by table"""
    tables = {}
    
    try:
        with open('/dropbox/03. Knowledge Graph/accurate_database_final_FL_corrected.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                table_name = row['table_name']
                if table_name not in tables:
                    tables[table_name] = []
                tables[table_name].append(row)
    except Exception as e:
        print(f"Error loading variable database: {e}")
        return {}
    
    return tables

def create_meaningful_relationships(tables):
    """Create meaningful relationships without self-references"""
    relationships = []
    
    # Get actual column names
    general_info_cols = [v['column_name'] for v in tables.get('general_information', [])]
    
    # Create relationships table by table
    for table_name, variables in tables.items():
        for variable in variables:
            column_name = variable['column_name']
            column_lower = column_name.lower()
            
            # Skip report_number columns
            if 'report_number' in column_lower:
                continue
            
            # 1. Relationships to project_name (only for non-general_info tables)
            if table_name != 'general_information' and 'project_name' in general_info_cols:
                relationships.append(create_relationship(
                    table_name, column_name,
                    'general_information', 'project_name',
                    'belongs_to_project', 'Belongs To Project'
                ))
            
            # 2. Unit relationships (only for actual _unit fields)
            if '_unit' in column_lower:
                base_var_name = column_name.replace('_unit', '')
                # Check if base variable exists in same table and is different
                table_cols = [v['column_name'] for v in tables.get(table_name, [])]
                if base_var_name in table_cols and base_var_name != column_name:
                    relationships.append(create_relationship(
                        table_name, base_var_name,
                        table_name, column_name,
                        'has_unit', 'Has Unit'
                    ))
            
            # 3. Cost relationships (only for cost_table)
            if table_name == 'cost_table':
                if any(keyword in column_lower for keyword in ['mining', 'process', 'tailings', 'infrastructure']):
                    if 'total_initial_direct_capex' in [v['column_name'] for v in tables['cost_table']]:
                        relationships.append(create_relationship(
                            table_name, column_name,
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
    tables = load_variable_database()
    
    if not tables:
        print("Failed to load variables")
        return
    
    print(f"Loaded {len(tables)} tables")
    
    print("\nCreating meaningful relationships...")
    relationships = create_meaningful_relationships(tables)
    
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
    
    output_path = '/dropbox/03. Knowledge Graph/meaningful_edge_dictionary.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in unique_relationships:
            writer.writerow(rel)
    
    print(f"Saved meaningful edge dictionary to: {output_path}")
    
    # Show relationship type breakdown
    print("\nRelationship type breakdown:")
    rel_counts = {}
    for rel in unique_relationships:
        rel_type = rel['predicate']
        rel_counts[rel_type] = rel_counts.get(rel_type, 0) + 1
    
    for rel_type, count in sorted(rel_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {rel_type}: {count}")
    
    print("\nSample relationships:")
    for i, rel in enumerate(unique_relationships[:15]):
        print(f"  {i+1}. {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")

if __name__ == "__main__":
    main()