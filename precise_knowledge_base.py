#!/usr/bin/env python3
"""
Precise Knowledge Base Builder

More precise relationship logic to avoid incorrect connections
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

def should_create_relationship(node1, node2):
    """Determine if a relationship should exist between two variables"""
    table1 = node1['table_name']
    col1 = node1['column_name']
    table2 = node2['table_name']
    col2 = node2['column_name']
    
    col1_lower = col1.lower()
    col2_lower = col2.lower()
    notes1 = node1.get('notes', '').lower()
    notes2 = node2.get('notes', '').lower()
    
    # Skip report_number columns
    if 'report_number' in col1_lower or 'report_number' in col2_lower:
        return None
    
    # Skip self-references
    if table1 == table2 and col1 == col2:
        return None
    
    # Unit relationships (base variables -> their units)
    if '_unit' in col2_lower:
        base_var = col2.replace('_unit', '')
        if table1 == table2 and col1 == base_var:
            return ('has_unit', 'Has Unit')
    
    # Cost relationships (cost components -> total costs)
    if table1 == 'cost_table' and table2 == 'cost_table':
        if 'total_initial_direct_capex' in col2_lower:
            if any(keyword in col1_lower for keyword in ['mining', 'process', 'plant', 'tailings', 'infrastructure', 'closure']):
                return ('contributes_to', 'Contributes To')
    
    # Geographic relationships (project -> location)
    if col1 == 'project_name' and table1 == 'general_information':
        if any(loc_field in col2_lower for loc_field in ['country', 'province', 'state', 'region', 'district']):
            if table2 == 'general_information':
                return ('is_located_at', 'Is Located At')
    
    # Project produces commodities
    if col1 == 'project_name' and table1 == 'general_information':
        if 'commodity' in col2_lower and 'commodity' in notes2:
            return ('produces', 'Produces')
    
    # Project has deposit type
    if col1 == 'project_name' and table1 == 'general_information':
        if 'deposit_type' in col2_lower and 'deposit' in notes2:
            return ('has_deposit_type', 'Has Deposit Type')
    
    # Project uses geological model
    if col1 == 'project_name' and table1 == 'general_information':
        if 'geological_model' in col2_lower and 'geological' in notes2:
            return ('uses_geological_model', 'Uses Geological Model')
    
    # Mineral relationships
    if col1 == 'mineral_name' and table1 == 'critical_minerals_extracted_sc':
        if table1 == table2:
            if 'classification' in col2_lower:
                return ('has_classification', 'Has Classification')
            elif 'geological_association' in col2_lower:
                return ('has_geological_association', 'Has Geological Association')
            elif 'economic_potential' in col2_lower:
                return ('has_economic_potential', 'Has Economic Potential')
    
    return None

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
    
    print("\nBuilding precise knowledge base...")
    relationships = []
    
    # For each variable as node1
    for i, node1 in enumerate(variables):
        if i % 50 == 0:
            print(f"Processing variable {i+1}/{len(variables)}")
        
        # Compare with every other variable as node2
        for j, node2 in enumerate(variables):
            if i == j:
                continue
            
            # Determine if relationship should exist
            relationship_info = should_create_relationship(node1, node2)
            if relationship_info:
                predicate, predicate_display = relationship_info
                relationships.append(create_relationship(
                    node1['table_name'], node1['column_name'],
                    node2['table_name'], node2['column_name'],
                    predicate, predicate_display
                ))
    
    print(f"Generated {len(relationships)} relationships")
    
    # Remove duplicates
    unique_relationships = []
    seen = set()
    
    for rel in relationships:
        rel_key = f"{rel['node1_table']}.{rel['node1_column']}.{rel['node2_table']}.{rel['node2_column']}.{rel['predicate']}"
        if rel_key not in seen:
            seen.add(rel_key)
            unique_relationships.append(remainder of script...
I'll continue with the rest of the script but it was cut off. Let me run this and see the results:<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>exec{