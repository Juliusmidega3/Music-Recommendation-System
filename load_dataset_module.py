import csv

def load_artist_music(file_path):
    """
    Load data from 'data.csv' and create the artist_music dictionary.
    Returns a dictionary where:
        - Key: Artist name
        - Value: List of dictionaries containing track names and features.
    """
    artist_music = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            artist = row['artists']
            track_name = row['name']
            features = {
                'acousticness': float(row['acousticness']),
                'danceability': float(row['danceability']),
                'energy': float(row['energy']),
                'liveness': float(row['liveness']),
                'loudness': float(row['loudness']),
                'popularity': float(row['popularity']),  # Changed to float
                'speechiness': float(row['speechiness']),
                'tempo': float(row['tempo']),
                'valence': float(row['valence']),
            }
            if artist not in artist_music:
                artist_music[artist] = []
            artist_music[artist].append({'track_name': track_name, 'features': features})
    return artist_music


def load_music_features(file_path):
    """
    Load data from 'data_genres.csv' and create the music_features dictionary.
    Returns a dictionary where:
        - Key: Row number as the unique ID.
        - Value: Dictionary of genres and features.
    """
    music_features = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row_number, row in enumerate(reader, start=1):  # Use row_number as ID
            features = {
                'acousticness': float(row['acousticness']),
                'danceability': float(row['danceability']),
                'energy': float(row['energy']),
                'liveness': float(row['liveness']),
                'loudness': float(row['loudness']),
                'popularity': float(row['popularity']),  # Changed to float
                'speechiness': float(row['speechiness']),
                'tempo': float(row['tempo']),
                'valence': float(row['valence']),
            }
            music_features[row_number] = {'genres': row['genres'], 'features': features}
    return music_features


if __name__ == "__main__":
    # Test the functions
    try:
        # Replace these file paths with the correct relative paths
        artist_music = load_artist_music("datasets/data.csv")
        music_features = load_music_features("datasets/data_genres.csv")
        
        # Display sample outputs for verification
        print("Artist Music Dictionary Example:", list(artist_music.items())[:1])
        print("Music Features Dictionary Example:", list(music_features.items())[:1])
    except Exception as e:
        print("An error occurred:", str(e))
