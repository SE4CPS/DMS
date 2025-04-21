## **COMP 163 DMS (Spring 2025): TEAM 11**

### **Team Members:**
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

![UI](https://github.com/user-attachments/assets/8168b159-9eb6-40fb-8394-8e4495d34ed8)


- Displays JSON Version Of All Flowers
  
![JSON](https://github.com/user-attachments/assets/28d3c0ed-cc64-4632-98bf-3f2569d46c05)

2. update_flowers.html
- Updates Flowers Name/Water Level/Last Watered/Water Requirement
  
![Update](https://github.com/user-attachments/assets/1f5cfabe-ada9-462f-867b-9b1240e252b5)

#### Part 2: Back-End Functionalities: 
1. gen_insert_data.py
- Generates New Data Using Faker
- New Data Is Used To Test Fast/Slow Query With Real-World Big Data

2. team11_flowers.db
- Holds All Of the Data For Tables
- Database Updates Every Time The Slow/Fast Query Button Is Clicked

![DatabaseTables](https://github.com/user-attachments/assets/c999d159-ed10-4422-bc2e-d2670a1f2911)


3. team_flowers.sql
- Used To Define teamm11_customers, team11_flowers, And team11_orders Tables
- Used To Create Indexes For orders_customer_id, customer_id, flower_id, And orders_flowers_id
- Used To Insert Manual Data

4. app.py
- Sets Up Slow Query Functionalities Using Encryption, Sorting Algorithms, And Join Statements
- Sets Up Fast Query Functionalities to Retrieve One Thousand Orders With order ID, customer name, flower ordered, and date ordered Using Decryption And Join Statements
  
![FastSlowButtons](https://github.com/user-attachments/assets/5faae0f9-ffa7-4b0d-ac87-c7fedb4bb354)


- Delete/Add/Update Flowers Functionalities
- Manages Homepage, JSON Version, UI(HTML) Routes And Table Functionalities

### Performace Summary

1. Slow Query

3. Fast Query


