# Xcalate — Frontend Integration Snippets

Copy-paste starting points for common patterns.

---

## 1. Axios Setup (`src/api.js`)

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api",
  withCredentials: true,
  timeout: 60000,
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

---

## 2. JWT Auth Flow

### Register
```javascript
const { data } = await api.post("/auth/register/", {
  username: "ramesh",
  email: "ramesh@test.com",
  password: "Test@1234",
  role: "local",
  phone: "+919999999999",
  region: "imphal",
  business_name: "Ramesh Handicrafts",
});

localStorage.setItem("access_token", data.access);
localStorage.setItem("refresh_token", data.refresh);
```

### Login
```javascript
const { data } = await api.post("/auth/login/", {
  username: "ramesh",
  password: "Test@1234",
});

localStorage.setItem("access_token", data.access);
localStorage.setItem("refresh_token", data.refresh);
```

### Get Current User
```javascript
const { data } = await api.get("/auth/me/");
console.log(data); // { username, role, phone, region, ... }
```

### Logout
```javascript
localStorage.removeItem("access_token");
localStorage.removeItem("refresh_token");
```

---

## 3. Playing Base64 Audio

Create `src/utils/audio.js`:

```javascript
export function playBase64Audio(base64, format = "mp3") {
  if (!base64) return null;

  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }

  const blob = new Blob([bytes], { type: `audio/${format}` });
  const url = URL.createObjectURL(blob);
  const audio = new Audio(url);

  audio.addEventListener("ended", () => URL.revokeObjectURL(url), { once: true });
  audio.play().catch((err) => console.error("Autoplay blocked:", err));

  return audio;
}
```

**Usage:**
```javascript
const { data } = await api.post("/companion/ask/", {
  question: "Where can I see a sunset?",
  target_language: "mni-IN",
});

playBase64Audio(data.audio.base64);
```

⚠️ **Always call this from a user click** — browsers block autoplay.

---

## 4. Voice Capture (Web Speech API)

Create `src/utils/speech.js`:

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

  recognition.onresult = (e) => onResult(e.results[0][0].transcript);
  recognition.onerror = (e) => onError?.(e.error);

  recognition.start();
  return recognition;
}
```

**Usage:**
```javascript
startListening({
  lang: "en-IN",
  onResult: async (question) => {
    const { data } = await api.post("/companion/ask/", {
      question,
      target_language: "mni-IN",
    });
    playBase64Audio(data.audio.base64);
  },
});
```

---

## 5. Offline Region Cache (IndexedDB)

Install: `npm install idb`

Create `src/utils/idb.js`:

```javascript
import { openDB } from "idb";

const dbPromise = openDB("xcalate", 1, {
  upgrade(db) {
    db.createObjectStore("regions");
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
};
```

**Download + cache a region:**
```javascript
async function downloadRegion(slug) {
  const { data } = await api.get(`/regions/${slug}/download/`);
  await idb.set(`region:${slug}`, data);
  console.log(`Cached ${data.places.length} places for ${slug}`);
}
```

**Read offline (falls back to cache if network fails):**
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

---

## 6. Standard Error Handling

```javascript
api.interceptors.response.use(
  (r) => r,
  (err) => {
    const data = err.response?.data;
    if (data?.message) {
      console.error(`[API] ${data.error}: ${data.message}`);
    }
    return Promise.reject(err);
  }
);
```

All errors follow this shape:
```json
{
  "error": "unsupported_language",
  "message": "Language 'xx-XX' is not supported",
  "code": "UNSUPPORTED_LANGUAGE"
}
```

---

## 7. Test Credentials (local dev)

| Username | Password | Role |
|---|---|---|
| `ramesh` | `Test@1234` | local (seller) |
| `adish` | `Test@1234` | tourist |

---

## 8. The 3 Things That Trip Up Frontend Devs

1. **Autoplay is blocked** → always trigger from a click
2. **`Bearer ` needs a space** → `Bearer eyJ...`
3. **JWT expires in 1 hour** → use `/auth/refresh/` or re-login

---

**Read `API.md` for full endpoint details. Read `FEATURES.md` for the map. This file is for the "how do I actually code it" moments.**