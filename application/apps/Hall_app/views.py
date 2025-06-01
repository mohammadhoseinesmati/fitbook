from application import app,db,limiter,redis_client
from application.apps.Hall_app import halls
from application.apps.Hall_app.model import Halls , Halls_Category , Halls_List_Point , Halls_Option , Halls_Photo , Halls_Point_Item , Halls_Reservation , Halls_Tag , Contact_Hall , Item_Point_Halls
from flask import jsonify , request 
from decimal import Decimal
import datetime

#Hall
####################################################
@halls.route("/" , methods = ['POST'])
def add_hall():
    data = request.get_json()
    
    required_fields = ['Name', 'Gernder', 'Location', 'City']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f"Field '{field}' is required."}), 400
    
    name = data['Name']
    gender = str(data['Gender']).strip()
    location = data['Location']
    city_id = str(data['City']).strip()
    description = data['Description']
    logo = data['Logo']
    
    if not gender.isdigit() or not city_id.isdigit() :
        return jsonify({'error' : 'please write digit for Gender and City'})
    
    gender = int(gender)
    city_id = int(city_id)
    
    response = Halls.Add_Hall_To_Db(name , gender , location , city_id , description , logo)
    return response
    
    
@halls.route("/" , methods = ['GET'])
def Halls_list():
    halls_list = Halls.query.all()
    _halls_ =[]
    if halls_list is None:
        return jsonify({"error" : "we dont have hall"})
    
    _halls_ = [hall.to_dict() for hall in halls_list ]
        
    return jsonify(_halls_) , 200


