"""Decode every shipped SVG QR asset; no physical camera/device claim."""
import hashlib
import io
import json
from pathlib import Path
import cairosvg
from PIL import Image
import zxingcpp

root=Path(__file__).resolve().parents[1]
rows=[]
for s in json.loads((root/'data/lesson.json').read_text())['segments']:
    path=root/'web/qr'/f"{s['id']}.svg"
    # Match the white QR background used by the shipped stylesheet.
    png=cairosvg.svg2png(bytestring=path.read_bytes(),background_color='white',output_width=600,output_height=600)
    found=zxingcpp.read_barcode(Image.open(io.BytesIO(png)))
    expected='https://portfolio-lac-five-10.vercel.app/projects/couchpilot/companion.html#segment='+s['id']
    assert found and found.text==expected,s['id']+' QR did not decode to the expected public card'
    rows.append({'asset':str(path.relative_to(root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'decoded':found.text})
report={'scope':'Software decoding of SVG-rendered QR images at 600 pixels. No physical camera or phone compatibility claim.','results':rows}
(root/'evaluation/qr-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('Decoded and verified all',len(rows),'shipped QR links')
