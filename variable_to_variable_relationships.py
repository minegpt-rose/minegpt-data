#!/usr/bin/env python3
"""
Variable-to-Variable Relationship Builder

Creates relationships where EACH variable becomes node1 and connects to OTHER variables as node2
following the exact format from comprehensive_edge_dictionary_curated
"""

import csv
import re
from typing import List, Dict

def load_variable_database() -> List[Dict]:
    """Load the complete variable database and return as a flat list"""
    variables = []
    
    try:
        with open('/dropbox/03. Knowledge Graph/accurate_database_final_FL_corrected.csv', 'r') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                variables.append({
                    'table': row['table_name'],
                    'column': row['column_name'],
                    'type': row.get('type', ''),
                    'notes': row.get('notes', ''),
                    'full_row': row
                })
    except Exception as e:
        print(f"Error loading variable database: {e}")
        return []
    
    return variables

def find_related_variables(source_var: Dict, all_variables: List[Dict]) -> List[Dict]:
    """Find other variables that relate to the source variable"""
    relationships = []
    
    source_table = source_var['table']
    source_column = source_var['column']
    source_type = source_var['type']
    source_notes = source_var['notes']
    source_lower = source_column.lower()
    
    # Skip report_number columns (handled separately)
    if source_column.lower() == 'report_number':
        return relationships
    
    # Look for relationships with other variables
    for target_var in all_variables:
        target_table = target_var['table']
        target_column = target_var['column']
        target_type = target_var['type']
        target_notes = target_var['notes']
        target_lower = target_column.lower()
        
        # Don't create relationships to self
        if source_table == target_table and source_column == target_column:
            continue
        
        # 1. Same column name across different tables
        if source_column == target_column and source_table != target_table:
            relationships.append(create_relationship(
                source_table, source_column, target_table, target_column,
                'same_column_across_tables', 'Same Column Across Tables'
            ))
        
        # 2. Foreign key relationships
        if 'report_number' in source_lower and target_table == 'general_information' and 'report_number' in target_lower:
            relationships.append(create_relationship(
                source_table, source_column, target_table, target_column,
                'references_report', 'References Report'
            ))
        
        # 3. Semantic similarity
        if (('company' in source_lower and 'company' in target_lower) or
            ('project' in source_lower and 'project' in target_lower) or
            ('location' in source_lower and 'location' in target_lower) or
            ('date' in source_lower and 'date' in target_lower) or
            ('cost' in source_lower and 'cost' in target_lower) or
            ('price' in source_lower and 'price' in target_lower)):
            
            # Only create relationship if they're meaningfully different
            if source_column != target_column:
                rel_type = f"related_{source_lower.split('_')[0] if '_' in source_lower else source_lower}"
                relationships.append(create_relationship(
                    source_table, source_column, target_table, target_column,
                    rel_type, f"Related {source_column.replace('_', ' ').title()}"
                ))
        
        # 4. Type-based relationships
        if ('date' in source_type.lower() and 'date' in target_type.lower() and 
            source_column != target_column):
            relationships.append(create_relationship(
                source_table, source_column, target_table, target_column,
                'temporally_related', 'Temporally Related'
            ))
        
        if (('coordinate' in source_type.lower() or 'location' in source_type.lower()) and 
            ('coordinate' in target_type.lower() or 'location' in target_type.lower()) and
            source_column != target_column):
            relationships.append(create_relationship(
                source_table, source_column, target_table, target_column,
                'spatially_related', 'Spatially Related'
            ))
        
        # 5. Notes-based relationships
        if source_notes and target_notes:
            if ('project_list' in source_notes and 'project_list' in target_notes and
                source_column != target_column):
                relationships.append(create_relationship(
                    source_table, source_column, target_table, target_column,
                    'project_data_related', 'Project Data Related'
                ))
    
    return relationships

def create_relationship(source_table, source_column, target_table, target_column, predicate, predicate_display):
    """Create a relationship dictionary with proper formatting"""
    return {
        'node1_table': source_table,
        'node1_column': source_column,
        'node1_report_number': '',
        'node1_display': source_column.replace('_', ' ').title(),
        'predicate': predicate,
        'predicate_display': predicate_display,
        'node2_table': target_table,
        'node2_column': target_column,
        'node1_report_number_copy': '',
        'node2_display': target_column.replace('_', ' ').title(),
        'Example': f"{source_column} — {predicate} → {target_column}"
    }

def main():
    """Main function - create variable-to-variable relationships"""
    print("Loading complete variable database...")
    all_variables = load_variable_database()
    
    if not all_variables:
        print("Failed to load variable database")
        return
    
    print(f"Loaded {len(all_variables)} variables")
    
    all_relationships = []
    
    # Process each variable as node1
    for i, source_var in enumerate(all_variables):
        relationships = find_related_variables(source_var, all_variables)
        all_relationships.extend(relationships)
        
        # Show progress
        if (i + 1) % 50 == 0:
            print(f"Processed {i + 1} variables, {len(all_relationships)} relationships")
    
    print(f"\nTotal variables processed: {len(all_variables)}")
    print(f"Total relationships generated: {len(all_relationships)}")
    
    # Write to CSV with exact format
    csv_headers = [
        'node1_table', 'node1_column', 'node1_report_number', 'node1_display',
        'predicate', 'predicate_display', 'node2_table', 'node2_column',
        'node1_report_number_copy', 'node2_display', 'Example'
    ]
    
    output_path = '/dropbox/03. Knowledge Graph/variable_to_variable_relationships.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in all_relationships:
            writer.writerow(rel)
    
    print(f"Saved variable-to-variable relationships to: {output_path}")
    
    # Show relationship type breakdown
    print("\nRelationship type breakdown:")
    rel_counts = {}
    for rel in all_relationships:
        rel_type = rel['predicate']
        rel_counts[rel_type] = rel_counts.get(rel_type, 0) + 1
    
    for rel_type, count in sorted(rel_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {rel_type}: {count}")
    
    print("\nSample relationships:")
    for i, rel in enumerate(all_relationships[:10]):
        print(f"  {i+1}. {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")

if __name__ == "__main__":
    main()