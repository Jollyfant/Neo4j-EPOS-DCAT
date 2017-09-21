import os

from src.neo4jdriver import Neo4JDB
from src.XMLParser import EPOSXMLParser

class EPOSClassRegistration:

  EPOS_DOMAINS = [
    "Seismology",
    "Near-Fault Observatories",
    "GNSS Data and Products",
    "Volcano Observatories",
    "Satellite Date",
    "Geomagnetic Observations",
    "Anthropogenic Hazards",
    "Geological Information and Modeling",
    "Multi-Scale Laboratories",
    "Geo-Energy Test Beds for Low Carbon Energy"
  ]

  def __init__(self):
    
    # Create connection to Neo4J
    self.DB = Neo4JDB()

  def StoreEdge(self, edge):
    self.DB.CreateEdges(edge)

  def StoreNode(self, node):
    self.DB.CreateNode(node)

  def Register(self, XMLDocument):

    """
    EPOSClassRegistration.Register
    Registers a file to the EPOS Database
    """

    Parser = EPOSXMLParser(XMLDocument)
    return Parser.node

if __name__ == "__main__":

  R = EPOSClassRegistration()

  # Initiallize collect all edges
  # these can only be added once all vertices are in place
  edges = []

  # Register all the nodes with EPOS
  for root, directories, files in os.walk("vertices"):
    for file in files:
      if file.endswith(".xml"):

        # Register an object
        node = R.Register(os.path.join(root, file))
        R.StoreNode(node)
        edges.extend(node.edges)

  R.StoreEdge(edges)
