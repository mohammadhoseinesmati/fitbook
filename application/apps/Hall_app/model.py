from application import db
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, Numeric, ForeignKey , Text , Table , Float , DECIMAL ,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask import jsonify
from datetime import datetime 
from application.utils import Password_Hash
from sqlalchemy.exc import SQLAlchemyError


class Halls(db.Model) :
    
    __tablename__ = "Halls"
    
    id = Column(Integer , primary_key=True , autoincrement= True)
    Name = Column(String(50) , nullable= False)
    Gender = Column(Integer , nullable=False)
    Description = Column(Text , nullable=True)
    Point = Column(Float , nullable= True)
    Location = Column(String(200) , nullable=False)
    City_id = Column(Integer , ForeignKey("City.id" , ondelete="SET NULL" , onupdate="CASCADE"))
    # Admin_id = Column(Integer , ForeignKey("Admin"))
    Logo = Column(String(200) , nullable=True)
    
    city = relationship('City', backref='hall')
    photos = relationship('Halls_Photo' , backref='hall')
    itempoints = relationship('Halls_Point_Item' , backref='hall')
    rating_givens = relationship('Halls_List_Point', backref='hall')
    categories = relationship(
        'Category',
        secondary='Halls_Category',
        primaryjoin='Halls.id==Halls_Category.Halls_id',
        secondaryjoin='Category.id==Halls_Category.Category_id',
        backref='halls'
    )
    tags = relationship('Halls_Tag' , backref='hall')
    contacts = relationship('Contact_Hall' , backref='hall')
    
    
    def __init__(self, Name, Gender, Location, city_id, Description=None, Logo=None):
        self.Name = Name
        self.Gender = Gender
        self.Location = Location
        self.City_id = city_id
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
    
    def Check_Exist_Hall(id):
        exist_hall = Halls.query.filter(Halls.id == id).first()
        if exist_hall == None:
            return False
        else:
            return True
    
    def Select_Hall_By_City(city_id):
        try:
            halls_list = Halls.query.filter(Halls.city_id == city_id).all()
        
            if halls_list == None:
                return jsonify({"error" : "we dont have hall"}) , 400
    
            _halls_ = [hall.to_dict() for hall in halls_list ]
            return jsonify(_halls_) , 200
    
        except:
            return jsonify({"error" : "please enter a correct number"}) , 400
        
        
    def Add_Hall_To_Db(name , gendr , location , city_id , description=None , logo = None):
        try:
            new_hall = Halls(name , gendr , location , city_id , description , logo)
            db.session.add(new_hall)
            db.session.commit()
            
            return jsonify({"message" : F"add {new_hall.Name} is succefull"}) , 200
        except SQLAlchemyError as er:
            db.session.rollback()
            return jsonify({'message': f'Error : {er}',}), 400
        
    def Delete_Hall(Hall_id):
        hall = Halls.query.filter(Halls.id == Hall_id).first()
        if hall == None:
            return jsonify({"error" : "this Hall is not exist"}) , 400
        db.session.delete(hall)
        db.session.commit()
        
        return jsonify({"message" : f"delete {hall.Name} is succed"}) , 200
        
        
    
class Halls_Tag(db.Model):
    __tablename__ = 'Halls_Tag'
    id = Column(Integer , primary_key=True , autoincrement=True)
    Title = Column(String(50), nullable=False)
    Halls_id = Column(Integer , ForeignKey('Halls.id' , ondelete='SET NULL', onupdate='CASCADE'))
    
    # gyms = relationship("Gym", secondary=gyms_tags_table, back_populates="tags")
    
    #fumctions
    def to_dict(self):
        return {
            "Title" : self.Title,
            "hall_id" : self.Halls_id
        }
    
    def Add_Tag_To_Hall(title , hall_id):
        result = Halls.Check_Exist_Hall(hall_id)
        if result :
            new_tag = Halls_Tag(Title = title , Halls_id = hall_id)
            db.session.add(new_tag)
            db.session.commit()
            return jsonify({"message" : "tag is accept"}) , 200
        else:
            return jsonify({"error" : "gym is not exist"}) , 400
        
    def Delete_Tag(id):
        tag = Halls_Tag.query.filter(Halls_Tag.id == id).first()
        
        if tag == None :
            return jsonify({"error" : "tag is not exsist"}) , 400
        
        db.session.delete(tag)
        db.session.commit()
        
        return jsonify({"message" : f"delete {tag.Title} is succed"}) , 200
        
    def Select_By_Hall_id(hall_id):
        tags = Halls_Tag.query.filter(Halls_Tag.Halls_id == hall_id)
        
        if tags == None:
            return jsonify({"message" : "don`t have tag"}) , 400
        
        tags_list = [Halls_Tag.to_dict(tag) for tag in tags]
        
        return jsonify(tags_list) , 200
    
    def Select_By_Title(title):
        tags = Halls_Tag.query.filter(Halls_Tag.Title == title).all()
        
        if tags == None:
            return jsonify({"message" : "don`t have tag"}) , 400
        
        tags_list = [Halls_Tag.to_dict(tag) for tag in tags]
        
        return jsonify(tags_list) , 200
    
  
   
