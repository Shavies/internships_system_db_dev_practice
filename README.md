* [ ] **ความคืบหน้าปัจจุบัน**
  * Authentication สำหรับ user และ admin ด้วย phone_number, password
  * แยก Role ของ User ระหว่าง STUDENT, OWNER ผ่านการ register(แก้ไขในอนาคต)
  * เก็บข้อมูล user ที่จำเป็น ก่อนเชื่อมไปยังตาราง student และ ตาราง mentor เพื่อเก็บข้อมูลแยกกันในอนาคต
 
* [ ] **สร้างและเปิดใช้งาน Virtual Environment**

  * Windows (PowerShell)

    * `python -m venv .venv`
    * `.venv\Scripts\Activate.ps1`
  * macOS/Linux

    * `python3 -m venv .venv`
    * `source .venv/bin/activate`

* [ ] **ติดตั้ง dependencies**

  * รัน: `pip install -r requirements.txt`

* [ ] **ตั้งค่า Environment Variables (ปัจจุบันยังไม่มี ENV)**

  * ถ้ามีไฟล์ `.env.example` ให้ทำ:

    * copy เป็น `.env`
    * ใส่ค่าตามที่กำหนด (เช่น `SECRET_KEY`, `DEBUG`, `DATABASE_URL` ฯลฯ)
  * ปัจจุบันโปรเจคยังไม่มี env นะครับ

* [ ] **สร้างฐานข้อมูล / รัน migrations**

  * `python manage.py makemigrations`
  * `python manage.py migrate`

* [ ] **สร้าง Superuser (เพื่อเข้า Django Admin)**

  * `python manage.py createsuperuser`
  * ใช้ `phone_number` + `password` ตามที่ระบบกำหนด

* [ ] **รันเซิร์ฟเวอร์**

  * `python manage.py runserver`

* [ ] **เปิดหน้าใช้งาน**

  * เว็บ: `http://localhost:8000/`
  * Admin: `http://localhost:8000/admin/`


## Setup bash Summary

```bash
python -m venv .venv
.venv\Scripts\activate # Mac -> source .venv/bin/activate  
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
