# Inventory Management System

## Tech Stack

- FastAPI
- Jinja2
- SQLAlchemy (SQLite)
- Uvicorn
- aiofiles
- python-multipart

## Setup

1. **Clone the repository** (if not already):
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn jinja2 sqlalchemy aiofiles python-multipart passlib[bcrypt]
   ```
4. **Run the app:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Default Credentials

- **Admin**
  - Username: `admin`
  - Password: `admin123`
- **Viewer**
  - Username: `user`
  - Password: `user123`

You can also register new users via the signup page.

## Project Structure

```
/app
 ├── main.py
 ├── models.py
 ├── database.py
 ├── auth.py
 ├── inventory.py
 ├── templates/
 │    ├── base.html
 │    ├── login.html
 │    ├── signup.html
 │    ├── dashboard.html
 │    ├── add.html
 │    ├── edit.html
 │    └── search.html
 └── static/
      └── style.css
```

## How to Test

- Register a new user or use the default credentials above.
- Admins can add, edit, delete, and search inventory items.
- Viewers can only search and view inventory items.

## AI Chat Assistant (for Regular Users)

- Only available to users with the 'viewer' role (not admins).
- Uses OpenAI API and a help guide for RAG-style answers.
- To use:
  1. Set your OpenAI API key in `app/.env`:
     ```
     OPENAI_API_KEY=sk-...
     ```
  2. Start the app as usual.
  3. Log in as a regular user and go to `/chat` or click the Chat Assistant link (if available).
  4. Ask questions about how to use the system!

## Deployment: Hosting on Render

You can easily deploy this FastAPI app for free using [Render](https://render.com/):

1. **Push your code to GitHub** (include all files, especially `render.yaml` and `requirements.txt`).
2. **Create a new Web Service on Render:**
   - Go to [https://dashboard.render.com/](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo.
   - Render will auto-detect the `render.yaml` and set up the build and start commands.
3. **Set environment variables:**
   - In the Render dashboard, add `OPENAI_API_KEY` under Environment → Environment Variables.
   - (Optional) You can also use an `.env` file in the `app/` directory for secrets.
4. **Deploy:**
   - Click "Manual Deploy" or wait for auto-deploy.
   - Once deployed, open your Render URL to access the app.

**Notes:**

- Static files are served from `/static`.
- The app will be available at your Render-provided URL (e.g., `https://your-app.onrender.com`).
- Make sure to keep your OpenAI API key secret!

---