class Contact_Hall(db.Model):
    __tablename__ = 'Contact_Hall'
    id = Column(Integer , primary_key=True , autoincrement=True)
    Halls_id = Column(Integer , ForeignKey('Halls.id' , ondelete='SET NULL' , onupdate='CASCADE'))
    PhoneNumber = Column(String(20),nullable=True)
    
    # gyms = relationship("Gym", secondary=gyms_contacts_table, back_populates="contacts")
    #fumctions
    def to_dict(self):
        return {
            "PhoneNumber" : self.PhoneNumber,
            "hall_id" : self.Halls_id
        }
    
    def Add_Contact_To_Hall(phonenumber , hall_id):
        result = Halls.Check_Exist_Hall(hall_id)
        if result :
            new_contact = Contact_Hall(PhoneNumber = phonenumber , Halls_id = hall_id)
            db.session.add(new_contact)
            db.session.commit()
            return jsonify({"message" : "contact is accepted"}) , 200
        else:
            return jsonify({"error" : "hall is not exist"}) , 400
        
    def Delete_Contact(id):
        contact = Contact_Hall.query.filter(Contact_Hall.id == id).first()
        
        if contact == None :
            return jsonify({"error" : "contact is not exsist"}) , 400
        
        db.session.delete(contact)
        db.session.commit()
        
        return jsonify({"message" : f"delete {contact.PhoneNumber} is succed"}) , 200
        
    def Select_By_Hall_id(hall_id):
        contacts = Contact_Hall.query.filter(Contact_Hall.Halls_id == hall_id).all()
        
        if contacts == None:
            return jsonify({"message" : "don`t have contact"}) , 400
        
        contacts_list = [Contact_Hall.to_dict(contact) for contact in contacts]
        
        return jsonify(contacts_list) , 200
    


class Halls_Photo(db.Model):
    __tablename__ = 'Halls_Photo'
    id = Column(Integer , primary_key= True , autoincrement=True)
    Halls_id = Column(Integer , ForeignKey('Halls.id' , ondelete='SET NULL' , onupdate='CASCADE'), nullable=False)
    Photo_Url = Column(String(200))
    
    #fumctions
    def to_dict(self):
        return {
            "Photo_Url" : self.Photo_Url
        }
    
    def Add_Photo_To_Hall(photo_url , hall_id):
        result = Halls.Check_Exist_Hall(hall_id)
        if result :
            new_photo = Halls_Photo(Photo_Url = photo_url , Halls_id = hall_id)
            db.session.add(new_photo)
            db.session.commit()
            return jsonify({"message" : "photo is accepted"}) , 200
        else:
            return jsonify({"error" : "hall is not exist"}) , 400
        
    def Delete_Photo(id):
        photo = Halls_Photo.query.filter(Halls_Photo.id == id).first()
        
        if photo == None :
            return jsonify({"error" : "photo is not exsist"}) , 400
        
        db.session.delete(photo)
        db.session.commit()
        
        return jsonify({"message" : f"delete photo is succed"}) , 200
        
    def Select_By_Hall_id(hall_id):
        photos = Halls_Photo.query.filter(Halls_Photo.Halls_id == hall_id).all()
        
        if photos == None:
            return jsonify({"message" : "don`t have contact"}) , 400
        
        photos_list = [Halls_Photo.to_dict(photo) for photo in photos]
        
        return jsonify(photos_list) , 200

    
    
