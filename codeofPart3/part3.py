from db import get_customer_info   # import ฟังก์ชันที่เราสร้างไว้ใน db.py

if __name__ == "__main__":
    # เรียกดูข้อมูลลูกค้าด้วย ID อย่างเดียว (ไม่มีช่วงวัน)
    result1 = get_customer_info(123)
    print("ข้อมูลลูกค้า ID 123:", result1)

    # เรียกดูข้อมูลลูกค้าด้วย ID และช่วงวันที่สร้าง
    result2 = get_customer_info(123, "2024-01-01", "2024-12-31")
    print("ข้อมูลลูกค้าที่สร้างในปี 2024:", result2)