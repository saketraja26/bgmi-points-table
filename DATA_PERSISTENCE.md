# Data Persistence Options for Online Deployment

## ⚠️ IMPORTANT: CSV Files Don't Persist Online

Your current app stores data in CSV files, which **will be deleted** every time Render restarts your app (usually every 15 minutes of inactivity on free tier, or on each deploy).

## 🎯 Solutions for Online Data Storage

### **Option 1: PostgreSQL Database (Recommended for Render)**

1. **Create Free PostgreSQL on Render**:
   - Go to Render Dashboard → "New +" → "PostgreSQL"
   - Name: `aarohan-bgmi-db`
   - Free tier is sufficient
   - Copy the "Internal Database URL"

2. **Update your app** (I can help with this):
   - Replace CSV storage with PostgreSQL
   - Add `psycopg2-binary` to requirements.txt
   - Modify `app.py` to use database instead of files

### **Option 2: Supabase (Free PostgreSQL with Easy Setup)**

1. Sign up at [supabase.com](https://supabase.com)
2. Create new project
3. Get connection string
4. Update app to use Supabase

### **Option 3: Google Sheets API (Simple but Slower)**

1. Store data in Google Sheets
2. Use `gspread` library to read/write
3. Good for small tournaments

### **Option 4: Railway PostgreSQL**

If you deploy on Railway instead:
- Click "New" → "Database" → "Add PostgreSQL"
- Free 500MB storage
- Auto-connects to your app

### **Option 5: Accept Data Loss + Manual Backup**

- Keep CSV files for local use only
- Manually backup data periodically
- **Not recommended for live tournaments**

---

## 🚀 Quick Fix: Add PostgreSQL to Current Setup

Would you like me to:
1. Convert your app to use PostgreSQL database?
2. Keep CSV files for local development?
3. Auto-detect environment (local = CSV, online = PostgreSQL)?

Let me know and I'll implement the database solution!
