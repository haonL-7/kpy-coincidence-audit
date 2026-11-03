
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
BASE = os.environ.get("KPY_BASE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
figs = os.path.join(BASE, "figs")
plt.rcParams.update({"font.family":"Arial","savefig.bbox":"standard","savefig.pad_inches":0,"pdf.fonttype":42})
G="#8A8A8A"
fig=plt.figure(figsize=(7.0,1.9)); ax=fig.add_axes([0,0,1,1]); ax.axis("off")
ax.set_xlim(0,100); ax.set_ylim(0,27)

def box(x,y,w,h,txt,fc="#FFFFFF",ec="#9AA7B1",fs=6.8,bold=False,tc="#111111"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.22,rounding_size=0.7",fc=fc,ec=ec,lw=0.8))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs,
            fontweight=("bold" if bold else "normal"),color=tc,linespacing=1.25)
def arr(x1,y1,x2,y2,c=G):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=6.5,lw=0.8,color=c,
                                 shrinkA=0.5,shrinkB=0.5))

box(1,9.5,16,8,"co-occupancy\nclaim","#F2F6FA","#C9D8E6",6.9,True)
box(22,17.5,26,6.5,"1  declare the reference set")
box(22,10.2,26,6.5,"2  match protein composition")
box(22,2.9,26,6.5,"3  state power (catalogued n)")
box(53,9.5,17,8,"all three\nreported?","#F2F6FA","#C9D8E6",6.9,True)
box(75,17.0,24,7.5,"comparison\ninterpretable","#E8F5EF","#8CC9AC",6.9,True,"#255C42")
box(75,3.0,24,7.5,"not\ninterpretable","#FBEDED","#E0A9A9",6.9,False,"#7A3B3B")

for yy in (20.7,13.4,6.1):
    arr(17.6,13.5,21.5,yy)
    arr(48.5,yy,52.5,13.5)
arr(70.5,15.2,74.5,20.2,"#4E8F6E"); ax.text(72.6,18.6,"yes",fontsize=6.2,color="#4E8F6E",ha="center")
arr(70.5,11.8,74.5,7.0,"#B06060"); ax.text(72.6,8.6,"no",fontsize=6.2,color="#B06060",ha="center")

fig.savefig(os.path.join(figs,"Fig4_protocol.pdf")); fig.savefig(os.path.join(figs,"Fig4_protocol.png"),dpi=300)
sub=os.path.join(figs,"submission"); os.makedirs(sub,exist_ok=True)
fig.savefig(os.path.join(sub,"Fig4.pdf")); fig.savefig(os.path.join(sub,"Fig4.tif"),dpi=600,pil_kwargs={"compression":"tiff_lzw"})
print("ok")
