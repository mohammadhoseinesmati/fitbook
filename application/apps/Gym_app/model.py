from application import db
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, Numeric, ForeignKey , Text , Table , Float , DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask import jsonify
from datetime import datetime 
from application.utils import Password_Hash
from application.apps.User_app import model
from application.apps.Category_app import model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# gyms_tags_table = Table(
#  'gyms_tags', db.metadata,
#  Column('gym_id', Integer, ForeignKey('gym.id', ondelete='CASCADE')),
#  Column('tag_id', Integer, ForeignKey('tag.id', ondelete='CASCADE'))
# )

# gyms_contacts_table = Table(
#     'contact_gyms', db.metadata,
#     Column('gym_id' , Integer , ForeignKey('Gym.id' , ondelete='CASCADE')),
#     Column('contact_id' , Integer , ForeignKey('Contact.id' , ondelete='CASCADE')),
    
# )

class Gym(db.Model):
    
    __tablename__ = "Gym"
    
    id = Column(Integer , primary_key=True , autoincrement=True)
    Name = Column(String(50) , nullable=False , unique=True)
    Gender = Column(Integer , nullable=False )
    Description = Column(Text , nullable=True)
    Point = Column(Float , default=0.0)
    Location = Column(String(200) , nullable= False)
    city_id = Column(Integer, ForeignKey('City.id', ondelete='SET NULL', onupdate='CASCADE'))
    Logo = Column(String(100) , nullable=True)
    
    
    #ارتباط های یک به چند
    city = relationship('City', backref='gym')
    photos = relationship('Gyms_Photo' , backref='gym' , lazy='dynamic')
    itempoints = relationship('Gyms_point_item' , backref='gym')
    rating_givens = relationship('Gyms_List_point', backref='gym')
    categories = relationship(
        'Category',
        secondary='Gyms_Category',
        primaryjoin='Gym.id==Gyms_Category.Gyms_id',
        secondaryjoin='Category.id==Gyms_Category.Category_id',
        backref='gyms'
    )
    tags = relationship('Gyms_Tag' , backref='gym' , lazy='dynamic')
    contacts = relationship('Contact_Gym' , backref='gym' , lazy='dynamic')
    options = relationship("Gyms_Options" , backref='gym' , cascade='all , delete-orphan')
    
    
    #ارتباط های چند به چند
    # tags = relationship('Gyms_Tag', secondary=gyms_tags_table , back_populates='gyms')
    # contacts = relationship('Contact_GYm' , secondary=gyms_contacts_table , back_populates='gyms')
    
    #fumctions
    def __init__(self, Name, Gender, Location, city_id, Description=None, Logo=None):
        self.Name = Name
        self.Gender = Gender
        self.Location = Location
        self.city_id = city_id
        self.Description = Description
        self.Logo = Logo
        
    def to_dict(self):
        return {
        'name': self.Name,
        'description': self.Description,
        'point': self.Point,
        'location': self.Location,
        'city': self.city.name_en,
        'logo': self.Logo,
        'categories': [category.Title for category in self.categories]
    }
    
    def Check_Exist_Gym(id):
        #select * from "Gym" where id = id;
        exist_gym = Gym.query.filter(Gym.id == id).first()
        if exist_gym == None:
            return False
        else:
            return True
    
    def select_gym_by_city(city_id):
        try:
            #select * from "Gym" where city_id = city_id;
            gyms_list = Gym.query.filter(Gym.city_id == city_id).all()
        
            if gyms_list == None:
                return jsonify({"error" : "we dont have gym"}) , 400
    
            _gyms_ = [gym.to_dict() for gym in gyms_list ]
            return jsonify(_gyms_) , 200
    
        except:
            return jsonify({"error" : "please enter a correct number"}) , 400
        
        
    def add_gym_to_db(name , gendr , location , city_id , description=None , logo = None):
        try:
            #insert from "Gym" ("Name" , "Gender" , "Description" , "Point" , "Location" , "city_id" , "Logo" ) values(name , gendr , location , city_id , description , logo);
            new_gym = Gym(name , gendr , location , city_id , description , logo)
            db.session.add(new_gym)
            db.session.commit()
            
            return jsonify({"message" : F"add {new_gym.Name} is succefull"}) , 200
        except SQLAlchemyError as er:
            db.session.rollback()
            return jsonify({'message': f'Error : {er}',}), 400
        
    def delete_gym(gym_id):
        #select * from "Gym" where 'id' = gym_id;
        gym = Gym.query.filter(Gym.id == gym_id).first()
        if gym == None:
            return jsonify({"error" : "this gym is not exist"}) , 400
        #Delete from "Gym" where 'id' = gym_id;
        db.session.delete(gym)
        db.session.commit()
        
        return jsonify({"message" : f"delete {gym.Name} is succed"}) , 200
        
        
    
