#!/usr/bin/env python3
"""
Accurate Relationship Builder

Uses ONLY actual table and column names from the database
Avoids hallucination by working with real data only
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

def get_actual_column_names(tables, table_name):
    """Get actual column names for a table"""
    if table_name in tables:
        return [v['column_name'] for v in tables[table_name]]
    return []

def create_accurate_relationships(tables):
    """Create relationships using ONLY actual table and column names"""
    relationships = []
    
    # Get actual column names for key tables
    general_info_cols = get_actual_column_names(tables, 'general_information')
    
    # Only create relationships for variables that actually exist
    for table_name, variables in tables.items():
        for variable in variables:
            column_name = variable['column_name']
            column_lower = column_name.lower()
            
            # Skip report_number columns
            if 'report_number' in column_lower:
                continue
            
            # 1. Relationships to project_name (only if project_name exists)
            if table_name != 'general_information' and 'project_name' in general_info_cols:
                relationships.append(create_relationship(
                    table_name, column_name,
                    'general_information', 'project_name',
                    'belongs_to_project', 'Belongs To Project'
                ))
            
            # 2. Company relationships (only if company_name exists)
            if ('company' in column_lower or 'owner' in column_lower or 'operator' in column_lower) and 'company_name' in general_info_cols:
                relationships.append(create_relationship(
                    table_name, column_name,
                    'general_information', 'company_name',
                    'related_to_company', 'Related To Company'
                ))
            
            # 3. Geographic relationships (only for actual location fields)
            location_fields = ['country', 'province', 'state', 'region', 'district', 'location', 'coordinates']
            for loc_field in location_fields:
                if loc_field in column_lower and loc_field in general_info_cols:
                    relationships.append(create_relationship(
                        table_name, column_name,
                        'general_information', loc_field,
                        'located_in', 'Located In'
                    ))
            
            # 4. Unit relationships (only for actual _unit fields)
            if '_unit' in column_lower:
                base_var_name = column_name.replace('_unit', '')
                # Check if base variable exists in same table
                table_cols = get_actual_column_names(tables, table_name)
                if base_var_name in table_cols:
                    relationships.append(create_relationship(
                        table_name, base_var_name,
                        table_name, column_name,
                        'has_unit', 'Has Unit'
                    ))
            
            # 5. Cost relationships (only for cost-related tables)
            if table_name == 'cost_table' and any(keyword in column_lower for keyword in ['cost', 'capex', 'opex', 'expenditure']):
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
    
    print("\nCreating accurate relationships...")
    relationships = create_accurate_relationships(tables)
    
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
    
    output_path = '/dropbox/03. Knowledge Graph/accurate_edge_dictionary.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in unique_relationships:
            writer.writerow(rel)
    
    print(f"Saved accurate edge dictionary to: {output_path}")
    
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