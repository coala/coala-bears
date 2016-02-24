from bears.xml.XMLBear import XMLBear
from tests.LocalBearTestHelper import verify_local_bear


valid_xml_file = """
<?xml version="1.0"?>
<a/>
""".splitlines(keepends=True)

invalid_xml_file = """
<a>blah</a>
""".splitlines(keepends=True)

InvalidXMLTest = verify_local_bear(XMLBear,
                                   valid_files=(valid_xml_file,),
                                   invalid_files=(invalid_xml_file,),)
