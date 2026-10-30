# -*- coding: utf-8 -*-
"""构建 ai-costume-gallery-cn 站点

产出：
  index.html                单文件画廊（数据内嵌，file:// 可直接打开）
  data/costume-zh.json      中文记录（供复用/校对）
  data/meta.json            分类 / 标签元数据
  data/translations.csv     日⇄中 + 英⇄中 对照表
  robots.txt / sitemap.xml / 404.html

用法：
  SITE_URL=https://your-domain.com python build_gallery.py
"""
import json, os, sys, csv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from translations import CAT_ZH, TAG_ZH, TAG_JA, TAG_GROUPS, UI

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(root, "manifest.json"), encoding="utf-8"))

# 站点地址：部署前用环境变量覆盖，否则 canonical / sitemap 会指向占位域名
SITE_URL = os.environ.get("SITE_URL", "https://example.com").rstrip("/")

CAT_ORDER = ["春", "夏", "秋", "冬", "ランジェリー", "セクシー", "水着", "パーティ"]

items = []
for r in rows:
    items.append({
        "i": r["id"],
        "c": r["分类"],
        "t": r["标签"],
        "th": r["thumb_path"],
        "im": r["img_path"],
        "pg": r["png_path"],
    })

cats = [c for c in CAT_ORDER if any(x["c"] == c for x in items)]
groups = [{"k": k, "ja": ja, "zh": zh, "tags": ts} for k, ja, zh, ts in TAG_GROUPS]

payload = json.dumps({
    "items": items, "cats": cats, "groups": groups,
    "catZh": CAT_ZH, "tagZh": TAG_ZH, "tagJa": TAG_JA, "ui": UI,
}, ensure_ascii=False, separators=(",", ":"))

