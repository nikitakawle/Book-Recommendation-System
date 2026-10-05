# 📚 Book Recommendation System

A Machine Learning-based Book Recommendation System built using collaborative filtering and demographic-based filtering.  
This project recommends books using:

- 📌 Popularity-Based Recommendation
- 🔍 Item-Based Collaborative Filtering (Cosine Similarity)
- 🎯 Personalized Recommendation (Age & Country Based)

---

## 🚀 Live Features

### 🏆 Popular Books
Displays top-rated and most-rated books.

### 🔍 Similar Book Recommendation
Find books similar to a selected book using cosine similarity.

### 🎯 Personalized Recommendation
Recommends books based on:
- User Age (converted into age groups)
- User Country
- Book popularity within demographic

---

## 🧠 Machine Learning Approach

### 1️⃣ Popularity-Based Filtering
- Aggregated ratings using:
  - Average Rating
  - Rating Count
- Recommended books with high rating and high popularity.

### 2️⃣ Collaborative Filtering
- Created User-Book Pivot Table
- Used Cosine Similarity to compute similarity between books.
- Recommended top 8 similar books.

### 3️⃣ Demographic-Based Filtering
- Converted Age into Age Groups:
  - Teen
  - Young Adult
  - Adult
  - Senior
- Filtered books based on:
  - Country
  - Age Group
  - Popularity (rating count threshold)

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Pickle

---

## 📂 Project Structure

```
📁 Book-Recommendation-System
│-- app.py
│-- popular_books.pkl
│-- pivot_table.pkl
│-- books.pkl (excluded via .gitignore)
│-- requirements.txt
│-- README.md
│-- .gitignore
```

---

## ⚙️ Installation & Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/book-recommendation-system.git
cd book-recommendation-system
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the application

```bash
streamlit run app.py
```

---

## 📊 Dataset

The dataset contains:

- User ID
- Book ISBN
- Book Rating
- Book Title
- Author
- Publisher
- Age
- Country

Large dataset files are excluded from GitHub due to size limitations.

---

## 💡 Future Improvements

- Hybrid Recommendation (Similarity + Demographic)
- Model Optimization
- Deployment on Streamlit Cloud
- User Login & History Tracking

---

## 👩‍💻 Author

**Sanjivani Arunkumar Pawar**  
Mumbai, India  

---

⭐ If you like this project, consider giving it a star!