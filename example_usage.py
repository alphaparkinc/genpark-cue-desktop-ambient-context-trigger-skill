from client import CueDesktopAmbientTrigger
import json

cue = CueDesktopAmbientTrigger()
print("=== CUE DESKTOP AMBIENT TRIGGER BENCHMARK ===")
res = cue.run_cue_benchmark()
print(json.dumps(res, indent=2))
