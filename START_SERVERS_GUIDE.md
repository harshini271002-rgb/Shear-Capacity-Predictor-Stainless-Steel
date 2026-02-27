# 🚀 HOW TO START THE SERVERS

## ⚠️ The localhost link requires servers to be running first!

### **Quick Start - Method 1 (Easiest):**

1. **Open File Explorer**
2. **Navigate to:** `E:\Input Day 2`
3. **Double-click:** `start_servers.bat`
4. **Wait 5 seconds** for both servers to start
5. Browser will automatically open to the application

---

### **Quick Start - Method 2 (Manual):**

**Step 1: Start Frontend Server**
```powershell
cd "E:\Input Day 2"
python -m http.server 8080 --directory frontend
```
*(Keep this window open)*

**Step 2: Start Backend Server** (New terminal window)
```powershell
cd "E:\Input Day 2\backend"
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```
*(Keep this window open too)*

**Step 3: Open Browser**
```
http://localhost:8080/complete_analysis.html
```

---

## ✅ How to Tell if Servers are Running:

You should see:
- **Frontend**: `Serving HTTP on :: port 8080...`
- **Backend**: `Uvicorn running on http://127.0.0.1:8000`

---

## 🔗 Your Links (Only work when servers are running):

### **Main Application:**
```
http://localhost:8080/complete_analysis.html
```

### **Alternative Apps:**
```
http://localhost:8080/interactive_predictor.html
http://localhost:8080/dashboard.html
http://localhost:8080/beam_visualizer.html
```

---

## 🛠️ Troubleshooting:

**Problem:** Port already in use  
**Solution:** Close any other applications using port 8080 or 8000

**Problem:** Python not found  
**Solution:** Make sure Python is installed and in PATH

**Problem:** Backend import errors  
**Solution:** Install dependencies first:
```powershell
cd "E:\Input Day 2"
pip install -r requirements.txt
```

---

## 📌 EASIEST METHOD:

Just **double-click `start_servers.bat`** in your `E:\Input Day 2` folder!

The browser will automatically open to the correct page.
