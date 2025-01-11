# Book Recommendation System  

A full-stack book recommendation system that provides book suggestions based on similar books (using ISBN) or user preferences (User_ID). The system uses a preprocessed dataset for training the recommendation model and displays recommendations via a web interface.  

## Features  
- **Frontend**: Built with Nuxt.js, it provides a user-friendly interface for book recommendations.  
- **Backend**: Developed with FastAPI to serve recommendation data and handle requests.  
- **Machine Learning**: A recommendation engine that uses preprocessed data to train a model for finding similar books and user-based recommendations.  
- **Data**: Dataset sourced from [Kaggle - book-recommendation-dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset).  

---

## Frontend  

### Pages  
1. **Home (`index.vue`)**: 
    - A landing page with an overview of the system.
    - Endpoint: `/`
2. **Books (`books.vue`)**:  
    - Search for similar books using ISBN.  
    - Get personalized recommendations based on User_ID.  
    - Endpoint: `/books`
3. **Popular (`popular.vue`)**: 
    - Displays the most popular books.  
    - Endpoint: `/popular`

### Setup and Run  
1. Navigate to the `frontend` folder:  
   ```bash
   cd frontend
   ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Start the development server:
    ```bash
    npm run dev
    ```
The frontend will be available at http://localhost:3000.

## Backend
Data Preparation

1. Extract the dataset archive:
    - Navigate to BookRecSys/backend/app/data.
    - Extract archive.zip.
    - Move the extracted files to raw/ folder.
    - Create filtered/ folder.

2. Create a replicated environment to run the project
```bash
# Go to the backend folder and run the command to create a replicated environment
cd backend
conda env create -f environment.yml
```

3. Filter and preprocess the data:
```bash
python3 -m app.data_processing.scripts.process_and_load
```
- This will create FilteredBooks.csv, FilteredUsers.csv, and FilteredRatings.csv in the filtered/ folder.

4. Train the recommendation model:
```bash
python3 -m app.ml_models.training_script
```

### Run the Backend
1. Navigate to the backend folder:
```bash
cd backend
```

2. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The backend will be available at http://localhost:8000.