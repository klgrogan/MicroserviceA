import json
import time
import random

# File paths
input_file = "song_data.json"  # Corrected input file
output_file = "recommendations_service.txt"  # Corrected output file


def write_to_file(file_path, content):
    """
    Writes text content to a file.
    If content is a list, writes each item as a JSON object.
    """
    mode = "w" # replace "w" with "a" to append to recommendations_service.txt
    with open(file_path, mode) as file:
        if isinstance(content, list):
            file.write("\n".join(json.dumps({"id": song_id}) for song_id in content) + "\n")
        else:
            file.write(json.dumps({"id": content}) + "\n")



def read_song_data():
    """Reads data from song_data.json"""
    try:
        with open(input_file, "r") as file:  # Use input_file here
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def find_similar_songs(song_id, song_data):
    """
    Finds at least 10 similar songs based on genre, tempo, and instrumentation.
    If not enough exact or partial matches are found, fills with random songs.
    """
    try:
        seed_song = next(song for song in song_data if song["id"] == song_id)
    except StopIteration:
        return []

    # Exact matches based on all criteria
    similar_songs = [
        song["id"] for song in song_data
        if song["id"] != song_id and
        song["genre"] == seed_song["genre"] and
        abs(song["tempo"] - seed_song["tempo"]) <= 20 and
        song["instrumentation"] == seed_song["instrumentation"]
    ]

    # If fewer than 10 exact matches, add songs matching at least 2 criteria
    if len(similar_songs) < 10:
        two_criteria_matches = [
            song["id"] for song in song_data
            if song["id"] != song_id and
            song["id"] not in similar_songs and
            (
                (song["genre"] == seed_song["genre"] and abs(song["tempo"] - seed_song["tempo"]) <= 20) or
                (song["genre"] == seed_song["genre"] and song["instrumentation"] == seed_song["instrumentation"]) or
                (abs(song["tempo"] - seed_song["tempo"]) <= 20 and song["instrumentation"] == seed_song["instrumentation"])
            )
        ]
        similar_songs.extend(two_criteria_matches[:10 - len(similar_songs)])

    # If still fewer than 10, add songs matching at least 1 criterion
    if len(similar_songs) < 10:
        one_criteria_matches = [
            song["id"] for song in song_data
            if song["id"] != song_id and
            song["id"] not in similar_songs and
            (
                song["genre"] == seed_song["genre"] or
                abs(song["tempo"] - seed_song["tempo"]) <= 20 or
                song["instrumentation"] == seed_song["instrumentation"]
            )
        ]
        similar_songs.extend(one_criteria_matches[:10 - len(similar_songs)])

    # If still fewer than 10, fill with random songs from the dataset
    if len(similar_songs) < 10:
        remaining_songs = [
            song["id"] for song in song_data
            if song["id"] != song_id and song["id"] not in similar_songs
        ]
        random.shuffle(remaining_songs)
        similar_songs.extend(remaining_songs[:10 - len(similar_songs)])

    # Ensure exactly 10 recommendations
    return similar_songs[:10]


def process_song_id(song_id):
    """
    Processes song ID received from another service.
    """
    song_data = read_song_data()
    if song_data:
        if any(song["id"] == song_id for song in song_data):
            #write_to_file(output_file, song_id) //not sure if you wanted the original song_id, delete hash to include
            # Find similar song IDs and write them
            similar_song_ids = find_similar_songs(song_id, song_data)
            if similar_song_ids:
                write_to_file(output_file, similar_song_ids)


def listen_for_song_id():
    """
    Continuously listens for a song ID in song_id.txt, processes it,
    and appends recommendations to recommendations_service.txt.
    """
    processed_ids = set()  # Keep track of already processed song IDs
    while True:
        try:
            with open("song_id.txt", "r") as f:
                song_id = f.read().strip()

            if song_id and song_id not in processed_ids:
                process_song_id(song_id)
                processed_ids.add(song_id)  # Mark the ID as processed

                # Clear the song_id.txt file after processing
                with open("song_id.txt", "w") as f:
                    f.truncate()
        except FileNotFoundError:
            time.sleep(5)  # Wait before checking again


if __name__ == "__main__":
    listen_for_song_id()



