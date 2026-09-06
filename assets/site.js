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
