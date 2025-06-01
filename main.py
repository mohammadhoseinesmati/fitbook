from application import app
from dotenv import load_dotenv


# import debugpy
# debugpy.listen(("0.0.0.0", 5678))  # پورت دیباگ
# print("🔍 Waiting for debugger attach...")
# debugpy.wait_for_client()  # تا وصل نشی، کد جلو نمیره


load_dotenv()
if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True, port=80)