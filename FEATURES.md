# xcalate API Features

Base URL: `http://localhost:8000`

Authenticated requests use:

```http
Authorization: Bearer <access-token>
```

## Authentication

| Endpoint | Method | Auth Required | Role |
|---|---|---|---|
| `/api/auth/register/` | POST | No | `tourist` or `local` |
| `/api/auth/login/` | POST | No | Any registered user |
| `/api/auth/refresh/` | POST | No | Valid refresh token |
| `/api/auth/me/` | GET | Yes | Any |
| `/api/auth/me/` | PATCH | Yes | Any |

### Register

Request:

```json
{
  "username": "maya",
  "email": "maya@example.com",
  "password": "strong-password",
  "role": "tourist",
  "phone": "+919876543210",
  "region": "imphal"
}
```

Response: `201 Created`

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>",
  "user": {
    "id": 1,
    "username": "maya",
    "email": "maya@example.com",
    "role": "tourist",
    "phone": "+919876543210",
    "region": "imphal",
    "bio": "",
    "avatar_url": "",
    "business_name": ""
  }
}
```

Registration does not accept `role: "admin"`. Admin users are created through `createsuperuser`.

### Login

Request:

```json
{
  "username": "maya",
  "password": "strong-password"
}
```

Response: `200 OK`

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

### Refresh token

Request:

```json
{
  "refresh": "<refresh-token>"
}
```

Response: `200 OK`

```json
{
  "access": "<new-access-token>"
}
```

### Current profile

Request:

```http
GET /api/auth/me/
Authorization: Bearer <access-token>
```

Response: `200 OK`

```json
{
  "id": 1,
  "username": "maya",
  "email": "maya@example.com",
  "role": "tourist",
  "phone": "+919876543210",
  "region": "imphal",
  "bio": "",
  "avatar_url": "",
  "business_name": ""
}
```

### Update current profile

Request:

```json
{
  "phone": "+919800000000",
  "bio": "Exploring Manipur",
  "region": "loktak"
}
```

Response: `200 OK`

```json
{
  "id": 1,
  "username": "maya",
  "email": "maya@example.com",
  "role": "tourist",
  "phone": "+919800000000",
  "region": "loktak",
  "bio": "Exploring Manipur",
  "avatar_url": "",
  "business_name": ""
}
```

## Marketplace

| Endpoint | Method | Auth Required | Role |
|---|---|---|---|
| `/api/marketplace/listings/` | GET | No | Any |
| `/api/marketplace/listings/` | POST | Yes | `local` only |
| `/api/marketplace/listings/<slug>/` | GET | No | Any |
| `/api/marketplace/listings/<slug>/contact/` | POST | Yes | Any |
| `/api/marketplace/my-listings/` | GET | Yes | Any; returns owned listings |
| `/api/marketplace/my-contacts/` | GET | Yes | Any; returns contacts for owned listings |
| `/api/marketplace/categories/` | GET | No | Any |

The listings endpoint supports these query parameters: `type`, `region`, `category`, `search`, `min_price`, `max_price`, `featured`, and `limit`.

### List listings

Request:

```http
GET /api/marketplace/listings/?type=product&region=imphal&featured=true&limit=20
```

Response: `200 OK`

```json
{
  "count": 1,
  "results": [
    {
      "id": 4,
      "title": "Loktak Handwoven Shawl",
      "slug": "loktak-handwoven-shawl-a1b2c3d4",
      "type": "product",
      "short_description": "Handwoven shawl made locally.",
      "price": "1800.00",
      "price_unit": "per item",
      "images": ["https://example.com/shawl.jpg"],
      "region": "imphal",
      "category": "textile",
      "is_featured": true,
      "seller_username": "ningol"
    }
  ]
}
```

### Create a listing

Only authenticated users with role `local` can create listings.

Request:

```json
{
  "type": "service",
  "title": "Loktak Lake Guide",
  "description": "Local guided tours around Loktak Lake.",
  "short_description": "A local guide for Loktak Lake.",
  "price": "1500.00",
  "price_unit": "per day",
  "images": ["https://example.com/loktak.jpg"],
  "region": "loktak",
  "category": "guide",
  "contact_phone": "+919876543210",
  "contact_email": "guide@example.com",
  "whatsapp": "+919876543210"
}
```

Response: `201 Created`

```json
{
  "id": 5,
  "user": 2,
  "seller": {
    "username": "ningol",
    "phone": "+919876543210",
    "business_name": "Ningol Experiences",
    "region": "loktak"
  },
  "type": "service",
  "title": "Loktak Lake Guide",
  "slug": "loktak-lake-guide-e5f6a7b8",
  "price": "1500.00",
  "price_unit": "per day",
  "is_active": true,
  "is_featured": false,
  "view_count": 0
}
```

### Listing detail

Request:

```http
GET /api/marketplace/listings/loktak-lake-guide-e5f6a7b8/
```

Response: `200 OK`

```json
{
  "id": 5,
  "user": 2,
  "seller": {
    "username": "ningol",
    "phone": "+919876543210",
    "business_name": "Ningol Experiences",
    "region": "loktak"
  },
  "title": "Loktak Lake Guide",
  "type": "service",
  "category": "guide",
  "price": "1500.00",
  "price_unit": "per day",
  "view_count": 13
}
```

Each successful GET increments `view_count` by one.

### Contact seller

Request:

```http
POST /api/marketplace/listings/loktak-lake-guide-e5f6a7b8/contact/
Authorization: Bearer <access-token>
```

```json
{
  "name": "Maya Devi",
  "phone": "+919800000000",
  "email": "maya@example.com",
  "message": "I would like to book a guide for Saturday."
}
```

Response: `201 Created`

```json
{
  "id": 12,
  "created_at": "2026-09-21T10:30:00Z",
  "message": "Seller will contact you"
}
```

### My listings

Request:

```http
GET /api/marketplace/my-listings/
Authorization: Bearer <access-token>
```

Response: `200 OK`

```json
[
  {
    "id": 5,
    "title": "Loktak Lake Guide",
    "slug": "loktak-lake-guide-e5f6a7b8",
    "type": "service",
    "category": "guide",
    "price": "1500.00",
    "is_active": true
  }
]
```

### My contacts

Returns only contact requests for listings owned by the authenticated user.

Request:

```http
GET /api/marketplace/my-contacts/
Authorization: Bearer <access-token>
```

Response: `200 OK`

```json
[
  {
    "id": 12,
    "listing": 5,
    "listing_title": "Loktak Lake Guide",
    "name": "Maya Devi",
    "phone": "+919800000000",
    "email": "maya@example.com",
    "message": "I would like to book a guide for Saturday.",
    "created_at": "2026-09-21T10:30:00Z"
  }
]
```

### Marketplace categories

Request:

```http
GET /api/marketplace/categories/
```

Response: `200 OK`

```json
{
  "products": [
    "handicraft",
    "textile",
    "food",
    "art",
    "jewelry",
    "other"
  ],
  "services": [
    "guide",
    "workshop",
    "transport",
    "performance",
    "other"
  ]
}
```

## Existing Features: Places, Regions, Homestays, Companion

### Places

| Endpoint | Method | Auth Required | Role |
|---|---|---|---|
| `/api/places/` | GET | No | Any |
| `/api/places/categories/` | GET | No | Any |
| `/api/places/<slug>/` | GET | No | Any |

### Regions

| Endpoint | Method | Auth Required | Role |
|---|---|---|---|
| `/api/regions/` | GET | No | Any |
| `/api/regions/<slug>/` | GET | No | Any |
| `/api/regions/<slug>/download/` | GET | No | Any |

### Homestays

| Endpoint | Method | Auth Required | Role |
|---|---|---|---|
| `/api/homestays/` | GET | No | Any |
| `/api/homestays/` | POST | Yes | `local` only |
| `/api/homestays/<slug>/` | GET | No | Any |
| `/api/homestays/<slug>/bookings/` | GET | No | Any |
| `/api/homestays/<slug>/bookings/` | POST | Yes | Any |
| `/api/homestays/<slug>/reviews/` | GET | No | Any |
| `/api/homestays/<slug>/reviews/` | POST | Yes | Any |

### Companion and Translation

| Endpoint | Method | Auth Required | Role |
|---|---|---|---|
| `/api/companion/ask/` | POST | No | Any |
| `/api/health/` | GET | No | Any |
| `/api/languages/` | GET | No | Any |
| `/api/voices/` | GET | No | Any |
| `/api/voice/translate/` | POST | No | Any |
| `/api/text/translate/` | POST | No | Any |
| `/api/text/tts/` | POST | No | Any |

## API Directory

A JSON endpoint directory is available at:

```http
GET /
```

The Django admin is available at `/admin/`.