class Gyms_Tag(db.Model):
    __tablename__ = 'Gyms_Tag'
    id = Column(Integer , primary_key=True , autoincrement=True)
    Title = Column(String(50), nullable=False)
    Gyms_id = Column(Integer , ForeignKey('Gym.id' , ondelete='SET NULL', onupdate='CASCADE'))
    
    # gyms = relationship("Gym", secondary=gyms_tags_table, back_populates="tags");
    
    #fumctions
    def to_dict(self):
        return {
            "Title" : self.Title,
            "gym_id" : self.Gyms_id
        }
    
    def add_tag_to_gym(title , gym_id):
        result = Gym.Check_Exist_Gym(gym_id)
        if result :
            #insert from "Gyms_Tag" ("Title" , "Gyms_id" ) values('title' , gym_id );
            new_tag = Gyms_Tag(Title = title , Gyms_id = gym_id)
            db.session.add(new_tag)
            db.session.commit()
            return jsonify({"message" : "tag is accept"}) , 200
        else:
            return jsonify({"error" : "gym is not exist"}) , 400
        
    def delete_tag(id):
        #select * from "Gyms_Tag" where 'id' = id;
        tag = Gyms_Tag.query.filter(Gyms_Tag.id == id).first()
        
        if tag == None :
            return jsonify({"error" : "tag is not exsist"}) , 400
        #Delete from "Gyms_Tag" where 'id' = id;
        db.session.delete(tag)
        db.session.commit()
        
        return jsonify({"message" : f"delete {tag.Title} is succed"}) , 200
        
    def select_by_gym_id(gym_id):
        #select * from "Gyms_Tag" where 'Gyms_id' = gym_id;
        tags = Gyms_Tag.query.filter(Gyms_Tag.Gyms_id == gym_id)
        
        if tags == None:
            return jsonify({"message" : "don`t have tag"}) , 400
        
        tags_list = [Gyms_Tag.to_dict(tag) for tag in tags]
        
        return jsonify(tags_list) , 200
    
    def select_by_gym_title(title):
        #select * from "Gyms_Tag" where 'Title' = title;
        tags = Gyms_Tag.query.filter(Gyms_Tag.Title == title).all()
        
        if tags == None:
            return jsonify({"message" : "don`t have tag"}) , 400
        
        tags_list = [Gyms_Tag.to_dict(tag) for tag in tags]
        
        return jsonify(tags_list) , 200
    
  
   
class Contact_Gym(db.Model):
    __tablename__ = 'Contact_Gym'
    id = Column(Integer , primary_key=True , autoincrement=True)
    Gyms_id = Column(Integer , ForeignKey('Gym.id' , ondelete='SET NULL' , onupdate='CASCADE'))
    PhoneNumber = Column(String(20),nullable=True)
    
    # gyms = relationship("Gym", secondary=gyms_contacts_table, back_populates="contacts")
    #fumctions
    def to_dict(self):
        return {
            "PhoneNumber" : self.PhoneNumber,
            "gym_id" : self.Gyms_id
        }
    
    def add_contact_to_gym(phonenumber , gym_id):
        result = Gym.Check_Exist_Gym(gym_id)
        if result :
            new_contact = Contact_Gym(PhoneNumber = phonenumber , Gyms_id = gym_id)
            db.session.add(new_contact)
            db.session.commit()
            return jsonify({"message" : "contact is accepted"}) , 200
        else:
            return jsonify({"error" : "gym is not exist"}) , 400
        
    def delete_contact(id):
        contact = Contact_Gym.query.filter(Contact_Gym.id == id).first()
        
        if contact == None :
            return jsonify({"error" : "contact is not exsist"}) , 400
        
        db.session.delete(contact)
        db.session.commit()
        
        return jsonify({"message" : f"delete {contact.PhoneNumber} is succed"}) , 200
        
    def select_by_gym_id(gym_id):
        contacts = Contact_Gym.query.filter(Contact_Gym.Gyms_id == gym_id).all()
        
        if contacts == None:
            return jsonify({"message" : "don`t have contact"}) , 400
        
        contacts_list = [Contact_Gym.to_dict(contact) for contact in contacts]
        
        return jsonify(contacts_list) , 200
    


