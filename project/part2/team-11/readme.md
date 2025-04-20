## **COMP 163 DMS (Spring 2025): TEAM 11**

### **CREATED BY:**
- Agustin Rodriguez Jauregui
- Mohamed Abdullah
- Arsalan Khojazada

## **Flower Store**

### **Components:**
- Able To Add/Remove Flowers And Water
- Visible Flower Store Orders/Customers
- Fast/Slow Query Testable
- Water Level For Flowers can decrease/increase

### **Technology:**
- Database: SQLite
- Front-end: HTML
- Back-end: Flask, Python

### **Set Up:**
1. Need Python Installed On Machine Used
2. Clone The DMS git project into Any IDE (PyCharm or VS Code)
3. Once Project Is Open, Install The Following Libraries With Terminal:
- `pip install flask`
- `pip install Faker`
4. Go To Python File `app.py`
5. Go To The Local Host Link Found In Terminal

### Website

#### Part 1: Front-End Functionalities: 
1. flowers11.html
- Displays All Flowers And Attributes
- Displays Customers And Orders
- Opportunity To Add New Flower
<img src="![image](https://github.com/user-attachments/assets/65618091-d54f-4be5-956a-fea555e562bb)" width="500" height="500">

- Displays JSON Version Of All Flowers
<img src="![image](https://github.com/user-attachments/assets/3049a30e-3121-4cc0-a9f8-971f96f2996a)" width="500" height="500">

2. update_flowers.html
- Updates Flowers Name/Water Level/Last Watered/Water Requirement
<img src="![image](https://github.com/user-attachments/assets/16d866ef-c799-460d-a432-10526075eed5)" width="500" height="500">

#### Part 2: Back-End Functionalities: 
1. gen_insert_data.py
- Generates New Data Using Faker
- New Data Is Used To Test Fast/Slow Query With Real-World Big Data

2. team11_flowers.db
- Holds All Of the Data For Tables
- Database Updates Every Time The Slow/Fast Query Button Is Clicked
<img src="![image](https://github.com/user-attachments/assets/6c3d730b-63d2-4ae0-83fe-83f83273185e)" width="500" height="500">

3. team_flowers.sql
- Used To Define teamm11_customers, team11_flowers, And team11_orders Tables
- Used To Create Indexes For orders_customer_id, customer_id, flower_id, And orders_flowers_id
- Used To Insert Manual Data

4. app.py
- Sets Up Slow Query Functionalities Using Encryption, Sorting Algorithms, And Join Statements
- Sets Up Fast Query Functionalities to Retrieve One Thousand Orders With order ID, customer name, flower ordered, and date ordered Using Decryption And Join Statements
<img src="![image](https://github.com/user-attachments/assets/b1ddeebc-06c3-43e6-a874-6c03f6837ebc)" width="500" height="500">

- Delete/Add/Update Flowers Functionalities
- Manages Homepage, JSON Version, UI(HTML) Routes And Table Functionalities

### Performace Summary

1. Slow Query

3. Fast Query


