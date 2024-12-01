from collections import Counter
import math

def calculate_mean(data):
    """
    Calculate the mean of a list of numbers.
    """
    return sum(data) / len(data) if data else 0

def calculate_mode(data):
    """
    Calculate the mode of a list of numbers.
    Returns the most frequent value, or multiple modes if there's a tie.
    """
    frequency = Counter(data)
    max_count = max(frequency.values())
    modes = [key for key, count in frequency.items() if count == max_count]
    return modes[0] if len(modes) == 1 else modes

def calculate_variance(data):
    """
    Calculate the variance of a list of numbers.
    """
    mean = calculate_mean(data)
    return sum((x - mean) ** 2 for x in data) / len(data) if data else 0

def calculate_standard_deviation(data):
    """
    Calculate the standard deviation of a list of numbers.
    """
    variance = calculate_variance(data)
    return math.sqrt(variance)

def calculate_min(data):
    """
    Find the minimum value in a list of numbers.
    """
    return min(data) if data else None

def calculate_max(data):
    """
    Find the maximum value in a list of numbers.
    """
    return max(data) if data else None

def get_statistics_for_feature(data, feature):
    """
    Calculate statistics for a specific feature in the dataset.
    Returns a dictionary of statistical measures.
    """
    feature_values = [item['features'][feature] for item in data.values() if feature in item['features']]
    return {
        'mean': calculate_mean(feature_values),
        'mode': calculate_mode(feature_values),
        'variance': calculate_variance(feature_values),
        'standard_deviation': calculate_standard_deviation(feature_values),
        'min': calculate_min(feature_values),
        'max': calculate_max(feature_values),
    }

def query_best_genre(data, feature):
    """
    Find the genre with the highest average value for a specific feature.
    """
    genre_averages = {}
    for entry in data.values():
        genre = entry['genres']
        if feature not in entry['features']:
            print(f"Skipping entry due to missing feature '{feature}': {entry}")
            continue  # Skip entries missing the feature
        value = entry['features'][feature]
        if genre not in genre_averages:
            genre_averages[genre] = []
        genre_averages[genre].append(value)
    # Calculate average for each genre
    for genre in genre_averages:
        genre_averages[genre] = calculate_mean(genre_averages[genre])
    return max(genre_averages, key=genre_averages.get) if genre_averages else None

def query_extreme_artist(data, feature, find_max=True):
    """
    Find the artist with the extreme value (min or max) for a specific feature.
    """
    extreme_artist = None
    extreme_value = float('-inf') if find_max else float('inf')
    for artist, tracks in data.items():
        for track in tracks:
            if feature not in track['features']:
                print(f"Skipping track due to missing feature '{feature}': {track}")
                continue  # Skip tracks missing the feature
            value = track['features'][feature]
            if (find_max and value > extreme_value) or (not find_max and value < extreme_value):
                extreme_value = value
                extreme_artist = artist
    return extreme_artist, extreme_value

if __name__ == "__main__":
    from load_dataset_module import load_artist_music, load_music_features

    # Load datasets
    artist_music = load_artist_music("datasets/data.csv")
    music_features = load_music_features("datasets/data_genres.csv")

    # Test feature statistics
    print("Statistics for 'danceability':", get_statistics_for_feature(music_features, 'danceability'))

    # Test genre query
    print("Genre with the best 'liveliness':", query_best_genre(music_features, 'liveliness'))

    # Test artist query
    print("Artist with the highest 'loudness':", query_extreme_artist(artist_music, 'loudness', find_max=True))
    print("Artist with the lowest 'loudness':", query_extreme_artist(artist_music, 'loudness', find_max=False))
