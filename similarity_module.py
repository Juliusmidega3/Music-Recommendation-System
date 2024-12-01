import math
import ast  # For safely parsing list-like strings from the dataset
import csv  # Import the csv module for reading CSV files

# Similarity Functions
def euclidean_similarity(features1, features2):
    """Compute Euclidean distance."""
    return math.sqrt(sum((features1[key] - features2[key]) ** 2 for key in features1 if key in features2))


def cosine_similarity(features1, features2):
    """Compute Cosine similarity."""
    dot_product = sum(features1[key] * features2[key] for key in features1 if key in features2)
    magnitude1 = math.sqrt(sum(value ** 2 for value in features1.values()))
    magnitude2 = math.sqrt(sum(value ** 2 for value in features2.values()))
    return dot_product / (magnitude1 * magnitude2) if magnitude1 and magnitude2 else 0


def pearson_similarity(features1, features2):
    """Compute Pearson correlation coefficient."""
    mean1 = sum(features1.values()) / len(features1)
    mean2 = sum(features2.values()) / len(features2)
    numerator = sum((features1[key] - mean1) * (features2[key] - mean2) for key in features1 if key in features2)
    denominator = math.sqrt(sum((features1[key] - mean1) ** 2 for key in features1)) * \
                           math.sqrt(sum((features2[key] - mean2) ** 2 for key in features2))
    return numerator / denominator if denominator else 0


def jaccard_similarity(features1, features2):
    """Compute Jaccard similarity."""
    set1, set2 = set(features1.keys()), set(features2.keys())
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union) if union else 0


def manhattan_similarity(features1, features2):
    """Compute Manhattan distance."""
    return sum(abs(features1[key] - features2[key]) for key in features1 if key in features2)


# Compute Similarity Between Tracks
def compute_track_similarity(music_features, track_id1, track_id2, similarity_function):
    """
    Compute similarity between two music tracks using a specified similarity function.
    Args:
        music_features: Dictionary containing music features.
        track_id1: ID of the first track.
        track_id2: ID of the second track.
        similarity_function: Function to compute similarity (e.g., Euclidean, Cosine).
    Returns:
        Similarity score between the two tracks.
    """
    try:
        features1 = music_features[track_id1]['features']
        features2 = music_features[track_id2]['features']
        return similarity_function(features1, features2)
    except KeyError as e:
        print(f"Error: Track ID not found - {e}")
        return None


# Compute Similarity Between Artists
def compute_artist_similarity(artist_music, artist1, artist2, similarity_function):
    """
    Compute similarity between two artists by aggregating their track features.
    Args:
        artist_music: Dictionary containing artist and their tracks.
        artist1: Name of the first artist.
        artist2: Name of the second artist.
        similarity_function: Function to compute similarity (e.g., Euclidean, Cosine).
    Returns:
        Similarity score between the two artists.
    """
    try:
        # Aggregate features by averaging for each artist
        features1 = [track['features'] for track in artist_music[artist1]]
        features2 = [track['features'] for track in artist_music[artist2]]

        avg_features1 = {key: sum(f[key] for f in features1) / len(features1) for key in features1[0]}
        avg_features2 = {key: sum(f[key] for f in features2) / len(features2) for key in features2[0]}

        return similarity_function(avg_features1, avg_features2)
    except KeyError as e:
        print(f"Error: Artist not found - {e}")
        return None


# Load Artist Data with Updated Parsing (from previous example)
def load_artist_music(file_path):
    """
    Load data from 'data.csv' and create the artist_music dictionary.
    Each individual artist is a key in the dictionary.
    """
    artist_music = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parse the artists field (convert string list to actual list)
            artists = ast.literal_eval(row['artists'])  # Safely parse list
            track_name = row['name']
            features = {
                'acousticness': float(row['acousticness']),
                'danceability': float(row['danceability']),
                'energy': float(row['energy']),
                'liveness': float(row['liveness']),
                'loudness': float(row['loudness']),
                'popularity': float(row['popularity']),
                'speechiness': float(row['speechiness']),
                'tempo': float(row['tempo']),
                'valence': float(row['valence']),
            }
            for artist in artists:  # Process each artist in the list
                artist = artist.strip()  # Remove extra spaces, if any
                if artist not in artist_music:
                    artist_music[artist] = []
                artist_music[artist].append({'track_name': track_name, 'features': features})
    return artist_music


if __name__ == "__main__":
    from load_dataset_module import load_music_features

    # Load datasets
    artist_music = load_artist_music("datasets/data.csv")
    music_features = load_music_features("datasets/data_genres.csv")

    # Test Available Artists
    print("Available artists:", list(artist_music.keys())[:10])

    # Test Similarity Between Tracks
    print("Euclidean Similarity Between Tracks:", compute_track_similarity(music_features, 1, 2, euclidean_similarity))
    print("Cosine Similarity Between Tracks:", compute_track_similarity(music_features, 1, 2, cosine_similarity))

    # Test Similarity Between Artists
    artist1 = "Sergei Rachmaninoff"
    artist2 = "John McCormack"

    if artist1 in artist_music and artist2 in artist_music:
        print("Euclidean Artist Similarity:", compute_artist_similarity(artist_music, artist1, artist2, euclidean_similarity))
    else:
        print(f"One or both artists ({artist1}, {artist2}) not found in the dataset.")
