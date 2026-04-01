from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from auth import login_required
from db import get_db

bp = Blueprint('chat', __name__)

@bp.route('/chat')
@login_required
def index():
    db = get_db()
    # Optimized query: Fetch the latest 100 messages, but keep them ordered ascending linearly for the chatview
    cur = db.execute('''
        SELECT * FROM (
            SELECT m.id, m.content, m.timestamp, m.user_id, u.username
            FROM messages m
            JOIN users u ON m.user_id = u.id
            ORDER BY m.timestamp DESC
            LIMIT 100
        ) ORDER BY timestamp ASC
    ''')
    messages = cur.fetchall()
            
    return render_template('chat/index.html', messages=messages, active_page='chat')

@bp.route('/send-message', methods=('POST',))
@login_required
def send_message():
    content = request.form.get('content', '').strip()
    
    if not content:
        flash('Message cannot be empty.', 'error')
    else:
        db = get_db()
        try:
            db.execute(
                'INSERT INTO messages (user_id, content) VALUES (?, ?)',
                (g.user['id'], content)
            )
            db.commit()
        except Exception as e:
            flash(f'Error sending message: {str(e)}', 'error')

    return redirect(url_for('chat.index'))
