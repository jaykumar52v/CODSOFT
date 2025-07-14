import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import tkinter as tk
from tkinter import ttk, messagebox

# ========== MOVIE DATABASE WITH DECADE-BASED YEARS ==========
def create_movie_database():
    movies = [
        {"title": "The Shawshank Redemption", "year_range": "90s", "genre": "Drama", "category": "Classic"},
        {"title": "The Godfather", "year_range": "70s", "genre": "Crime", "category": "Classic"},
        {"title": "The Dark Knight", "year_range": "2000s", "genre": "Action", "category": "Superhero"},
        {"title": "Back to the Future", "year_range": "80s", "genre": "Sci-Fi", "category": "Adventure"},
        {"title": "Titanic", "year_range": "90s", "genre": "Romance", "category": "Drama"},
        {"title": "Avengers: Endgame", "year_range": "Modern", "genre": "Action", "category": "Superhero"},
        {"title": "The Social Network", "year_range": "2000s", "genre": "Drama", "category": "Biography"},
        {"title": "Pulp Fiction", "year_range": "90s", "genre": "Crime", "category": "Cult"},
        {"title": "Forrest Gump", "year_range": "90s", "genre": "Drama", "category": "Classic"},
        {"title": "Star Wars: A New Hope", "year_range": "70s", "genre": "Sci-Fi", "category": "Space Opera"},
        {"title": "The Lion King", "year_range": "90s", "genre": "Animation", "category": "Musical"},
        {"title": "Inception", "year_range": "2000s", "genre": "Sci-Fi", "category": "Mind-Bending"},
        {"title": "Jurassic Park", "year_range": "90s", "genre": "Adventure", "category": "Sci-Fi"},
        {"title": "Black Panther", "year_range": "Modern", "genre": "Action", "category": "Superhero"},
        {"title": "The Matrix", "year_range": "90s", "genre": "Sci-Fi", "category": "Action"},
        {"title": "E.T. the Extra-Terrestrial", "year_range": "80s", "genre": "Sci-Fi", "category": "Family"},
        {"title": "The Terminator", "year_range": "80s", "genre": "Sci-Fi", "category": "Action"},
        {"title": "Frozen", "year_range": "Modern", "genre": "Animation", "category": "Musical"},
        {"title": "Gladiator", "year_range": "2000s", "genre": "Action", "category": "Historical"},
        {"title": "The Silence of the Lambs", "year_range": "90s", "genre": "Thriller", "category": "Crime"},
        {"title": "Raiders of the Lost Ark", "year_range": "80s", "genre": "Adventure", "category": "Action"},
        {"title": "The Shining", "year_range": "80s", "genre": "Horror", "category": "Psychological"},
        {"title": "La La Land", "year_range": "Modern", "genre": "Musical", "category": "Romance"},
        {"title": "The Avengers", "year_range": "2000s", "genre": "Action", "category": "Superhero"},
        {"title": "Toy Story", "year_range": "90s", "genre": "Animation", "category": "Family"},
        {"title": "Die Hard", "year_range": "80s", "genre": "Action", "category": "Christmas"},
        {"title": "Get Out", "year_range": "Modern", "genre": "Horror", "category": "Thriller"},
        {"title": "The Notebook", "year_range": "2000s", "genre": "Romance", "category": "Drama"},
        {"title": "Whiplash", "year_range": "Modern", "genre": "Drama", "category": "Music"}
    ]
    return pd.DataFrame(movies)

# ========== CONTENT-BASED FILTERING ==========
class ContentRecommender:
    def __init__(self, movies_df):
        self.movies = movies_df
        # Create a metadata soup for each movie
        self.movies['metadata'] = self.movies.apply(
            lambda x: f"{x['genre']} {x['category']} {x['year_range']}", axis=1)
        
        # Create TF-IDF matrix
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies['metadata'])
        
        # Compute cosine similarity matrix
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
    
    def get_recommendations(self, user_preferences, top_n=5):
        # Create a pseudo-movie representing user preferences
        pseudo_movie = pd.Series({
            'title': 'user_query',
            'metadata': f"{user_preferences['genre']} {user_preferences['category']} {user_preferences['year_range']}"
        })
        
        # Transform user preferences using the same vectorizer
        user_tfidf = self.tfidf.transform([pseudo_movie['metadata']])
        
        # Calculate similarity between user preferences and all movies
        sim_scores = linear_kernel(user_tfidf, self.tfidf_matrix).flatten()
        
        # Get top movie indices
        movie_indices = sim_scores.argsort()[::-1][:top_n]
        
        return self.movies.iloc[movie_indices]

