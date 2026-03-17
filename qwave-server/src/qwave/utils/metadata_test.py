from pathlib import Path
from qwave.services.metadata_service import extract, search_musicbrainz

# dont fucking use this in prod...
blah = input("toss ur audio path lmao\n")
test_path = Path(blah)

if test_path.exists():
    print("Metadata:")
    metadata = extract(test_path)
    for key, value in metadata.items():
        print(f"{key}: {value}")
    
    if metadata.get("title") or metadata.get("artist"):
        print("\n\nMusicBrainz:")
        mb_result = search_musicbrainz(
            title = metadata.get("title"),
            artist = metadata.get("artist")
        )
        if mb_result:
            for key, value in mb_result.items():
                print(f"{key}: {value}")
        else:
            print("none lmao")
else:
    print("are you lost lmao its not here")
