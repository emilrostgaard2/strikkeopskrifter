// Garnberegner – bruges på opskriftssider.
// Siden definerer window.OPSKRIFT = { sizes, yarns:{key:{name,grams[],perBall,shops:[{s,n,p,url}]}} }
(function(){
  const O = window.OPSKRIFT; if(!O) return;
  let size = O.defaultSize ?? 2, yarn = Object.keys(O.yarns)[0];
  const dk = n => n.toLocaleString('da-DK');
  const kr = n => n.toFixed(2).replace('.',',');

  function render(){
    for (const k in O.yarns){
      const y=O.yarns[k], g=y.grams[size], balls=Math.ceil(g/y.perBall);
      const el=document.querySelector(`[data-amt="${k}"]`);
      if(el) el.innerHTML=`${g} g<small>${balls} nøgler</small>`;
    }
    const y=O.yarns[yarn], g=y.grams[size], balls=Math.ceil(g/y.perBall);
    document.getElementById('cmp-title').textContent=`${y.name} til str. ${O.sizes[size]} – ${balls} nøgler`;
    const list=y.shops.map(s=>({...s,total:Math.round(s.p*balls)})).sort((a,b)=>a.total-b.total);
    document.getElementById('shops').innerHTML=list.map((s,i)=>`
      <div class="shop ${i===0?'best':''}">
        <div class="name">${s.s}<small>${s.n} · ${kr(s.p)} kr. pr. nøgle</small></div>
        <div class="price">${dk(s.total)} kr.<small>${balls} × ${kr(s.p)}</small></div>
        <a class="go" href="${s.url||'#'}" rel="sponsored nofollow" target="_blank">${s.cart?'Læg i kurven':'Gå til '+s.s}</a>
      </div>`).join('');
  }
  document.querySelectorAll('.sizes button').forEach(b=>b.addEventListener('click',()=>{
    document.querySelectorAll('.sizes button').forEach(x=>x.setAttribute('aria-pressed','false'));
    b.setAttribute('aria-pressed','true'); size=+b.dataset.i; render();
  }));
  document.querySelectorAll('input[name="yarn"]').forEach(r=>r.addEventListener('change',e=>{yarn=e.target.value;render();}));
  render();
})();
