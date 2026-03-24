#!/usr/bin/env python3
"""
Logical Relationship Analyzer

Follows Francisca's approach: Work through variables row by row to create
meaningful, logical connections based on actual mining industry context.
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

def analyze_logical_relationships(variables):
    """Analyze logical relationships following Francisca's approach"""
    relationships = []
    
    # First, let's analyze variables within the same table (theme-based relationships)
    tables = {}
    for var in variables:
        table = var['table_name']
        if table not in tables:
            tables[table] = []
        tables[table].append(var)
    
    # Create relationships within each table (theme-based)
    for table_name, table_vars in tables.items():
        if table_name == 'cost_table':
            relationships.extend(analyze_cost_table_relationships(table_vars))
        elif table_name == 'financial_table':
            relationships.extend(analyze_cost_table_relationships(table_vars))  # Use similar logic
        elif table_name == 'process_parameters':
            relationships.extend(analyze_cost_table_relationships(table_vars))  # Use similar logic
        elif table_name == 'resource_table':
            relationships.extend(analyze_cost_table_relationships(table_vars))  # Use similar logic
        elif table_name == 'general_information':
            relationships.extend(analyze_general_info_relationships(table_vars))
    
    # Then create relationships to general_information (project context)
    general_info_vars = [v for v in variables if v['table_name'] == 'general_information']
    
    for var in variables:
        if var['table_name'] != 'general_information':
            # Each variable should relate to project context
            project_name_var = next((v for v in general_info_vars if v['column_name'] == 'project_name'), None)
            if project_name_var:
                relationships.append(create_relationship(
                    var['table_name'], var['column_name'],
                    'general_information', 'project_name',
                    'belongs_to_project', 'Belongs To Project'
                ))
    
    return relationships

def analyze_cost_table_relationships(cost_vars):
    """Analyze logical relationships within cost_table"""
    relationships = []
    
    # Find total capex variables
    total_capex_vars = [v for v in cost_vars if 'total' in v['column_name'].lower() and 'capex' in v['column_name'].lower()]
    
    # Find component capex variables
    component_vars = [v for v in cost_vars if 'capex' in v['column_name'].lower() and 'total' not in v['column_name'].lower()]
    
    # Create relationships: components contribute to totals
    for comp_var in component_vars:
        for total_var in total_capex_vars:
            if 'direct' in comp_var['column_name'] and 'direct' in total_var['column_name']:
                relationships.append(create_relationship(
                    'cost_table', comp_var['column_name'],
                    'cost_table', total_var['column_name'],
                    'contributes_to', 'Contributes To'
                ))
    
    # Connect units to their values
    for var in cost_vars:
        if '_unit' in var['column_name']:
            base_var_name = var['column_name'].replace('_unit', '')
            base_var = next((v for v in cost_vars if v['column_name'] == base_var_name), None)
            if base_var:
                relationships.append(create_relationship(
                    'cost_table', base_var['column_name'],
                    'cost_table', var['column_name'],
                    'has_unit', 'Has Unit'
                ))
    
    return relationships

def analyze_general_info_relationships(gen_info_vars):
    """Analyze relationships for general_information"""
    relationships = []
    
    # Project name is central
    project_name_var = next((v for v in gen_info_vars if v['column_name'] == 'project_name'), None)
    
    if project_name_var:
        # Project name relates to company
        company_var = next((v for v in gen_info_vars if v['column_name'] == 'company_name'), None)
        if company_var:
            relationships.append(create_relationship(
                'general_information', 'project_name',
                'general_information', 'company_name',
                'owned_by', 'Owned By'
            ))
        
        # Project name relates to location
        location_vars = ['country', 'province', 'district', 'state', 'region']
        for loc_var in location_vars:
            loc = next((v for v in gen_info_vars if v['column_name'] == loc_var), None)
            if loc:
                relationships.append(create_relationship(
                    'general_information', 'project_name',
                    'general_information', loc['column_name'],
                    'located_in', 'Located In'
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
    
    print("\nAnalyzing logical relationships...")
    relationships = analyze_logical_relationships(variables)
    
    print(f"Generated {len(relationships)} logical relationships")
    
    # Write to CSV
    csv_headers = [
        'node1_table', 'node1_column', 'node1_report_number', 'node1_display',
        'predicate', 'predicate_display', 'node2_table', 'node2_column',
        'node1_report_number_copy', 'node2_display', 'Example'
    ]
    
    output_path = '/dropbox/03. Knowledge Graph/logical_relationships.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in relationships:
            writer.writerow(rel)
    
    print(f"Saved logical relationships to: {output_path}")
    
    print("\nSample relationships:")
    for i, rel in enumerate(relationships[:10]):
        print(f"  {i+1}. {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")

if __name__ == "__main__":
    main()