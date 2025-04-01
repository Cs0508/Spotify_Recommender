# Configuration Guide for CSV Processing

This document explains the purpose of each `.txt` file in the `dataset/config/` directory and how they are used in the CSV processing pipeline.

## 📁 Configuration Files

### 1️⃣ `date_cols.txt` (Date Columns)
**Purpose:**  
Contains column names that represent date or timestamp values.  

**Processing Steps:**  
- These columns are converted to **datetime format**.  
- If conversion fails, they will be **set as NaT (Not a Time)**.  
- Rows with missing dates will be **dropped**.  

**Example Entries:**
```plaintext
release_date
generated_on
```

---

### 2️⃣ `id_cols.txt` (ID Columns)
**Purpose:**  
Contains column names that represent categorical identifiers (e.g., track IDs, playlist IDs).  

**Processing Steps:**  
- These columns are **converted to category type**.  
- They are then transformed into **numerical codes**.  

**Example Entries:**
```plaintext
track_id
playlist_id
album_id
artist_ids
```

---

### 3️⃣ `numeric_cols.txt` (Numerical Columns)
**Purpose:**  
Contains column names that represent numerical values, which require normalization.  

**Processing Steps:**  
- Missing values are **filled with the median**.  
- Values are **scaled using MinMaxScaler (0 to 1 normalization)**.  

**Example Entries:**
```plaintext
danceability
energy
loudness
speechiness
acousticness
instrumentalness
liveness
valence
tempo
```

---

### 4️⃣ `ignore_cols.txt` (Ignored Columns) (Optional)
**Purpose:**  
Contains column names that should be **ignored** during data processing.  

**Processing Steps:**  
- These columns are **excluded** from the final output.  

**Example Entries:**
```plaintext
num_followers
num_tracks
```

---

## 🚀 How to Modify the Configuration
1. Open the `.txt` file corresponding to the category you want to modify.  
2. Add or remove column names as needed (one per line).  
3. Save the file and re-run the script.  

By organizing column names into separate configuration files, this approach ensures **flexibility, scalability, and easier customization** when processing different datasets.

