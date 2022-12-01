from pathlib import Path
import run_without_deepl

path = Path(__file__).parent.parent / "data" / "audio" / "test.mp3"

print(path)
run_without_deepl.main()
