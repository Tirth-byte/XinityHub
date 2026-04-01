import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, g

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.root_path, 'database.db'),
        UPLOAD_FOLDER=os.path.join(app.root_path, 'uploads'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize the database logic
    import db
    db.init_app(app)

    # Register the auth blueprint
    import auth
    app.register_blueprint(auth.bp)

    # Register the teams blueprint
    import teams
    app.register_blueprint(teams.bp)

    # Register the projects blueprint
    import projects
    app.register_blueprint(projects.bp)

    # Register the chat blueprint
    import chat
    app.register_blueprint(chat.bp)

    # Register the announcements blueprint
    import announcements
    app.register_blueprint(announcements.bp)

    # Register the AI blueprint
    import ai_bot
    app.register_blueprint(ai_bot.bp)

    @app.route('/')
    def index():
        return redirect(url_for('projects.index'))

    @app.route('/dashboard')
    @auth.login_required
    def dashboard():
        conn = db.get_db()
        user_id = g.user['id']
        
        # User's teams (created by user or where user is a member)
        cur = conn.execute('''
            SELECT DISTINCT t.* FROM teams t 
            LEFT JOIN team_members tm ON t.id = tm.team_id 
            WHERE t.creator_id = ? OR tm.user_id = ?
        ''', (user_id, user_id))
        user_teams = cur.fetchall()
        
        # Latest announcements
        cur = conn.execute('SELECT * FROM announcements ORDER BY created_at DESC LIMIT 5')
        announcements = cur.fetchall()
        
        return render_template('dashboard.html', active_page='dashboard', teams=user_teams, announcements=announcements)

    @app.route('/uploads/<name>')
    def download_file(name):
        return send_from_directory(app.config["UPLOAD_FOLDER"], name)

    return app

# The standard entry point if someone runs `python app.py` instead of `flask run`
app = create_app()

if __name__ == '__main__':
    # Initialize the database automatically if missing inside production environment
    with app.app_context():
        import db
        if not os.path.exists(app.config['DATABASE']) or os.path.getsize(app.config['DATABASE']) == 0:
            db.init_db()
            print("Database implicitly initialized for deployment environment.")
            
    # Cloud environments strictly bind dynamic available ports onto 0.0.0.0
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
