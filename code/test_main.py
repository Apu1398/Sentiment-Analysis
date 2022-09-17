import json
from main import main

expectedResult = {"Angry": 'VERY_LIKELY', "Joy": 'VERY_UNLIKELY', "Sorrow": 'VERY_UNLIKELY', "Surprise": 'UNLIKELY', "headwear": 'VERY_UNLIKELY' }


def testMain():
    expectedResultJson = json.dumps(expectedResult)

    assert main({"name": "face-test.png"},"") == expectedResultJson