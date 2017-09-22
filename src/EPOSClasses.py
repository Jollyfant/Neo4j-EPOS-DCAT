import xml.etree.ElementTree
import hashlib

class EPOSClass:

  """
  Master class for EPOS Nodes
  All EPOS classes inherit from this class
  Prepares attributes for insertion in Neo4J
  """

  # Namespace definitions for XML parsing
  NAMESPACES = {
    "dct": "{http://purl.org/dc/terms/}",
    "dcat": "{http://www.w3.org/ns/dcat#}",
    "locn": "{http://www.w3.org/ns/locn#}",
    "schema": "{http://schema.org/}",
    "vcard": "{http://www.w3.org/2006/vcard/ns#}",
    "epos": "{http://www.epos-ip.org/terms.html}",
    "eposap": "{http://www.epos-ip.org/terms.html}"
  }

  def __init__(self, URI):

    self.URI = URI

    # Add the Unique Resource Identifier to the node
    self.query = ["`dct:identifier`:'" + self.URI + "'"]

    self.edges = []


  def GetResourceLabel(self, identifier):

    """
    EPOSClass.GetResourceLabel
    Returns class of the relationship endpoint
    """

    if identifier == "eposap:legalContact":
      return "eposap:Person"
    elif identifier == "eposap:financialContact":
      return "eposap:Person"
    elif identifier == "dcat:contactPoint":
      return "eposap:Person"
    elif identifier == "eposap:affiliation":
      return "eposap:Organization"
    elif identifier == "eposap:publisher":
      return "eposap:Organization"
    else:
      raise ValueError("Unknown resource label (%s)" % identifier)


  def CreateEdgeQuery(self, fromLabel, fromURI, toLabel, toURI, relation):

    """
    EPOSClass.CreateEdgeQuery
    Creates neo4j query to connect two vertices (x, y), with a relation (r) (x -[r]-> y)
    """

    # Node identification from URI dct:identifier
    x = "(x:" + fromLabel + " {`dct:identifier`:'" + fromURI + "'})"
    y = "(y:" + toLabel + " {`dct:identifier`:'" + toURI + "'})"
    r = "(x)-[:`" + relation + "`]->(y)"

    # Concatenate and append the edge query
    self.edges.append("MATCH %s, %s MERGE %s" % (x, y, r))


  def AddEdge(self, root, identifier):

    namespace, name = identifier.split(":")
    _element = root.find(self.Namespace(namespace) + name)

    if _element is not None and _element.text is not None:

      # Get the label of the target
      targetLabel = self.GetResourceLabel(identifier)
      self.CreateEdgeQuery(self.Label, self.URI, targetLabel, _element.text, identifier)

  def AddAttribute(self, root, identifier):

    # Get the namespace:name (e.g. vcard:fn)
    namespace, name = identifier.split(":")
    _element = root.find(self.Namespace(namespace) + name)

    # Check if the attribute exists (add a string)
    if _element is not None and _element.text is not None:
      self.query.append("`" + identifier + "`:'" + _element.text + "'")

  def Namespace(self, name):
    return self.NAMESPACES[name]

  @property
  def Label(self):
    return "eposap:" + self.Name

  @property
  def Name(self):
    return self.__class__.__name__

  @property
  def Query(self):
    return ",".join(self.query)

  @property
  def Match(self):
    return "MATCH (x:" + self.Label + " { " + self.Query + " }) RETURN x"

  @property
  def Create(self):
    return "CREATE (x:" + self.Label + " { " + self.Query + " })"


class WebService(EPOSClass):

  """
  Subclass for EPOS WebService
  """

  def __init__(self, root, URI):

    EPOSClass.__init__(self, URI)

    # Check WebService namespace
    if root.tag != self.NAMESPACES["epos"] + "WebService":
      raise ValueError("Document does not have correct WebService namespace.")

    # dct attributes
    self.AddAttribute(root, "dct:title")
    self.AddAttribute(root, "dct:description")
    self.AddAttribute(root, "dct:issued")
    self.AddAttribute(root, "dct:modified")
    self.AddAttribute(root, "dct:license")
    self.AddAttribute(root, "dct:conformsTo")
    self.AddAttribute(root, "dct:identifier")
    self.AddAttribute(root, "dct:keyword")
    self.AddAttribute(root, "dct:hasVersion")

    # eposap attributes
    self.AddAttribute(root, "eposap:domain")
    self.AddAttribute(root, "eposap:subDomain")
    self.AddAttribute(root, "eposap:operation")

    self.AddEdge(root, "dcat:contactPoint")
    self.AddEdge(root, "eposap:publisher")


class Organization(EPOSClass):

  """
  Subclass for EPOS Node Organization
  """

  def __init__(self, root, URI):

    EPOSClass.__init__(self, URI)

    # Check Person namespace
    if root.tag != self.NAMESPACES["epos"] + "Organisation":
      raise ValueError("Document does not have correct Organisation namespace.")

    # vcard attributes
    self.AddAttribute(root, "vcard:fn")
    self.AddAttribute(root, "vcard:hasEmail")
    self.AddAttribute(root, "vcard:hasTelephone")
    self.AddAttribute(root, "vcard:hasURL")
    self.AddAttribute(root, "vcard:hasLogo")

    spatial = root.find(self.NAMESPACES["dct"] + "spatial").find(self.NAMESPACES["dct"] + "Location")
    self.AddAttribute(spatial, "locn:geometry")

    # eposap:legalContact references a eposap:Person vertice
    self.AddEdge(root, "eposap:legalContact")
    self.AddEdge(root, "eposap:financialContact")
     

class Person(EPOSClass):

  """
  Subclass for EPOS Node Person
  """

  def __init__(self, root, URI):

    EPOSClass.__init__(self, URI)

    # Check Person namespace
    if root.tag != self.NAMESPACES["epos"] + "Person":
      raise ValueError("Document does not have correct Person namespace.")

    # vcard attributes
    self.AddAttribute(root, "vcard:fn")
    self.AddAttribute(root, "vcard:hasEmail")
    self.AddAttribute(root, "vcard:hasTelephone")
    self.AddAttribute(root, "vcard:hasURL")

    self.AddEdge(root, "eposap:affiliation")
