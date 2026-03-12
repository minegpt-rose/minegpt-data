
# MineGPT Edge Relationship Processor
# Row-by-row mapping based on comprehensive_edge_dictionary_curated

import csv

class EdgeProcessor:
    def __init__(self, edge_dictionary_path):
        self.edge_mappings = self._load_edge_dictionary(edge_dictionary_path)
        
    def _load_edge_dictionary(self, path):
        # Load the edge dictionary
        mappings = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 12:  # Ensure we have enough columns
                        mappings.append({
                            'category': row[0],
                            'node1_table': row[1],
                            'node1_column': row[2],
                            'predicate': row[5],
                            'predicate_display': row[6],
                            'node2_table': row[7],
                            'node2_column': row[8],
                            'example': row[11]
                        })
        except Exception as e:
            print(f'Error loading edge dictionary: {e}')
        return mappings
    
    def find_relationships_for_column(self, table_name, column_name):
        # Find all relationships for a specific table.column
        matches = []
        for mapping in self.edge_mappings:
            if (mapping['node1_table'] == table_name and 
                mapping['node1_column'] == column_name):
                matches.append(mapping)
        return matches
    
    def process_database_row(self, table_name, column_name, value):
        # Process a database row and return relationships
        relationships = []
        
        # Find matching edge mappings
        mappings = self.find_relationships_for_column(table_name, column_name)
        
        for mapping in mappings:
            relationships.append({
                'source_table': table_name,
                'source_column': column_name,
                'source_value': value,
                'relationship_type': mapping['predicate'],
                'target_table': mapping['node2_table'],
                'target_column': mapping['node2_column'],
                'example': mapping['example']
            })
        
        return relationships

# Usage example
if __name__ == '__main__':
    processor = EdgeProcessor('comprehensive_edge_dictionary_curated.csv')
    
    # Test with general_information.project_name
    relationships = processor.find_relationships_for_column('general_information', 'project_name')
    print(f'Found {len(relationships)} relationships for project_name:')
    for rel in relationships:
        print(f'  - {rel["predicate"]} → {rel["node2_table"]}.{rel["node2_column"]}')
