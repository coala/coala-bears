import os

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

dtd_file = os.path.join(os.path.dirname(__file__),
                        "test_files",
                        "note.dtd")

schema_file = os.path.join(os.path.dirname(__file__),
                           "test_files",
                           "note.xsd")

valid_xml_path = list(open(os.path.join(
    os.path.dirname(__file__),
    "test_files",
    "note.xml"), 'r'))

valid_xml_url = list(open(os.path.join(
    os.path.dirname(__file__),
    "test_files",
    "concept-valid.xml"), 'r'))

invalid_xml_schema = list(open(os.path.join(
    os.path.dirname(__file__),
    "test_files",
    "xsd-error.xml"), 'r'))

invalid_xml_dtd = list(open(os.path.join(
    os.path.dirname(__file__),
    "test_files",
    "dtd-error.xml"), 'r'))

invalid_xml_url = list(open(os.path.join(
    os.path.dirname(__file__),
    "test_files",
    "concept-invalid.xml"), 'r'))

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
