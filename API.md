# Xcalate API — Frontend Integration Guide

> **Manipur Travel Companion** — Complete API Reference for Frontend Developers
> **Backend:** Django + DRF + Groq AI + Sarvam AI
> **Version:** 1.0 · **Last Updated:** September 2026

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Quick Start](#2-quick-start)
3. [Base Setup (axios)](#3-base-setup-axios)
4. [Authentication (JWT)](#4-authentication-jwt)
5. [Audio Playback Helper](#5-audio-playback-helper-critical)
6. [Voice Capture (Web Speech API)](#6-voice-capture-web-speech-api)
7. [API Reference](#7-api-reference)
8. [Error Handling](#8-error-handling)
9. [Offline / PWA Patterns](#9-offline--pwa-patterns)
10. [Cheat Sheets](#10-cheat-sheets)
11. [Common Gotchas](#11-common-gotchas)
12. [Test Checklist](#12-test-checklist)

---

## 1. Project Overview

**Xcalate** is a PWA tourist guide for Manipur with four core features:

| Feature | What it does |
|---|---|
| 🗺️ **Discovery** | Browse places, restaurants, monuments by region |
| 🏠 **Homestay Marketplace** | Airbnb-style listings with bookings & reviews |
| 🛒 **Local Marketplace** | Buy products & services directly from Manipuri sellers |
| 🤖 **AI Voice Companion** | Speak a question → AI answers in Manipuri/Hindi/English with voice |

### Architecture

```
┌──────────────────┐    HTTPS     ┌──────────────────┐    HTTPS     ┌──────────────┐
│  Frontend (PWA)  │ ◄──────────► │  Django Backend  │ ◄──────────► │  Groq AI     │
│  Next.js / Vite  │              │  localhost:8000  │              │  Sarvam AI   │
└──────────────────┘              └──────────────────┘              └──────────────┘
```

**Key point:** You never talk to Groq or Sarvam directly. The backend proxies everything and returns clean JSON.

---

## 2. Quick Start

### 2.1 Run the backend locally

```bash
git clone https://github.com/Jssnsbbsb/xcalate.git
cd xcalate
python -m venv venv
venv\Scripts\activate                # Windows
# source venv/bin/activate           # macOS/Linux
pip install -r requirements.txt
```

### 2.2 Create `.env` (ask backend dev for real values)

```env
SECRET_KEY=any-random-string-for-dev
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

SARVAM_API_KEY=<ask backend dev>
SARVAM_BASE_URL=https://api.sarvam.ai

GROQ_API_KEY=<ask backend dev>
GROQ_MODEL=openai/gpt-oss-120b

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### 2.3 Initialize DB & run

```bash
python manage.py migrate
python manage.py seed_all          # optional — populates test data
python manage.py runserver
```

Backend runs at **`http://127.0.0.1:8000`** ✅

### 2.4 Verify it works

Open in browser:
- `http://127.0.0.1:8000/api/health/` → `{"status": "ok", "message": "API is live 🚀"}`

If you see that JSON, you're good. ✅

---

## 3. Base Setup (axios)

### 3.1 Install axios

```bash
npm install axios
```

### 3.2 Frontend `.env`

Create `.env` in your frontend project root:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

> For Next.js, use `NEXT_PUBLIC_API_URL` instead.

### 3.3 Create `src/api.js`

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api",
  withCredentials: true,
  timeout: 60000, // 60s — AI calls can take a few seconds
});

// Attach JWT to every request if we have one
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### 3.4 Quick test

```javascript
import api from "./api";

api.get("/health/").then(r => console.log(r.data));
// → { status: "ok", message: "API is live 🚀" }
```

---

## 4. Authentication (JWT)

All auth endpoints are prefixed with `/api/auth/`.

### 4.1 Register

```http
POST /api/auth/register/
Content-Type: application/json
```

**Body:**
```json
{
  "username": "ramesh",
  "email": "ramesh@test.com",
  "password": "Test@1234",
  "role": "local",
  "phone": "+919999999999",
  "region": "imphal",
  "business_name": "Ramesh Handicrafts"
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `username` | string | ✅ | Unique |
| `email` | string | ✅ | Unique |
| `password` | string | ✅ | Min 8 chars |
| `role` | string | ✅ | `tourist` or `local` (NOT `admin`) |
| `phone` | string | ❌ | |
| `region` | string | ❌ | Region slug |
| `business_name` | string | ❌ | For local sellers only |
| `bio` | string | ❌ | |
| `avatar_url` | string | ❌ | |

**Response `201`:**
```json
{
  "user": {
    "id": 1,
    "username": "ramesh",
    "email": "ramesh@test.com",
    "role": "local",
    "phone": "+919999999999",
    "region": "imphal",
    "business_name": "Ramesh Handicrafts"
  },
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 4.2 Login

```http
POST /api/auth/login/
```

**Body:**
```json
{ "username": "ramesh", "password": "Test@1234" }
```

**Response `200`:** same shape as register.

### 4.3 Refresh Token

```http
POST /api/auth/refresh/
```

**Body:**
```json
{ "refresh": "eyJhbGciOiJIUzI1NiIs..." }
```

**Response `200`:**
```json
{ "access": "eyJhbGciOiJIUzI1NiIs..." }
```

### 4.4 Current User Profile

```http
GET /api/auth/me/
Authorization: Bearer <access_token>
```

**Response `200`:**
```json
{
  "id": 1,
  "username": "ramesh",
  "email": "ramesh@test.com",
  "role": "local",
  "phone": "+919999999999",
  "region": "imphal",
  "bio": "",
  "avatar_url": "",
  "business_name": "Ramesh Handicrafts"
}
```

### 4.5 Update Profile

```http
PATCH /api/auth/me/
Authorization: Bearer <access_token>
```

**Body (any subset):**
```json
{ "bio": "Third-generation weaver", "phone": "+918888888888" }
```

### 4.6 Token Lifetime

| Token | Lifetime |
|---|---|
| `access` | 1 hour |
| `refresh` | 7 days |

**When `access` expires**, call `/auth/refresh/` with the `refresh` token to get a new `access`. If `refresh` also expires → re-login.

### 4.7 Frontend Auth Flow (localStorage)

```javascript
// After register/login
localStorage.setItem("access_token", data.access);
localStorage.setItem("refresh_token", data.refresh);

// Logout
localStorage.removeItem("access_token");
localStorage.removeItem("refresh_token");
```

The axios interceptor (§3.3) auto-attaches the token to every request.

---

## 5. Audio Playback Helper ⭐ (CRITICAL)

Every audio endpoint returns **base64-encoded MP3s**. Use this helper **everywhere**.

### 5.1 Create `src/utils/audio.js`

```javascript
/**
 * Play base64-encoded audio returned from the Xcalate API.
 * Works for /companion/ask/, /text/tts/, /voice/translate/.
 */
export function playBase64Audio(base64, format = "mp3") {
  if (!base64) {
    console.warn("[audio] no audio data");
    return null;
  }

  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }

  const blob = new Blob([bytes], { type: `audio/${format}` });
  const url = URL.createObjectURL(blob);
  const audio = new Audio(url);

  audio.addEventListener("ended", () => URL.revokeObjectURL(url), { once: true });

  audio.play().catch((err) => {
    console.error("[audio] autoplay blocked? Trigger from a user click.", err);
  });

  return audio;
}

export function base64ToAudioUrl(base64, format = "mp3") {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  const blob = new Blob([bytes], { type: `audio/${format}` });
  return URL.createObjectURL(blob);
}
```

### 5.2 ⚠️ Browser Autoplay Policy

**Browsers block audio that plays without a user gesture.**

- ✅ **Works:** user clicks mic → you call API → play audio
- ❌ **Blocked:** page loads → audio tries to play

**Always trigger API + audio from a user click.**

---

## 6. Voice Capture (Web Speech API)

Speech capture happens **in the browser**. The backend only receives text.

### 6.1 Create `src/utils/speech.js`

```javascript
export function startListening({ onResult, onError, lang = "en-IN" }) {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SR) {
    onError?.("Speech Recognition not supported. Use Chrome/Edge.");
    return null;
  }

  const recognition = new SR();
  recognition.lang = lang;
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (e) => {
    const transcript = e.results[0][0].transcript;
    onResult(transcript);
  };

  recognition.onerror = (e) => onError?.(e.error);
  recognition.start();
  return recognition;
}
```

### 6.2 Full Companion Flow

```javascript
import api from "./api";
import { startListening } from "./utils/speech";
import { playBase64Audio } from "./utils/audio";

async function handleMicClick() {
  startListening({
    lang: "en-IN",
    onResult: async (question) => {
      const { data } = await api.post("/companion/ask/", {
        question,
        target_language: "mni-IN", // Manipuri
        include_audio: true,
      });

      console.log("English:", data.answer_en);
      console.log("Manipuri:", data.answer_translated);

      playBase64Audio(data.audio.base64, data.audio.format);
    },
    onError: (err) => console.error("Speech error:", err),
  });
}
```

> ⚠️ **HTTPS requirement:** Web Speech API works on `localhost` in dev. In production, you need **HTTPS**.

---

## 7. API Reference

**Base URL:** `http://127.0.0.1:8000/api`
**Content-Type:** `application/json` (unless noted)
**Auth:** Bearer JWT (only where marked ✅)

### 7.1 Meta Endpoints

#### `GET /api/health/`

```json
{ "status": "ok", "message": "API is live 🚀" }
```

#### `GET /api/languages/`

```json
{
  "languages": [
    { "code": "hi-IN", "name": "Hindi" },
    { "code": "mni-IN", "name": "Manipuri" },
    { "code": "bn-IN", "name": "Bengali" },
    { "code": "ta-IN", "name": "Tamil" },
    { "code": "en-IN", "name": "English (India)" }
  ]
}
```

#### `GET /api/voices/`

```json
{
  "voices": [
    { "id": "anushka", "name": "Anushka", "gender": "female", "language": "hi-IN" },
    { "id": "abhilash", "name": "Abhilash", "gender": "male", "language": "hi-IN" }
  ]
}
```

---

### 7.2 Places

#### `GET /api/places/`

**Query params:**

| Param | Type | Example | Notes |
|---|---|---|---|
| `category` | string | `monument` | See categories below |
| `region` | string | `imphal` | Region slug |
| `featured` | bool | `true` | Only featured spots |
| `search` | string | `lake` | Search name + description |
| `limit` | int | `20` | Default 50, max 200 |

**Categories:** `monument`, `nature`, `restaurant`, `heritage`, `temple`, `market`, `adventure`

**Regions:** `imphal`, `loktak`, `ukhrul`, `churachandpur`, `senapati`, `tamenglong`, `bishnupur`, `thoubal`

**Response:**
```json
{
  "count": 48,
  "results": [
    {
      "id": 1,
      "name": "Kangla Fort",
      "slug": "kangla-fort",
      "category": "heritage",
      "region": "imphal",
      "short_description": "Ancient fortified palace of Manipuri kings...",
      "images": ["https://picsum.photos/seed/kangla-fort/1200/800"],
      "latitude": 24.8080,
      "longitude": 93.9420,
      "rating": 4.7,
      "rating_count": 218,
      "price_range": "budget",
      "tags": ["heritage", "fort", "history"],
      "is_featured": true
    }
  ]
}
```

#### `GET /api/places/categories/`

```json
{
  "categories": [
    { "id": "monument", "label": "Monument" },
    { "id": "nature", "label": "Nature" },
    { "id": "restaurant", "label": "Restaurant" }
  ]
}
```

#### `GET /api/places/<slug>/`

Returns full detail (includes `description`, `address`, `opening_hours`, `contact`).

---

### 7.3 Regions & Offline

#### `GET /api/regions/`

```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "slug": "imphal",
      "name": "Imphal",
      "description": "The capital of Manipur...",
      "cover_image": "https://picsum.photos/seed/imphal/1200/800",
      "latitude": 24.817,
      "longitude": 93.936,
      "zoom": 12,
      "size_mb": 2.5,
      "place_count": 18
    }
  ]
}
```

#### `GET /api/regions/<slug>/`

```json
{
  "id": 1, "slug": "imphal", "name": "Imphal",
  "...": "...",
  "has_places": true,
  "has_homestays": true
}
```

#### ⭐ `GET /api/regions/<slug>/download/`

**THE OFFLINE BUNDLE** — cache this entire response in IndexedDB.

```json
{
  "region": { },
  "places": [],
  "homestays": [],
  "artists": [],
  "version": 1,
  "generated_at": "2026-09-21T15:30:00Z"
}
```

**Frontend usage:**
```javascript
const { data } = await api.get(`/regions/${slug}/download/`);
await idb.set(`region:${slug}`, data);
```

---

### 7.4 Homestays

#### `GET /api/homestays/`

**Query params:** `region`, `min_price`, `max_price`, `guests`, `search`, `limit`

```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "slug": "lakeside-homestay-loktak",
      "title": "Lakeside Homestay near Loktak",
      "region": "loktak",
      "price_per_night": "1500.00",
      "max_guests": 4,
      "bedrooms": 2,
      "beds": 3,
      "bathrooms": 1,
      "amenities": ["wifi", "meals_included"],
      "images": ["https://..."],
      "rating": 4.8,
      "rating_count": 23,
      "latitude": 24.55,
      "longitude": 93.80
    }
  ]
}
```

#### `POST /api/homestays/` ✅ Auth Required (role: local)

**Body:**
```json
{
  "title": "Lakeside Homestay",
  "description": "Cozy place near Loktak",
  "region": "loktak",
  "address": "Thanga Village",
  "latitude": 24.55,
  "longitude": 93.80,
  "price_per_night": 1500,
  "max_guests": 4,
  "bedrooms": 2,
  "beds": 3,
  "bathrooms": 1,
  "amenities": ["wifi", "meals_included"],
  "images": ["https://cloudinary.com/.../img1.jpg"]
}
```

**Returns:** `201 Created` with full object.

#### `GET /api/homestays/<slug>/`

Full detail + embedded `reviews` array.

---

### 7.5 Bookings & Reviews

#### `POST /api/homestays/<slug>/bookings/` ✅ Auth Required

```json
{
  "guest_name": "Adish",
  "guest_phone": "+919999999999",
  "guest_email": "adish@example.com",
  "check_in": "2026-10-01",
  "check_out": "2026-10-03",
  "guests": 2,
  "message": "Looking forward to it!"
}
```

**Returns:** `201` with `status: "pending"`.

#### `GET /api/homestays/<slug>/bookings/` ✅ Auth Required

```json
{
  "count": 3,
  "results": [
    {
      "id": 1, "guest_name": "Adish",
      "check_in": "2026-10-01", "check_out": "2026-10-03",
      "guests": 2, "status": "pending", "created_at": "..."
    }
  ]
}
```

**Status values:** `pending`, `accepted`, `declined`, `completed`

#### `POST /api/homestays/<slug>/reviews/` ✅ Auth Required

```json
{ "author_name": "Adish", "rating": 5, "comment": "Amazing stay!" }
```

**Note:** posting a review auto-recomputes the homestay's average rating.

#### `GET /api/homestays/<slug>/reviews/`

```json
{
  "count": 5,
  "results": [
    { "id": 1, "author_name": "Adish", "rating": 5, "comment": "Amazing!", "created_at": "..." }
  ]
}
```

---

### 7.6 Marketplace (Products & Services)

#### `GET /api/marketplace/listings/`

**Query params:** `type` (`product`/`service`), `region`, `category`, `search`, `min_price`, `max_price`, `featured`, `limit`

```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "slug": "handwoven-manipuri-phanek",
      "type": "product",
      "title": "Handwoven Manipuri Phanek",
      "short_description": "Traditional wrap-around skirt woven by Imphal artisans",
      "price": "1800.00",
      "price_unit": "per item",
      "region": "imphal",
      "category": "textile",
      "images": ["https://..."],
      "is_featured": false,
      "seller_username": "ramesh"
    }
  ]
}
```

#### `POST /api/marketplace/listings/` ✅ Auth Required (role: local)

**Body:**
```json
{
  "type": "product",
  "title": "Handwoven Manipuri Phanek",
  "short_description": "Traditional wrap-around skirt woven by Imphal artisans",
  "description": "Authentic handwoven Phanek using traditional motifs...",
  "price": 1800,
  "price_unit": "per item",
  "region": "imphal",
  "category": "textile",
  "contact_phone": "+919999999999",
  "whatsapp": "+919999999999",
  "images": ["https://cloudinary.com/.../phanek.jpg"]
}
```

**Product categories:** `handicraft`, `textile`, `food`, `art`, `jewelry`, `other`
**Service categories:** `guide`, `workshop`, `transport`, `performance`, `other`

#### `GET /api/marketplace/listings/<slug>/`

Full detail + nested seller object.

#### `GET /api/marketplace/my-listings/` ✅ Auth Required

Returns the current user's own listings.

#### `GET /api/marketplace/categories/`

```json
{
  "products": ["handicraft", "textile", "food", "art", "jewelry", "other"],
  "services": ["guide", "workshop", "transport", "performance", "other"]
}
```

#### `POST /api/marketplace/listings/<slug>/contact/` ✅ Auth Required

**Body:**
```json
{
  "name": "Adish",
  "phone": "+918888888888",
  "email": "adish@test.com",
  "message": "Interested in this shawl. Can you ship to Delhi?"
}
```

**Returns:** `201 Created`.

#### `GET /api/marketplace/my-contacts/` ✅ Auth Required

Returns all contact requests for the current user's listings.

---

### 7.7 AI Companion ⭐

#### `POST /api/companion/ask/`

**Body:**
```json
{
  "question": "Where can I see a sunset?",
  "target_language": "mni-IN",
  "region": "imphal",
  "speaker": "anushka",
  "include_audio": true
}
```

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `question` | string | ✅ | — | Max 1000 chars |
| `target_language` | string | ❌ | `hi-IN` | Any code from `/languages/` |
| `region` | string | ❌ | — | Narrows AI context |
| `speaker` | string | ❌ | `anushka` | Voice ID from `/voices/` |
| `include_audio` | bool | ❌ | `true` | Set `false` for faster text-only |

**Response:**
```json
{
  "question": "Where can I see a sunset?",
  "answer_en": "Head to Kangla Fort around 5 PM for a beautiful sunset.",
  "answer_translated": "শাম ৫ বাজে কাংলা কিলে যান...",
  "target_language": "mni-IN",
  "audio": {
    "format": "mp3",
    "base64": "//uQxAAAAAAAAAAAA...",
    "sample_rate": 22050
  }
}
```

**Performance:**

| `include_audio` | Time |
|---|---|
| `false` | ~1-2s (text only) |
| `true` | ~3-5s (text + translate + TTS) |

---

### 7.8 Voice & Text Utilities

#### `POST /api/voice/translate/`

**Content-Type:** `multipart/form-data`

| Field | Type | Required | Notes |
|---|---|---|---|
| `audio` | File | ✅ | `.wav`, `.mp3`, `.webm` ≤ 25 MB |
| `target_language` | string | ✅ | Any code from `/languages/` |
| `source_language` | string | ❌ | Default: `unknown` (auto) |
| `speaker` | string | ❌ | Default: `anushka` |
| `stt_mode` | string | ❌ | `transcribe` \| `translate` \| `verbatim` \| `translit` \| `codemix` |

**Response:**
```json
{
  "request_id": "vt_1726920000",
  "transcript": "मुझे flight book करनी है",
  "translated_text": "I want to book a flight",
  "source_language_detected": "hi-IN",
  "target_language": "en-IN",
  "audio": { "format": "mp3", "base64": "...", "sample_rate": 22050 },
  "processing_time_ms": 2450
}
```

**Example:**
```javascript
const form = new FormData();
form.append("audio", audioBlob, "recording.webm");
form.append("target_language", "mni-IN");

const { data } = await api.post("/voice/translate/", form, {
  headers: { "Content-Type": "multipart/form-data" },
});

playBase64Audio(data.audio.base64, data.audio.format);
```

#### `POST /api/text/translate/`

```json
// Request
{
  "input": "Hello, how are you?",
  "source_language": "auto",
  "target_language": "mni-IN"
}

// Response
{
  "translated_text": "হ্যালো, তুমি কেমন আছো?",
  "source_language_detected": "en-IN",
  "target_language": "mni-IN",
  "detected_source_language": "en-IN"
}
```

#### `POST /api/text/tts/`

```json
// Request
{
  "text": "নমস্কার",
  "target_language": "mni-IN",
  "speaker": "anushka",
  "pace": 1.0,
  "codec": "mp3"
}

// Response
{
  "request_id": "abc123",
  "audio": {
    "format": "mp3",
    "base64": "...",
    "sample_rate": 22050
  }
}
```

---

## 8. Error Handling

Every error follows the same shape:

```json
{
  "error": "machine_readable_code",
  "message": "Human-readable message",
  "code": "HTTP_LEVEL_CODE"
}
```

### 8.1 Error Code Reference

| HTTP | Code | Meaning | Frontend Action |
|---|---|---|---|
| 400 | `INVALID_FORMAT` | Bad file/text format | Show validation message |
| 400 | `AUDIO_TOO_LONG` | File > 25 MB | Show "File too large" |
| 401 | `UNAUTHORIZED` | Missing/expired token | Redirect to login |
| 403 | `FORBIDDEN` | Wrong role (e.g., tourist trying to sell) | Show permission error |
| 422 | `UNSUPPORTED_LANGUAGE` | Language not supported | Show language picker |
| 429 | `RATE_LIMITED` | Too many requests | Retry with backoff |
| 502 | `GROQ_ERROR` | AI failure | "Try again in a moment" |
| 502 | `SARVAM_ERROR` | Translation/TTS failure | Show text only |
| 504 | `SARVAM_TIMEOUT` | Upstream slow | "Try again" |

### 8.2 Global error interceptor

```javascript
api.interceptors.response.use(
  (r) => r,
  (err) => {
    const data = err.response?.data;
    if (data?.message) {
      console.error(`[API ${err.response.status}] ${data.error}: ${data.message}`);
    }
    if (err.response?.status === 401) {
      // Token expired — redirect to login
      localStorage.removeItem("access_token");
      // window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);
```

---

## 9. Offline / PWA Patterns

### 9.1 IndexedDB wrapper (`src/utils/idb.js`)

```javascript
import { openDB } from "idb";

const dbPromise = openDB("xcalate", 1, {
  upgrade(db) {
    db.createObjectStore("regions");
    db.createObjectStore("meta");
  },
});

export const idb = {
  async set(key, value) {
    return (await dbPromise).put("regions", value, key);
  },
  async get(key) {
    return (await dbPromise).get("regions", key);
  },
  async del(key) {
    return (await dbPromise).delete("regions", key);
  },
  async keys() {
    return (await dbPromise).getAllKeys("regions");
  },
};
```

### 9.2 Download region flow

```javascript
async function downloadRegion(slug) {
  const { data } = await api.get(`/regions/${slug}/download/`);
  await idb.set(`region:${slug}`, data);
  console.log(`Downloaded ${slug}: ${data.places.length} places`);
}
```

### 9.3 Offline read

```javascript
async function getRegionData(slug) {
  try {
    const { data } = await api.get(`/regions/${slug}/download/`);
    await idb.set(`region:${slug}`, data);
    return data;
  } catch {
    return await idb.get(`region:${slug}`);
  }
}
```

### 9.4 Suggested offline strategy

| Data | Strategy |
|---|---|
| Regions list | Cache-first |
| Region bundle (`/download/`) | On-demand download, then cache-first |
| Place detail | Network-first, fall back to cached bundle |
| Companion Q&A | Cache popular questions for offline fallback |
| Homestays | Cache-first for browsed listings |

---

## 10. Cheat Sheets

### 10.1 All endpoints at a glance

| Method | Endpoint | Auth? | Purpose |
|---|---|---|---|
| GET | `/api/health/` | ❌ | Health check |
| GET | `/api/languages/` | ❌ | Supported languages |
| GET | `/api/voices/` | ❌ | TTS voices |
| POST | `/api/auth/register/` | ❌ | Register |
| POST | `/api/auth/login/` | ❌ | Login → JWT |
| POST | `/api/auth/refresh/` | ❌ | Refresh access token |
| GET | `/api/auth/me/` | ✅ | Current user |
| PATCH | `/api/auth/me/` | ✅ | Update profile |
| GET | `/api/places/` | ❌ | List places |
| GET | `/api/places/categories/` | ❌ | Categories |
| GET | `/api/places/<slug>/` | ❌ | Place detail |
| GET | `/api/regions/` | ❌ | List regions |
| GET | `/api/regions/<slug>/` | ❌ | Region detail |
| GET | `/api/regions/<slug>/download/` | ❌ | ⭐ Offline bundle |
| GET | `/api/homestays/` | ❌ | List homestays |
| POST | `/api/homestays/` | ✅ local | Create homestay |
| GET | `/api/homestays/<slug>/` | ❌ | Homestay detail |
| GET | `/api/homestays/<slug>/bookings/` | ✅ | List inquiries |
| POST | `/api/homestays/<slug>/bookings/` | ✅ | Send inquiry |
| GET | `/api/homestays/<slug>/reviews/` | ❌ | List reviews |
| POST | `/api/homestays/<slug>/reviews/` | ✅ | Post review |
| GET | `/api/marketplace/listings/` | ❌ | List listings |
| POST | `/api/marketplace/listings/` | ✅ local | Create listing |
| GET | `/api/marketplace/listings/<slug>/` | ❌ | Listing detail |
| GET | `/api/marketplace/my-listings/` | ✅ | Own listings |
| GET | `/api/marketplace/categories/` | ❌ | Categories |
| POST | `/api/marketplace/listings/<slug>/contact/` | ✅ | Contact seller |
| GET | `/api/marketplace/my-contacts/` | ✅ | Contacts received |
| POST | `/api/companion/ask/` | ❌ | ⭐ AI voice companion |
| POST | `/api/voice/translate/` | ❌ | Audio → translated audio |
| POST | `/api/text/translate/` | ❌ | Text translation |
| POST | `/api/text/tts/` | ❌ | Text → speech |

### 10.2 Language codes

| Language | Code |
|---|---|
| Manipuri | `mni-IN` |
| Hindi | `hi-IN` |
| English (India) | `en-IN` |
| Bengali | `bn-IN` |
| Tamil | `ta-IN` |
| Telugu | `te-IN` |
| Kannada | `kn-IN` |
| Malayalam | `ml-IN` |
| Marathi | `mr-IN` |
| Gujarati | `gu-IN` |
| Punjabi | `pa-IN` |
| Odia | `or-IN` |
| Assamese | `as-IN` |
| Urdu | `ur-IN` |

### 10.3 Region slugs

`imphal` · `loktak` · `ukhrul` · `churachandpur` · `senapati` · `tamenglong` · `bishnupur` · `thoubal`

### 10.4 Place categories

`monument` · `nature` · `restaurant` · `heritage` · `temple` · `market` · `adventure`

### 10.5 Copy-paste snippets

**Fetch places:**
```javascript
const { data } = await api.get("/places/", {
  params: { region: "imphal", category: "restaurant", limit: 10 },
});
```

**Download region:**
```javascript
const { data } = await api.get("/regions/imphal/download/");
```

**Ask companion:**
```javascript
const { data } = await api.post("/companion/ask/", {
  question: "Where can I eat local food?",
  target_language: "mni-IN",
});
playBase64Audio(data.audio.base64);
```

**Send booking:**
```javascript
await api.post(`/homestays/${slug}/bookings/`, {
  guest_name: "Adish",
  guest_phone: "+919999999999",
  check_in: "2026-10-01",
  check_out: "2026-10-03",
  guests: 2,
});
```

**Post review:**
```javascript
await api.post(`/homestays/${slug}/reviews/`, {
  author_name: "Adish",
  rating: 5,
  comment: "Amazing stay!",
});
```

---

## 11. Common Gotchas

### ⚠️ 1. Autoplay blocked
**Problem:** Audio doesn't play automatically.
**Fix:** Trigger API + `playBase64Audio()` from a user click.

### ⚠️ 2. CORS error
**Problem:** `Access to XMLHttpRequest has been blocked by CORS policy`
**Fix:** Frontend must run on `http://localhost:5173`. Ping backend dev if using another port.

### ⚠️ 3. HTTPS required for Web Speech API
**Problem:** `SpeechRecognition is not defined`
**Fix:** Use Chrome/Edge. Works on `localhost`. For production, deploy with HTTPS.

### ⚠️ 4. `target_language` unsupported
**Problem:** `{"error": "unsupported_language"}`
**Fix:** Use codes from `/api/languages/` only.

### ⚠️ 5. Token expires mid-session
**Problem:** `401 Unauthorized` after an hour.
**Fix:** Use `/auth/refresh/` or catch the 401 and re-login.

### ⚠️ 6. `Bearer` needs a space
**Problem:** Header rejected.
**Fix:** `Authorization: Bearer eyJ...` (space after "Bearer").

### ⚠️ 7. First AI request is slow
**Problem:** First `/companion/ask/` takes 5-6s.
**Fix:** Cold start — normal. Subsequent calls ~2-3s.

### ⚠️ 8. Mobile Safari voice
**Problem:** `webkitSpeechRecognition` missing.
**Fix:** Feature-detect + show fallback text input.

---

## 12. Test Checklist

Before you start building, verify each of these:

- [ ] `GET /api/health/` returns `{status: ok}`
- [ ] `GET /api/languages/` returns language list
- [ ] `GET /api/voices/` returns voices
- [ ] `GET /api/places/` returns array
- [ ] `GET /api/regions/` returns regions
- [ ] `GET /api/regions/imphal/download/` returns bundle
- [ ] `GET /api/homestays/` returns array
- [ ] `GET /api/marketplace/listings/` returns array
- [ ] `POST /api/auth/register/` creates user + returns tokens
- [ ] `POST /api/auth/login/` returns tokens
- [ ] `GET /api/auth/me/` (with token) returns profile
- [ ] `POST /api/companion/ask/` returns an answer
- [ ] CORS works — call `/api/health/` from React console

All ✅ → **start building.** 🚀

---

## 📞 Contact

| Question | Who to ping |
|---|---|
| API returns unexpected data | Backend dev |
| CORS error | Backend dev |
| Sarvam/Groq keys | Backend dev |
| Feature request | Backend dev |

**Backend repo:** https://github.com/Jssnsbbsb/xcalate
**Frontend repo:** https://github.com/Jssnsbbsb/xcalate-frontend

---

**Good luck! Build something amazing.** 💪🇮🇳