class Gyms_Photo(db.Model):
    __tablename__ = 'Gyms_Photo'
    id = Column(Integer , primary_key= True , autoincrement=True)
    Gyms_id = Column(Integer , ForeignKey('Gym.id' , ondelete='SET NULL' , onupdate='CASCADE'), nullable=False)
    Photo_Url = Column(String(200))
    
    #fumctions
    def to_dict(self):
        return {
            "Photo_Url" : self.Photo_Url
        }
    
    def add_photo_to_gym(photo_url , gym_id):
        result = Gym.Check_Exist_Gym(gym_id)
        if result :
            new_photo = Gyms_Photo(Photo_Url = photo_url , Gyms_id = gym_id)
            db.session.add(new_photo)
            db.session.commit()
            return jsonify({"message" : "photo is accepted"}) , 200
        else:
            return jsonify({"error" : "gym is not exist"}) , 400
        
    def delete_photo(id):
        photo = Gyms_Photo.query.filter(Gyms_Photo.id == id).first()
        
        if photo == None :
            return jsonify({"error" : "photo is not exsist"}) , 400
        
        db.session.delete(photo)
        db.session.commit()
        
        return jsonify({"message" : f"delete {photo.id} is succed"}) , 200
        
    def select_by_gym_id(gym_id):
        photos = Gyms_Photo.query.filter(Gyms_Photo.Gyms_id == gym_id).all()
        
        if photos == None:
            return jsonify({"message" : "don`t have contact"}) , 400
        
        photos_list = [Gyms_Photo.to_dict(photo) for photo in photos]
        
        return jsonify(photos_list) , 200

    
    
class item_point_gyms(db.Model):
    __tablename__ = 'item_point_gyms'
    id = Column(Integer , primary_key=True , autoincrement=True)
    title = Column(String(50) , nullable=False)
    description = Column(String(250) , nullable=True)
    
    item_Points = relationship('Gyms_point_item' , backref='items')
    
    #fumctions
    def add_item(title , description = None):
        new_item = item_point_gyms(title = title , description = description)
        
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify({"message" : "add item is succed"}) , 200
    
    def delete_item(id):
        exist_item = item_point_gyms.query.filter(item_point_gyms.id == id).first()
        
        
        if exist_item == None:
            return jsonify({"error" : "this item is not exist"}) , 400
        
        db.session.delete(exist_item)
        db.session.commit()
        
        return jsonify({"message" : f"delete {exist_item.title} is succed"})
    
    def select_item(id):
        item = item_point_gyms.query.filter(item_point_gyms.id == id).first()
        if item == None:
            return None
        
        return item
    
    
        
class Gyms_point_item(db.Model):
    __tablename__ = 'Gyms_point_item'
    id = Column(Integer , primary_key=True , autoincrement=True)
    item_point_id = Column(Integer , ForeignKey('item_point_gyms.id', ondelete='SET NULL', onupdate='CASCADE') , nullable=False)    
    gyms_id = Column(Integer , ForeignKey('Gym.id' , ondelete='SET NULL' , onupdate='CASCADE') , nullable=False)
    point = Column(Float , nullable=False)

    _gym = relationship('Gym' , backref='item_Points' )
    _item = relationship('item_point_gyms' , backref="_item" )
    
    #fumctions
    def Add_or_Update(item_point_id , gyms_id):
        item  = Gyms_point_item.query.filter(Gyms_point_item.item_point_id == item_point_id , Gyms_point_item.gyms_id == gyms_id).first()
        points = Gyms_List_point.return_points( gyms_id , item_point_id)
        
        if points == None:
            point = 0.0
        else:
            point = float(sum(points)) / float(len(points))
        
        new_item = None
        if item == None:
            new_item = Gyms_point_item(item_point_id = item_point_id , gyms_id = gyms_id , point = point)
            
            db.session.add(new_item)
            db.session.commit()
            return True
        
        #Update "Gyms_point_item" Set "Point" = (Select Avg("point") from "Gyms_List_point" where "gyms_point_item_id" = item_point_id And "gyms_id" = gyms_id) 
        # where "item_point_id" = item_point_id And "gyms_id" = gyms_id;
        item.point = point
        db.session.refresh(item)
        db.session.commit()
        
        return True
    
    def selecet_by_gym(id):
        list_item = Gyms_point_item.query.filter(Gyms_point_item.gyms_id == id).all()
        gym_list_item_point = []
        
        for item in list_item:
            gym_list_item_point.append({
                "item" : item._item.title,
                "Point" : item.point
            })
        
        return jsonify(gym_list_item_point) , 200
           
    
       
