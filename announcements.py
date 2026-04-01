from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from auth import login_required
from db import get_db

bp = Blueprint('announcements', __name__)

@bp.route('/announcements')
def index():
    db = get_db()
    cur = db.execute('SELECT * FROM announcements ORDER BY created_at DESC')
    announcements = cur.fetchall()
    return render_template('announcements/index.html', announcements=announcements, active_page='announcements')

@bp.route('/add-announcement', methods=('POST',))
@login_required
def add_announcement():
    # Only allow the first user or a user explicitly named 'admin' to post announcements 
    if g.user['username'].lower() != 'admin' and g.user['id'] != 1:
        flash('Only system administrators can broadcast announcements.', 'error')
        return redirect(url_for('announcements.index'))

    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    
    if not title or not content:
        flash('Headline and content are required.', 'error')
    else:
        db = get_db()
        try:
            db.execute(
                'INSERT INTO announcements (title, content) VALUES (?, ?)',
                (title, content)
            )
            db.commit()
            flash('Announcement successfully broadcasted!', 'success')
        except Exception as e:
            flash(f'Error creating announcement: {str(e)}', 'error')

    return redirect(url_for('announcements.index'))
