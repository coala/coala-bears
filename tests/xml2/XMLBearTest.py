import os

from bears.xml2.XMLBear import XMLBear
from tests.LocalBearTestHelper import verify_local_bear


def load_testdata(filename):
    path = os.path.join(os.path.dirname(__file__),
                        "test_files",
                        filename)
    with open(path) as f:
        return f.read()

valid_xml_file = """<?xml version="1.0"?>
<a/>
"""

invalid_xml_file = """
<a>blah</a>
"""

invalid_xml_chars = """<?xml version="1.0"?>
<a>hey & hi</a>
"""

valid_xml_chars = """<?xml version="1.0"?>
<a>hey and hi</a>
"""

dtd_file = os.path.join(os.path.dirname(__file__),
                        "test_files",
                        "note.dtd")

schema_file = os.path.join(os.path.dirname(__file__),
                           "test_files",
                           "note.xsd")

valid_xml_path = load_testdata("note.xml")
valid_xml_url = load_testdata("concept-valid.xml")
invalid_xml_schema = load_testdata("xsd-error.xml")
invalid_xml_dtd = load_testdata("dtd-error.xml")
invalid_xml_url = load_testdata("concept-invalid.xml")

dtd_url = "http://docs.oasis-open.org/dita/v1.0.1/dtd/concept.dtd"

XMLBearCorrectedTest = verify_local_bear(
    XMLBear,
    valid_files=(valid_xml_file, valid_xml_chars),
    invalid_files=(invalid_xml_file, invalid_xml_chars),
    tempfile_kwargs={"suffix": ".xml"})

XMLBearSchemaTest = verify_local_bear(
    XMLBear,
    valid_files=(valid_xml_path,),
    invalid_files=(invalid_xml_schema,),
    settings={'xml_schema': schema_file},
    tempfile_kwargs={"suffix": ".xml"})

XMLBearDTDPathTest = verify_local_bear(
    XMLBear,
    valid_files=(valid_xml_path,),
    invalid_files=(invalid_xml_dtd,),
    settings={'xml_dtd': dtd_file},
    tempfile_kwargs={"suffix": ".xml"})

XMLBearDTDUrlTest = verify_local_bear(
    XMLBear,
    valid_files=(valid_xml_url,),
    invalid_files=(invalid_xml_url,),
    settings={'xml_dtd': dtd_url},
    tempfile_kwargs={"suffix": ".xml"})