class Gyms_List_point(db.Model):
    __tablename__ = 'Gyms_List_point'
    id = Column(Integer , primary_key=True , autoincrement=True)
    gyms_id = Column (Integer , ForeignKey('Gym.id' , ondelete='SET NULL' , onupdate='CASCADE'))
    gyms_point_item_id = Column(Integer , ForeignKey('Gyms_point_item.id' , ondelete='SET NULL' , onupdate='CASCADE'))
    user_id = Column(Integer , ForeignKey('User.id' , ondelete='SET NULL' , onupdate='CASCADE') , nullable=False)
    point = Column(Integer , nullable=True )
    
    
    _gym = relationship('Gym', backref='user_ratings')
    gym_point_item = relationship('Gyms_point_item', backref='user_ratings')
    _user = relationship('User', backref='ratings_given')
    
    #fumctions
    def return_points(gym_id , gym_point_item_id):
        lists = Gyms_List_point.query.filter(Gyms_List_point.gyms_point_item_id == gym_point_item_id , Gyms_List_point.gyms_id == gym_id).all()
        points = [item.point for item in lists]
           
        return points
    
    def selecet_by_user(id):
        list_item = Gyms_List_point.query.filter(Gyms_List_point.user_id == id).all()
        user_list_point = []
        
        for item in list_item:
            user_list_point.append({
                "Gym" : item._gym.Name,
                "Item" : item.gym_point_item.title,
                "Point" : item.point
            })
        
        return user_list_point
   
    def update_point(gyms_id ,gyms_point_item_id , user_id , point):
        item  = Gyms_List_point.query.filter(Gyms_List_point.gyms_id == gyms_id ,
                                             Gyms_List_point.gyms_point_item_id == gyms_point_item_id,
                                             Gyms_List_point.user_id == user_id).first()
        
        if item == None:
            new_item = Gyms_List_point(gyms_id = gyms_id , gyms_point_item_id = gyms_point_item_id, user_id = user_id, point = point)        
            db.session.add(new_item)
            db.session.commit()
            db.session.refresh(new_item)
            Gyms_point_item.Add_or_Update(gyms_point_item_id , gyms_id)
            return jsonify({"message" : "add item point is succed"}) , 200
        
        item.point = point
        db.session.refresh(new_item)
        db.session.commit()
        Gyms_point_item.Add_or_Update(gyms_point_item_id , gyms_id)
        
        return jsonify({"message" : "update successfully"}) , 200
   
class Gyms_Category(db.Model):
    __tablename__ = 'Gyms_Category'
    id = Column(Integer , primary_key=True , autoincrement=True)
    Gyms_id = Column(Integer , ForeignKey('Gym.id', ondelete='SET NULL', onupdate='CASCADE'))
    Category_id = Column(Integer , ForeignKey('Category.id', ondelete='SET NULL', onupdate='CASCADE'))

    
    _gym = relationship('Gym', backref='category')
    category = relationship('Category', backref='gym')
    
    #fumctions
    def add_category_to_gym(gym_id , category_id):
        try:
            new_item = Gyms_Category(Gyms_id = gym_id , Category_id = category_id)
            db.session.add(new_item)
            db.session.commit()
            return jsonify({"message" : "add category is succed"}) , 200
        except SQLAlchemyError as es:
            return jsonify({"error" : es}) , 400
    
    def select_gym_by_category(category_id):
        list_all = Gyms_Category.query.filter(Gyms_Category.Category_id == category_id)
        if list_all == None:
            return jsonify({"error" : "this category dosen`t have gym"})
        
        gym_list = [item._gym for item in list_all]
        
        respons = [gym.to_dict() for gym in gym_list]
        
        return jsonify(respons) , 200
    
    def delete_category_of_gym(id):
        category = Gyms_Category.query.filter(Gyms_Category.id == id).first()
        
        if category == None:
            return jsonify({"error" : "category is not exist"}) , 400
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({"message" : "category is deleted"}) , 200
        
    
    
