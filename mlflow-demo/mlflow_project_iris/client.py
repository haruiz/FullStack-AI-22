import requests
import json

if __name__ == '__main__':
    url = "http://localhost:8081/invocations"
    payload = json.dumps({
      "instances": [
        {
          "sepal-length": 5,
          "sepal-width": 3.2,
          "petal-length": 1.2,
          "petal-width": 0.2
        }
      ]
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
