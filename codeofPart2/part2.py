from db import get_customer_info  # เรียกใช้ฟังก์ชันจาก db.py

if __name__ == "__main__":
    # รับค่า ID ของลูกค้าที่ต้องการค้นหา
    customer_id = input("กรุณาใส่ Customer ID: ")

    # เรียกใช้ฟังก์ชันเพื่อค้นหาข้อมูลลูกค้า
    info = get_customer_info(customer_id)

    # ตรวจสอบว่าพบลูกค้าหรือไม่
    if info:
        print("ข้อมูลลูกค้า:")
        print(f"Name: {info['name']}")   # แสดงชื่อ
        print(f"Email: {info['email']}") # แสดงอีเมล
    else:
        print("ไม่พบลูกค้ารายนี้ในระบบ")  # กรณีไม่พบข้อมูล