from bears.xml.XMLBear import XMLBear
from tests.LocalBearTestHelper import verify_local_bear


valid_xml_file = """<?xml version="1.0"?>
<a/>
""".splitlines(keepends=True)

invalid_xml_file = """
<a>blah</a>
""".splitlines(keepends=True)

invalid_xml_chars = """<?xml version="1.0"?>
<a>hey & hi</a>
""".splitlines(keepends=True)

valid_xml_chars = """<?xml version="1.0"?>
<a>hey and hi</a>
""".splitlines(keepends=True)

InvalidXMLCorrectedTest = verify_local_bear(
                                        XMLBear,
                                        valid_files=(valid_xml_file,),
                                        invalid_files=(invalid_xml_file,),
                                        tempfile_kwargs={"suffix": ".xml"})

InvalidXMLSyntaxTest = verify_local_bear(
                                        XMLBear,
                                        valid_files=(valid_xml_chars,),
                                        invalid_files=(invalid_xml_chars,),
                                        tempfile_kwargs={"suffix": ".xml"})