class Item_Point_Halls(db.Model):
    __tablename__ = 'Item_Point_Halls'
    id = Column(Integer , primary_key=True , autoincrement=True)
    Title = Column(String(50) , nullable=False)
    Description = Column(String(250) , nullable=True)
    
    item_Points = relationship('Halls_Point_Item' , backref='items')
    
    #fumctions
    def add_item(title , description = None):
        new_item = Item_Point_Halls(Title = title , Description = description)
        
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify({"message" : "add item is succed"}) , 200
    
    def Delete_Item(id):
        exist_item = Item_Point_Halls.query.filter(Item_Point_Halls.id == id).first()
        
        
        if exist_item == None:
            return jsonify({"error" : "this item is not exist"}) , 400
        
        db.session.delete(exist_item)
        db.session.commit()
        
        return jsonify({"message" : f"delete {exist_item.Title} is succed"})
    
    def Select_Item(id):
        item = Item_Point_Halls.query.filter(Item_Point_Halls.id == id).first()
        if item == None:
            return None
        
        return item
    
    
        
class Halls_Point_Item(db.Model):
    __tablename__ = 'Halls_Point_Item'
    id = Column(Integer , primary_key=True , autoincrement=True)
    Item_Point_id = Column(Integer , ForeignKey('Item_Point_Halls.id', ondelete='SET NULL', onupdate='CASCADE') , nullable=False)    
    Halls_id = Column(Integer , ForeignKey('Halls.id' , ondelete='SET NULL' , onupdate='CASCADE') , nullable=False)
    point = Column(Float , nullable=False)

    _hall = relationship('Halls' , backref='item_Points' )
    _item = relationship('Item_Point_Halls' )
    
    #fumctions
    def Add_or_Update(item_point_id , halls_id):
        item  = Halls_Point_Item.query.filter(Halls_Point_Item.Item_Point_id == item_point_id , Halls_Point_Item.Halls_id == halls_id).first()
            
        
        points = Halls_List_Point.return_points(halls_id , item_point_id )
        if points == None:
            point = 0.0
        else: 
            point = float(sum(points)) / float(len(points))
            return jsonify({"error" : "we dont have point"})
            
        if item == None:
            new_item = Halls_Point_Item(Item_Point_id = item_point_id , Halls_id = halls_id , point = point)
            
            db.session.add(new_item)
            db.session.commit()
            return True
        
        
        item.point = point
        db.session.refresh(item)
        db.session.commit()

        
        return jsonify({"message" : "update succesfully"}) , 200
    
    def selecet_by_hall(id):
        list_item = Halls_Point_Item.query.filter(Halls_Point_Item.Halls_id == id).all()
        gym_list_item_point = []
        
        for item in list_item:
            gym_list_item_point.append({
                "item" : item.Item_Point_id,
                "Point" : item.point
            })
        
        return gym_list_item_point
    
    
       
class Halls_List_Point(db.Model):
    __tablename__ = 'Halls_List_Point'
    id = Column(Integer , primary_key=True , autoincrement=True)
    Halls_id = Column (Integer , ForeignKey('Halls.id' , ondelete='SET NULL' , onupdate='CASCADE'))
    Halls_Point_Item_id = Column(Integer , ForeignKey('Halls_Point_Item.id' , ondelete='SET NULL' , onupdate='CASCADE'))
    User_id = Column(Integer , ForeignKey('User.id' , ondelete='SET NULL' , onupdate='CASCADE') , nullable=False)
    Point = Column(Integer , nullable=False )
    
    
    _hall = relationship('Halls', backref='user_ratings')
    hall_point_item = relationship('Halls_Point_Item', backref='user_ratings')
    _user = relationship('User', backref='ratings_for_hall')
    
    #fumctions
    def return_points(hall_id , hall_point_item_id):
        lists = Halls_List_Point.query.filter(Halls_List_Point.Halls_Point_Item_id == hall_point_item_id , Halls_List_Point.Halls_id == hall_id).all()
        points = [item.Point for item in lists]
        print("points list: ", len(points))
        return points
    
    def selecet_by_user(id):
        list_item = Halls_List_Point.query.filter(Halls_List_Point.User_id == id).all()
        user_list_point = []
        
        for item in list_item:
            user_list_point.append({
                "Gym" : item._hall.Name,
                "Item" : item.Halls_Point_Item_id,
                "Point" : item.Point
            })
        
        return user_list_point
   
    def update_point(hall_id ,halls_point_item_id , user_id , point):
        item  = Halls_List_Point.query.filter(Halls_List_Point.Halls_id == hall_id ,
                                             Halls_List_Point.Halls_Point_Item_id == halls_point_item_id,
                                             Halls_List_Point.User_id == user_id).first()
        
        if item == None:
            new_item = Halls_List_Point(Halls_id = hall_id , Halls_Point_Item_id = halls_point_item_id, User_id = user_id, Point = point)        
            db.session.add(new_item)
            db.session.commit()
            db.session.refresh(new_item)
            Halls_Point_Item.Add_or_Update(halls_point_item_id , hall_id)
            return jsonify({"message" : "add item point is succed"}) , 200
        
        item.Point = point
        db.session.commit()
        
        return jsonify({"message" : "update succesfully"}) , 200
   
   
   
