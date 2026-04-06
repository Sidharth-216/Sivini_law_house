# Sivini Law House - Legal Management Platform

A full-stack legal service platform that combines law-firm operations, client collaboration, online consultations, document workflows, invoicing, and AI-assisted legal interactions in one system.

## Why This Project

Most legal workflows are split across emails, spreadsheets, video apps, and offline paperwork. This project unifies those processes into one web platform for:

- Law firms managing clients, appointments, tasks, and billing
- Clients tracking case progress, documents, payments, and communication
- Online legal consultations with chat and video
- AI-supported legal assistance and virtual courtroom practice

## Core Features

### Authentication and User Management
- Client and lawyer registration/login
- CAPTCHA-protected login flow
- Face recognition login endpoint
- Password reset with OTP/email verification
- Profile management for both client and lawyer roles

### Client and Lawyer Dashboards
- Role-specific dashboards and pages
- Appointment booking and management
- Notification system (view, mark as read, delete)
- Review and feedback module

### Case, Document, and Task Workflows
- Case notes create/read/update/delete
- Document upload and retrieval
- Task management with status tracking
- Calendar support for appointments/events

### Billing and Payments
- Invoice creation and updates
- Payment status tracking (paid/pending/remaining)
- QR-based payment flow and payment history pages

### Real-time Communication and Consultations
- Real-time messaging with Socket.IO
- Video call room flows (create/join)
- Lawyer-client communication management pages

### AI and Smart Features
- AI legal chatbot integration (HuggingFace Inference API)
- Virtual courtroom practice flow with response/rating logic

## Tech Stack

### Backend
- Python, Flask
- Flask-SocketIO
- Flask-Mail
- Flask-CORS
- SQLite3

### Frontend
- HTML templates (multi-page app)
- CSS and JavaScript per feature module
- GSAP animations

### AI/ML and Media
- OpenCV (face recognition)
- NumPy
- Pillow
- HuggingFace Inference Client

### Realtime/Video
- Node.js + Express
- Socket.IO
- WebRTC signaling flow

## Project Structure

```text
.
|- app.py                         # Main Flask application and routes
|- database.py                    # DB helper/related logic
|- image_upload.py                # Upload-related utility logic
|- sqlite_maintainance_script.py  # Backup + maintenance script for SQLite
|- server.js                      # Node signaling server (video/realtime)
|- package.json                   # Node dependencies
|- lawfirm.db                     # Main SQLite database
|- templates/                     # HTML pages (dashboard, billing, docs, etc.)
|- static/                        # CSS/JS/images
|- db_backups/                    # Generated database backups
|- env/                           # Local Python virtual environment
```

## Quick Start

## 1) Prerequisites
- Python 3.10+
- Node.js 18+
- pip and npm

## 2) Python Setup

```bash
# from project root
python -m venv env
source env/bin/activate

pip install flask flask-socketio flask-mail flask-cors python-dotenv
pip install opencv-python numpy pillow huggingface-hub werkzeug pyjwt
```

## 3) Node Setup

```bash
npm install
```

## 4) Environment Variables

Create a local `.env` file in project root:

```env
DEL_EMAIL=your_email@gmail.com
PASSWORD=your_app_password
HF_API_TOKEN=your_huggingface_token
SECRET_KEY=replace_with_a_strong_secret
```

## 5) Run the App

Start Flask backend:

```bash
python app.py
```

Start Node signaling server (new terminal):

```bash
npm start
```

Then open the Flask URL shown in terminal (commonly `http://localhost:5001`).

## Database Maintenance

Run periodic maintenance and backup:

```bash
python sqlite_maintainance_script.py
```

Backups are saved under `db_backups/`.

## Key Modules and Pages

- Authentication: login, register, forgot/reset password, face login
- Lawyer operations: lawyer dashboard, client management, message management, enquiry management
- Client operations: appointment booking, profile, case notes, notifications
- Billing: invoices, payment records, QR payment flow
- Smart modules: chatbot, courtroom simulation, knowledge base
- Communication: chat rooms, video consultation pages

## Security and Production Notes

Before production deployment, strongly recommended:

- Move all secrets to `.env` only and never commit them
- Hash passwords using secure hashing (not plaintext)
- Add strict input validation and consistent parameterized queries
- Add CSRF protection and harden session handling
- Add a pinned `requirements.txt` for reproducible setup
- Add logging, error monitoring, and automated tests

## Roadmap Ideas

- Dockerized deployment for Flask + Node + SQLite backup jobs
- Role-based permission granularity (admin/senior/junior lawyer)
- Advanced legal search and citation assistance
- E-signature flow linked directly with case documents
- Audit trail for compliance and case-level activity history

## Contributing

Contributions are welcome. Suggested flow:

1. Fork the repository
2. Create a feature branch
3. Commit focused changes with clear messages
4. Open a pull request with testing notes

## License

Add your preferred license file (MIT/Apache-2.0/etc.) and update this section.

---

If you want, I can also generate a `requirements.txt` from current imports and add a deployment-ready README section for Render/EC2/VPS setup.