html = r"""<!doctype html>
<html lang="zh-CN" data-theme="light" data-lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>服装集 COSTUME-DB-01 · 离线索引</title>
<meta name="description" content="AI 绘画服装参考图库中文版：1407 件服装、8 个分类、86 个材质与单品标签，可按颜色・单品・鞋袜・配饰・材质・长度分面筛选，支持中日双语与浅深主题。">
<meta name="keywords" content="AI服装参考,服装图库,穿搭参考,绘画参考,服装设计,服装タグ,costume reference">
<meta name="author" content="Brilliant666">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="__SITE__/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="服装集 COSTUME-DB-01">
<meta property="og:title" content="服装集 COSTUME-DB-01 · 1407 件服装 / 86 个标签">
<meta property="og:description" content="AI 绘画服装参考图库中文版。按颜色・单品・鞋袜・配饰・材质・长度六组分面筛选。">
<meta property="og:url" content="__SITE__/">
<meta property="og:image" content="__SITE__/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="zh_CN">
<meta property="og:locale:alternate" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="服装集 COSTUME-DB-01 · 1407 件服装">
<meta name="twitter:description" content="AI 绘画服装参考图库中文版，按材质・颜色・单品标签分面筛选。">
<meta name="twitter:image" content="__SITE__/og-cover.jpg">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%238fb4ff'/%3E%3Ctext x='16' y='23' font-size='19' font-family='sans-serif' font-weight='700' text-anchor='middle' fill='%230d0f12'%3EC%3C/text%3E%3C/svg%3E">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ImageGallery","name":"服装集 COSTUME-DB-01","alternateName":"AI Costume Gallery 中文版","url":"__SITE__/","inLanguage":["zh-CN","ja"],"numberOfItems":4221,"about":"AI 绘画・服装设计・穿搭参考","isAccessibleForFree":true,"creator":{"@type":"Person","name":"ギア","url":"https://x.com/giaaibusi"}}
</script>
<script>
(function(){
  try{
    var t=localStorage.getItem('cg.theme'); if(t==='light'||t==='dark') document.documentElement.dataset.theme=t;
    var l=localStorage.getItem('cg.lang');  if(l==='ja'||l==='zh')      document.documentElement.dataset.lang=l;
  }catch(e){}
})();
</script>
<style>
:root{
  --r:14px;
  --f:system-ui,-apple-system,"Segoe UI","Hiragino Sans","Noto Sans SC","Microsoft YaHei",sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --imgbg:#e9e9e7;
}
html[data-theme="dark"]{
  --bg:#0d0f12;--bg2:#14171c;--panel:#1a1e24;--line:#272c34;--line2:#343a44;
  --tx:#e9ecf1;--tx2:#a3abb8;--tx3:#6c7482;
  --ac:#8fb4ff;--ac2:#c3d5ff;--on-ac:#0b1220;
  --hover:#232831;--hover-border:#3b4350;
  --sh:0 10px 30px rgba(0,0,0,.45);
  --tools-bg:rgba(13,15,18,.86);
  --title-grad:linear-gradient(90deg,var(--ac2),#e3c8ff);
  --scrim:rgba(5,6,8,.9);
  --badge-bg:rgba(13,15,18,.78);
  --glow1:#1b2433;--glow2:#211a2b;
  --close-border:#5a6270;
  --nav-bg:rgba(13,15,18,.68);--nav-bg-h:rgba(13,15,18,.9);
  --panel-sh:0 18px 44px rgba(0,0,0,.55);
}
html[data-theme="light"]{
  --bg:#f4f6f9;--bg2:#ffffff;--panel:#ffffff;--line:#e3e7ed;--line2:#ccd4e0;
  --tx:#16191f;--tx2:#525b6a;--tx3:#8a93a3;
  --ac:#2563eb;--ac2:#1e40af;--on-ac:#ffffff;
  --hover:#eef1f6;--hover-border:#b9c3d2;
  --sh:0 8px 24px rgba(16,24,40,.10);
  --tools-bg:rgba(255,255,255,.9);
  --title-grad:linear-gradient(90deg,#2563eb,#7c3aed);
  --scrim:rgba(15,23,42,.55);
  --badge-bg:rgba(22,25,31,.78);
  --glow1:#e6eefc;--glow2:#f0e9fb;
  --close-border:#b9c3d2;
  --nav-bg:rgba(22,25,31,.62);--nav-bg-h:rgba(22,25,31,.88);
  --panel-sh:0 18px 44px rgba(16,24,40,.18);
}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--bg);color:var(--tx);font-family:var(--f);-webkit-font-smoothing:antialiased;min-height:100vh;
  background-image:radial-gradient(1200px 500px at 15% -10%,var(--glow1) 0,transparent 60%),
                   radial-gradient(900px 400px at 100% 0,var(--glow2) 0,transparent 55%);
  transition:background-color .22s ease,color .22s ease}
button,select,input{font:inherit;color:inherit}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-thumb{background:var(--line2);border-radius:6px}
::-webkit-scrollbar-track{background:transparent}

/* hero */
.hero{padding:34px clamp(16px,4vw,48px) 18px;max-width:1680px;margin:0 auto}
.eyebrow{font-size:11.5px;letter-spacing:.22em;color:var(--tx3);text-transform:uppercase}
.hero h1{margin:8px 0 6px;font-size:clamp(25px,3.4vw,38px);font-weight:700;letter-spacing:.02em}
.hero h1 span{background:var(--title-grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero h1 em{font-style:normal}
.sub{color:var(--tx2);font-size:13.5px;margin:0;line-height:1.75;max-width:860px}
.sub p{margin:0}
.stats{display:flex;gap:26px;margin-top:18px;flex-wrap:wrap}
.stats div{display:flex;flex-direction:column;gap:2px}
.stats b{font-size:20px;font-weight:700;font-variant-numeric:tabular-nums}
.stats span{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--tx3)}

/* tools */
.tools{position:sticky;top:0;z-index:30;background:var(--tools-bg);backdrop-filter:blur(14px);
  -webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--line);transition:background-color .22s ease}
.tools-in{max-width:1680px;margin:0 auto;padding:10px clamp(16px,4vw,48px);position:relative}
.tabs{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.tabs::-webkit-scrollbar{display:none}
.tab{flex:0 0 auto;display:flex;align-items:center;gap:8px;height:36px;padding:0 15px;border:1px solid var(--line2);
  border-radius:10px;background:transparent;color:var(--tx2);font-size:13px;cursor:pointer;white-space:nowrap;transition:.15s}
.tab:hover{background:var(--hover);color:var(--tx)}
.tab[aria-selected="true"]{background:var(--ac);border-color:var(--ac);color:var(--on-ac);font-weight:700}
.tab .n{font-size:11px;opacity:.62;font-variant-numeric:tabular-nums}
.tab[aria-selected="true"] .n{opacity:.8}
.row2{display:flex;align-items:center;gap:10px;margin-top:10px;flex-wrap:wrap}
.search{position:relative;display:flex;align-items:center}
.search svg{position:absolute;left:11px;color:var(--tx3);pointer-events:none}
.search input{width:260px;height:36px;padding:0 12px 0 34px;border:1px solid var(--line2);border-radius:10px;
  background:var(--bg2);font-size:13px;outline:none;transition:.15s}
.search input::placeholder{color:var(--tx3)}
.search input:focus{border-color:var(--ac);box-shadow:0 0 0 3px color-mix(in srgb,var(--ac) 18%,transparent)}
.ftog{height:36px;padding:0 13px;display:flex;align-items:center;gap:7px;border:1px solid var(--line2);
  border-radius:10px;background:transparent;color:var(--tx2);font-size:13px;cursor:pointer;transition:.15s;white-space:nowrap}
.ftog:hover{background:var(--hover);color:var(--tx)}
.ftog[aria-expanded="true"]{border-color:var(--ac);color:var(--ac);background:var(--hover)}
.ftog b{font-size:11px;min-width:16px;height:16px;display:none;align-items:center;justify-content:center;
  border-radius:8px;background:var(--ac);color:var(--on-ac);font-weight:700;padding:0 4px}
.ftog b.on{display:inline-flex}
.count{margin-left:auto;font-size:12.5px;color:var(--tx3);font-variant-numeric:tabular-nums;white-space:nowrap}
.count b{color:var(--tx);font-weight:700}

/* 开关组 */
.switches{display:flex;gap:8px;align-items:center}
.switch{display:flex;border:1px solid var(--line2);border-radius:10px;overflow:hidden;background:var(--bg2)}
.switch button{height:34px;min-width:34px;padding:0 9px;border:0;background:transparent;color:var(--tx2);
  font-size:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:5px;transition:.13s;white-space:nowrap}
.switch button+button{border-left:1px solid var(--line2)}
.switch button:hover{background:var(--hover);color:var(--tx)}
.switch button[aria-pressed="true"]{background:var(--ac);color:var(--on-ac);font-weight:700}
.switch svg{width:14px;height:14px;display:block}

/* 筛选面板 */
.fpanel{position:absolute;left:clamp(16px,4vw,48px);right:clamp(16px,4vw,48px);top:calc(100% - 6px);
  z-index:40;background:var(--panel);border:1px solid var(--line2);border-radius:16px;box-shadow:var(--panel-sh);
  padding:16px 18px 18px;display:none;max-height:min(68vh,620px);overflow:auto}
.fpanel.open{display:block}
.fp-top{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin-bottom:14px;
  padding-bottom:13px;border-bottom:1px solid var(--line)}
select{height:36px;padding:0 30px 0 11px;border:1px solid var(--line2);border-radius:10px;background:var(--bg2);
  font-size:12.5px;cursor:pointer;outline:none;appearance:none;max-width:230px;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%238a93a3' stroke-width='2.5'><path d='m6 9 6 6 6-6'/></svg>");
  background-repeat:no-repeat;background-position:right 9px center}
select:focus{border-color:var(--ac)}
.btn-clear{margin-left:auto;height:34px;padding:0 13px;border:1px solid var(--line2);border-radius:9px;
  background:transparent;color:var(--tx2);font-size:12.5px;cursor:pointer;transition:.15s}
.btn-clear:hover{border-color:var(--ac);color:var(--ac)}
.tgrp{margin-bottom:14px}
.tgrp:last-child{margin-bottom:0}
.tgrp h4{margin:0 0 8px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--tx3);font-weight:700;
  display:flex;align-items:center;gap:8px}
.tgrp h4::after{content:'';flex:1;height:1px;background:var(--line)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{padding:5px 11px;border:1px solid var(--line2);border-radius:99px;background:var(--bg2);
  font-size:12px;color:var(--tx2);cursor:pointer;transition:.13s;white-space:nowrap}
.chip:hover{border-color:var(--ac);color:var(--ac)}
.chip[aria-pressed="true"]{background:var(--ac);border-color:var(--ac);color:var(--on-ac);font-weight:700}
.chip .c{opacity:.6;font-size:10.5px;margin-left:4px;font-variant-numeric:tabular-nums}

/* grid */
main{max-width:1680px;margin:0 auto;padding:22px clamp(16px,4vw,48px) 90px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;cursor:pointer;
  transition:transform .18s ease,box-shadow .18s ease,border-color .18s;outline:none;display:flex;flex-direction:column}
.card:hover,.card:focus-visible{transform:translateY(-4px);box-shadow:var(--sh);border-color:var(--hover-border)}
.card:focus-visible{box-shadow:0 0 0 2px var(--ac)}
.ph{position:relative;aspect-ratio:2/3;background:var(--imgbg);overflow:hidden}
.ph img{width:100%;height:100%;object-fit:contain;display:block}
/* 卡片图片渐显：加载完成前透明，避免硬切 */
.card img{opacity:0;transition:opacity .32s ease}
.card img.ld{opacity:1}
.badge{position:absolute;top:10px;left:10px;display:flex;gap:6px;flex-wrap:wrap}
.badge span{background:var(--badge-bg);color:#fff;font-size:10.5px;padding:3px 8px;border-radius:99px;
  backdrop-filter:blur(4px);font-variant-numeric:tabular-nums;letter-spacing:.03em}
.badge span.cat{background:var(--ac);color:var(--on-ac);font-weight:700}
.meta{padding:9px 12px;display:flex;align-items:center;justify-content:space-between;gap:8px}
.meta .mid{font-family:var(--mono);font-size:11px;color:var(--tx3);letter-spacing:.04em}
.meta .mcat{font-size:11px;color:var(--tx2);white-space:nowrap}
/* 标签改为悬停浮层，不占卡片高度 */
.tagbar{position:absolute;left:0;right:0;bottom:0;padding:26px 10px 9px;display:flex;flex-wrap:wrap;gap:4px;
  background:linear-gradient(transparent,rgba(8,10,14,.82));opacity:0;transition:opacity .18s ease;pointer-events:none}
.card:hover .tagbar,.card:focus-visible .tagbar{opacity:1}
.tagbar i{font-style:normal;font-size:10px;padding:2px 7px;border-radius:5px;
  background:rgba(255,255,255,.16);color:#fff;backdrop-filter:blur(3px);white-space:nowrap}
.meta .id{font-family:var(--mono);font-size:11px;color:var(--tx3);letter-spacing:.04em}
.tags{display:flex;flex-wrap:wrap;gap:4px;margin-top:auto}
.tags i{font-style:normal;font-size:10.5px;padding:2px 7px;border-radius:5px;background:var(--hover);color:var(--tx2);
  white-space:nowrap}
.tags i.more{background:transparent;color:var(--tx3);padding:2px 2px}
.empty{grid-column:1/-1;padding:90px 0;text-align:center;color:var(--tx3);font-size:14px;line-height:1.9}
/* 分页：与原站一致，每次追加一页 */
.loadmore{display:block;margin:34px auto 0;height:46px;padding:0 30px;border:1px solid var(--line2);
  border-radius:12px;background:var(--panel);color:var(--tx2);font-size:13.5px;cursor:pointer;transition:.15s}
.loadmore:hover{border-color:var(--ac);color:var(--ac)}
.loadmore[hidden]{display:none}
.empty b{display:block;color:var(--tx2);font-size:15px;margin-bottom:6px}

/* modal */
.modal{position:fixed;inset:0;z-index:60;background:var(--scrim);backdrop-filter:blur(6px);
  display:none;align-items:center;justify-content:center;padding:max(12px,env(safe-area-inset-top)) 12px}
.modal.open{display:flex}
.mbox{width:min(1180px,100%);max-height:100%;display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:18px;
  background:var(--bg2);border:1px solid var(--line);border-radius:18px;padding:16px;box-shadow:var(--sh)}
.mimg{position:relative;background:var(--imgbg);border-radius:12px;display:flex;align-items:center;
  justify-content:center;min-height:0;height:min(80vh,940px);overflow:hidden}
.mimg img{max-width:100%;max-height:100%;object-fit:contain;display:block}
.nav{position:absolute;top:50%;transform:translateY(-50%);width:54px;height:54px;border-radius:50%;border:0;
  background:var(--nav-bg);color:#fff;font-size:21px;cursor:pointer;transition:.15s;
  display:flex;align-items:center;justify-content:center;backdrop-filter:blur(4px)}
.nav:hover{background:var(--nav-bg-h)}
.nav.l{left:10px}.nav.r{right:10px}
.nav:disabled{opacity:.25;cursor:default}
.mside{display:flex;flex-direction:column;gap:14px;min-width:0;overflow:auto}
.mside .mid{font-family:var(--mono);font-size:12px;color:var(--tx3);word-break:break-all;letter-spacing:.04em}
.mkv{display:grid;grid-template-columns:auto 1fr;gap:7px 12px;margin:0;font-size:12.5px}
.mkv dt{color:var(--tx3);white-space:nowrap}
.mkv dd{margin:0;color:var(--tx);text-align:right}
.mtags{display:flex;flex-wrap:wrap;gap:5px}
.mtags button{font-size:11px;padding:4px 9px;border-radius:6px;border:1px solid var(--line2);background:var(--bg2);
  color:var(--tx2);cursor:pointer;transition:.13s}
.mtags button:hover{border-color:var(--ac);color:var(--ac)}
.macts{display:flex;flex-direction:column;gap:8px;margin-top:auto}
.macts a,.macts button{height:38px;display:flex;align-items:center;justify-content:center;border-radius:10px;
  border:1px solid var(--line2);background:var(--panel);color:var(--tx);font-size:13px;text-decoration:none;
  cursor:pointer;transition:.15s}
.macts a:hover,.macts button:hover{border-color:var(--ac);color:var(--ac)}
.mclose{position:absolute;top:14px;right:16px;width:50px;height:50px;border-radius:50%;border:1px solid var(--close-border);
  background:var(--panel);color:var(--tx);font-size:22px;cursor:pointer;z-index:2;transition:.15s;line-height:1}
.mclose:hover{background:var(--hover)}
.hint{font-size:11px;color:var(--tx3);line-height:1.7}
.hint kbd{font-family:var(--mono);font-size:10px;padding:1px 5px;border:1px solid var(--line2);border-radius:4px;
  background:var(--panel);color:var(--tx2)}
footer{max-width:1680px;margin:0 auto;padding:0 clamp(16px,4vw,48px) 60px;color:var(--tx3);font-size:12px;line-height:1.9}
footer a{color:var(--tx3)}
footer a:hover{color:var(--ac)}

@media(max-width:1080px){ .count{margin-left:0} .switches{margin-left:auto} }
@media(max-width:980px){
  .mbox{grid-template-columns:1fr;overflow:auto;padding:12px}
  .mimg{height:54vh}
  .mside{overflow:visible}
  .fpanel{left:8px;right:8px;padding:14px}
}
@media(max-width:560px){
  .grid{grid-template-columns:repeat(2,1fr);gap:10px}
  .meta{padding:9px 10px 11px}
  .tags i:nth-child(n+4){display:none}
  .search input{width:100%}
  .search{flex:1 1 100%}
  .switch button{padding:0 7px;font-size:11px}
  .chip{font-size:11px;padding:4px 9px}
}
</style>
</head>
<body>

<header class="hero">
  <div class="eyebrow" data-i18n="eyebrow">COSTUME-DB-01</div>
  <h1><span data-i18n="brand1">服装集</span> <em data-i18n="brand2">数据库</em></h1>
  <div class="sub"><p data-i18n="sub1"></p><p data-i18n="sub2" style="margin-top:6px"></p></div>
  <div class="stats">
    <div><b id="stItem">0</b><span data-i18n="statItem">服装</span></div>
    <div><b id="stImg">0</b><span data-i18n="statImg">图片</span></div>
    <div><b id="stCat">0</b><span data-i18n="statCat">分类</span></div>
    <div><b id="stTag">0</b><span data-i18n="statTag">标签</span></div>
  </div>
</header>

<div class="tools">
  <div class="tools-in">
    <div class="tabs" id="tabs" role="tablist"></div>
    <div class="row2">
      <label class="search">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <input id="q" type="search" autocomplete="off">
      </label>
      <button class="ftog" id="ftog" aria-expanded="false"><span data-i18n="filter">筛选</span><b id="fn"></b></button>
      <span class="count" id="count"></span>
      <div class="switches">
        <div class="switch" id="themeSw" role="group">
          <button data-t="light" title="Light" aria-label="Light">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/></svg>
          </button>
          <button data-t="dark" title="Dark" aria-label="Dark">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
          </button>
        </div>
        <div class="switch" id="langSw" role="group">
          <button data-l="zh">中文</button>
          <button data-l="ja">日本語</button>
        </div>
      </div>
    </div>

    <div class="fpanel" id="fpanel">
      <div class="fp-top">
        <select id="cat"></select>
        <select id="sort">
          <option value="cat" data-i18n="sortCat"></option>
          <option value="id" data-i18n="sortId"></option>
          <option value="tag" data-i18n="sortTag"></option>
        </select>
        <button class="btn-clear" id="clearTags" data-i18n="clearTags">清除全部标签</button>
      </div>
      <div id="tgrps"></div>
    </div>
  </div>
</div>

<main><div class="grid" id="grid"></div><button class="loadmore" id="more" hidden></button></main>

<footer id="foot"></footer>

<div class="modal" id="modal" role="dialog" aria-modal="true">
  <div class="mbox">
    <button class="mclose" id="mclose" aria-label="close">×</button>
    <div class="mimg">
      <img id="mimg" alt="">
      <button class="nav l" id="mprev" aria-label="prev">‹</button>
      <button class="nav r" id="mnext" aria-label="next">›</button>
    </div>
    <div class="mside">
      <div class="mid" id="mid"></div>
      <dl class="mkv" id="mkv"></dl>
      <div class="mtags" id="mtags"></div>
      <div class="macts">
        <a id="mfull" href="#" target="_blank" rel="noopener" data-i18n="openFull">打开原寸 PNG</a>
        <a id="mmid" href="#" target="_blank" rel="noopener" data-i18n="openMid">打开中图 WEBP</a>
        <button id="mcopy" data-i18n="copyPath">复制本地路径</button>
      </div>
      <div class="hint" id="mhint"></div>
    </div>
  </div>
</div>

<script>
const DB = __PAYLOAD__;
const ITEMS = DB.items, CATS = DB.cats, GROUPS = DB.groups;
const CZ = DB.catZh, TZ = DB.tagZh, TJ = DB.tagJa, UI = DB.ui;

const $ = s => document.querySelector(s);
const esc = s => String(s==null?'':s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

let LANG  = document.documentElement.dataset.lang  || 'zh';
let THEME = document.documentElement.dataset.theme || 'light';
const PAGE = 120;   // 与原站一致
const S = {cat:null, sort:'cat', q:'', tags:new Set(), n:PAGE};

const t = k => (UI[LANG] && UI[LANG][k]) || (UI.ja[k] || k);
const isZh = () => LANG === 'zh';
const nC = c => isZh() ? (CZ[c]||c) : c;
const nT = x => isZh() ? (TZ[x]||x) : (TJ[x]||x);
const gName = g => isZh() ? g.zh : g.ja;

/* ── 静态文案 ── */
function applyStatic(){
  document.documentElement.lang = isZh() ? 'zh-CN' : 'ja';
  document.title = t('title');
  document.querySelectorAll('[data-i18n]').forEach(el=>{ el.textContent = t(el.dataset.i18n); });
  $('#q').placeholder = t('search');
  $('#mhint').innerHTML = t('hint');
  $('#foot').innerHTML = t('footer');
  $('#stItem').textContent = ITEMS.length;
  $('#stImg').textContent = ITEMS.length * 3;
  $('#stCat').textContent = CATS.length;
  $('#stTag').textContent = Object.keys(TZ).length;
  document.querySelectorAll('#themeSw button').forEach(b=>b.setAttribute('aria-pressed', b.dataset.t===THEME?'true':'false'));
  document.querySelectorAll('#langSw button').forEach(b=>b.setAttribute('aria-pressed', b.dataset.l===LANG?'true':'false'));
}

/* ── 主题 / 语言 ── */
$('#themeSw').addEventListener('click', e=>{
  const b=e.target.closest('button'); if(!b) return;
  THEME = b.dataset.t;
  document.documentElement.dataset.theme = THEME;
  try{ localStorage.setItem('cg.theme', THEME); }catch(_){}
  applyStatic();
});
$('#langSw').addEventListener('click', e=>{
  const b=e.target.closest('button'); if(!b) return;
  LANG = b.dataset.l;
  document.documentElement.dataset.lang = LANG;
  try{ localStorage.setItem('cg.lang', LANG); }catch(_){}
  applyStatic(); drawTabs(); drawCatSel(); drawTagGroups(); draw();
  if($('#modal').classList.contains('open')) showM();
});

/* ── 系列 tabs ── */
function drawTabs(){
  const box=$('#tabs'); box.innerHTML='';
  const mk=(k,label,n)=>{
    const b=document.createElement('button');
    b.className='tab'; b.setAttribute('role','tab');
    b.setAttribute('aria-selected', S.cat===k?'true':'false');
    b.innerHTML='<span>'+esc(label)+'</span><span class="n">'+n+'</span>';
    b.onclick=()=>{ S.cat=k; drawTabs(); drawCatSel(); draw(); };
    box.appendChild(b);
  };
  mk(null, t('all'), ITEMS.length);
  CATS.forEach(c=>mk(c, nC(c), ITEMS.filter(x=>x.c===c).length));
}

function drawCatSel(){
  const sel=$('#cat'); sel.innerHTML='';
  const add=(v,label)=>{const o=document.createElement('option');o.value=v;o.textContent=label;sel.appendChild(o)};
  add('', t('catAll')+' ('+ITEMS.length+')');
  CATS.forEach(c=>add(c, nC(c)+' ('+ITEMS.filter(x=>x.c===c).length+')'));
  sel.value = S.cat||'';
}

/* ── 标签分面 ── */
function drawTagGroups(){
  const box=$('#tgrps'); box.innerHTML='';
  GROUPS.forEach(g=>{
    const avail = g.tags.filter(tg=>ITEMS.some(x=>x.t.includes(tg)));
    if(!avail.length) return;
    const wrap=document.createElement('div'); wrap.className='tgrp';
    const h=document.createElement('h4'); h.textContent=gName(g); wrap.appendChild(h);
    const chips=document.createElement('div'); chips.className='chips';
    avail.forEach(tg=>{
      const n = ITEMS.filter(x=>x.t.includes(tg)).length;
      const b=document.createElement('button');
      b.className='chip';
      b.title = tg;
      b.setAttribute('aria-pressed', S.tags.has(tg)?'true':'false');
      b.innerHTML = esc(nT(tg))+'<span class="c">'+n+'</span>';
      b.onclick=()=>{
        if(S.tags.has(tg)) S.tags.delete(tg); else S.tags.add(tg);
        b.setAttribute('aria-pressed', S.tags.has(tg)?'true':'false');
        draw();
      };
      chips.appendChild(b);
    });
    wrap.appendChild(chips);
    box.appendChild(wrap);
  });
}

/* ── 面板开合 ── */
const ftog=$('#ftog'), fpanel=$('#fpanel');
ftog.onclick=()=>{
  const o=fpanel.classList.toggle('open');
  ftog.setAttribute('aria-expanded', o?'true':'false');
};
document.addEventListener('click', e=>{
  if(!fpanel.classList.contains('open')) return;
  if(fpanel.contains(e.target) || ftog.contains(e.target)) return;
  fpanel.classList.remove('open');
  ftog.setAttribute('aria-expanded','false');
});
document.addEventListener('keydown', e=>{
  if(e.key==='Escape' && fpanel.classList.contains('open') && !$('#modal').classList.contains('open')){
    fpanel.classList.remove('open'); ftog.setAttribute('aria-expanded','false');
  }
});
$('#clearTags').onclick=()=>{ S.tags.clear(); drawTagGroups(); draw(); };
$('#cat').addEventListener('change', e=>{ S.cat=e.target.value||null; drawTabs(); draw(); });
$('#sort').addEventListener('change', e=>{ S.sort=e.target.value; draw(); });
let tid=null;
$('#q').addEventListener('input', e=>{
  clearTimeout(tid);
  tid=setTimeout(()=>{ S.q=e.target.value.trim().toLowerCase(); draw(); },130);
});

/* ── 过滤 ── */
function hit(x){
  if(S.cat && x.c!==S.cat) return false;
  for(const tg of S.tags) if(!x.t.includes(tg)) return false;
  if(S.q){
    const hay=(x.i+' '+x.c+' '+nC(x.c)+' '+x.t.join(' ')+' '+x.t.map(nT).join(' ')).toLowerCase();
    if(!hay.includes(S.q)) return false;
  }
  return true;
}
function badge(){
  const n = S.tags.size + (S.cat?1:0);
  const el=$('#fn'); el.textContent=n||''; el.classList.toggle('on', n>0);
}

/* ── 排序 ── */
const CAT_IDX = c => { const i=CATS.indexOf(c); return i<0?99:i; };
const SORTERS = {
  cat: (a,b)=> (CAT_IDX(a.c)-CAT_IDX(b.c)) || a.i.localeCompare(b.i),
  id:  (a,b)=> a.i.localeCompare(b.i),
  tag: (a,b)=> b.t.length-a.t.length || a.i.localeCompare(b.i),
};

/* ── 渲染 ── */
const grid=$('#grid'), countEl=$('#count'), moreEl=$('#more');
let VIEW=[];

function draw(){
  VIEW = ITEMS.filter(hit).sort(SORTERS[S.sort] || SORTERS.cat);
  countEl.innerHTML = S.tags.size
    ? t('count').replace('{n}',VIEW.length).replace('{t}',S.tags.size)
    : t('countNoTag').replace('{n}',VIEW.length);

  if(!VIEW.length){
    grid.innerHTML = '<div class="empty"><b>'+esc(t('emptyTitle'))+'</b>'+esc(t('emptyDesc'))+'</div>';
    moreEl.hidden = true;
    badge(); return;
  }

  // 每次筛选/排序变化都回到第一页
  S.n = PAGE;
  grid.innerHTML = VIEW.slice(0, S.n).map(card).join('');
  sweepLoaded();
  syncMore();
  badge();
}

// 追加下一页（不清空已有卡片）
function addMore(){
  if(S.n >= VIEW.length) return;
  const from = S.n;
  S.n = Math.min(S.n + PAGE, VIEW.length);
  grid.insertAdjacentHTML('beforeend', VIEW.slice(from, S.n).map((x,k)=>card(x, from+k)).join(''));
  sweepLoaded();
  syncMore();
}

function card(x, i){
  const tags = x.t.slice(0,5).map(tg=>'<i title="'+esc(tg)+'">'+esc(nT(tg))+'</i>').join('');
  const over = x.t.length>5 ? '<i class="more">+'+(x.t.length-5)+'</i>' : '';
  return '<article class="card" tabindex="0" data-i="'+i+'">'+
    '<div class="ph"><img'+(i<12?' fetchpriority="high"':' loading="lazy"')+' decoding="async" src="'+esc(x.th)+'" alt="'+esc(x.i)+'">'+
      '<div class="tagbar">'+tags+over+'</div></div>'+
    '<div class="meta"><span class="mid">'+esc(x.i)+'</span><span class="mcat">'+esc(nC(x.c))+'</span></div></article>';
}

// 已在缓存中的图片不会触发 load，直接补渐显类
function sweepLoaded(){
  grid.querySelectorAll('img').forEach(im=>{ if(im.complete) im.classList.add('ld'); });
}

function syncMore(){
  const rest = VIEW.length - S.n;
  moreEl.hidden = rest <= 0;
  moreEl.textContent = rest > 0 ? ('加载更多（剩余 ' + rest + ' 件）') : '';
}

moreEl.onclick = addMore;
// 滚动接近底部时自动加载下一页（与原站一致，预取 800px）
if('IntersectionObserver' in window){
  new IntersectionObserver(es=>{ if(es.some(e=>e.isIntersecting)) addMore(); }, {rootMargin:'800px'}).observe(moreEl);
}
grid.addEventListener('load', e=>{ if(e.target.tagName==='IMG') e.target.classList.add('ld'); }, true);
grid.addEventListener('error', e=>{ if(e.target.tagName==='IMG') e.target.classList.add('ld'); }, true);
grid.addEventListener('click', e=>{
  const c=e.target.closest('.card'); if(!c) return;
  openM(+c.dataset.i);
});
grid.addEventListener('keydown', e=>{
  if(e.key!=='Enter' && e.key!==' ') return;
  const c=e.target.closest('.card'); if(!c) return;
  e.preventDefault(); openM(+c.dataset.i);
});

/* ── 灯箱 ── */
const modal=$('#modal'), mimg=$('#mimg');
let MI = 0;

function openM(i){
  MI = i;
  modal.classList.add('open');
  document.body.style.overflow='hidden';
  showM();
  $('#mclose').focus();
}
function closeM(){
  modal.classList.remove('open');
  document.body.style.overflow='';
  mimg.removeAttribute('src');
  const c=document.querySelector('.card[data-i="'+MI+'"]');
  if(c) c.focus();
}
function showM(){
  const x=VIEW[MI]; if(!x) return;
  // 先缩略图，再换中图（渐进加载）
  mimg.src = x.th;
  const mid = new Image();
  mid.onload = ()=>{ if(VIEW[MI]===x) mimg.src = x.im; };
  mid.src = x.im;
  mimg.alt = x.i;

  $('#mid').textContent = x.i + ' · ' + nC(x.c);
  $('#mfull').href = x.pg;
  $('#mmid').href = x.im;

  $('#mkv').innerHTML = [
    [t('kCat'), nC(x.c)],
    [t('kId'), x.i],
    [t('kTagN'), x.t.length + ' ' + t('tagUnit')],
  ].map(([k,v])=>'<dt>'+esc(k)+'</dt><dd>'+esc(v)+'</dd>').join('');

  $('#mtags').innerHTML = x.t.map(tg=>'<button data-t="'+esc(tg)+'" title="'+esc(tg)+'">'+esc(nT(tg))+'</button>').join('');

  const single = VIEW.length<2;
  $('#mprev').disabled = single;
  $('#mnext').disabled = single;
}

$('#mtags').onclick = e=>{
  const b=e.target.closest('button'); if(!b) return;
  const tg=b.dataset.t;
  closeM();
  S.tags.add(tg);
  drawTagGroups(); draw();
};
$('#mprev').onclick = ()=>step(-1);
$('#mnext').onclick = ()=>step(1);
$('#mclose').onclick = closeM;
modal.onclick = e=>{ if(e.target===modal) closeM(); };
function step(n){
  const j = MI+n;
  if(j<0 || j>=VIEW.length) return;
  MI=j; showM();
}
document.addEventListener('keydown', e=>{
  if(!modal.classList.contains('open')) return;
  if(e.key==='Escape') closeM();
  else if(e.key==='ArrowRight'){ e.preventDefault(); step(1); }
  else if(e.key==='ArrowLeft'){ e.preventDefault(); step(-1); }
});

let tx=null;
mimg.addEventListener('touchstart', e=>{ tx=e.touches[0].clientX; }, {passive:true});
mimg.addEventListener('touchend', e=>{
  if(tx===null) return;
  const dx=e.changedTouches[0].clientX-tx;
  if(Math.abs(dx)>40) step(dx<0?1:-1);
  tx=null;
}, {passive:true});

$('#mcopy').onclick = function(){
  const x=VIEW[MI]; if(!x) return;
  const done=ok=>{ this.textContent = ok?t('copied'):t('copyFail'); setTimeout(()=>{ this.textContent=t('copyPath'); },1400); };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(x.pg).then(()=>done(true)).catch(()=>done(false));
  } else done(false);
};

applyStatic(); drawTabs(); drawCatSel(); drawTagGroups(); draw();
</script>
</body>
</html>"""

