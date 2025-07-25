import psycopg2              # ไลบรารีเชื่อมต่อ PostgreSQL
import configparser          # ใช้อ่านไฟล์ config.ini

def get_customer_info(customer_id, start_date=None, end_date=None):
    """
    ฟังก์ชันสำหรับดึงข้อมูลลูกค้าจากฐานข้อมูล โดยกรองด้วย ID และสามารถกรองช่วงวันที่สร้าง (created_at) ได้ถ้าระบุ
    Parameters:
        customer_id (int): รหัสลูกค้าที่ต้องการดึงข้อมูล
        start_date (str): วันที่เริ่มต้นในรูปแบบ 'YYYY-MM-DD' (ถ้ามี)
        end_date (str): วันที่สิ้นสุดในรูปแบบ 'YYYY-MM-DD' (ถ้ามี)
    Returns:
        List of tuples: ผลลัพธ์จากฐานข้อมูล (ชื่อ, อีเมล)
    """

    # โหลดค่า config จากไฟล์ config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    conn_string = config['database']['connection_string']  # ดึงค่า connection string

    # เขียน SQL โดยใช้ parameter placeholder เพื่อป้องกัน SQL injection
    sql = "SELECT name, email FROM customer WHERE id = %(id)s"
    params = {'id': customer_id}

    # ถ้าระบุ start_date และ end_date เพิ่มเงื่อนไขช่วงวันที่เข้าไป
    if start_date and end_date:
        sql += " AND created_at BETWEEN %(start_date)s AND %(end_date)s"
        params['start_date'] = start_date
        params['end_date'] = end_date

    try:
        # เชื่อมต่อกับฐานข้อมูลด้วย context manager (with) เพื่อปิด connection อัตโนมัติ
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)   # execute คำสั่ง SQL พร้อม parameter
                return cur.fetchall()     # คืนค่าผลลัพธ์แบบ list of tuples

    except Exception as e:
        print(f"Database Error: {e}")     # แจ้งข้อผิดพลาดกรณีเชื่อมต่อไม่ได้
        return None