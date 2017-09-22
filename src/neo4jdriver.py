import json
from neo4j.v1 import GraphDatabase, basic_auth

with open("config.json") as conf:
  CONFIG = json.load(conf)  

class Neo4JDB:

  """
  Neo4J Database Class for EPOS Metadata ingestion
  """

  host = "bolt://%s:%s" % (CONFIG["HOST"], CONFIG["PORT"])

  def __init__(self):

    # Get a driver
    self.driver = GraphDatabase.driver(
      self.host,
      auth=basic_auth(CONFIG["USER"], CONFIG["PASS"])
    )

  def CreateNode(self, thing):

    """
    Neo4JDB.CreateNode
    Attempts to create a new node if it does not exist
    """

    # Check if the node exists
    if self.driver.session().run(thing.Match).single() is None:
      print "Added node of type %s" % thing
      self.driver.session().run(thing.Create)
    else:
      print "Node of type %s exists. Skipping." % thing.__class__ 

  def CreateEdges(self, edges):
    for edge in edges:
      print "Adding edge."
      self.driver.session().run(edge)
