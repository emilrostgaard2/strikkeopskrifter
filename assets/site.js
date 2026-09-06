// Garnberegner – bruges på opskriftssider.
// Siden definerer window.OPSKRIFT = { sizes, defaultSize, yarns:{ key:{ name, garn:<slug i data/priser.json>, perBall, grams[], shops:[…fallback] } } }
// Hvis data/priser.json findes, erstattes shops med dagens priser fra feeds (kørt af _build/feeds.py).
(function(){
  const O = window.OPSKRIFT; if(!O) return;
  const ROOT = document.querySelector('script[src*="assets/site.js"]').getAttribute('src').replace('assets/site.js','');
  let size = O.defaultSize ?? 2, yarn = Object.keys(O.yarns)[0], priser = null;
  const dk = n => n.toLocaleString('da-DK');
  const kr = n => n.toFixed(2).replace('.',',');

  // Skift antal i et kurv-deeplink (Shopify ":1" / Woo "quantity=1" inde i htmlurl=)
  const withQty = (url, q) => url
    .replace(/(%3A|:)1(?=(&|$))/, `$1${q}`)
    .replace(/quantity(%3D|=)1(?=(%26|&|$))/, `quantity$1${q}`);

  function shopsFor(y){
    const g = priser && y.garn && priser[y.garn];
    if(!g) return y.shops || [];
    return Object.values(g.shops).filter(s=>s.price).map(s=>{
      const v = s.variants.find(v=>v.stock==='in_stock' && v.cart) || s.variants.find(v=>v.cart);
      const note = [s.free_shipping_from ? `Fri fragt over ${s.free_shipping_from} kr.` : (s.shipping ? `Fragt ${kr(s.shipping)} kr.` : ''),
                    s.colors_in_stock ? `${s.colors_in_stock} farver på lager` : ''].filter(Boolean).join(' · ');
      return { s:s.shop, n:note, p:s.price, url:s.url, cart: v ? v.cart : null };
    });
  }

  function render(){
    for (const k in O.yarns){
      const y=O.yarns[k], g=y.grams[size], balls=Math.ceil(g/y.perBall);
      const el=document.querySelector(`[data-amt="${k}"]`);
      if(el) el.innerHTML=`${g} g<small>${balls} nøgler</small>`;
    }
    const y=O.yarns[yarn], g=y.grams[size], balls=Math.ceil(g/y.perBall);
    document.getElementById('cmp-title').textContent=`${y.name} til str. ${O.sizes[size]} – ${balls} nøgler`;
    const list=shopsFor(y).map(s=>({...s,total:Math.round(s.p*balls)})).sort((a,b)=>a.total-b.total);
    document.getElementById('shops').innerHTML = list.length ? list.map((s,i)=>`
      <div class="shop ${i===0?'best':''}">
        <div class="name">${s.s}<small>${s.n} · ${kr(s.p)} kr. pr. nøgle</small></div>
        <div class="price">${dk(s.total)} kr.<small>${balls} × ${kr(s.p)}</small></div>
        <a class="go" href="${s.cart ? withQty(s.cart, balls) : s.url}" rel="sponsored nofollow" target="_blank">${s.cart?'Læg i kurven':'Gå til '+s.s}</a>
      </div>`).join('') : '<p class="muted small">Ingen aktuelle priser på dette garn endnu.</p>';
  }
  document.querySelectorAll('.sizes button').forEach(b=>b.addEventListener('click',()=>{
    document.querySelectorAll('.sizes button').forEach(x=>x.setAttribute('aria-pressed','false'));
    b.setAttribute('aria-pressed','true'); size=+b.dataset.i; render();
  }));
  document.querySelectorAll('input[name="yarn"]').forEach(r=>r.addEventListener('change',e=>{yarn=e.target.value;render();}));
  render();
  fetch(ROOT+'data/priser.json').then(r=>r.ok?r.json():null).then(d=>{ if(d){ priser=d; render(); } }).catch(()=>{});
})();