@halls.route("/city" , methods = ['GET'])
def Halls_From_City():
    data = request.get_json()

    try:
        city_id = int(data['City'])
        Halls_list = Halls.query.filter(Halls.city_id == city_id).all()
        
        if Halls_list is None:
            return jsonify({"error" : "we dont have hall"})
    
        _halls_ = [hall.to_dict() for hall in Halls_list ]
        return jsonify(_halls_) , 200
    
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/delete" , methods=["GET"])
def Delete_halls():
    data = request.get_json()  
    try:
        id = int(data["hall_id"])
        response = Halls.Delete_Hall(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    

#Halls_Tag
#############################################################  
@halls.route("/add-tag" , methods = ["POST"])
def add_tag():
    data = request.get_json()
    try:
        hall_id = int(data["hall_id"])
        title = data["title"]
        
        response = Halls_Tag.Add_Tag_To_Hall(title , hall_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/delete-tag" , methods=["GET"])
def delete_tag():
    data = request.get_json()
    
    try:
        id = int(data["tag_id"])
        response = Halls_Tag.Delete_Tag(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/select-halltag" , methods = ["GET"])
def select_tag():
    data = request.get_json()
    
    try:
        hall_id = int(data["hall_id"])
        response = Halls_Tag.Select_By_Hall_id(hall_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/select-titletag" , methods = ["GET"])
def select_tag_title():
    data = request.get_json()
    
    try:
        title = int(data["title"])
        response = Halls_Tag.Select_By_Title(title)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    

#Halls_Contact
################################################################
@halls.route("/add-contact" , methods = ["POST"])
def add_contact():
    data = request.get_json()
    try:
        hall_id = int(data["hall_id"])
        phoneNumber = data["phoneNumber"]
        
        response = Contact_Hall.Add_Contact_To_Hall(phoneNumber , hall_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/delete-contact" , methods=["GET"])
def delete_contact():
    data = request.get_json()
    
    try:
        id = int(data["tag_id"])
        response = Contact_Hall.Delete_Contact(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/select-contact" , methods = ["GET"])
def select_contact():
    data = request.get_json()
    
    try:
        hall_id = int(data["hall_id"])
        response = Contact_Hall.Select_By_Hall_id(hall_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
    
#Halls_Photo
#############################################################       
@halls.route("/add-photo" , methods = ["POST"])
def add_photo():
    data = request.get_json()
    try:
        hall_id = int(data["hall_id"])
        photoUrl = data["photoUrl"]
        
        response = Halls_Photo.Add_Photo_To_Hall(photoUrl , hall_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/delete-photo" , methods=["GET"])
def delete_photo():
    data = request.get_json()
    
    try:
        id = int(data["photo_id"])
        response = Halls_Photo.Delete_Photo(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/select-photo" , methods = ["GET"])
def select_photo():
    data = request.get_json()
    
    try:
        hall_id = int(data["hall_id"])
        response = Halls_Photo.Select_By_Hall_id(hall_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
    
#Item_Point_Halls
#############################################################       
@halls.route("/add-item" , methods = ["POST"])
def add_item():
    data = request.get_json()
    try:
        title = data["title"]
        description = data["description"]
        
        response = Item_Point_Halls.add_item( title , description)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/delete-item" , methods=["GET"])
def delete_item():
    data = request.get_json()
    
    try:
        id = int(data["item_id"])
        response = Item_Point_Halls.Delete_Item(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/select-item" , methods = ["GET"])
def select_item():
    data = request.get_json()
    
    try:
        id = int(data["id"])
        response = Item_Point_Halls.Select_Item(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
    

#Halls_Point_Item
##################################################################
@halls.route("/select-item-point" , methods = ["POST"])
def select_item_point():
    data = request.get_json()
    
    try:
        halls_id = int(data["halls_id"])
        response = Halls_Point_Item.selecet_by_hall(halls_id)
        
        return jsonify(response) , 200
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/add-list" , methods = ["POST"])
def add_item_point():
    data = request.get_json()
    
    try:
        halls_id = int(data["halls_id"])
        item_point_id = int(data["item_point_id"])
        response = Halls_Point_Item.Add_or_Update(item_point_id,halls_id)
        
        return jsonify(response) , 200
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
    
    
#Halls_List_Point
##################################################################   
@halls.route("/update-point" , methods=["POST"])
def update_point():
    data = request.get_json()
    try:
        halls_id = int(data["halls_id"])
        point_item_id = int(data["point_item_id"])
        user_id = int(data["user_id"])
        point = int(data["point"])
        
        response = Halls_List_Point.update_point(halls_id , point_item_id , user_id , point)
        return response
    except Exception as e :
        return jsonify({"error" : str(e)}) , 400
    
    
    
#Halls_Category
##################################################################         
@halls.route("/addcategory" , methods=["POST"])
def add_category():
    data = request.get_json()
    try:
        hall_id = int(data["hall_id"])
        category_id = int(data["category_id"])   
        response = Halls_Category.Add_Category_To_Hall(hall_id , category_id)
    
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
    
        
@halls.route("/selectbycat" , methods = ["GET"])
def select_by_category():
    data = request.get_json()
    try:
        category_id = int(data['category'])
        response = Halls_Category.Select_Hall_By_Category(category_id) , 400
        
        return response
    
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/deletecat" , methods = ["GET"])
def delete_cat_from_gym():
    data = request.get_json()
    try:
        id = int(data['category'])
        response = Halls_Category.Delete_Category_Of_Hall(id)
        
        return response
    
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
    
    
#Gyms_Options
################################################################## 
@halls.route("/add-option" , methods=["POST"])
def add_gymoptions():
    data = request.get_json()
    
    try :
        hall_id = int(data["hall_id"])
        start_time = data["start_time"]
        end_time = data["end_time"]
        price = Decimal(data["price"])
        
        response = Halls_Option.add_option(hall_id , start_time , end_time , price)
        
        return response
    except Exception as es:
        return jsonify({"error" : str(es)}) , 400
    
@halls.route("/delete-options" , methods=["GET"])
def delete_gym_option():
    data = request.get_json()
    
    try:
        id = int(data["id"])
        response = Halls_Option.delete_option(id)
        
        return response
    
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/select-option" , methods=["GEt"])
def select_gym_options():
    data = request.get_json()
    
    try:
        hall_id = int(data["hall_id"])
        
        response = Halls_Option.select_options(hall_id)
        
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/update-option" , methods=["POST"])
def update_option():
    data = request.get_json()
    
    try :
        id = int(data["id"])
        hall_id = int(data["hall_id"])
        start_time = data["start_time"]
        end_time = data["end_time"]
        price = Decimal(data["price"])
        
        response = Halls_Option.update_option( id ,hall_id , start_time ,end_time ,  price )
        
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
    
    
#Gyms_Reservation
################################################################## 
@halls.route("/add-reservation" , methods=["POST"])
def add_reservation_hall():
    data = request.get_json()
    
    try:
        date = data["date"]
        halls_option_id = int(data["halls_option_id"])
        user_id = int(data["User_id"])
        date_Reserve =data["date_Reserve"]
        status = bool(data["status"])
        count = int(data["count"])
        
        response = Halls_Reservation.Add_Reservation( date, halls_option_id , user_id , date_Reserve , status , count)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/delete-reserve" , methods=["GET"])
def delete_reserve():
    data = request.get_json()
    
    try:
        id = int(data["id"])
        response = Halls_Reservation.Delete_Reservation(id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
    
@halls.route("/select-reservations" , methods=["POST"])
def select_reservations():
    data = request.get_json()
    
    try:
        hall_option_id = int(data["hall_option_id"])
        user_id = int(data["user_id"])
        
        response = Halls_Reservation.select_reservations(hall_option_id , user_id)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400
@halls.route("/update-reservation" , methods=["POST"])
def update_reservations():
    data = request.get_json()
    
    try:
        id = int(data["id"])
        date = data["date"]
        halls_option_id = int(data["halls_option_id"])
        user_id = int(data["User_id"])
        date_Reserve =data["date_Reserve"]
        status = bool(data["status"])
        count = int(data["count"])
        response = Halls_Reservation.Update_Reservation( id ,date , halls_option_id , user_id , date_Reserve , status , count)
        return response
    except Exception as e:
        return jsonify({"error" : str(e)}) , 400