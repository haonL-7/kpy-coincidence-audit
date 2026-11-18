import os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
BASE = os.environ.get('KPY_BASE', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
figs = os.path.join(BASE, 'figs'); sub = os.path.join(figs, 'submission')
os.makedirs(sub, exist_ok=True)
plt.rcParams.update({'font.family':'Arial','font.size':7,'axes.labelsize':7.2,
 'xtick.labelsize':6.6,'ytick.labelsize':6.6,'axes.linewidth':0.6,'xtick.major.width':0.6,
 'ytick.major.width':0.6,'xtick.major.size':2.4,'ytick.major.size':2.4,'axes.spines.top':False,
 'axes.spines.right':False,'pdf.fonttype':42})
rows = [
  ('Acetylation',              1.03, 11.13, False),
  ('Crotonylation',            3.35,  5.19, False),
  ('2-Hydroxyisobutyrylation', 3.92,  4.68, False),
  ('Malonylation',             3.67,  2.78, False),
  ('Succinylation',            3.42,  3.35, False),
  ('Butyrylation',             1.58, 16.48, False),
  ('Lactylation',              3.62,  5.67, False),
  ('Glutarylation',            3.60,  1.97, False),
  ('Propionylation',           4.22, 65.12, False),
  ('Pyruvylation (Kpy)',       2.95,  2.60, True),
]
BLUE, ORANGE, GREY, GREEN = '#0072B2', '#D55E00', '#B9C2C9', '#4E8F6E'
fig, ax = plt.subplots(figsize=(3.6, 3.15))
ys = list(range(len(rows)))[::-1]
for y, (name, fold, orv, kpy) in zip(ys, rows):
    c = ORANGE if kpy else BLUE
    ax.plot([fold, orv], [y, y], color=GREY, lw=1.0, zorder=1)
    ax.scatter([orv], [y], s=26, marker='s', facecolor=c, edgecolor=c, linewidth=0.8, zorder=3)
    ax.scatter([fold], [y], s=26, facecolor='white', edgecolor=c, linewidth=1.1, zorder=4)
    if abs(orv - fold) < 0.25:
        ax.annotate('%.2f' % orv, (orv, y), textcoords='offset points', xytext=(0, -11),
                    ha='center', fontsize=5.6, color=BLUE)
        ax.annotate('%.2f' % fold, (fold, y), textcoords='offset points', xytext=(0, 7),
                    ha='center', fontsize=5.6, color=BLUE)
    else:
        dx, ha = (6, 'left') if orv > fold else (-6, 'right')
        ax.annotate('%.2f' % orv, (orv, y), textcoords='offset points', xytext=(dx, -2),
                    ha=ha, fontsize=5.6, color='#333333')
ax.axvline(1, color='#999999', lw=0.6, ls=(0, (1, 2)))
ax.axvline(5.19, color=GREEN, lw=0.7, ls=(0, (3, 2)))
ax.annotate('median 5.19', (5.19, -0.62), xycoords=('data','data'), ha='center',
            va='top', fontsize=5.8, color=GREEN)

ax.set_xscale('log')
ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows], fontsize=6.4)
ax.set_ylim(-1.5, len(rows)-0.4)
ax.set_xlim(0.85, 190)
ax.set_xticks([1, 2, 5, 10, 20, 50]); ax.set_xticklabels(['1','2','5','10','20','50'])
ax.set_xlabel('Fold over the null (log scale)')
h1 = ax.scatter([], [], s=24, facecolor='white', edgecolor=BLUE, linewidth=1.0, label='pooled fold')
h2 = ax.scatter([], [], s=26, marker='s', facecolor=BLUE, edgecolor=BLUE, linewidth=0.8, label='within-protein OR')
h3 = ax.scatter([], [], s=26, marker='s', facecolor=ORANGE, edgecolor=ORANGE, linewidth=0.8, label='Kpy')
ax.legend(handles=[h1,h2,h3], frameon=False, fontsize=5.8, ncol=3, loc='upper center',
          bbox_to_anchor=(0.5, -0.19), handletextpad=0.3, columnspacing=1.1, borderpad=0.0)
fig.tight_layout(pad=0.3)
fig.savefig(os.path.join(figs,'Fig3_estimator.png'), dpi=300)
fig.savefig(os.path.join(sub,'Fig3.pdf')); fig.savefig(os.path.join(sub,'Fig3.tif'), dpi=600, pil_kwargs={'compression':'tiff_lzw'})
print('ok')