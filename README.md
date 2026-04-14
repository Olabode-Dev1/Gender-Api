# Gender Classification API

A simple backend API that classifies a name using the Genderize API and returns a processed response.

---

## Endpoint

GET /api/classify?name={name}

---

## Example Request

/api/classify?name=john

---

## Example Response

```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 1.0,
    "sample_size": 2692560,
    "is_confident": true,
    "processed_at": "2026-04-14T22:43:34Z"
  }
}
