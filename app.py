""" Single-file Flask app that serves a stylish image panel (HTML/CSS/JS embedded via render_template_string). Save as app.py and run with python app.py after installing Flask.

Requirements: pip install flask

Usage: python app.py Open http://127.0.0.1:5000/ in your browser

This file keeps all HTML/CSS/JS in a template string so it's easy to run and modify. """ from flask import Flask, render_template_string, jsonify

app = Flask(name)

Sample image data (replace URLs or add your own)

IMAGES = [ { "title": "Aurora Lake", "desc": "Northern lights over a serene lake", "img": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "badge": "Featured" }, { "title": "Desert Dunes", "desc": "Golden sand dunes at sunset", "img": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "avatar": "https://images.unsplash.com/photo-1545996124-f6b83452b3d3?q=80&w=400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "badge": "New" }, { "title": "Misty Forest", "desc": "Fog rolling through tall pines", "img": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "badge": "Classic" }, { "title": "City Lights", "desc": "A neon city skyline at night", "img": "https://images.unsplash.com/photo-1499346030926-9a72daac6c63?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "avatar": "https://images.unsplash.com/photo-1545996124-f6b83452b3d3?q=80&w=400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "badge": "Trending" }, { "title": "Coastal Cliffs", "desc": "Waves crashing against rugged cliffs", "img": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "badge": "Popular" }, { "title": "Snow Peaks", "desc": "Sunrise on the snowy mountain peaks", "img": "https://images.unsplash.com/photo-1444090542259-0af8fa96557e?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "avatar": "https://images.unsplash.com/photo-1545996124-f6b83452b3d3?q=80&w=400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder", "badge": "Adventure" } ]

TEMPLATE = """ <!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Flask Stylish Image Panel</title>
  <style>
    /* Copy of the stylish CSS used in the single-file HTML version */
    :root{--bg:#0f1724;--card:#0b1220;--accent:#7c3aed;--muted:rgba(255,255,255,0.65);--glass: rgba(255,255,255,0.04);--gap:16px;--radius:16px;--max-width:1200px;--shadow: 0 6px 20px rgba(2,6,23,0.6);font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;}
    *{box-sizing:border-box}html,body{height:100%;}body{margin:0;padding:40px 20px;background:linear-gradient(180deg,var(--bg), #071025 60%);color: #fff;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;display:flex;justify-content:center;align-items:flex-start;gap:24px;min-height:100vh;} .wrap{width:100%;max-width:var(--max-width);margin:0 auto;} header{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:20px;} .title{display:flex;flex-direction:column;} h1{margin:0;font-size:1.35rem;letter-spacing:-0.02em} p.lead{margin:4px 0 0;color:var(--muted);font-size:0.95rem} .panel{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));border-radius:calc(var(--radius) + 6px);padding:18px;box-shadow:var(--shadow);border:1px solid rgba(255,255,255,0.03);backdrop-filter: blur(6px) saturate(120%);} .controls{display:flex;gap:12px;align-items:center} .btn{background:var(--glass);border:1px solid rgba(255,255,255,0.03);padding:8px 12px;border-radius:10px;color:var(--muted);font-weight:600;font-size:0.92rem;cursor:pointer;transition:all .18s ease;} .btn:hover{transform:translateY(-3px);box-shadow:0 8px 20px rgba(0,0,0,0.5)} .grid{display:grid;grid-template-columns: repeat(3, 1fr);gap:var(--gap);margin-top:16px;} @media (max-width:980px){.grid{grid-template-columns:repeat(2,1fr)}} @media (max-width:600px){.grid{grid-template-columns:1fr}header{flex-direction:column;align-items:flex-start}} .card{position:relative;height:260px;overflow:hidden;border-radius:var(--radius);background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(0,0,0,0.12));cursor:zoom-in;transition:transform .35s cubic-bezier(.2,.9,.2,1), box-shadow .25s;border:1px solid rgba(255,255,255,0.03);display:flex;align-items:flex-end;justify-content:flex-start;} .card:hover{transform:translateY(-8px) scale(1.02);box-shadow:0 18px 40px rgba(2,6,23,0.7)} .card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;transition:transform .6s ease;transform-origin:center center;} .card:hover img{transform:scale(1.1)} .meta{position:relative;z-index:2;padding:14px;background:linear-gradient(180deg, rgba(0,0,0,0.0), rgba(0,0,0,0.45));width:100%;display:flex;align-items:center;gap:10px;} .avatar{width:44px;height:44px;border-radius:10px;overflow:hidden;border:1px solid rgba(255,255,255,0.06)} .avatar img{width:100%;height:100%;object-fit:cover} .info{flex:1} .info .name{font-weight:700} .info .desc{font-size:0.85rem;color:var(--muted);margin-top:4px} .badge{background:linear-gradient(90deg, rgba(124,58,237,0.14), rgba(59,130,246,0.08));color:var(--accent);padding:6px 10px;border-radius:999px;font-weight:700;font-size:0.85rem;border:1px solid rgba(124,58,237,0.12)} .overlay {position:absolute;inset:0;display:flex;align-items:flex-start;justify-content:flex-end;padding:12px;gap:8px;z-index:3;} .icon{background:rgba(0,0,0,0.4);backdrop-filter:blur(6px);padding:8px;border-radius:10px;border:1px solid rgba(255,255,255,0.04);cursor:pointer;display:inline-flex;align-items:center;justify-content:center;} .lightbox{position:fixed;inset:0;display:none;align-items:center;justify-content:center;background:rgba(1,2,6,0.72);z-index:9999;padding:28px} .lightbox.open{display:flex} .lightbox .viewer{max-width:1200px;width:100%;max-height:90vh;overflow:hidden;border-radius:12px;box-shadow:0 30px 80px rgba(2,6,23,0.9);} .viewer img{width:100%;height:auto;display:block} .lightbox .caption{padding:12px 16px;background:#05131f;color:var(--muted);font-size:0.95rem} .closeBtn{position:absolute;top:18px;right:18px;background:transparent;border:0;color:#fff;font-size:20px;cursor:pointer} .card:focus{outline:3px solid rgba(124,58,237,0.18);outline-offset:4px}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="title">
        <h1>Flask Stylish Image Panel</h1>
        <p class="lead">Responsive image grid with hover effects, captions and a lightweight lightbox — powered by Flask.</p>
      </div>
      <div class="controls">
        <button class="btn" onclick="shuffleGrid()">Shuffle</button>
        <button class="btn" onclick="toggleCols()">Toggle Columns</button>
      </div>
    </header><section class="panel">
  <div class="grid" id="grid">
    {%- for item in images %}
    <article class="card" tabindex="0" data-title="{{ item.title }}" data-desc="{{ item.desc }}" data-src="{{ item.img }}">
      <img src="{{ item.img }}" alt="{{ item.title }}">
      <div class="overlay">
        <div class="icon" title="Like">❤</div>
        <div class="icon" title="Open">🔍</div>
      </div>
      <div class="meta">
        <div class="avatar"><img src="{{ item.avatar }}" alt="avatar"></div>
        <div class="info">
          <div class="name">{{ item.title }}</div>
          <div class="desc">{{ item.desc }}</div>
        </div>
        <div class="badge">{{ item.badge }}</div>
      </div>
    </article>
    {%- endfor %}
  </div>
</section>

  </div>  <!-- Lightbox -->  <div class="lightbox" id="lightbox" aria-hidden="true">
    <button class="closeBtn" onclick="closeLightbox()" aria-label="Close">✕</button>
    <div class="viewer" id="viewer">
      <img src="" alt="" id="viewerImg">
      <div class="caption" id="viewerCaption"></div>
    </div>
  </div>  <script>
    const grid = document.getElementById('grid');
    const lightbox = document.getElementById('lightbox');
    const viewerImg = document.getElementById('viewerImg');
    const viewerCaption = document.getElementById('viewerCaption');

    function openLightbox(src, title, desc){
      viewerImg.src = src;
      viewerImg.alt = title || desc || 'Image';
      viewerCaption.textContent = title ? (title + ' — ' + desc) : desc;
      lightbox.classList.add('open');
      lightbox.setAttribute('aria-hidden','false');
      document.body.style.overflow = 'hidden';
    }
    function closeLightbox(){
      lightbox.classList.remove('open');
      lightbox.setAttribute('aria-hidden','true');
      viewerImg.src = '';
      document.body.style.overflow = '';
    }

    grid.addEventListener('click', (e)=>{
      const card = e.target.closest('.card');
      if(!card) return;
      const src = card.getAttribute('data-src') || card.querySelector('img')?.src;
      const title = card.getAttribute('data-title');
      const desc = card.getAttribute('data-desc');
      openLightbox(src, title, desc);
    });

    grid.addEventListener('keydown', (e)=>{
      if(e.key === 'Enter'){
        const card = e.target.closest('.card');
        if(!card) return;
        const src = card.getAttribute('data-src') || card.querySelector('img')?.src;
        const title = card.getAttribute('data-title');
        const desc = card.getAttribute('data-desc');
        openLightbox(src, title, desc);
      }
    });

    document.addEventListener('keydown',(e)=>{ if(e.key === 'Escape') closeLightbox(); });
    lightbox.addEventListener('click',(e)=>{ if(e.target === lightbox) closeLightbox(); });

    function shuffleGrid(){
      const items = Array.from(grid.children);
      for(let i = items.length -1; i>0; i--){
        const j = Math.floor(Math.random()*(i+1));
        grid.insertBefore(items[j], items[i]);
      }
    }
    function toggleCols(){
      const style = getComputedStyle(grid);
      const cols = style.gridTemplateColumns.split(' ').length;
      if(cols === 3) grid.style.gridTemplateColumns = 'repeat(2, 1fr)';
      else if(cols === 2) grid.style.gridTemplateColumns = 'repeat(1, 1fr)';
      else grid.style.gridTemplateColumns = '';
    }
  </script></body>
</html>
"""@app.route('/') def index(): return render_template_string(TEMPLATE, images=IMAGES)

@app.route('/api/images') def api_images(): return jsonify(IMAGES)

if name == 'main': app.run(debug=True)

