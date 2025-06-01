from application import app,db,limiter,redis_client
from application.apps.Gym_app import gyms
from application.apps.Gym_app.model import Gym , Gyms_Category , Gyms_List_point , Gyms_Options , Gyms_Photo , Gyms_point_item , Gyms_Reservation , Gyms_Tag , Contact_Gym , item_point_gyms
from flask import jsonify , request 
from decimal import Decimal
import datetime


#Gym
####################################################
@gyms.route("/" , methods = ['POST'])
def add_gym():
    data = request.get_json()
    
    required_fields = ['Name', 'Gernder', 'Location', 'City']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Field '{field}' is required."}), 400
    
    name = data['Name']
    gender = str(data['Gernder']).strip()
    location = data['Location']
    city_id = str(data['City']).strip()
    description = data['Description']
    logo = data['Logo']
    
    if not gender.isdigit() or not city_id.isdigit() :
        return jsonify({'error' : 'please write digit for Gender and City'})
    
    gender = int(gender)
    city_id = int(city_id)
    
    response = Gym.add_gym_to_db(name , gender , location , city_id , description , logo)
    return response
    
    
@gyms.route("/" , methods = ['GET'])
def Gyms_list():
    gyms_list = Gym.query.all()
    _gyms_ =[]
    if gyms_list is None:
        return jsonify({"error" : "we dont have gym"})
    
    _gyms_ = [gym.to_dict() for gym in gyms_list ]
        
    return jsonify(_gyms_) , 200


