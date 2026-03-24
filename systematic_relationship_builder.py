#!/usr/bin/env python3
"""
Systematic Relationship Builder

Work through each variable row by row to create meaningful mining relationships
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
    except Exception as app:
        print(f"Error loading variable database: {app}")
        return []
    
    return variables

def analyze_variable(variable, index):
    """Analyze a single variable and return meaningful relationships"""
    relationships = []
    
    table_name = variable['table_name']
    column_name = variable['column_name']
    column_lower = column_name.lower()
    notes = variable.get('notes', '').lower()
    
    # Skip report_number columns (primary keys)
    if 'report_number' in column_lower:
        return relationships
    
    # Skip non-mining fields
    if 'pipeline' in column_lower or 'campaign' in column_lower:
        return relationships
    
    # Variable-specific relationships
    if table_name == 'critical_minerals_project_info':
        if column_name == 'project_name':
            # Same project across tables
            relationships.append(create_relationship(
                table_name, column_name,
                'general_information', 'project_name',
                'same_project', 'Same Project'
            ))
        elif column_name == 'report_year':
            # Year for the project
            relationships.append(create_relationship(
                table_name, column_name,
                'general_information', 'project_name',
                'report_year_for', 'Report Year For'
            ))
        elif column_name == 'commodity_focus':
            # Project produces this commodity
            relationships.append(create_relationship(
                'general_information', 'project_name',
                table_name, column_name,
                'produces', 'Produces'
            ))
        elif column_name == 'deposit_type':
            # Project has this deposit type
            relationships.append(create_relationship(
                'general_information', 'project_name',
                table_name, column_name,
                'has_deposit_type', 'Has Deposit Type'
            ))
        elif column_name == 'geological_model':
            # Project uses this geological model
            relationships.append(create_relationship(
                'general_information', 'project_name',
                table_name, column_name,
                'uses_geological_model', 'Uses Geological Model'
            ))
    
    elif table_name == 'critical_minerals_extracted_sc':
        if column_name == 'mineral_name':
            # Project produces this mineral
            relationships.append(create_relationship(
                'general_information', 'project_name',
                table_name, column_name,
                'produces', 'Produces'
            ))
        elif column_name == 'classification':
            # Mineral has this classification
            relationships.append(create_relationship(
                table_name, 'mineral_name',
                table_name, column_name,
                'has_classification', 'Has Classification'
            ))
        elif column_name == 'geological_association':
            # Mineral has this geological association
            relationships.append(create_relationship(
                table_name, 'mineral_name',
                table_name, column_name,
                'has_geological_association', 'Has Geological Association'
            ))
        elif column_name == 'economic_potential':
            # Mineral has this economic potential
            relationships.append(create_relationship(
                table_name, 'mineral_name',
                table_name, column_name,
                'has_economic_potential', 'Has Economic Potential'
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
    
    print("\nAnalyzing variables row by row...")
    
    # Start from row 22 (after general_information)
    start_index = 22
    new_relationships = []
    
    for i in range(start_index, min(start_index + 20, len(variables))):
        variable = variables[i]
        print(f"Analyzing row {i+1}: {variable['table_name']}.{variable['column_name']}")
        
        relationships = analyze_variable(variable, i)
        new_relationships.extend(relationships)
        
        if relationships:
            print(f"  Added {len(relationships)} relationships")
            for rel in relationships:
                print(f"    {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")
    
    print(f"\nGenerated {len(new_relationships)} new relationships")
    
    # Load existing relationships
    existing_relationships = []
    try:
        with open('/dropbox/03. Knowledge Graph/proper_mining_relationships.csv', 'r') as f:
            reader = csv.DictReader(f)
            existing_relationships = list(reader)
    except:
        existing_relationships = []
    
    # Combine relationships
    all_relationships = existing_relationships + new_relationships
    
    # Write to CSV
    csv_headers = [
        'node1_table', 'node1_column', 'node1_report_number', 'node1_display',
        'predicate', 'predicate_display', 'node2_table', 'node2_column',
        'node1_report_number_copy', 'node2_display', 'node2_display',
        'Example'
    ]
    
    output_path = '/dropbox/03. Knowledge Graph/expanded_mining_relationships.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in all_relationships:
            writer.writerow(rel)
    
    print(f"Saved expanded mining relationships to: {output_path}")
    print(f"Total relationships: {len(all_relationships)}")

if __name__ == "__main__":
    main()