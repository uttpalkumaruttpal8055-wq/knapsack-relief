"""Portable SVG figures; no plotting dependency required for fallback checks."""
import math
from html import escape
from pathlib import Path
import numpy as np
from .qaoa import probabilities
from .problem import energies

def svg(path, title, body):
    Path(path).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="900" height="560" viewBox="0 0 900 560">'
        '<rect width="900" height="560" fill="#101f30"/>'
        '<style>text{fill:#e6f4ff;font-family:Arial;font-size:16px}</style>'
        f'<text x="30" y="35" font-size="22">{escape(title)}</text>'+body+'</svg>',encoding='utf-8')

def topology(config, path):
    n = config['num_qubits']
    pos = [(450+210*math.cos(2*math.pi*i/n),285+210*math.sin(2*math.pi*i/n)) for i in range(n)]
    body = ''
    for a,b in config['undirected_edges']:
        x,y=pos[a]; xx,yy=pos[b]
        body += f'<line x1="{x}" y1="{y}" x2="{xx}" y2="{yy}" stroke="#5faeb5" stroke-width="3"/>'
    for i,(x,y) in enumerate(pos):
        body += f'<circle cx="{x}" cy="{y}" r="23" fill="#23546a"/><text x="{x-5}" y="{y+6}">{i}</text>'
    svg(path, f"Processor {config['name']}: {n} qubits, {len(config['undirected_edges'])} edges",body)

def landscape(path, encoding='hinge'):
    e=energies(encoding)
    g=np.linspace(0,2*np.pi,61); b=np.linspace(0,np.pi,41)
    grid=np.array([[probabilities(gg,bb,encoding)@e for gg in g] for bb in b])
    lo,hi=float(grid.min()),float(grid.max())
    body=''
    for y in range(len(b)):
        for x in range(len(g)):
            t=(grid[y,x]-lo)/(hi-lo)
            color=f'#{int(40+185*t):02x}{int(195-140*t):02x}{int(180-100*t):02x}'
            body+=f'<rect x="{100+x*11}" y="{70+y*9}" width="11" height="9" fill="{color}"/>'
    body+='<text x="260" y="490">gamma: 0 to 2*pi (raw integer cost)</text><text x="30" y="530">beta: 0 to pi; lower expected cost is better. Grid is illustrative, optimization uses multistart search.</text>'
    svg(path,f'p=1 QAOA cost landscape ({encoding}); range {lo:.2f} to {hi:.2f}',body)
    return dict(gamma=g.tolist(),beta=b.tolist(),expected_cost=grid.tolist())

def comparison(rows,path):
    fields=['depth','cx_count','routing_swaps']
    body=''
    for k,field in enumerate(fields):
        top=max([r[field] for r in rows]+[1])
        for j,r in enumerate(rows):
            y=85+k*145+j*30
            width=480*r[field]/top
            label=f"{r['processor']} / {r['encoding']} {r['mode']}"
            body+=f'<text x="20" y="{y+17}">{escape(label)}</text><rect x="305" y="{y}" width="{width}" height="21" fill="#6edace"/><text x="{315+width}" y="{y+17}">{r[field]}</text>'
        body+=f'<text x="305" y="{70+k*145}">{field}</text>'
    svg(path,'Measured Qiskit routing costs (ideal/noisy use same circuit)',body)
