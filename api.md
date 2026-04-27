# StayEase API Contract

## 1. Send Message Endpoint

**Endpoint:** `POST /api/chat/{conversation_id}/message`

**Description:** Sends a message from a guest to the AI agent and returns the agent's response. The `conversation_id` is used to maintain conversation history.

### Request Body Schema

```json
{
  "message": "string"
}
```

### Response Body Schema (Success - 200 OK)

```json
{
  "response": "string",
  "intent": "string | null",
  "data": "object | null"
}
```

### Realistic Example

**Request:**
`POST /api/chat/session-550e8400/message`
```json
{
  "message": "I need a room in Sylhet for 3 nights for 2 guests"
}
```

**Response (200 OK):**
```json
{
  "response": "I found 2 great options in Sylhet for your dates. Would you like to hear more details about 'Tea Garden Resort' or 'Green View Guesthouse'?",
  "intent": "search",
  "data": {
    "properties": [
      {
        "id": 105,
        "title": "Tea Garden Resort",
        "price_per_night": 6500.00,
        "currency": "BDT",
        "location": "Sylhet",
        "max_guests": 3
      },
      {
        "id": 106,
        "title": "Green View Guesthouse",
        "price_per_night": 3000.00,
        "currency": "BDT",
        "location": "Sylhet",
        "max_guests": 2
      }
    ]
  }
}
```

### Error Responses

**404 Not Found (Conversation doesn't exist)**
```json
{
  "detail": "Conversation session-550e8400 not found."
}
```

**422 Unprocessable Entity (Validation Error)**
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error (LLM/DB Failure)**
```json
{
  "detail": "Failed to connect to the language model."
}
```

---

## 2. Get Conversation History Endpoint

**Endpoint:** `GET /api/chat/{conversation_id}/history`

**Description:** Retrieves the entire chat history for a given conversation session.

### Request Parameters

- `conversation_id` (Path): The unique UUID of the conversation.

### Response Body Schema (Success - 200 OK)

```json
{
  "conversation_id": "string",
  "messages": [
    {
      "role": "string",
      "content": "string",
      "timestamp": "string (datetime)"
    }
  ]
}
```

### Realistic Example

**Request:**
`GET /api/chat/session-12345678/history`

**Response (200 OK):**
```json
{
  "conversation_id": "session-12345678",
  "messages": [
    {
      "role": "user",
      "content": "Tell me about the Seaside Villa in Cox's Bazar.",
      "timestamp": "2026-04-27T10:00:00Z"
    },
    {
      "role": "agent",
      "content": "Seaside Villa is a beautiful property in Cox's Bazar with a sea view. It costs 5000 BDT per night and has WiFi and AC. Would you like to book it?",
      "timestamp": "2026-04-27T10:00:15Z"
    },
    {
      "role": "user",
      "content": "Yes, please book it for May 1st to May 3rd for 2 people. My name is Shibly.",
      "timestamp": "2026-04-27T10:01:00Z"
    },
    {
      "role": "agent",
      "content": "Great! Your booking (ID: 101) is confirmed. The total price is 10000 BDT.",
      "timestamp": "2026-04-27T10:01:10Z"
    }
  ]
}
```

### Error Responses

**404 Not Found (Conversation doesn't exist)**
```json
{
  "detail": "Conversation session-12345678 not found."
}
```
