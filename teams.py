from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from auth import login_required
from db import get_db

bp = Blueprint('teams', __name__)

@bp.route('/teams')
@login_required
def index():
    db = get_db()
    
    # Fetch all teams with their creator's username
    teams = db.execute(
        'SELECT t.id, t.name, t.description, t.creator_id, u.username as creator_name '
        'FROM teams t JOIN users u ON t.creator_id = u.id ORDER BY t.name ASC'
    ).fetchall()
    
    # Fetch all team members and group them by team_id
    members_data = db.execute(
        'SELECT tm.team_id, tm.user_id, u.username '
        'FROM team_members tm JOIN users u ON tm.user_id = u.id'
    ).fetchall()
    
    team_members = {}
    for row in members_data:
        t_id = row['team_id']
        if t_id not in team_members:
            team_members[t_id] = []
        team_members[t_id].append({'user_id': row['user_id'], 'username': row['username']})
        
    return render_template('teams/index.html', active_page='teams', teams=teams, team_members=team_members)

@bp.route('/create-team', methods=('POST',))
@login_required
def create_team():
    name = request.form['name'].strip()
    description = request.form['description'].strip()
    error = None

    if not name:
        error = 'Team name is required.'

    if error is not None:
        flash(error, 'error')
    else:
        db = get_db()
        try:
            # Insert into teams table
            cur = db.execute(
                'INSERT INTO teams (name, description, creator_id) VALUES (?, ?, ?)',
                (name, description, g.user['id'])
            )
            team_id = cur.lastrowid
            
            # Immediately add the creator as a team member
            db.execute(
                'INSERT INTO team_members (user_id, team_id) VALUES (?, ?)',
                (g.user['id'], team_id)
            )
            db.commit()
            flash(f'Team "{name}" successfully created!', 'success')
        except Exception as e:
            flash(f'Error creating team: {str(e)}', 'error')

    return redirect(url_for('teams.index'))

@bp.route('/join-team', methods=('POST',))
@login_required
def join_team():
    team_id = request.form['team_id']
    db = get_db()
    
    try:
        db.execute(
            'INSERT INTO team_members (user_id, team_id) VALUES (?, ?)',
            (g.user['id'], team_id)
        )
        db.commit()
        flash('Successfully joined the team!', 'success')
    except db.IntegrityError:
        flash('You are already a member of this team.', 'error')
    except Exception as e:
        flash(f'Error joining team: {str(e)}', 'error')
        
    return redirect(url_for('teams.index'))