@gyms.route("/city" , methods = ['GET'])
def Gyms_From_City():
    data = request.get_json()

    try:
        city_id = int(data['City'])
        gyms_list = Gym.query.filter(Gym.city_id == city_id).all()
        
        if gyms_list is None:
            return jsonify({"error" : "we dont have gym"})
    
        _gyms_ = [gym.to_dict() for gym in gyms_list ]
        return jsonify(_gyms_) , 200
    
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/delete" , methods=["GET"])
def Delete_gyms():
    data = request.get_json()  
    try:
        id = int(data["gym_id"])
        response = Gym.delete_gym(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
#Gyms_Tag
#############################################################  
@gyms.route("/add-tag" , methods = ["POST"])
def add_tag():
    data = request.get_json()
    try:
        gym_id = int(data["gym_id"])
        title = data["title"]
        
        response = Gyms_Tag.add_tag_to_gym(title , gym_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/delete-tag" , methods=["GET"])
def delete_tag():
    data = request.get_json()
    
    try:
        id = int(data["tag_id"])
        response = Gyms_Tag.delete_tag(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/select-gymtag" , methods = ["GET"])
def select_tag():
    data = request.get_json()
    
    try:
        gym_id = int(data["gym_id"])
        response = Gyms_Tag.select_by_gym_id(gym_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/select-titletag" , methods = ["GET"])
def select_tag_title():
    data = request.get_json()
    
    try:
        title = int(data["title"])
        response = Gyms_Tag.select_by_gym_title(title)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
        
#Gym_Contact
################################################################
@gyms.route("/add-contact" , methods = ["POST"])
def add_contact():
    data = request.get_json()
    try:
        gym_id = int(data["gym_id"])
        phoneNumber = data["phoneNumber"]
        
        response = Contact_Gym.add_contact_to_gym(phoneNumber , gym_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/delete-contact" , methods=["GET"])
def delete_contact():
    data = request.get_json()
    
    try:
        id = int(data["tag_id"])
        response = Contact_Gym.delete_contact(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/select-contact" , methods = ["GET"])
def select_contact():
    data = request.get_json()
    
    try:
        gym_id = int(data["gym_id"])
        response = Contact_Gym.select_by_gym_id(gym_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400

#Gyms_Photo
#############################################################       
@gyms.route("/add-photo" , methods = ["POST"])
def add_photo():
    data = request.get_json()
    try:
        gym_id = int(data["gym_id"])
        photoUrl = data["photoUrl"]
        
        response = Gyms_Photo.add_photo_to_gym(photoUrl , gym_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/delete-photo" , methods=["GET"])
def delete_photo():
    data = request.get_json()
    
    try:
        id = int(data["photo_id"])
        response = Gyms_Photo.delete_photo(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/select-photo" , methods = ["GET"])
def select_photo():
    data = request.get_json()
    
    try:
        gym_id = int(data["gym_id"])
        response = Gyms_Photo.select_by_gym_id(gym_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400

#item_point_gyms
#############################################################       
@gyms.route("/add-item" , methods = ["POST"])
def add_item():
    data = request.get_json()
    try:
        title = data["title"]
        description = data["description"]
        
        response = item_point_gyms.add_item(title , description)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/delete-item" , methods=["GET"])
def delete_item():
    data = request.get_json()
    
    try:
        id = int(data["item_id"])
        response = item_point_gyms.delete_item(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/select-item" , methods = ["GET"])
def select_item():
    data = request.get_json()
    
    try:
        id = int(data["id"])
        response = item_point_gyms.select_item(id)
        return jsonify({"message" : f"{response.title}"})
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
#Gyms_point_item
##################################################################
@gyms.route("/select-item-point" , methods = ["POST"])
def select_item_point():
    data = request.get_json()
    
    try:
        gyms_id = int(data["gyms_id"])
        response = Gyms_point_item.selecet_by_gym(gyms_id)
        
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/add-list" , methods = ["POST"])
def add_item_point():
    data = request.get_json()
    
    try:
        gyms_id = int(data["gyms_id"])
        item_point_id = int(data["item_point_id"])
        response = Gyms_point_item.Add_or_Update(item_point_id,gyms_id)
        
        return jsonify(response) , 200
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
        
#Gyms_List_point
##################################################################   
@gyms.route("/update-point" , methods=["POST"])
def update_point():
    data = request.get_json()
    try:
        gyms_id = int(data["gyms_id"])
        point_item_id = int(data["point_item_id"])
        user_id = int(data["user_id"])
        point = int(data["point"])
        
        response = Gyms_List_point.update_point(gyms_id , point_item_id , user_id , point)
        return response
    except Exception as e :
        return jsonify({"error" : str(e)}) , 400
        

#Gyms_Category
##################################################################         
@gyms.route("/addcategory" , methods=["POST"])
def add_category():
    data = request.get_json()
    try:
        gym_id = int(data["gym_id"])
        category_id = int(data["category_id"])   
        response = Gyms_Category.add_category_to_gym(gym_id , category_id)
    
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
    
        
@gyms.route("/selectbycat" , methods = ["GET"])
def select_by_category():
    data = request.get_json()
    try:
        category_id = int(data['category'])
        response = Gyms_Category.select_gym_by_category(category_id) , 400
        
        return response
    
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/deletecat" , methods = ["GET"])
def delete_cat_from_gym():
    data = request.get_json()
    try:
        id = int(data['category'])
        response = Gyms_Category.delete_category_of_gym(id)
        
        return response
    
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400

#Gyms_Options
################################################################## 
@gyms.route("/add-option" , methods=["POST"])
def add_gymoptions():
    data = request.get_json()
    
    try :
        gym_id = int(data["gym_id"])
        title = data["title"]
        price = Decimal(data["price"])
        category_id = int(data["category_id"])
        gender = bool(data["gender"])
        age = int(data["age"])
        datetime_class = data["datetime_class"]
        date_start = data["date_start"]
        num_sessions = data["num_sessions"]
        coach = data["coach"]
        capacity = int(data["capacity"])
        
        response = Gyms_Options.add_option(gym_id , title , price , category_id , gender , coach,
                                            datetime_class , age  , date_start ,
                                           num_sessions  , capacity)
        
        return response
    except Exception as es:
        return jsonify({"error" : str(es)}) , 400
    
@gyms.route("/delete-options" , methods=["GET"])
def delete_gym_option():
    data = request.get_json()
    
    try:
        id = int(data["id"])
        response = Gyms_Options.delete_option(id)
        
        return response
    
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/select-option" , methods=["GEt"])
def select_gym_options():
    data = request.get_json()
    
    try:
        gym_id = int(data["gym_id"])
        category_id = int(data["category_id"])
        
        response = Gyms_Options.select_options(gym_id , category_id)
        
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/update-option" , methods=["POST"])
def update_option():
    data = request.get_json()
    
    try :
        id = int(data["id"])
        gym_id = int(data["gym_id"])
        title = data["title"]
        price = Decimal(data["price"])
        category_id = int(data["category_id"])
        gender = bool(data["gender"])
        age = int(data["age"])
        datetime_class = data["datetime_class"]
        date_start = data["date_start"]
        num_sessions = data["num_sessions"]
        coach = data["coach"]
        capacity = int(data["capacity"])
        
        response = Gyms_Options.update_option( id ,gym_id , title , price , category_id , gender,
                                          coach, datetime_class, age  , date_start ,
                                           num_sessions ,  capacity)
        
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    

#Gyms_Reservation
################################################################## 
@gyms.route("/add-reservation" , methods=["POST"])
def add_reservation_gym():
    data = request.get_json()
    
    try:
        gyms_option_id = int(data["gyms_option_id"])
        user_id = int(data["User_id"])
        date_Reserve =data["Date_Reserve"]
        status = bool(data["status"])
        
        response = Gyms_Reservation.Add_Reservation(gyms_option_id , user_id , date_Reserve , status)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/delete-reserve" , methods=["GET"])
def delete_reserve():
    data = request.get_json()
    
    try:
        id = int(data["id"])
        response = Gyms_Reservation.Delete_Reservation(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@gyms.route("/select-reservations" , methods=["POST"])
def select_reservations():
    data = request.get_json()
    
    try:
        gym_option_id = int(data["gym_option_id"])
        user_id = int(data["user_id"])
        
        response = Gyms_Reservation.select_reservations(gym_option_id , user_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
@gyms.route("/update-reservation" , methods=["POST"])
def update_reservations():
    data = request.get_json()
    
    try:
        id = int(data["id"])
        gyms_option_id = int(data["gyms_option_id"])
        user_id = int(data["User_id"])
        date_Reserve = data["Date_Reserve"]
        status = bool(data["status"])
        response = Gyms_Reservation.Update_Reservation( id ,gyms_option_id , user_id , date_Reserve , status)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
        
        

        
    
