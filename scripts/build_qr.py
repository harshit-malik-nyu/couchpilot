"""QR links contain public original-content IDs only. Build dependency: qrcode 8.2."""
import json
from pathlib import Path
import qrcode
import qrcode.image.svg
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'web/qr';out.mkdir(exist_ok=True)
for s in json.loads((ROOT/'data/lesson.json').read_text())['segments']:
 url='https://portfolio-lac-five-10.vercel.app/projects/couchpilot/companion.html#segment='+s['id']
 img=qrcode.make(url,image_factory=qrcode.image.svg.SvgPathImage)
 img.save(out/(s['id']+'.svg'))
