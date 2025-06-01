from application.apps.User_app import users
from flask import jsonify,request,url_for , render_template
from application.apps.User_app.utils import Send_Mail
from jwt import ExpiredSignatureError,InvalidTokenError
import jwt
from datetime import datetime,timedelta
from application import app,db,limiter,redis_client
from application.apps.User_app.model import User , Wallet
from flask_jwt_extended import create_access_token, create_refresh_token , jwt_required,get_jwt_identity
from application.utils import check_Password,Password_Hash



#+
@users.route('/signin', methods=['POST'])
def signin():
        data = request.get_json()

        email = str(data['email']).strip().lower()
        password = data['password']


      #   language_code = 'en'
      #   request.headers.clear()
        language_code = data['language_code']

        user = User.query.filter(User.email == email).first()
        if user == None:
                message =  {
                      'message_en' : 'email or password incorrect !!',
                      'message_fa' : 'ایمل یا رمزعبور نادرست است'

                      }
                return jsonify({'message' : message.get(f'message_{language_code}') }),400
              
        
        if user.is_active == False:
              User.Delete_User(email)
              message =  {
                  'message_en' : 'please again register',
                  'message_fa' : 'لطفا از ابتدا ثبت نام کنید'
                  }
              return jsonify({'message' : message.get(f'message_{language_code}')}),410
              

        
        if check_Password(user.password , password):
                message =  {
                      'message_en' : 'login success',
                      'message_fa' : 'ورود موفقیت آمیز بود'

                      }
                access_token =create_access_token(identity=user.email,fresh=True,expires_delta=timedelta(minutes=30))
                refresh_token=create_refresh_token(identity=user.email,expires_delta=timedelta(days=15))
                return jsonify({"access_token":access_token , 'refresh_token' : refresh_token , 'is_completed' :  user.is_complate , 'message' : message.get(f'message_{language_code}')}),200
        else:
                  message =  {
                      'message_en' : 'email or password incorrect !!!',
                      'message_fa' : 'ایمل یا رمز-عبور نادرست است'

                      }
                  return jsonify({'message' : message.get(f'message_{language_code}')}),400                 

#+
@users.route('/send_active_link',methods = ['POST'])
@limiter.limit("10 per minute")
def Send_Active_Link():
        data = request.get_json()
        email = str(data['email']).strip().lower()
        password = data['password']
        language_code = data['language_code']
        user = User.query.filter(User.email == email).first()
        if user != None:
              message =  {
                      'message_en': 'user exist already !',
                      'message_fa': 'کاربر از قبل وجود دارد '

                      }
              return jsonify({'message' : message.get(f'message_{language_code}')}),409
        if redis_client.get(email+"active_link") != None:
              message =  {
                      'message_en': 'The activation link has already been sent to you',
                      'message_fa': 'لینک فعالسازی از قبل برای شما ارسال شده است'
                      }
              return jsonify({'message' : message.get(f'message_{language_code}')}),409
        try:
                
                
                token = jwt.encode({'email':email ,'password':password, 'exp':datetime.utcnow()+timedelta(minutes=15)},app.config['SECRET_KEY'],algorithm='HS256')
                active_link = url_for('users.give_token' , token = token , _external = True,)
                Send_Mail(subject='active your account' , recipients=[email] , body=f"your link is : \n {active_link}")
                redis_client.set(email+"active_link", 1 , ex=900 )

        
        except Exception as E:
                  message =  {
                      'message_en': 'can\'n sent email please try again later.',
                      'message_fa': 'لینک فعالسازی ارسال نشده بعدا مجددا تلاش کنید'                   
                                        }
                  return jsonify({'message' : message.get(f'message_{language_code}')}),500

        message =  {
                      'message_en': 'please check your email !',
                      'message_fa': 'لطفا ایمیل خود را چک کنید'                 
                                        }
        return jsonify({'message' : message.get(f'message_{language_code}')}),200   


@users.route('/give_token/<token>',methods = ['GET'])
def give_token(token):
        
        try:
                decode_token = jwt.decode(token ,app.config['SECRET_KEY'], algorithms='HS256' )
                email = str(decode_token['email']).lower()
                password = decode_token['password']
                User.Add_User(email=email,password= password)
                return jsonify({'message_en' : 'account is active!!!. please login','message_fa' : 'اکانت شما فعال شد . لطفا وارد شوید'}),201
        except ExpiredSignatureError:
                return jsonify({'message_en': 'please signup again!.','message_fa' : 'لطفا مجددا ثبت نام کنید'}), 402
        except InvalidTokenError:
                return jsonify({'message_en': 'it is wrong','message_fa' : 'مشکلی رخ داده'}), 405
        
