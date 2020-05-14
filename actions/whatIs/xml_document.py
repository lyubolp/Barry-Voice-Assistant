"""
:version: 1.0
:author Lyuboslav Karev

    Holds the XMLDocument class and it's exception
"""
import xml.etree.ElementTree as ET
from content import Content, ContentType


class IncompatibleException(Exception):
    """The content cannot be formed with this XML file"""


class XMLDocument:
    """
    XMLDocument is the class that is used to read, write and parse XML documents.
    It can be also used to parse HTML files.
    It wraps some of the built-in xml manipulation functions is the xml.etree package
    """

    def __init__(self, path=None):
        """
        self._doc is the document itself, as a file
        self._root is the root element of the opened document
        self._path is the path to file itself (if no path is presented, the class assumes the path
            is "./temp.xml"
        """
        self._doc = None
        self._root = None
        if path is None:
            self._path: str = "temp.xml"
        else:
            self._path = path

    def open(self, file_path: str):
        """
        Opens a file located and tries to parse it.
        If the file does not exist, throws a FileNotFoundError exception.
        If the file cannot be parsed, throws a xml.etree.ElementTree.ParseError exception.

        :param file_path: the location of the file
        """
        self._doc = ET.parse(file_path)
        self._root = self._doc.getroot()
        self._path = file_path

    def open_from_string(self, xml_string: str):
        """
        Reads a string and tries to parse it.
        If the string cannot be parsed, throws a xml.etree.ElementTree.ParseError exception.
        :param xml_string: the XML string
        :return: None
        """
        self._root = ET.fromstring(xml_string)

    def save(self):
        """
        Saves the current XML tree to the file.
        :return:
        """
        data = ET.tostring(self._root).decode("utf-8")
        file = open(self._path, "w")
        file.write(data)

    def add_element(self, parent_tag: str, tag: str, content: str, attributes: dict = dict()):
        """
        Adds an subelement to an element
        :param parent_tag: the name of the tag to act as a parent of the new element
        :param tag: the tag of the new element
        :param content: the content of the next element
        :param attributes: (Optional) - key/value pairs with the attributes
        :return: None
        """
        added_item = ET.SubElement(self.get_last_element(parent_tag), tag, attributes)
        added_item.text = content

    def add_attribute(self, tag: str, key_value: (str, str)):
        """
        Adds an attribute to an element
        :param tag: The name of the element
        :param key_value: pair of strings - key, value to add to the attributes list
        :return: None
        """
        self.get_last_element(tag).attrib[key_value[0]] = key_value[1]

    def add_content(self, tag: str, content: str):
        """
        Adds content to an element
        :param tag: The name of the element
        :param content: The content itself
        :return:
        """
        self.get_last_element(tag).text = content

    def edit_element(self, old_tag: str, new_tag: str):
        """
        Changes the name (the tag) of the element
        :param old_tag:
        :param new_tag:
        :return: None
        """
        self.get_first_element(old_tag).tag = new_tag

    def edit_attribute(self, tag: str, key_value: (str, str)):
        """
        Changes an attribute of an element
        :param tag: The name of the element
        :param key_value: key_value: pair of strings - key, value to add to the attributes list
        :return: None
        """
        self.get_first_element(tag).attrib[key_value[0]] = key_value[1]

    def edit_content(self, tag: str, content: str):
        """
        Changes the content of an element
        :param tag: The name of the element
        :param content: The new content
        :return: None
        """
        self.get_first_element(tag).text = content

    def get_elements(self, name: str) -> list:
        """
        Returns all elements with a given name
        :param name:
        :return: list of ET.Element, containing all the elements with the given name
        """
        return self._root.findall(".//" + name)

    def get_first_element(self, name: str) -> ET.Element:
        """
        Returns the first tag that matches name
        :param name:
        :return: an ET.Element, that represents the element searched.
        """
        if self._root.tag == name:
            return self._root
        return self._root.find(".//" + name)

    def get_last_element(self, name: str) -> ET.Element:
        """
        Returns the first tag that matches name
        :param name:
        :return: an ET.Element, that represents the element searched.
        """
        if self._root.tag == name:
            return self._root
        return self._root.findall(".//" + name)[-1]

    def get_attributes(self, tag: str) -> dict:
        """
        Returns all attributes of an element
        :param tag: The name of the element, for which we want it's attributes.
        :return: A dict of the attributes - key/value
        """
        return self.get_first_element(tag).attrib

    def get_content(self, tag: str) -> str:
        """
        Returns the content of an element
        :param tag: The name of the element to search
        :return: str containing the content of the element
        """
        return self.get_first_element(tag).text

    def get_root(self) -> ET.Element:
        """
        :return: the root element of the document (useful for iterating through the elements)
        """
        return self._root

    def remove_element(self, tag: str):
        """
        Removes an element
        :param tag: the name of the element to remove
        :return: None
        """
        parent_of_element = self._root.find(".//" + tag + "/..")
        parent_of_element.remove(self.get_first_element(tag))

    def remove_attribute(self, tag: str, attribute_name: str):
        """
        Removes an attribute from an element
        :param tag: The name of the element
        :param attribute_name: The attribute to remove
        :return: None
        """
        del self.get_attributes(tag)[attribute_name]

    def remove_content(self, tag: str):
        """
        Clears the content of an element
        :param tag: The name of the element
        :return: None
        """
        self.get_first_element(tag).text = None

    def init_with_root(self, root_name: str):
        """
        Initializes the XMLDocument with a root element
        :param root_name: The name of the root element
        """
        self._root = ET.Element(root_name)

    def to_string(self) -> str:
        """
        Convert the XML tree to string
        :return: the xml as a string, non-formatted
        """
        return str(ET.tostring(self._root, encoding="unicode", method="xml"))

    def fill_content(self, article: Content):
        """
        Fills the current XMLDocument with content (headers, text and images)
        :param article: The Content object that has the article
        """
        content_index = 0
        for element in self._root:
            is_text_matching = (element.tag == 'text' and
                                article.content[content_index][0] == ContentType.TEXT)
            is_title_matching = (element.tag == 'title' and
                                 article.content[content_index][0] == ContentType.TITLE)
            is_image_matching = (element.tag == 'image' and
                                 article.content[content_index][0] == ContentType.IMAGE)

            if is_text_matching or is_title_matching:
                element.text = article.content[content_index][1]
                content_index += 1
            elif is_image_matching:
                element.attrib['src'] = article.content[content_index][1].src
                content_index += 1
            else:
                raise IncompatibleException

    def get_path(self) -> str:
        """
        :return: The path of the current XMLDocument
        """
        return self._path
