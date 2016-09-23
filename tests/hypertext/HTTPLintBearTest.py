from bears.hypertext.HTTPoliceLintBear import HTTPoliceLintBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
{
  "_expected": [],
  "log": {
    "creator": {"name": "demo"},
    "entries": [
      {
        "request": {
          "method": "GET",
          "url": "http://example.com/",
          "httpVersion": "HTTP/1.1",
          "headers": [
            {"name": "Host", "value": "example.com"},
            {"name": "User-Agent", "value": "demo"}
          ],
          "bodySize": 0
        },
        "response": {
          "httpVersion": "HTTP/1.1",
          "status": 200,
          "statusText": "OK",
          "headers": [
            {"name": "Date", "value": "Thu, 31 Dec 2015 18:26:56 GMT"},
            {"name": "Content-Type", "value": "text/plain"},
            {"name": "Content-Length", "value": "14"}
          ],
          "bodySize": 14,
          "content": {
            "size": 14,
            "text": "Hello world!\r\n"
          }
        }
      }
    ]
  }
}
""".splitlines(keepends=True)

bad_file = """
{
  "_expected": [1045],
  "log": {
    "creator": {"name": "demo"},
    "entries": [
      {
        "request": {
          "method": "GET",
          "url": "http://президент.рф/",
          "httpVersion": "HTTP/2",
          "headers": [
            {"name": "User-Agent", "value": "demo"}
          ],
          "bodySize": 0
        },
        "response": {
          "httpVersion": "HTTP/2",
          "status": 200,
          "statusText": "OK",
          "headers": [
            {"name": "Date", "value": "Thu, 31 Dec 2015 18:26:56 GMT"},
            {"name": "Content-Type", "value": "text/plain"},
            {"name": "Content-Length", "value": "14"}
          ],
          "bodySize": 14,
          "content": {
            "size": 14,
            "text": "Hello world!\r\n"
          }
        }
      }
    ]
  }
}
""".splitlines(keepends=True)


HTTPoliceLintBearTest = verify_local_bear(HTTPoliceLintBear,
                                          valid_files=(good_file,),
                                          invalid_files=(bad_file,))

HTTPoliceLintBearDisableTest = verify_local_bear(HTTPoliceLintBear,
                                                 valid_files=(
                                                     good_file, bad_file),
                                                 invalid_files=(),
                                                 settings={'silent': '1045'})