class Gyms_Options(db.Model):
    __tablename__ = "Gyms_Options"
    id = Column(Integer , primary_key=True , autoincrement=True)
    Gyms_id = Column(Integer , ForeignKey("Gym.id" , ondelete="SET NULL" , onupdate="CASCADE"))
    Tilte = Column(String(50) , nullable=False)
    Price = Column(DECIMAL(10,2) , nullable= False)
    Category_id = Column(Integer , ForeignKey("Category.id" , ondelete="SET NULL" , onupdate="CASCADE"))
    Gender = Column(Boolean , nullable=False)
    Age = Column(Integer , nullable=True)
    DateTimeClass = Column(String(100) , nullable=False)
    DateStart = Column(String(100) , nullable=True)
    NumberOfSession = Column(Integer , nullable=True)
    Coach = Column(String(50) , nullable= False)
    Class_Capacity = Column(Integer , nullable= True)
    
    _gym = relationship('Gym', backref='_options')
    category = relationship('Category', backref='_options')
    reservations = relationship(
        "Gyms_Reservation",
        backref="option",
        primaryjoin="Gyms_Options.id == Gyms_Reservation.Gyms_Option_id",
        cascade="all, delete-orphan"
    )
    
    
    def add_option( gym_id, title, price, category_id, gender, coach, datetime_class,
                   age=None, date_start=None, num_sessions=None, capacity=None):
        try:
            option = Gyms_Options(
                Gyms_id=gym_id,
                Tilte=title,
                Price=price,
                Category_id=category_id,
                Gender=gender,
                Age=age,
                DateTimeClass=datetime_class,
                DateStart=date_start,
                NumberOfSession=num_sessions,
                Coach=coach,
                Class_Capacity=capacity
            )
            db.session.add(option)
            db.session.commit()
            return jsonify({"message" : f"add {title} is succed"}) , 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error" : str(e)}) , 400
        
    def delete_option(id):
        option = Gyms_Options.query.filter(Gyms_Options.id == id).first()
        
        if option == None:
            return jsonify({"error" : "options is not exist"}) , 400
        
        db.session.delete(option)
        db.session.commit()
        
        return jsonify({"message" : f"delete {option.Title} is succed"})
    
    def select_options(gym_id = None , category_id = None):
        options = Gyms_Options()
        
        if gym_id is not None and category_id is not None:
            options = Gyms_Options.query.filter(Gyms_Options.Category_id == category_id , Gyms_Options.Gyms_id == gym_id).all()
            
        elif  category_id is not None:
            options = Gyms_Options.query.filter(Gyms_Options.Category_id == category_id).all()
        
        elif gym_id is not None:
            options = Gyms_Options.query.filter(Gyms_Options.Gyms_id == gym_id).all()
            
        if options == None:
            return jsonify({"error" : "options are not exists"}) , 400
        
        options_list = []
        for option in options:
            options_list.append({
                "gym" : option._gym.Name,
                "title": option.Tilte,
                "price": str(option.Price),
                "category": option.category.Title,
                "gender": option.Gender,
                "coach": option.Coach,
                "age": option.Age,
                "datetime_class": option.DateTimeClass,
                "date_start": option.DateStart,
                "num_sessions": option.NumberOfSession,
                "capacity": option.Class_Capacity,
                "reserves": [reserve.to_dict() for reserve in option.reservations]
            })

        return jsonify(options_list), 200
    
    def update_option(id, gym_id, title, price, category_id, gender, coach, datetime_class,
                   age=None, date_start=None, num_sessions=None, capacity=None):
        option = Gyms_Options.query.filter(Gyms_Options.id == id).first()
        
        if option is not None:
            option.Gyms_id=gym_id
            option.Tilte=title
            option.Price=price
            option.Category_id=category_id
            option.Gender=gender
            option.Age=age
            option.DateTimeClass=datetime_class
            option.DateStart=date_start
            option.NumberOfSession=num_sessions
            option.Coach=coach
            option.Class_Capacity=capacity
            
            db.session.commit()
            return jsonify({"message" : f"update {title} is succed"}) , 200
        
        return jsonify({"error" : "option not found"}) , 400
    
    
