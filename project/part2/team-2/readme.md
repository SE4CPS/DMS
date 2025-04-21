## 🌸 Flower Tracking App – Team 2

Our Flower Tracking App helps manage and monitor flower hydration levels for customers. It tracks when each flower was last watered, its current water level, and whether it meets the minimum/maximum hydration requirement. The app includes order tracking and customer information using a relational database structure.

### 🗄️ Database Overview
We created three main tables:

- `team2_flowers`: Stores flower data including `last_watered`, `water_level`, and hydration requirements.
- `team2_customers`: Contains customer information such as name and email.
- `team2_orders`: Tracks which customer ordered which flower and when.

All tables use `SERIAL PRIMARY KEY` for indexing, and foreign key constraints ensure data integrity between related tables.

### ⚙️ Features
- Add new flowers and track their hydration.
- View flower status to ensure proper watering.
- Track customer orders and flower purchases.
- SQl Water loss simulation to ensure proper water levels.
- Optimized query performance for hydration status checks.

### 💧 Water Loss Simulation

To make the flower hydration tracking more realistic, we implemented a **daily water loss simulation**. This simulates the natural decrease in water level for each flower based on the number of days since it was last watered.

### 🌡️ Water Status Indicator

To provide clear visual feedback on each flower’s hydration condition, we added a **Water Status** feature. This logic is handled on the backend and determines whether a flower is:

- **Underwatered** → `"Needs Water 💧"`
- **Healthy** → `"Healthy ✅"`
- **Overwatered** → `"Overwatered 🚨"`

### ⚡ Query Performance

We implemented and compared two query types:

| Query Type     | Execution Time |
|----------------|----------------|
| Initial (Unoptimized) Slow Query | ~39 seconds      
![image](https://github.com/user-attachments/assets/b4219cc6-09db-4653-af95-30894b7e25cc)|
| Optimized Fast Query            | ~0.2 seconds     
![image](https://github.com/user-attachments/assets/7c86e9ad-20b3-4e27-8c86-c1df19ec2735)|

The fast query was significantly more efficient after optimization, providing a smoother user experience.

### 💻 Technologies Used
- Python (Flask)
- PostgreSQL (neonDB)
- HTML/CSS
- JavaScript + AJAX for dynamic updates

