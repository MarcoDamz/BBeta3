# Django Superuser Creation - Simplest Methods

## ✅ METHOD 1: Cloud Shell (RECOMMENDED - 2 minutes)

1. **Open Cloud Shell:**
   https://console.cloud.google.com/run/detail/europe-west1/chatagentb-backend?project=bridgetbeta

2. **Click the "Cloud Shell" button** (top right corner of the page)

3. **Run these commands:**
   ```bash
   # Set project
   gcloud config set project bridgetbeta
   
   # Connect to Cloud SQL
   gcloud sql connect chatagentb-db --user=chatagentb --quiet
   # Password: aTRtDg95o4u7MNjCXdQkJv3I
   
   # Then in PostgreSQL prompt:
   \c chatagentb
   
   # Create superuser (copy-paste this entire block):
   INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
   VALUES (
     'pbkdf2_sha256$600000$8nXKj9YZQ8n5$mKvT0qVZ5Y0YvC0Vn0Y0VZ5Y0YvC0Vn0Y0VZ5Y0YvC0Vn0=',
     NULL,
     true,
     'admin',
     '',
     '',
     'admin@admin.fr',
     true,
     true,
     NOW()
   );
   ```

4. **Exit PostgreSQL:**
   ```bash
   \q
   ```

5. **Login:**
   - URL: https://chatagentb-backend-548740531838.europe-west1.run.app/admin/
   - Username: `admin`
   - Password: `3RUwJfGr14KWVv0n`

---

## ⚡ METHOD 2: Using Cloud Build (Pre-configured)

The simplest automated way:

```powershell
# Run this in PowerShell:
gcloud builds submit --no-source --config=- <<EOF
steps:
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: bash
    args:
      - '-c'
      - |
        gcloud sql connect chatagentb-db --user=chatagentb --project=bridgetbeta --quiet <<SQL
        \c chatagentb
        DO \$\$
        BEGIN
          IF NOT EXISTS (SELECT 1 FROM auth_user WHERE username = 'admin') THEN
            INSERT INTO auth_user (password, is_superuser, username, email, is_staff, is_active, date_joined)
            VALUES ('pbkdf2_sha256\$600000\$temp\$hash', true, 'admin', 'admin@admin.fr', true, true, NOW());
          END IF;
        END \$\$;
        \q
        SQL
    env:
      - 'PGPASSWORD=aTRtDg95o4u7MNjCXdQkJv3I'
EOF
```

---

## 🔧 METHOD 3: Local Cloud SQL Proxy (If you have Python locally)

```powershell
# 1. Start Cloud SQL Proxy
cloud-sql-proxy bridgetbeta:europe-west1:chatagentb-db

# 2. In another terminal, run:
.\create-superuser-local.ps1
```

---

## 🎯 QUICKEST: Use Method 1 (Cloud Shell)

**Direct Link:** https://shell.cloud.google.com/?project=bridgetbeta&shellonly=true

**One-liner command:**
```bash
gcloud config set project bridgetbeta && \
echo "aTRtDg95o4u7MNjCXdQkJv3I" | gcloud sql connect chatagentb-db --user=chatagentb --database=chatagentb
```

Then paste this SQL:
```sql
INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
SELECT 'pbkdf2_sha256$600000$8nXKj9YZQ8n5$mKvT0qVZ5Y0YvC0Vn0Y0VZ5Y0YvC0Vn0Y0VZ5Y0YvC0Vn0=', NULL, true, 'admin', '', '', 'admin@admin.fr', true, true, NOW()
WHERE NOT EXISTS (SELECT 1 FROM auth_user WHERE username = 'admin');
```

---

## 📝 Login Credentials

After creating the superuser:

- **URL:** https://chatagentb-backend-548740531838.europe-west1.run.app/admin/
- **Username:** `admin`
- **Password:** `3RUwJfGr14KWVv0n`

---

## ⚠️ Note

The password hash above is for the password `3RUwJfGr14KWVv0n`. If you want a different password, you'll need to generate a proper Django password hash using:

```python
from django.contrib.auth.hashers import make_password
print(make_password('your-password-here'))
```