// ---- Hydrering fra data/priser.json (garn-kort, garnsider) ----
(function(){
  const s = document.querySelector('script[src*="assets/site.js"]'); if(!s) return;
  const ROOT = s.getAttribute('src').replace('assets/site.js','');
  const kr = n => n.toFixed(2).replace('.',',');
  fetch(ROOT+'data/priser.json').then(r=>r.ok?r.json():null).then(P=>{
    if(!P) return;
    // Kort: <a class="card" data-garn="drops-baby-merino"> – fylder .img med billede og .price med fra-pris
    document.querySelectorAll('[data-garn]').forEach(el=>{
      const g=P[el.dataset.garn]; if(!g) return;
      const shop=Object.values(g.shops)[0]; if(!shop) return;
      const img=el.querySelector('.img');
      if(img && shop.image){ img.style.background=`center/cover url("${shop.image}")`; img.setAttribute('role','img'); img.setAttribute('aria-label',g.name); }
      const price=el.querySelector('.price');
      if(price && g.from_price){
        const disc = shop.old_price ? Math.round((1-shop.price/shop.old_price)*100) : 0;
        price.innerHTML=`fra ${kr(g.from_price)} kr.${disc>=10?` <span class="tag save">−${disc} %</span>`:''}`;
      }
      const n=el.querySelector('[data-shops]'); if(n) n.textContent=`${Object.keys(g.shops).length} butik${Object.keys(g.shops).length===1?'':'ker'}`;
    });
    // Garnside: <div id="garn-shops" data-garn="…"> – fuld butiksliste
    const box=document.getElementById('garn-shops');
    if(box && P[box.dataset.garn]){
      const g=P[box.dataset.garn];
      box.innerHTML=Object.values(g.shops).filter(x=>x.price).map((x,i)=>{
        const v=x.variants.find(v=>v.stock==='in_stock'&&v.cart)||x.variants.find(v=>v.cart);
        const note=[x.free_shipping_from?`Fri fragt over ${x.free_shipping_from} kr.`:'', x.colors_in_stock?`${x.colors_in_stock} farver på lager`:''].filter(Boolean).join(' · ');
        return `<div class="shop ${i===0?'best':''}"><div class="name">${x.shop}<small>${note}</small></div>
          <div class="price">${kr(x.price)} kr.${x.old_price?`<small><s>${kr(x.old_price)} kr.</s></small>`:''}</div>
          <a class="go" href="${v?v.cart:x.url}" rel="sponsored nofollow" target="_blank">${v?'Læg i kurven':'Gå til butik'}</a></div>`;
      }).join('') || '<p class="muted small">Ingen priser endnu.</p>';
      const from=document.getElementById('garn-from'); if(from&&g.from_price) from.firstChild.textContent=`fra ${kr(g.from_price)} kr. `;
      const hero=document.getElementById('garn-img'); const shop=Object.values(g.shops)[0];
      if(hero&&shop&&shop.image) hero.style.background=`center/cover url("${shop.image}")`;
      // Farvekort
      const sw=document.getElementById('garn-colors');
      if(sw&&shop){ sw.innerHTML=shop.variants.filter(v=>v.image).slice(0,24).map(v=>`<a href="${v.cart||v.url}" rel="sponsored nofollow" target="_blank" title="${v.nr} ${v.color}${v.stock!=='in_stock'?' (udsolgt)':''}" style="aspect-ratio:1;background:center/cover url('${v.image}');border:1px solid var(--line);display:block;${v.stock!=='in_stock'?'opacity:.35':''}"></a>`).join(''); }
    }
  }).catch(()=>{});
})();

// ---- Opskriftsoversigt fra data/opskrifter.json ----
(function(){
  const grid=document.getElementById('opskrift-grid'); if(!grid) return;
  const s=document.querySelector('script[src*="assets/site.js"]'); const ROOT=s.getAttribute('src').replace('assets/site.js','');
  const kr=n=>n.toLocaleString('da-DK');
  const q=document.getElementById('f-q'), cat=document.getElementById('f-kat'), des=document.getElementById('f-des'), sort=document.getElementById('f-sort'), count=document.getElementById('f-count');
  const params=new URLSearchParams(location.search);
  if(params.get('q')) q.value=params.get('q'); if(params.get('kategori')) cat.value=params.get('kategori');
  let ALL=[];
  const fixed=[...grid.querySelectorAll('.card')].map(c=>c.outerHTML); // egne opskriftssider (håndskrevne) står altid først
  function render(){
    let list=ALL.filter(o=>o.image);
    const t=(q.value||'').toLowerCase().trim();
    if(t) list=list.filter(o=>(o.name+' '+o.designer+' '+(o.desc||'')).toLowerCase().includes(t));
    if(cat.value) list=list.filter(o=>o.type===cat.value);
    if(des.value) list=list.filter(o=>o.designer===des.value);
    if(sort.value==='pris') list.sort((a,b)=>(a.price||9e9)-(b.price||9e9));
    if(sort.value==='navn') list.sort((a,b)=>a.name.localeCompare(b.name,'da'));
    count.textContent=`${list.length} opskrifter`;
    grid.innerHTML=(t||cat.value||des.value?'':fixed.join(''))+list.slice(0,200).map(o=>`
      <a class="card" href="${o.url}" rel="sponsored nofollow" target="_blank">
        <div class="img" role="img" aria-label="${o.name}" style="background:center/cover url('${o.image}')"></div>
        <b>${o.name}</b><span>${o.designer}${o.sizes?' · '+o.sizes:''}${o.kind==='pakke'?' · gratis opskrift':''}</span>
        <em class="price">${o.kind==='pakke'?'Garnpakke '+kr(o.price)+' kr.':'Opskrift '+kr(o.price)+' kr.'}</em>
      </a>`).join('');
  }
  fetch(ROOT+'data/opskrifter.json').then(r=>r.json()).then(d=>{
    ALL=d;
    [...new Set(d.map(o=>o.designer).filter(Boolean))].sort().forEach(x=>des.insertAdjacentHTML('beforeend',`<option value="${x}">${x}</option>`));
    render();
  });
  [q,cat,des,sort].forEach(el=>el.addEventListener('input',render));
})();

// ---- Forside: fyld opskrift-kort med rigtige opskrifter ----
(function(){
  const cards=[...document.querySelectorAll('[data-opskrift]')]; if(!cards.length) return;
  const s=document.querySelector('script[src*="assets/site.js"]'); const ROOT=s.getAttribute('src').replace('assets/site.js','');
  fetch(ROOT+'data/opskrifter.json').then(r=>r.json()).then(d=>{
    const pick=['sweater','cardigan','hue'].map(t=>d.find(o=>o.type===t&&o.image&&o.kind==='pakke'));
    cards.forEach((c,i)=>{ const o=pick[i]; if(!o) return;
      c.href=o.url; c.rel='sponsored nofollow'; c.target='_blank';
      c.querySelector('.img').style.background=`center/cover url('${o.image}')`;
      c.querySelector('b').textContent=o.name; c.querySelector('span').textContent=`${o.designer} · gratis opskrift`;
      c.querySelector('.price').textContent=`Garnpakke ${o.price.toLocaleString('da-DK')} kr.`; });
  });
})();