#+
@users.route('/complate_page', methods=['POST'])
@jwt_required()
def signup_user():
    data = request.get_json()
    f_name = data.get('f_name')
    l_name = data.get('l_name')
    phone = data.get('phone')
    gender = data.get('gender')
    city_id = data.get('city_id')
    language_code = data['language_code']


    try:
        identity = get_jwt_identity()
        user = User.query.filter(User.email == identity).first()
        
        if user is None:
            message =  {
                      'message_en': 'User not found',
                      'message_fa' : 'کاربر پیدا نشد'                
                                        }
            return jsonify({'message' : message.get(f'message_{language_code}')}),404   
            
        if user.is_complate :
                  message =  {
                      'message_en': 'your information is complate',
                      'message_fa' : 'اطلاعات شما از قبل تکمیل شده'               
                                        }
                  return jsonify({'message' : message.get(f'message_{language_code}')}),425   
        phone_user = User.query.filter(User.phone == phone).first()
        if phone_user != None :
                  message =  {
                      'message_en': 'this phone is for another user',
                      'message_fa' : 'این شماره برای کاربر دیگری است'             
                                        }
                  return jsonify({'message' : message.get(f'message_{language_code}')}),426   
       
              
 
              
        
        user.f_name = f_name
        user.l_name = l_name
        user.phone = phone
        user.gender = bool(gender)
        user.city_id = city_id
        user.photo_url = 'default'
        user.is_complate = True
        
        User.Add_Wallet(identity)
        db.session.commit()
        message =  {
                      'message_en': f"Welcome {f_name}",
                      'message_fa' : f'{f_name} خوش امدی'            
                                        }
        return jsonify({'message' : message.get(f'message_{language_code}')}),200   
       

    except Exception as e:
            message =  {
                      'message_en': f"Information completion failed. Please contact support\n{e}",
                      'message_fa' : 'تکمیل اطلاعات ناموفق بود لطفا با پشتیبانی تماس بگیرید'   
                                        }
            return jsonify({'message' : message.get(f'message_{language_code}')}),400 

#+
@users.route('/forget_password', methods=['POST'])
@limiter.limit("3 per minute")
def Forget_Password():
    data = request.get_json()
    email =str(data['email']).strip().lower()
    language_code = data['language_code']

    if not User.Check_Exist_User(email):
            message =  {
                      'message_en': 'can\'t find user!.' ,
                      'message_fa' : 'کاربر وجود ندارد'               
                                        }
            return jsonify({'message' : message.get(f'message_{language_code}')}),404   
    if redis_client.get(email+"reset_link") != None:
            message =  {
                      'message_en': 'The reset_password_link has already been sent to you',
                      'message_fa' : 'لینک بازیابی برای شما ارسال شده'            
                                        }
            return jsonify({'message' : message.get(f'message_{language_code}')}),425   
    
    rest_token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(minutes=15)},
                            app.config['SECRET_KEY'], algorithm='HS256')
    
    rest_token = rest_token.decode('utf-8') if isinstance(rest_token, bytes) else rest_token
    
    rest_link = url_for('users.Rest_Password', token=rest_token, _external=True)
    Send_Mail(subject='reset_password', recipients=[email], body=f'this is reset password link: {rest_link}')
    redis_client.set(email+"reset_link", 1 , ex=900 )
    message =  {
                      'message_en': 'send reset password link' ,
                      'message_fa' : "لینک بازیابی ارسال شد"          
                                        }
    return jsonify({'message' : message.get(f'message_{language_code}')}),200   

#+
@users.route('/rest_password', methods=['POST', 'GET'])
def Rest_Password():

    token = request.args.get('token')
    
    if not token:
        return jsonify({'message_en': 'There is a problem','message_fa' : "مشکلی وجود دارد"}), 400

    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        email = decoded_token['email']
        user = User.query.filter(User.email == email).first()
    except ExpiredSignatureError:
        User.Delete_User(email)
        return jsonify({'message_en': 'There is a problem.' , 'message_fa' : 'مشکلی وجود دارد'}), 400
    except jwt.InvalidTokenError:
        return jsonify({'message_en': 'There is a problem, please check your link!!!.', 'message_fa' : "مشکلی وجود دارد ، مجدد درخواست دهید"}), 400

    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if new_password != confirm_password:
            return jsonify({'message_en': f'Password and confirm password do not match',"message_fa" : "رمز و تکرار آن مطابقت ندارند "}), 400
        
        user.password = Password_Hash(new_password)
        db.session.commit()
        return jsonify({'message': 'Password change successful!!!.',"message_fa" : "رمز عبور با موفقیت تغییر کرد"}), 200

    return render_template('forget_password.html')


@users.route('/create_new_access_token',methods = ['PUT'])
@jwt_required(refresh=True)
def Create_Access_token():
      try:
            identity = get_jwt_identity()
            return jsonify({'access_token' : f"{create_access_token(identity=identity)}"}),200
      except ExpiredSignatureError:
            return jsonify({'access_token' : "error"}),401
            
            


@users.route('/log_out' , methods  = ['DELETE'])
@jwt_required(refresh=True)
def Log_Out():
      #delete refresh token from local memory
      return jsonify({'message' : 'log out successfully'}) 




        



