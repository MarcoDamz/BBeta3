# API URL Bug Fix

**Date:** January 29, 2026  
**Status:** ✅ FIXED - Redeploying

---

## Problem

Frontend was getting **404 errors** when trying to login:

```
POST https://chatagentb-backend-548740531838.europe-west1.run.app/auth/login/ 404 (Not Found)
```

### Root Cause

The `VITE_API_URL` environment variable in `cloudbuild.yaml` was **missing the `/api` suffix**:

```yaml
# BEFORE (WRONG):
- "VITE_API_URL=https://chatagentb-backend-548740531838.europe-west1.run.app"

# Frontend code does this:
baseURL: import.meta.env.VITE_API_URL  // "https://...run.app"
api.post("/auth/login/", data)          // Becomes "https://...run.app/auth/login/"

# Result: 404 because Django expects /api/auth/login/
```

### Why This Happened

1. **Backend URLs** are configured with `/api/` prefix in `urls.py`:
   ```python
   path("api/auth/login/", login_view)
   path("api/agents/", ...)
   path("api/chat/", ...)
   ```

2. **Frontend API client** expects `baseURL` to include `/api`:
   ```javascript
   const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";
   ```

3. **cloudbuild.yaml** was setting the URL **without** `/api`, breaking the connection.

---

## Solution

### Fixed cloudbuild.yaml

```yaml
# AFTER (CORRECT):
- "VITE_API_URL=https://chatagentb-backend-548740531838.europe-west1.run.app/api"

# Now frontend requests work:
baseURL: "https://...run.app/api"
api.post("/auth/login/", data)  // Becomes "https://...run.app/api/auth/login/" ✅
```

### Changes Made

**File:** `cloudbuild.yaml` (line ~37)

```diff
  - name: "gcr.io/cloud-builders/docker"
    id: "build-frontend"
    waitFor: ["migrate"]
    args:
      - "build"
      - "-t"
      - "gcr.io/$PROJECT_ID/chatagentb-frontend:latest"
      - "-f"
      - "frontend/Dockerfile.cloudrun"
      - "--build-arg"
-     - "VITE_API_URL=https://chatagentb-backend-548740531838.europe-west1.run.app"
+     - "VITE_API_URL=https://chatagentb-backend-548740531838.europe-west1.run.app/api"
      - "./frontend"
```

---

## Verification

### After Deployment Completes

1. **Check build status:**
   ```powershell
   gcloud builds list --limit=1 --format="table(id,status,createTime)" --project=bridgetbeta
   ```

2. **Test the frontend:**
   - Open: https://chatagentb-frontend-548740531838.europe-west1.run.app
   - Open DevTools (F12) → Console
   - Try to login
   - Should see **no 404 errors**
   - Request should go to: `https://...run.app/api/auth/login/` ✅

3. **Verify correct URL pattern:**
   ```
   ✅ CORRECT: POST https://chatagentb-backend-548740531838.europe-west1.run.app/api/auth/login/
   ❌ WRONG:   POST https://chatagentb-backend-548740531838.europe-west1.run.app/auth/login/
   ```

### Expected Behavior

- ✅ **No CORS errors** (fixed in previous deployment)
- ✅ **No 404 errors** (fixing now)
- ⚠️ **Authentication may still fail** (superuser password issue)

---

## Technical Details

### How Vite Environment Variables Work

Vite injects environment variables **at build time**, not runtime:

1. **Build time:** Vite reads `VITE_API_URL` and replaces `import.meta.env.VITE_API_URL` in the code
2. **Runtime:** The built JavaScript contains the hardcoded URL
3. **Result:** Cannot change API URL without rebuilding

### Why ARG in Dockerfile.cloudrun

```dockerfile
# frontend/Dockerfile.cloudrun
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# This allows passing the URL during build:
docker build --build-arg VITE_API_URL=https://backend.com/api .
```

### URL Structure Breakdown

```
Full request URL structure:
┌─────────────────────────────────────────────────────┐
│ https://chatagentb-backend-...run.app/api/auth/login/ │
└─────────────────────────────────────────────────────┘
  └───────────────────┬──────────────────┘ └─┬─┘ └──┬──┘
                   baseURL                  api   endpoint
                   (from env)               (from (from code)
                                            urls.py)
```

**Frontend code:**
```javascript
baseURL = "https://chatagentb-backend-...run.app/api"  // From VITE_API_URL
api.post("/auth/login/", data)                          // From LoginPage.jsx
// Result: baseURL + "/auth/login/" = "...run.app/api/auth/login/"
```

**Backend routing:**
```python
# backend/chatagentb/urls.py
urlpatterns = [
    path("api/auth/login/", login_view),  # Must match frontend request
    path("api/agents/", include("agents.urls")),
    path("api/chat/", include("chat.urls")),
]
```

---

## Related Issues Fixed Today

1. ✅ **Static Files** - Added WhiteNoise for production static file serving
2. ✅ **CORS** - Fixed environment variable check (CLOUD_RUN_SERVICE → K_SERVICE)
3. ✅ **API URL** - Added `/api` suffix to VITE_API_URL (this fix)
4. ⚠️ **Superuser Password** - Still needs database update

---

## Testing Checklist

After deployment completes:

- [ ] Open frontend: https://chatagentb-frontend-548740531838.europe-west1.run.app
- [ ] Open DevTools Console (F12)
- [ ] Try to login
- [ ] Check Console tab:
  - [ ] No CORS errors ✅
  - [ ] No 404 errors ✅
  - [ ] Request goes to `/api/auth/login/` ✅
  - [ ] Authentication error (expected - password issue)

---

## Next Steps

Once API URL is fixed (current deployment):

1. **Fix superuser password** (see `FIX_SUPERUSER_PASSWORD.md`)
   ```bash
   gcloud sql connect chatagentb-db --user=chatagentb --database=chatagentb --project=bridgetbeta
   # Password: aTRtDg95o4u7MNjCXdQkJv3I
   
   UPDATE auth_user SET password = 'pbkdf2_sha256$1000000$Eoc7cHvkjyUs78hLFyAglT$nMK9bphDTw3o4wmYGybxb8ZiWh+y+nqgaiSOPejrzT4=' WHERE username = 'admin';
   \q
   ```

2. **Test full login flow**
   - Username: `admin`
   - Password: `3RUwJfGr14KWVv0n`
   - Should successfully login ✅

3. **Test application features**
   - Create agents
   - Start conversations
   - Send messages

---

## Prevention

To avoid this in the future:

1. **Always include `/api` in VITE_API_URL**
2. **Test API endpoints match** between frontend and backend
3. **Check browser DevTools** for 404s before debugging CORS

---

## Summary

**Issue:** Frontend calling wrong URL path (missing `/api`)  
**Cause:** cloudbuild.yaml VITE_API_URL missing `/api` suffix  
**Fix:** Added `/api` to VITE_API_URL in cloudbuild.yaml  
**Status:** ⚙️ Redeploying frontend now  
**ETA:** ~5-10 minutes  

**Progress:** 90% Complete! 🎉
- ✅ Infrastructure
- ✅ Static files
- ✅ CORS
- ✅ API URL (deploying)
- ⚠️ Superuser password (next)