class Halls_Category(db.Model):
    
    __tablename__ = 'Halls_Category'
    id = Column(Integer , primary_key=True , autoincrement=True)
    Halls_id = Column(Integer , ForeignKey('Halls.id', ondelete='SET NULL', onupdate='CASCADE'))
    Category_id = Column(Integer , ForeignKey('Category.id', ondelete='SET NULL', onupdate='CASCADE'))

    
    _hall = relationship('Halls', backref='category')
    category = relationship('Category', backref='hall')
    
    #fumctions
    def Add_Category_To_Hall(hall_id , category_id):
        try:
            new_item = Halls_Category(Halls_id = hall_id , Category_id = category_id)
            db.session.add(new_item)
            db.session.commit()
            return jsonify({"message" : "add category is succed"}) , 200
        except SQLAlchemyError as es:
            return jsonify({"error" : es}) , 400
    
    def Select_Hall_By_Category(category_id):
        list_all = Halls_Category.query.filter(Halls_Category.Category_id == category_id)
        if list_all == None:
            return jsonify({"error" : "this category dosen`t have hall"})
        
        hall_list = [item._hall for item in list_all]
        
        respons = [hall.to_dict() for hall in hall_list]
        
        return jsonify(respons) , 200
    
    def Delete_Category_Of_Hall(id):
        category = Halls_Category.query.filter(Halls_Category.id == id).first()
        
        if category == None:
            return jsonify({"error" : "category is not exist"}) , 400
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({"message" : "category is deleted"}) , 200
    
    
class Halls_Option(db.Model):
    __tablename__ = "Halls_Option"
    id = Column(Integer , primary_key= True , autoincrement= True)
    Halls_id = Column(Integer , ForeignKey("Halls.id" , ondelete="SET NULL" , onupdate="CASCADE"))
    start_time = Column(DateTime , nullable= False)
    end_time = Column(DateTime , nullable=False)
    Price = Column(DECIMAL(10,2) , nullable=False)
    
    _halls = relationship("Halls" , backref="h_options")
    _reservations = relationship(
        "Halls_Reservation",
        backref="option",
        primaryjoin="Halls_Option.id == Halls_Reservation.Halls_Option_id",
        cascade="all, delete-orphan"
    )
    
    
    def add_option( halls_id, start_time, end_time, price):
        try:
            option = Halls_Option(
                Halls_id=halls_id,
                start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"),
                end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S"),
                Price=price
            )
            db.session.add(option)
            db.session.commit()
            return jsonify({"message" : "add option is succed"}) , 200
        except Exception as e:
            db.session.rollback()
            return jsonify(e) , 400
        
    def delete_option(id):
        option = Halls_Option.query.filter(Halls_Option.id == id).first()
        
        if option == None:
            return jsonify({"error" : "options is not exist"}) , 400
        
        db.session.delete(option)
        db.session.commit()
        
        return jsonify({"message" : f"delete {option.Title} is succed"})
    
    def select_options(halls_id):
        options = Halls_Option()
        
        if halls_id is not None:
            options = Halls_Option.query.filter(Halls_Option.Halls_id == halls_id).all()
            
        if options == None:
            return jsonify({"error" : "options are not exists"}) , 400
        
        options_list = []
        for option in options:
            options_list.append({
                "Halls_id" : option.Halls_id,
                "start_time": option.start_time,
                "price": str(option.Price),
                "end_time": option.end_time,
                "reserves": [reserve for reserve in option._reservations]
            })

        return jsonify(options_list), 200
    
    def update_option(id, halls_id, start_time, end_time, price):
        option = Halls_Option.query.filter(Halls_Option.id == id).first()
        
        if option is not None:
            option.Halls_id=halls_id
            option.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            option.end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            option.Price=price

            db.session.commit()
            return jsonify({"message" : f"update {halls_id} is succed"}) , 200
        
        return jsonify({"error" : "option not found"}) , 400
    
    
    