# ========== LIGHT THEME GUI APPLICATION ==========
class MovieRecommendationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recommendation System")
        self.root.geometry("550x600")
        self.root.configure(bg='white')
        
        # Create movie database
        self.movies_df = create_movie_database()
        self.recommender = ContentRecommender(self.movies_df)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Apply light theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='white', foreground='black')
        style.configure('TLabel', background='white', foreground='black', font=('Helvetica', 11))
        style.configure('TButton', background='#f0f0f0', foreground='black', font=('Helvetica', 11), padding=5)
        style.map('TButton', background=[('active', '#e0e0e0')])
        style.configure('TCombobox', fieldbackground='white', background='white', foreground='black')
        style.configure('TFrame', background='white')
        
        # Header
        header = ttk.Label(self.root, text="🎬 Movie Recommendation Engine", 
                         font=('Helvetica', 16, 'bold'))
        header.pack(pady=15)
        
        # Input Frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=20)
        
        # Genre Selection
        ttk.Label(input_frame, text="Select Genre:").grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.genre_var = tk.StringVar()
        self.genre_dd = ttk.Combobox(input_frame, textvariable=self.genre_var, 
                                   values=sorted(self.movies_df['genre'].unique()))
        self.genre_dd.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
        self.genre_dd.current(0)
        
        # Category Selection
        ttk.Label(input_frame, text="Select Category:").grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.category_var = tk.StringVar()
        self.category_dd = ttk.Combobox(input_frame, textvariable=self.category_var, 
                                       values=sorted(self.movies_df['category'].unique()))
        self.category_dd.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
        self.category_dd.current(0)
        
        # Year Range Selection
        ttk.Label(input_frame, text="Select Era:").grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.year_var = tk.StringVar()
        year_ranges = ["70s", "80s", "90s", "2000s", "Modern"]
        self.year_dd = ttk.Combobox(input_frame, textvariable=self.year_var, values=year_ranges)
        self.year_dd.grid(row=2, column=1, sticky='ew', pady=5, padx=5)
        self.year_dd.current(2)
        
        # Recommendation Button
        recommend_btn = ttk.Button(input_frame, text="Get Recommendations", 
                                 command=self.show_recommendations)
        recommend_btn.grid(row=3, column=0, columnspan=2, pady=15, sticky='ew')
        
        # Results Frame
        results_frame = ttk.Frame(self.root)
        results_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Results Label
        self.results_label = ttk.Label(results_frame, text="Recommended Movies Will Appear Here", 
                                     font=('Helvetica', 11))
        self.results_label.pack(pady=5)
        
        # Results Text
        self.results_text = tk.Text(results_frame, height=12, width=50, wrap='word',
                                  bg='white', fg='black', font=('Helvetica', 10),
                                  relief='groove', padx=10, pady=10)
        self.results_text.pack(fill='both', expand=True)
        self.results_text.config(state='disabled')
        
        # Footer
        footer = ttk.Label(self.root, text="Select your preferences and click 'Get Recommendations'",
                         font=('Helvetica', 9))
        footer.pack(pady=10)
    
    def show_recommendations(self):
        # Get user preferences
        user_prefs = {
            'genre': self.genre_var.get(),
            'category': self.category_var.get(),
            'year_range': self.year_var.get()
        }
        
        # Get recommendations
        recommendations = self.recommender.get_recommendations(user_prefs)
        
        # Display results
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        
        if len(recommendations) > 0:
            self.results_text.insert(tk.END, f"Movies Matching Your Preferences:\n\n")
            for idx, row in recommendations.iterrows():
                movie_info = f"🎞️ {row['title']}\n"
                movie_info += f"   Genre: {row['genre']}\n"
                movie_info += f"   Category: {row['category']}\n"
                movie_info += f"   Era: {row['year_range']}\n\n"
                self.results_text.insert(tk.END, movie_info)
        else:
            self.results_text.insert(tk.END, "No matching movies found. Try different preferences.")
        
        self.results_text.config(state='disabled')

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieRecommendationApp(root)
    root.mainloop()
