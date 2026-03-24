#!/usr/bin/env python3
"""
Quality Relationship Builder

Focuses on creating high-quality, meaningful relationships following Francisca's examples.
Removes duplicate and self-referential relationships.
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

def create_quality_relationships(variables):
    """Create high-quality relationships following Francisca's examples"""
    relationships = []
    
    # Get project_name variable
    project_name_var = next((v for v in variables if v['table_name'] == 'general_information' and v['column_name'] == 'project_name'), None)
    
    # Create relationships following Francisca's exact examples
    if project_name_var:
        # 1. Project ownership (Côté Gold — owned_by → Agnico Eagle)
        company_var = next((v for v in variables if v['table_name'] == 'general_information' and v['column_name'] == 'company_name'), None)
        if company_var:
            relationships.append(create_relationship(
                'general_information', 'project_name',
                'general_information', 'company_name',
                'owned_by', 'Owned By'
            ))
        
        # 2. Location relationships (Côté Gold — located_in → Canada)
        location_vars = ['country', 'province', 'district', 'state', 'region']
        for loc_var in location_vars:
            loc = next((v for v in variables if v['table_name'] == 'general_information' and v['column_name'] == loc_var), None)
            if loc:
                relationships.append(create_relationship(
                    'general_information', 'project_name',
                    'general_information', loc_var,
                    'located_in', 'Located In'
                ))
        
        # 3. Town relationships (Detour Lake — near_town → Cochrane)
        nearest_town = next((v for v in variables if v['table_name'] == 'general_information' and 'town' in v['column_name'].lower()), None)
        if nearest_town:
            relationships.append(create_relationship(
                'general_information', 'project_name',
                'general_information', nearest_town['column_name'],
                'near_town', 'Near Town'
            ))
        
        # 4. Coordinate relationships (Kamoa-Kakula — at_coordinates → POINT(...))
        coord_var = next((v for v in variables if v['table_name'] == 'general_information' and 'coordinate' in v['column_name'].lower()), None)
        if coord_var:
            relationships.append(create_relationship(
                'general_information', 'project_name',
                'general_information', coord_var['column_name'],
                'at_coordinates', 'At Coordinates'
            ))
        
        # 5. Commodity relationships (Brucejack — produces → Gold)
        commodity_var = next((v for v in variables if v['table_name'] == 'general_information' and 'commodity' in v['column_name'].lower()), None)
        if commodity_var:
            relationships.append(create_relationship(
                'general_information', 'project_name',
                'commodity_groups', 'commodity',
                'produces', 'Produces'
            ))
        
        # 6. Project stage (Horne 5 — has_stage → Feasibility)
        stage_var = next((v for v in variables if v['table_name'] == 'general_information' and 'stage' in v['column_name'].lower()), None)
        if stage_var:
            relationships.append(create_relationship(
                'general_information', 'project_name',
                'project_entities', 'project_stage',
                'has_stage', 'Has Stage'
            ))
        
        # 7. Mine type (Voisey's Bay — has_mine_type → Underground)
        mine_type_var = next((v for v in variables if v['table_name'] == 'general_information' and 'mine_type' in v['column_name'].lower()), None)
        if mine_type_var:
            relationships.append(create_relationship(
                'general_information', 'project_name',
                'mine_entities', 'mine_type',
                'has_mine_type', 'Has Mine Type'
            ))
        
        # 8. Deposit type (Eskay Creek — has_deposit_type → VMS)
        deposit_var = next((v for v in variables if v['table_name'] == 'general_information' and 'deposit_type' in v['column_name'].lower()), None)
        if deposit_var:
            relationships.append(create_relationship(
                'general_information', 'project_name',
                'deposit_types', 'deposit_type',
                'has_deposit_type', 'Has Deposit Type'
            ))
        
        # 9. Start year (Côté Gold — has_start_year → 2023)
        start_year_var = next((v for v in variables if v['table_name'] == 'general_information' and 'start_year' in v['column_name'].lower()), None)
        if start_year_var:
            relationships.append(create_relationship(
                'general_information', 'project_name',
                'temporal_entities', 'start_year',
                'has_start_year', 'Has Start Year'
            ))
        
        # 10. Currency (uses_currency → CAD/USD)
        currency_var = next((v for v in variables if v['table_name'] == 'general_information' and 'currency' in v['column_name'].lower()), None)
        if currency_var:
            relationships.append(create_relationship(
                'general_information', 'project_name',
                'financial_metrics', 'currency',
                'uses_currency', 'Uses Currency'
            ))
    
    # Add relationships from other tables to project_name
    for var in variables:
        if var['table_name'] != 'general_information':
            # Only create meaningful relationships (not every variable)
            column_lower = var['column_name'].lower()
            
            # Cost-related variables
            if any(cost_keyword in column_lower for cost_keyword in ['capex', 'opex', 'cost', 'expenditure', 'investment']):
                relationships.append(create_relationship(
                    var['table_name'], var['column_name'],
                    'general_information', 'project_name',
                    'has_cost', 'Has Cost'
                ))
            
            # Production-related variables
            if any(prod_keyword in column_lower for prod_keyword in ['production', 'throughput', 'capacity', 'tonnage']):
                relationships.append(create_relationship(
                    var['table_name'], var['column_name'],
                    'general_information', 'project_name',
                    'has_production', 'Has Production'
                ))
            
            # Resource-related variables
            if any(res_keyword in column_lower for res_keyword in ['resource', 'reserve', 'grade', 'tonnage']):
                relationships.append(create_relationship(
                    var['table_name'], var['column_name'],
                    'general_information', 'project_name',
                    'has_resource', 'Has Resource'
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
    print("Creating quality relationships...")
    variables = load_variable_database()
    
    if not variables:
        print("Failed to load variables")
        return
    
    print(f"Loaded {len(variables)} variables")
    
    relationships = create_quality_relationships(variables)
    
    print(f"Generated {len(relationships)} quality relationships")
    
    # Write to CSV
    csv_headers = [
        'node1_table', 'node1_column', 'node1_report_number', 'node1_display',
        'predicate', 'predicate_display', 'node2_table', 'node2_column',
        'node1_report_number_copy', 'node2_display', 'Example'
    ]
    
    output_path = '/dropbox/03. Knowledge Graph/quality_relationships.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in relationships:
            writer.writerow(rel)
    
    print(f"Saved quality relationships to: {output_path}")
    
    # Show relationship type breakdown
    print("\nRelationship type breakdown:")
    rel_counts = {}
    for rel in relationships:
        rel_type = rel['predicate']
        rel_counts[rel_type] = rel_counts.get(rel_type, 0) + 1
    
    for rel_type, count in sorted(rel_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {rel_type}: {count}")
    
    print("\nSample relationships:")
    for i, rel in enumerate(relationships[:15]):
        print(f"  {i+1}. {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")

if __name__ == "__main__":
    main()