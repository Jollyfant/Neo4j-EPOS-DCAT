from neo4j.v1 import GraphDatabase, basic_auth

class Neo4JDB:

  """
  Neo4J Database Class for EPOS Metadata ingestion
  """

  USER = "neo4j"
  PASS = "fjyjer"
  HOST = "localhost"
  PROTOCOL = "bolt://"

  PORT = 7687

  def __init__(self):

    # Get a driver
    self.driver = GraphDatabase.driver(
      self.PROTOCOL + self.HOST + ":" + str(self.PORT),
      auth=basic_auth(self.USER, self.PASS)
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
      self.driver.session().run(edge)