html = html.replace("__PAYLOAD__", payload).replace("__SITE__", SITE_URL)
out = os.path.join(root, "index.html")
open(out, "w", encoding="utf-8").write(html)
print("wrote index.html", "%.1f KB" % (os.path.getsize(out) / 1024))
print("items:", len(items), "| cats:", len(cats), "| groups:", len(groups))

# ── 导出可复用的数据文件 ─────────────────────────────
data_dir = os.path.join(root, "data")
os.makedirs(data_dir, exist_ok=True)

zh = []
for x in items:
    zh.append({
        "id": x["i"],
        "分类": x["c"], "分类_zh": CAT_ZH.get(x["c"], x["c"]),
        "标签": x["t"],
        "标签_zh": [TAG_ZH.get(t, t) for t in x["t"]],
        "标签_ja": [TAG_JA.get(t, t) for t in x["t"]],
        "缩略图": x["th"], "中图": x["im"], "原图": x["pg"],
    })
json.dump(zh, open(os.path.join(data_dir, "costume-zh.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

meta = {
    "site": "COSTUME-DB-01",
    "source": "https://ai-costume-gallery.pages.dev/",
    "author": "ギア (@giaaibusi)",
    "items": len(items),
    "images": len(items) * 3,
    "分类": [{"ja": c, "zh": CAT_ZH.get(c, c),
              "items": sum(1 for x in items if x["c"] == c)} for c in cats],
    "标签分组": [{"key": g["k"], "ja": g["ja"], "zh": g["zh"],
                  "tags": [{"en": t, "ja": TAG_JA.get(t, t), "zh": TAG_ZH.get(t, t)}
                           for t in g["tags"]]} for g in groups],
}
json.dump(meta, open(os.path.join(data_dir, "meta.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

with open(os.path.join(data_dir, "translations.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["字段", "原文", "日文", "中文"])
    for k, v in CAT_ZH.items():
        w.writerow(["カテゴリ", k, k, v])
    for k, v in TAG_ZH.items():
        w.writerow(["キーワード", k, TAG_JA.get(k, k), v])
print("wrote data/costume-zh.json, data/meta.json, data/translations.csv")

# ── SEO 附属文件 ─────────────────────────────────────
with open(os.path.join(root, "robots.txt"), "w", encoding="utf-8") as f:
    f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)

with open(os.path.join(root, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    f.write('  <url><loc>%s/</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>\n' % SITE_URL)
    f.write('</urlset>\n')

with open(os.path.join(root, "404.html"), "w", encoding="utf-8") as f:
    f.write("""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>404 · 页面不存在</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%238fb4ff'/%3E%3Ctext x='16' y='23' font-size='19' font-family='sans-serif' font-weight='700' text-anchor='middle' fill='%230d0f12'%3EC%3C/text%3E%3C/svg%3E">
<style>
html,body{margin:0;height:100%%}
body{background:#0d0f12;color:#e9ecf1;font-family:system-ui,-apple-system,"Noto Sans SC","Microsoft YaHei",sans-serif;
  display:flex;align-items:center;justify-content:center;text-align:center;
  background-image:radial-gradient(1200px 500px at 15%% -10%%,#1b2433 0,transparent 60%%),
                   radial-gradient(900px 400px at 100%% 0,#211a2b 0,transparent 55%%)}
.box{padding:24px}
h1{margin:0 0 10px;font-size:64px;font-weight:700;letter-spacing:.02em;
  background:linear-gradient(90deg,#c3d5ff,#e3c8ff);-webkit-background-clip:text;background-clip:text;color:transparent}
p{margin:0 0 22px;color:#a3abb8;font-size:14px;line-height:1.8}
a{display:inline-flex;align-items:center;height:40px;padding:0 20px;border-radius:10px;
  background:#8fb4ff;color:#0b1220;font-size:13.5px;font-weight:700;text-decoration:none}
a:hover{background:#c3d5ff}
</style></head>
<body><div class="box">
<h1>404</h1>
<p>页面不存在，或链接已失效。<br>Page not found.</p>
<a href="/">返回首页</a>
</div></body></html>
""")
print("wrote robots.txt, sitemap.xml, 404.html")
print("SITE_URL =", SITE_URL)