class Gyms_Reservation(db.Model):
    __tablename__ = "Gyms_Reservation"
    id = Column(Integer , primary_key=True,autoincrement=True)
    Gyms_Option_id = Column(Integer , ForeignKey("Gyms_Options.id" , ondelete="SET NULL" , onupdate="CASCADE"))
    User_id = Column(Integer , ForeignKey("User.id" , ondelete="SET NULL" , onupdate="CASCADE"))
    Date_Reserve = Column(TIMESTAMP , nullable= False , unique=True)
    Status = Column(Boolean , nullable=False)
    
    
    gym_option_reserve = relationship("Gyms_Options" , backref="gym_reserve")
    user_reserve = relationship("User" , backref="user_reserve")
    
    def to_dict(self):
        return{
            "Gyms_Option_id"  : self.Gyms_Option_id ,
            "User_id"  : self.User_id ,
            "Date_Reserve"  : str(self.Date_Reserve) ,
            "Status"  : str(self.Status)
        }
    
    
    def Add_Reservation(gyms_option_id , user_id , date_reserve , status):
        try:
            new_reservation = Gyms_Reservation(
                Gyms_Option_id = gyms_option_id,
                User_id = user_id , 
                Date_Reserve = datetime.strptime(date_reserve ,"%Y-%m-%d %H:%M:%S") ,
                Status = status
            )
            
            db.session.add(new_reservation)
            db.session.commit()
            
            return jsonify({"message" : "add reservation is succed"}) , 200
        
        except SQLAlchemyError as es:
            db.session.rollback()
            return jsonify({"error" : str(es)}) , 400
        
    def Delete_Reservation(id):
        reserve = Gyms_Reservation.query.filter(Gyms_Reservation.id == id).first()
        
        if reserve == None:
            return jsonify({"error" : "reserve does not exist"}) , 400
        
        db.session.delete(reserve)
        db.session.commit()
        
        return jsonify({"message" : f"delete {reserve.gym_option_reserve.Title} is succed"}),200
    
    def select_reservations(gym_option_id = None , user_id = None):
        reserves = Gyms_Reservation()
        
        if gym_option_id is not None and user_id is not None:
            reserves = Gyms_Reservation.query.filter(Gyms_Reservation.User_id == user_id , Gyms_Reservation.Gyms_Option_id == gym_option_id).all()
            
        elif  user_id is not None:
            reserves = Gyms_Reservation.query.filter(Gyms_Reservation.User_id == user_id).all()
        
        elif gym_option_id is not None:
            reserves = Gyms_Reservation.query.filter(Gyms_Reservation.Gyms_Option_id == gym_option_id).all()
            
        if reserves == None:
            return jsonify({"error" : "options are not exists"}) , 400
        
        reserves_list = []
        for reserve in reserves:
            reserves_list.append({
                "option" : reserve.gym_option_reserve.Tilte,
                "user": reserve.user_reserve.f_name,
                "Date_Reserve": str(reserve.Date_Reserve),
                "status": str(reserve.Status)
            })

        return jsonify(reserves_list), 200
    
    def Update_Reservation(id,gyms_option_id , user_id , date_reserve , status):
        reserve = Gyms_Reservation.query.filter(Gyms_Reservation.id == id).first()
        
        if reserve is not None:
            reserve.Gyms_Option_id = gyms_option_id,
            reserve.User_id = user_id , 
            reserve.Date_Reserve = datetime.strptime(date_reserve ,"%Y-%m-%d %H:%M:%S") ,
            reserve.Status = status

            db.session.commit()
            return jsonify({"message" : "add reservation is succed"}) , 200
        
        return jsonify({"error" : "reserve was not found"}) , 400
        
    
    
    
    
            
    
        
        
        

    
    
    

    
    

    