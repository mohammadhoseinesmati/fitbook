from application import db
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime 
from application.utils import Password_Hash





class User(db.Model):
    __tablename__ = 'User'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    f_name = Column(String(32),nullable=True)
    l_name = Column(String(32),nullable=True)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(165), nullable=False)
    phone = Column(String(16), unique=True)
    gender = Column(Boolean, nullable=True)
    photo_url = Column(String(128), nullable=True)
    create_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    city_id = Column(Integer, ForeignKey('City.id', ondelete='SET NULL', onupdate='CASCADE'))
    is_active = Column(Boolean , nullable=False)
    is_complate = Column(Boolean , nullable=False)

    
    # Relationship
    city = relationship('City', backref='User')
    wallet = relationship('Wallet', backref='User', lazy='dynamic')
    ratings_givens = relationship('Gyms_List_point', backref='user')
    user_reservations = relationship("Gyms_Reservation" , backref='user' , lazy='dynamic')


    
    
    def Check_Exist_User(check_email):
        exist_user = User.query.filter(User.email == check_email).first()
        if exist_user == None:
            return False
        else:
            return True
        
    def Add_User(email , password):
        if User.Check_Exist_User(email):
            raise ValueError('user exist!!!.')
        try:
            user = User(
            email = email,
            password = Password_Hash(password),
            create_at = datetime.utcnow(),
            is_active = bool(1),
            is_complate = bool(0)
            )
            db.session.add(user)
            db.session.commit()
        except:
            raise ValueError('user can\'t signup')
    
    def Add_Wallet( email):
        if not User.Check_Exist_User(email):
            raise ValueError('user not exist!!!.')
        user = User.query.filter(User.email == email).first()
        Wallet.add_wallet(user.id)

    def Delete_User( email):
        if not User.Check_Exist_User(email):
            raise ValueError('user not exist!!!.')
        try : 
            user = User.query.filter(User.email == email).first()
            db.session.delete(user)
            db.session.commit()
        except:
            raise ValueError('cant delete user!!!.')
        
    def Change_Password(email , newpassword):
        if not User.Check_Exist_User(email):
            raise ValueError('user not exist!!!.')
        try : 
          user = User.query.filter(User.email == email).first()
          user.password = Password_Hash(newpassword)
          db.session.commit()
        except:
            raise ValueError('can\'t change password')



        



        


class Wallet(db.Model):
    __tablename__ = 'Wallet'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False , unique=True)
    balance = Column(Numeric(10, 2), nullable=False)
    last_update = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    # Relationship
    user_rel = relationship('User', backref='wallets')


    def add_wallet(user_id):
        try:
            make_wallet = Wallet()
            make_wallet.user_id = user_id
            make_wallet.balance = 0
            make_wallet.last_update = datetime.utcnow()
            db.session.add(make_wallet)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError('cant craete wallet!!!')



