import psycopg2            # ไลบรารีเชื่อมต่อ PostgreSQL
import psycopg2.extras     # ใช้ DictCursor เพื่อให้ผลลัพธ์อยู่ในรูปแบบ dict
import configparser        # ใช้อ่านไฟล์ config (.ini)

def get_db_config():
    """
    อ่านค่าการเชื่อมต่อฐานข้อมูลจากไฟล์ app.config
    แล้วคืนค่าเป็น dictionary ที่มีข้อมูล host, dbname, user, password
    """
    config = configparser.ConfigParser()   # สร้าง object สำหรับอ่าน config
    config.read('app.config')             # อ่านไฟล์ config
    return config['postgresql']           # คืนค่าการตั้งค่าเฉพาะ section 'postgresql'

def get_customer_info(customer_id):
    """
    รับ customer_id แล้วดึงข้อมูล Name, Email ของลูกค้าจากฐานข้อมูล PostgreSQL
    คืนค่าเป็น dictionary หรือ None ถ้าไม่พบข้อมูล
    """

    db = get_db_config()  # ดึงค่าการเชื่อมต่อจาก config คือ host, dbname, user, password , port

    # สร้างการเชื่อมต่อกับ PostgreSQL โดยใช้ข้อมูลจาก config
    conn = psycopg2.connect(
        dbname=db['dbname'],
        user=db['user'],
        password=db['password'],
        host=db['host'],
        port=db['port']
    )

    try:
        # สร้าง cursor ที่แสดงผลลัพธ์เป็น dictionary แทน tuple
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # เขียนคำสั่ง SQL ระบุเฉพาะคอลัมน์ที่ต้องการเพื่อประหยัดทรัพยากร
            query = "SELECT Name, Email FROM Customer WHERE id = %s"
            cur.execute(query, (customer_id,))  # ใช้ parameterized query เพื่อกัน SQL injection
            row = cur.fetchone()  # ดึงผลลัพธ์แถวแรก (ถ้ามี)

            # คืนค่าผลลัพธ์เป็น dictionary หรือ None ถ้าไม่เจอข้อมูล
            return dict(row) if row else None

    finally:
        conn.close()  # ปิดการเชื่อมต่อฐานข้อมูลเสมอ ไม่ว่าจะสำเร็จหรือเกิดข้อผิดพลาด