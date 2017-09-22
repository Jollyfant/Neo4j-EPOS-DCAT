import xml.etree.ElementTree
from EPOSClasses import Person, Organization, WebService, Project, Publication

class EPOSXMLParser:

  """
  EPOSXMLParser
  Class for parsing EPOSXML
  """

  EPOS = "{http://www.epos-ip.org/terms.html}"

  def __init__(self, XMLDocument):

    self.root = xml.etree.ElementTree.parse(XMLDocument).getroot()

    # The root tag is incorrect
    if self.root.tag != self.EPOS + "Epos":
      raise ValueError("Document does not have correct Epos namespace (%s)" % XMLDocument)

    # Each document may only have a single document
    # as the path of the document is its URI.
    if len(self.root) > 1:
      raise ValueError("Document contains multiple objects.")

    identifier = XMLDocument

    for branch in self.root:

      # Get the tags branch
      if branch.tag == self.EPOS + "Person":
        self.node = Person(branch, identifier)
      elif branch.tag == self.EPOS + "Organisation":
        self.node = Organization(branch, identifier)
      elif branch.tag == self.EPOS + "WebService":
        self.node = WebService(branch, identifier)
      elif branch.tag == self.EPOS + "Project":
        self.node = Project(branch, identifier)
      elif branch.tag == self.EPOS + "Publication":
        self.node = Publication(branch, identifier)
