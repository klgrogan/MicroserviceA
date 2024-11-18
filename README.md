![microA](https://github.com/user-attachments/assets/0a088149-5a70-44f9-adf6-ed5b25995775)
microserviceA

Overview:

This microservice listens for a song_id in the song_id.txt file and writes recommendations to the
recommendations_service.txt file. The recommendations are based on similar songs from the
song_data.json file; I just genre, instrumentation and BPM +/-20 but can be changed.

Request/Receive:

The microservice works by continuously monitoring the song_id.txt file for new song IDs. Once a
valid song ID is written to this file, the service processes it and writes at least 10
recommendations to the recommendations_service.txt file. Its defaulted to check song_id.json every
5 seconds but that again can be changed.

Call example:

with open("song_id.txt", "w") as file:
    file.write("40")
