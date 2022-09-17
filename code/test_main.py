import main
import json

expectedResult = {"Angry": 'VERY_LIKELY', "Joy": 'VERY_UNLIKELY', "Sorrow": 'VERY_UNLIKELY', "Surprise": 'UNLIKELY', "headwear": 'VERY_UNLIKELY' }


def testMain():
    expectedResult = json.dumps(expectedResult)
      
    assert main({"name": "face-test.png"}) == expectedResult