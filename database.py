import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Payal@2302",
    database="online_job_portal"
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    job_id INT,
    application_date DATE,
    status VARCHAR(50) DEFAULT 'Pending',

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE,

    FOREIGN KEY (job_id)
    REFERENCES jobs(job_id)
    ON DELETE CASCADE
)
""")

connection.commit()

print("Applications table created successfully!")

cursor.close()
connection.close()