class Halls_Reservation(db.Model):
    __tablename__ = "Halls_Reservation"
    id = Column(Integer , primary_key= True , autoincrement=True)
    Date = Column(TIMESTAMP , nullable=False)
    Halls_Option_id = Column(Integer , ForeignKey("Halls_Option.id" , ondelete="SET NULL" , onupdate="CASCADE"))
    Count = Column(Integer , default=1 )
    User_id = Column(Integer , ForeignKey("User.id" , ondelete="SET NULL" , onupdate="CASCADE"))
    date_reservation = Column(TIMESTAMP , nullable=False)
    Status = Column(Boolean , default=False , nullable=False)
    
    hall_option_reserve = relationship("Halls_Option" , backref="halls_option_reserve")
    user_reserve_hall = relationship("User" , backref="user_reserve_hall")
    
    
    def Add_Reservation(date , halls_option_id , userid , date_reservation , status ,  count = None):
        try:
            new_reserve = Halls_Reservation(
                Date = datetime.strptime(date , "%Y-%m-%d %H:%M:%S"),
                Halls_Option_id = halls_option_id,
                Count = count , 
                User_id = userid ,
                date_reservation = datetime.strptime(date_reservation , "%Y-%m-%d %H:%M:%S"),
                Status = status               
            )
            
            db.session.add(new_reserve)
            db.session.commit()
            
            return jsonify({"message" : "reserve was successfully"}) , 200
        
        except SQLAlchemyError as es:
            db.session.rollback()
            return jsonify(es) , 400
        
    def Delete_Reservation(id):
        reserve = Halls_Reservation.query.filter(Halls_Reservation.id == id).first()
        
        if reserve == None:
            return jsonify({"error" : "reserve does not exist"}),400
        
        db.session.delete(reserve)
        db.session.commit()
        
        return jsonify({"message" : "delete was succesfully"}), 200
    
    def select_reservations(hall_option_id = None , user_id = None):
        reserves = Halls_Reservation()
        
        if hall_option_id is not None and user_id is not None:
            reserves = Halls_Reservation.query.filter(Halls_Reservation.User_id == user_id , Halls_Reservation.Halls_Option_id == hall_option_id).all()
            
        elif  user_id is not None:
            reserves = Halls_Reservation.query.filter(Halls_Reservation.User_id == user_id).all()
        
        elif hall_option_id is not None:
            reserves = Halls_Reservation.query.filter(Halls_Reservation.Halls_Option_id == hall_option_id).all()
            
        if reserves == None:
            return jsonify({"error" : "options are not exists"}) , 400
        
        reserves_list = []
        for reserve in reserves:
            reserves_list.append({
                "option" : reserve.Halls_Option_id,
                "user": reserve.user_reserve_hall.f_name,
                "price": str(reserve.date_reservation),
            })

        return jsonify(reserves_list), 200
    
    
    def Update_Reservation( id, date , halls_option_id , userid , date_reservation , status ,  count = None):
        reserve = Halls_Reservation.query.filter(Halls_Reservation.id == id).first()
        
        # if reserve == None:
        #     return jsonify({"error" : "reserve was not found"}) , 400
        
        reserve.Date = datetime.strptime(date , "%Y-%m-%d %H:%M:%S")
        reserve.Halls_Option_id = halls_option_id
        reserve.Count = count 
        reserve.User_id = userid 
        reserve.date_reservation = datetime.strptime(date_reservation , "%Y-%m-%d %H:%M:%S")
        reserve.Status = status 
        
        
        db.session.commit()
        db.session.refresh(reserve)
        return jsonify({"message" : "add reservation is succed"}) , 200
        
    
                
    
    
    
    
