 * [ ] **สร้างและเปิดใช้งาน Virtual Environment**

  * Windows (PowerShell)

    * `python -m venv .venv`
    * `.venv\Scripts\Activate.ps1`
  * macOS/Linux

    * `python3 -m venv .venv`
    * `source .venv/bin/activate`

* [ ] **ติดตั้ง dependencies**

  * รัน: `pip install -r requirements.txt`

* [ ] **สร้างฐานข้อมูล / รัน migrations**

  * `python manage.py makemigrations`
  * `python manage.py migrate`

* [ ] **สร้าง Superuser (เพื่อเข้า Django Admin)**

  * `python manage.py createsuperuser`
  * ใช้ `phone_number` + `password`

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
