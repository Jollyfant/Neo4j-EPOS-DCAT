# Neo4j-EPOS-DCAT

Prototype implementation of relational EPOS metadata using graph database neo4j. The model consists of vertices (node) and edges (relationships between nodes) as is defined in the EPOS-DCAT .xml files. Relationships must point to an entry in the hierarchical vertices structure.

## Ingesting

Metadata is taken from the `vertices/` directory and added to the graph. Only a selection of attributes are added.

## Running

`python register.py`