#+
@users.route('/getuser_info' , methods = ['GET'])
@jwt_required()
def getuserinfo():
      data = request.get_json()
      language_code = data['language_code']
      try :
            identity = get_jwt_identity()
            user = User.query.filter(User.email == identity).first()
            gen = ''
            if user.gender :
                  gen = 'Male'
            else:
                  gen = 'Famale'
            wallet = Wallet.query.filter(Wallet.user_id == user.id).first()
            city = ''
            if language_code == 'en':
                  city = user.city.name_en
            else:
                  city = user.city.name_fa


            return jsonify(
                  {
                        'email' : f'{user.email}',
                        'f_name' : f'{user.f_name}',
                        'l_name' : f'{user.l_name}',
                        'email' : f'{user.email}',
                        'phone' : f'{user.phone}',
                        'city' : f'{city}',
                        'gender' : f'{gen}',
                        'balance' : f'{wallet.balance}'


                  }
                ),200
      except ExpiredSignatureError:
            return jsonify({'message' : 'yourtoken has expire'}),400
      except InvalidTokenError:
            return jsonify({'message' : 'yourtoken has invalid'}),400
      except Exception as e:
            return jsonify({'message' : f'{e}'}),400
            
#+         
@users.route('/increase_wallet' , methods = ['POST'])
@jwt_required()
def Increase_Wallet():
      

      
                
      identity = get_jwt_identity()
      data = request.get_json()
      amount = data['amount']
      language_code = data['language_code']
      if amount <= 0 :
            message =  {
                      'message_en' : 'amount cant be 0 ',
                      'message_fa' : 'مقدار افزایشی نمیتواند صفر یا کمتر باشد'

                      }
            return jsonify({'message' : message.get(f'message_{language_code}') }),400
      
      user = User.query.filter(User.email == identity).first()
      wallet = Wallet.query.filter(Wallet.user_id == user.id).first()

      if wallet == None:
            message =  {
                      'message_en' : 'your information not complate',
                      'message_fa' : 'اطلاعات شما کامل نیست'

                      }
            return jsonify({'message' : message.get(f'message_{language_code}') }),400
      wallet.balance += amount
      db.session.commit()
      message =  {
                      'message_en' : 'success increase',
                      'message_fa' : 'شارز حساب موفقیت آمیز بود'

                      }
      return jsonify({'message' : message.get(f'message_{language_code}') }),200
 

            
      
@users.route('/decrease_wallet' , methods = ['POST'])
@jwt_required()
def Decrease_Wallet():
      identity = get_jwt_identity()
      data = request.get_json()
      amount = data['amount']
      language_code = data['language_code']

      if amount <= 0 :
            message =  {
                      'message_en' : 'amount cant be 0 ',
                      'message_fa' : 'مقدار کاهشی نمیتواند صفر یا کمتر باشد'

                      }
            return jsonify({'message' : message.get(f'message_{language_code}') }),400
      
      user = User.query.filter(User.email == identity).first()
      wallet = Wallet.query.filter(Wallet.user_id == user.id).first()

      if wallet == None:
            message =  {
                      'message_en' : 'your information not complate',
                      'message_fa' : 'اطلاعات شما کامل نیست'

                      }
            return jsonify({'message' : message.get(f'message_{language_code}') }),400
      result = wallet.balance - amount
      if result>=0:
            wallet.balance -= amount
            db.session.commit()
            message =  {
                      'message_en' : 'success  Decrease',
                      'message_fa' : 'کاهش از حساب موفقیت آمیز بود'

                      }
            return jsonify({'message' : message.get(f'message_{language_code}') }),200
      else:
            message =  {
                      'message_en' : 'not have enught',
                      'message_fa' : 'موجودی کافی نیست'

                      }
            return jsonify({'message' : message.get(f'message_{language_code}') }),400
            



#+
@users.route('/update_user', methods=['PUT'])
@jwt_required()
def Update_User():
        data = request.get_json()
        photo_url = str(data['photo_url'])
        f_name = str(data['f_name'])
        l_name = str(data['l_name'])
        email = str(data['email'])
        phone_number = str(data['phone_number'])
        city = int(data['city'])
        gender = bool(data['gender'])
        language_code = data['language_code']

        

        identity = get_jwt_identity()
        user = User.query.filter(User.email == identity).first()
        try:
               user.photo_uri = photo_url
               user.f_name = f_name
               user.l_name = l_name
               user.email = email
               user.phone = phone_number
               user.city_id = city
               user.gender = gender
               db.session.commit()
               message =  {
                      'message_en' : 'update success ',
                      'message_fa' : ' ویرایش موفقیت آمیز بود'

                      }
               return jsonify({'message' : message.get(f'message_{language_code}') }),200
              
        except Exception as e :
            return jsonify({'message' : f'{e} , {user}'}),400
        



#not complate
@users.route('/del_user', methods=['DELETE'])
def DELETE_USER():
      pass
#not complate



            
      
      
      
            
      






 
 
 
 


    



        

       



        
        