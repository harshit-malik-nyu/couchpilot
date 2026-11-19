"""Render an original silent lesson; no copied YouTube content or footage."""
import base64,json,subprocess,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];build=ROOT/'build';build.mkdir(exist_ok=True)
lesson=json.loads((ROOT/'data/lesson.json').read_text())
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
for i,s in enumerate(lesson['segments']):
 im=Image.new('RGB',(960,540),'#101c2a');d=ImageDraw.Draw(im)
 d.text((55,38),'COUCHPILOT ORIGINAL / EXPERIMENTS',font=ImageFont.truetype(font,16),fill='#9fe7d9')
 d.text((55,105),s['title'].replace(' · ',' / '),font=ImageFont.truetype(font,32),fill='white')
 d.rounded_rectangle((55,185,900,425),radius=20,fill='#1e3043')
 for j,line in enumerate(textwrap.wrap(s['text'],58)):
  d.text((80,210+j*34),line,font=ImageFont.truetype(font,24),fill='#d3deeb')
 for j in range(6):d.rounded_rectangle((55+j*141,475,177+j*141,481),radius=3,fill='#9fe7d9' if j==i else '#35465b')
 d.text((55,500),'Silent visual lesson / 02:00 / Original educational fixture',font=ImageFont.truetype(font,14),fill='#9fb0c6')
 im.save(build/f'{i}.png')
subprocess.run(['ffmpeg','-y','-framerate','1/20','-i',str(build/'%d.png'),'-c:v','libx264','-threads','1','-r','10','-pix_fmt','yuv420p','-crf','28','-movflags','+faststart',str(build/'lesson.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
encoded=base64.b64encode((build/'lesson.mp4').read_bytes()).decode()
(ROOT/'web/media.js').write_text('window.LESSON_VIDEO="data:video/mp4;base64,'+encoded+'";\n')
(ROOT/'web/lesson.js').write_text('window.LESSON='+json.dumps(lesson)+';\n')
print('Original clip bytes', (build/'lesson.mp4').stat().st_size)
