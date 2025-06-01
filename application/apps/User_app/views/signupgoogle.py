from application.apps.User_app import users
from application import google_oauth, db
from flask import url_for, jsonify, request, redirect
from application.utils import decoder, generate_random_password, Password_Hash
from application.apps.User_app.utils import Send_Mail
from application.apps.User_app.model import User
from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

#new changes
@users.route('/create_link_google', methods=['GET'])
def Create_Link_Google():
    redirect_uri = "http://127.0.0.1:80/user/google_authorize"#url_for('users.Google_Authorize', _external=True)
    params = {
        'scope': 'email',
        'response_type': 'code',
        'redirect_uri': redirect_uri
    }
    try:
        authorize_link = google_oauth.get_authorize_url(**params)
    except:
        return jsonify({'message':'an error to make link'})
    return jsonify({'authorize_link': authorize_link})


@users.route('/google_authorize', methods=['GET'])
def Google_Authorize():
    code = request.args.get('code')
    if not code:
        return jsonify({'message': 'Invalid authorization code'}), 400

    data = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': "http://127.0.0.1:80/user/google_authorize"#url_for('users.Google_Authorize', _external=True)
    }

    try:
        token = google_oauth.get_access_token(data=data, decoder=decoder)
        if not token:
            return jsonify({'message': 'Failed to get access token'}), 400

        google_info = google_oauth.get_session(token)
        user_info = google_info.get('https://www.googleapis.com/oauth2/v2/userinfo').json()
        email = user_info.get('email')

        if not email:
            return jsonify({'message': 'Failed to get user email from Google'}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return redirect(url_for('users.SignUp_Google', token= token))

        return jsonify({
            'access_token': create_access_token(identity=email),
            'refresh_token': create_refresh_token(identity=email),
            'is_completed': user.is_complate
        })

    except Exception as e:
        return jsonify({'message': str(e)}), 500


@users.route('/signup_google/<token>', methods=['Get'])
def SignUp_Google(token):
    
    try:
        google_info = google_oauth.get_session(token)
        user_info = google_info.get('https://www.googleapis.com/oauth2/v2/userinfo').json()
        email = user_info.get('email')

        
        if not email:
            return jsonify({'message': 'Email is required'}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return redirect(url_for('users.SignIn_Google', token=token))

        user = User()
        user.email = email
        user.password = Password_Hash(generate_random_password())
        user.create_at = datetime.utcnow()
        user.is_active = True
        user.is_complate = False
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=email, fresh=True)
        refresh_token = create_refresh_token(identity=email)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'is_completed': user.is_complate
        })
    except :
        return jsonify({'message': 'can\'t sign up'}), 400
    
    
    


@users.route('/signin_google/<token>', methods=['POST'])
def SignIn_Google(token):
    try:
        google_info = google_oauth.get_session(token)
        user_info = google_info.get('https://www.googleapis.com/oauth2/v2/userinfo').json()
        email = user_info.get('email')
        if not email:
            return jsonify({'message': 'Email is required'}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        if not user.is_complate:
            return redirect(url_for('users.CompleteInformation', email=email))

        access_token = create_access_token(identity=email, fresh=True)
        refresh_token = create_refresh_token(identity=email)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'is_completed': user.is_complate
        })
    except:
        return jsonify({'message': 'can\'t sign in'}), 400





