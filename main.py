from load_dataset_module import load_artist_music, load_music_features
from similarity_module import compute_track_similarity, compute_artist_similarity, euclidean_similarity, cosine_similarity, pearson_similarity, jaccard_similarity, manhattan_similarity

def get_similarity_function(choice):
    """Return the corresponding similarity function based on user input."""
    if choice == 1:
        return euclidean_similarity
    elif choice == 2:
        return cosine_similarity
    elif choice == 3:
        return pearson_similarity
    elif choice == 4:
        return jaccard_similarity
    elif choice == 5:
        return manhattan_similarity
    else:
        print("Invalid choice! Defaulting to Euclidean similarity.")
        return euclidean_similarity

def compare_tracks(music_features):
    """Allow user to compare two music tracks."""
    try:
        track_id1 = int(input("Enter the ID of the first track: "))
        track_id2 = int(input("Enter the ID of the second track: "))
        
        print("Select a similarity metric:")
        print("1. Euclidean")
        print("2. Cosine")
        print("3. Pearson")
        print("4. Jaccard")
        print("5. Manhattan")
        similarity_choice = int(input("Enter your choice (1-5): "))

        similarity_function = get_similarity_function(similarity_choice)

        similarity = compute_track_similarity(music_features, track_id1, track_id2, similarity_function)
        print(f"Similarity between track {track_id1} and track {track_id2}: {similarity}")
    except ValueError:
        print("Invalid input! Please enter valid track IDs.")

def compare_artists(artist_music):
    """Allow user to compare two artists."""
    try:
        artist1 = input("Enter the name of the first artist: ")
        artist2 = input("Enter the name of the second artist: ")

        if artist1 not in artist_music or artist2 not in artist_music:
            print("One or both artists not found.")
            return

        print("Select a similarity metric:")
        print("1. Euclidean")
        print("2. Cosine")
        print("3. Pearson")
        print("4. Jaccard")
        print("5. Manhattan")
        similarity_choice = int(input("Enter your choice (1-5): "))

        similarity_function = get_similarity_function(similarity_choice)

        similarity = compute_artist_similarity(artist_music, artist1, artist2, similarity_function)
        print(f"Similarity between artists {artist1} and {artist2}: {similarity}")
    except ValueError:
        print("Invalid input! Please enter valid artist names.")

def main():
    """Main program function to interact with the user."""
    # Load data
    artist_music = load_artist_music("datasets/data.csv")
    music_features = load_music_features("datasets/data_genres.csv")
    
    while True:
        print("\nWelcome to the Music Recommendation System!")
        print("1. Compare Music Tracks")
        print("2. Compare Artists")
        print("3. Exit")
        
        try:
            choice = int(input("Enter your choice (1-3): "))
            
            if choice == 1:
                compare_tracks(music_features)
            elif choice == 2:
                compare_artists(artist_music)
            elif choice == 3:
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")
        except ValueError:
            print("Invalid input! Please enter a valid option.")

if __name__ == "__main__":
    main()
