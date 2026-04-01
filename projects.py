import os
from datetime import datetime
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app
from werkzeug.utils import secure_filename
from auth import login_required
from db import get_db

bp = Blueprint('projects', __name__)

ALLOWED_PROJECT_EXTENSIONS = {'pdf', 'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PROJECT_EXTENSIONS

@bp.route('/projects')
def index():
    db = get_db()
    
    cur = db.execute('''
        SELECT p.*, t.name as team_name, u.username as creator_name 
        FROM projects p 
        JOIN teams t ON p.team_id = t.id 
        JOIN users u ON t.creator_id = u.id 
        ORDER BY p.id DESC
    ''')
    projects = cur.fetchall()
            
    return render_template('projects/index.html', projects=projects, active_page='projects')

@bp.route('/submit-project', methods=('GET', 'POST'))
@login_required
def submit_project():
    db = get_db()
    user_id = g.user['id']
    
    # Fetch user's teams for the dropdown
    cur = db.execute('''
        SELECT DISTINCT t.* FROM teams t 
        LEFT JOIN team_members tm ON t.id = tm.team_id 
        WHERE t.creator_id = ? OR tm.user_id = ?
    ''', (user_id, user_id))
    user_teams = cur.fetchall()
    
    if not user_teams:
        flash('You must join or create a team before submitting a project.', 'error')
        return redirect(url_for('teams.index'))
        
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        team_id = request.form.get('team_id')
        
        error = None
        if not title or not description or not team_id:
            error = 'Title, description, and team selection are required.'

        file = request.files.get('file')
        file_filename = None
        
        if not file or file.filename == '':
            error = 'A project file (PDF or ZIP) is required.'
        elif not allowed_file(file.filename):
            error = 'Invalid file type. Only PDF and ZIP files are allowed.'

        if error is not None:
            flash(error, 'error')
        else:
            try:
                # Securely grab and salt the file
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                file_filename = f"{timestamp}_{filename}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_filename))
                
                # Link project into Database with the associated team_id
                db.execute(
                    'INSERT INTO projects (team_id, title, description, file_path) VALUES (?, ?, ?, ?)',
                    (team_id, title, description, file_filename)
                )
                db.commit()
                
                flash('Project successfully submitted!', 'success')
                return redirect(url_for('projects.index'))
                
            except Exception as e:
                flash(f'Database error: {str(e)}', 'error')

    return render_template('projects/submit.html', active_page='submit-project', user_teams=user_teams)
