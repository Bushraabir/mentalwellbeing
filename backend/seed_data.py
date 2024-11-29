import sqlite3

DATABASE = "backend/database/mental_wellness.db"

def insert_sample_articles():
    """Insert sample articles into the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO articles (title, content, image_url, video_url)
        VALUES (?, ?, ?, ?)
    """, [
        ("The Importance of Self-Care", 
         "Self-care is crucial for maintaining mental health. This article provides practical tips to incorporate self-care into your daily routine.", 
         "datasets/photos/self-care.jpg", 
         None),
        
        ("Guided Meditation Techniques", 
         "Explore various guided meditation techniques to reduce stress and improve focus. This includes breathing exercises and visualization methods.", 
         None, 
         "datasets/videos/guided_meditation.mp4"),
        
        ("Coping with Stress in Daily Life", 
         "Learn how to manage stress effectively with actionable strategies. Discover ways to balance work, relationships, and self-care.", 
         "datasets/photos/stress-relief.jpg", 
         None)
    ])
    conn.commit()
    conn.close()
    print("Sample articles inserted successfully!")

if __name__ == "__main__":
    insert_sample_articles()
