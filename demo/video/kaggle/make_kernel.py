"""Builds the Kaggle TTS kernel from narration.json (inlined, so no dataset is needed) and writes its metadata.

    python make_kernel.py            # writes build/ ; then: cd build && kaggle kernels push -p .
The kernel installs Kokoro-82M in a Python 3.12 venv (Kaggle's 3.13 is too new for it), speaks every
line with voice af_heart at speed 1.0, 24 kHz, and leaves vo/<id>.wav plus vo/lengths.json in its output.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
KERNEL_ID = "shivanshkalra/proofpay-voiceover"

TEMPLATE = r'''
import json, subprocess, textwrap

LINES = json.loads(r"""__LINES__""")

def sh(cmd):
    print("+", cmd, flush=True)
    subprocess.run(cmd, shell=True, check=True)

sh("apt-get update -qq && apt-get install -y -qq espeak-ng > /dev/null")
sh("pip install -q uv && uv venv -q -p 3.12 /kaggle/tmp/tts")
sh('uv pip install -q --python /kaggle/tmp/tts/bin/python "kokoro>=0.9.4" soundfile "numpy<2.3" '
   "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl")

json.dump(LINES, open("/kaggle/working/lines.json", "w"))
open("/kaggle/working/tts.py", "w").write(textwrap.dedent("""
    import json, os
    import numpy as np, soundfile as sf
    from kokoro import KPipeline
    lines = json.load(open("/kaggle/working/lines.json"))
    os.makedirs("/kaggle/working/vo", exist_ok=True)
    pipe = KPipeline(lang_code="a")
    lengths = {}
    for l in lines:
        chunks = [np.asarray(r.audio) for r in pipe(l["spoken"], voice="af_heart", speed=1.0) if r.audio is not None]
        audio = np.concatenate(chunks)
        sf.write(f"/kaggle/working/vo/{l['id']}.wav", audio, 24000)
        lengths[l["id"]] = round(len(audio) / 24000, 3)
        print(l["id"], lengths[l["id"]], flush=True)
    json.dump(lengths, open("/kaggle/working/vo/lengths.json", "w"), indent=2)
"""))
sh("/kaggle/tmp/tts/bin/python /kaggle/working/tts.py")
sh("rm -f /kaggle/working/tts.py /kaggle/working/lines.json")
'''


def main():
    lines = json.loads((HERE.parent / "narration.json").read_text(encoding="utf-8"))["lines"]
    spoken = [{"id": l["id"], "spoken": l["spoken"]} for l in lines]
    build = HERE / "build"
    build.mkdir(exist_ok=True)
    (build / "tts_kernel.py").write_text(TEMPLATE.replace("__LINES__", json.dumps(spoken)), encoding="utf-8")
    (build / "kernel-metadata.json").write_text(json.dumps({
        "id": KERNEL_ID,
        "title": "proofpay-voiceover",
        "code_file": "tts_kernel.py",
        "language": "python",
        "kernel_type": "script",
        "is_private": True,
        "enable_gpu": False,
        "enable_internet": True,
        "dataset_sources": [],
        "competition_sources": [],
        "kernel_sources": [],
    }, indent=2), encoding="utf-8")
    print(f"wrote {build} with {len(spoken)} lines")


if __name__ == "__main__":
    main()
