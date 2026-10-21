"""Desentupidor Ancelmo — site completo em um arquivo Python.

Como publicar: crie um arquivo streamlit_app.py, cole este código e envie
requirements.txt junto. Para a arte, use assets/arte_ancelmo.png.
Para adicionar fotos por link use fotos.txt, e vídeos do YouTube em videos.txt.
"""

from __future__ import annotations

import streamlit as st

import base64
from html import escape
from urllib.parse import urlparse
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

BASE = Path(__file__).parent
ASSETS = BASE / "assets"
WHATSAPP = "https://wa.me/5579981677091"
WHATSAPP_ORCAMENTO = (
    "https://wa.me/5579981677091?text="
    "Ol%C3%A1%21%20Gostaria%20de%20um%20or%C3%A7amento%20gratuito%20de%20desentupimento."
)
INSTAGRAM = "https://www.instagram.com/desintupudorancelmo/"
YOUTUBE = "https://www.youtube.com/@ancelmobatista2850"
TELEFONE = "tel:+5579981677091"

CSS = r"""
<style>
:root { --brand: #AD1811; --deep: #850e0b; --ink:#4f100f; --cream:#fff8f5; --paper:#fffefe; --muted:#ffe0d8; }
html, body, .stApp, [data-testid="stAppViewContainer"] { background:var(--brand)!important; margin:0; padding:0; overflow-x:hidden!important; }
[data-testid="stHeader"] {background:transparent!important;}
[data-testid="stMainBlockContainer"], .block-container { max-width:1260px!important; padding-top:1.1rem!important; padding-left: clamp(12px,3vw,30px)!important; padding-right: clamp(12px,3vw,30px)!important; }
[data-testid="stMain"] {background:var(--brand)!important;}
[data-testid="stBottom"] {background:transparent!important;}
.anz, .anz * { box-sizing:border-box; }
.anz {font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; color:white;line-height:1.52; max-width:100%; overflow-x:clip;}
.anz a {text-decoration:none!important}
.anz .topline {display:flex;align-items:center;justify-content:space-between;gap:18px;padding:14px 3px 18px;border-bottom:1px solid rgba(255,255,255,.25)}
.anz .wordmark {display:flex;align-items:center;gap:12px;min-width:0}
.anz .mark {display:grid;place-items:center;flex:0 0 51px;width:51px;height:51px;border:2px solid white;border-radius:14px;box-shadow:inset 0 0 0 4px rgba(255,255,255,.11)}
.anz .mark svg{height:28px;width:28px;stroke:white}
.anz .brandname{display:flex;flex-direction:column;line-height:1.12;font-weight:900;letter-spacing:.025em;font-size:21px}
.anz .brandname small{font-size:10px;font-weight:750;letter-spacing:.22em;margin-top:6px;opacity:.86}
.anz .navlinks{display:flex;gap:24px;align-items:center;justify-content:flex-end;flex-wrap:wrap}
.anz .navlinks a{font-size:12px;color:#fff;font-weight:700;letter-spacing:.045em;opacity:.94}
.anz .navlinks .nav-cta{background:#fff;color:var(--ink);padding:12px 15px;border-radius:40px;white-space:nowrap}
.anz .hero{min-height:535px;position:relative;display:grid;grid-template-columns: minmax(0,1.1fr) minmax(290px,.9fr);gap:26px;align-items:center;padding:62px 4px 44px;isolation:isolate}
.anz .hero::after {content:"";position:absolute;inset:0 -15px -8px;z-index:-1;background: radial-gradient(ellipse at 72% 40%, rgba(255,255,255,.12), transparent 44%),repeating-linear-gradient(130deg, transparent 0 32px, rgba(255,255,255,.022) 33px 34px, transparent 35px 72px);pointer-events:none}
.anz .kicker{display:inline-flex;align-items:center;gap:9px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.34);border-radius:100px;padding:9px 15px;color:white;font-size:11px;font-weight:800;letter-spacing:.16em;text-transform:uppercase}
.anz .live-dot{width:8px;height:8px;border-radius:50%;background:#fff;box-shadow:0 0 0 4px rgba(255,255,255,.2)}
.anz h1,.anz h2,.anz h3,.anz p{margin:0}
.anz h1{font-size:clamp(39px,5.5vw,74px);line-height:1.04;letter-spacing:-.05em;font-weight:900;margin-top:23px;max-width:740px}
.anz .hero-highlight{color:#fff3cc;}
.anz .lead{font-size:clamp(15px,1.58vw,19px);color:#fff0ea;max-width:570px;line-height:1.7;margin-top:20px}
.anz .buttons{display:flex;gap:13px;flex-wrap:wrap;margin-top:30px}
.anz .btn{min-height:49px;display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:14px 20px;border-radius:9px;font-size:13px;font-weight:850;letter-spacing:.018em;box-shadow:0 6px 22px rgba(60,5,3,.1)}
.anz .btn-primary{background:#fff;color:var(--deep)!important}
.anz .btn-outline{border:1px solid rgba(255,255,255,.7);color:#fff!important;background:rgba(255,255,255,.06)}
.anz .hero-foot{display:flex;gap:22px;flex-wrap:wrap;margin-top:30px;color:#ffe4dd;font-size:12px;font-weight:700}
.anz .hero-foot span:before{content:"✓";display:inline-grid;place-items:center;margin-right:7px;color:var(--deep);background:#fff;border-radius:100%;width:18px;height:18px;font-size:11px}
.anz .art-wrap{position:relative;width:min(100%,450px);margin:0 auto;isolation:isolate}
.anz .art-wrap:before{content:"";position:absolute;inset:22px -17px -15px 15px;z-index:-1;border:2px solid rgba(255,255,255,.55);border-radius:27px;transform:rotate(5deg)}
.anz .art-card{min-height:390px;display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative;border:9px solid rgba(255,255,255,.94);background: #fff9f5; border-radius:22px;box-shadow:0 34px 80px rgba(68,2,0,.35)}
.anz .art-card:before{content:"";position:absolute;inset:0;opacity:.45;pointer-events:none;background: radial-gradient(#ad181132 1.3px, transparent 1.5px) 0 0 / 16px 16px,linear-gradient(135deg,#fff 0%,#ffece7 100%)}
.anz .art-image{position:relative;display:block;max-width:100%;max-height:430px;width:auto;height:auto;object-fit:contain}
.anz .fallback-art{position:relative;width:100%;min-height:390px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--brand);text-align:center;padding:20px 27px}
.anz .fallback-badge{border:3px solid var(--brand);padding:20px 17px;border-radius:50%;background:white;box-shadow:0 0 0 9px #ad181114}
.anz .fallback-badge svg{width:73px;height:73px;stroke:var(--brand)}
.anz .fallback-small{font-size:11px;letter-spacing:.3em;text-transform:uppercase;font-weight:900;margin-top:27px}
.anz .fallback-big{font-size:clamp(29px,3vw,44px);line-height:1.03;font-weight:1000;letter-spacing:-.04em;margin-top:7px}
.anz .fallback-caption{margin-top:14px;padding:8px 12px;border-radius:5px;background:var(--brand);color:#fff;letter-spacing:.16em;font-size:11px;font-weight:850}
.anz .art-label{position:absolute;bottom:-16px;left:-15px;background:#fff;border-radius:9px;padding:13px 17px;display:flex;align-items:center;gap:12px;box-shadow:0 10px 30px rgba(78,7,5,.25);color:var(--brand);font-size:12px;font-weight:950;z-index:1}
.anz .art-label b{font-size:22px;line-height:1}
.anz .ribbon{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:rgba(255,255,255,.25);border-top:1px solid rgba(255,255,255,.3);border-bottom:1px solid rgba(255,255,255,.3)}
.anz .ribbon>div{padding:20px 10px;text-align:center;background:var(--brand)}
.anz .ribbon strong{display:block;font-size:15px;font-weight:900;letter-spacing:-.02em}
.anz .ribbon span{color:#ffe1da;font-size:11px;letter-spacing:.08em;text-transform:uppercase;font-weight:600}
.anz .section{padding:68px 4px 22px}
.anz .section-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:900;letter-spacing:.2em;color:#ffdcd6;text-transform:uppercase}
.anz .section-eyebrow:before{content:"";width:22px;height:2px;background:#fff;display:block}
.anz .section-title{font-size:clamp(28px,3.4vw,45px);line-height:1.12;font-weight:900;letter-spacing:-.035em;margin:10px 0 11px}
.anz .section-description{font-size:15px;color:#ffe5df;max-width:800px;line-height:1.7}
.anz .services{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px;margin-top:28px}
.anz .service{background:var(--paper);color:var(--ink);border-radius:13px;padding:25px 22px;min-height:162px;box-shadow:0 9px 24px rgba(86,7,2,.08);border:1px solid #f7dcd8;position:relative;overflow:hidden}
.anz .service::after{content:"";position:absolute;right:0;top:0;width:38px;height:38px;border-bottom-left-radius:50px;background:#ffede8}
.anz .service-icon{display:grid;place-items:center;width:39px;height:39px;background:#ffe4dc;border-radius:11px;font-size:21px;color:var(--brand);font-weight:900;margin-bottom:14px}
.anz .service h3{font-size:16px;line-height:1.2;font-weight:900;letter-spacing:-.02em}
.anz .service p{color:#795454;font-size:12.5px;line-height:1.55;margin-top:8px}
.anz .band{margin-top:32px;display:grid;grid-template-columns:1.1fr .9fr;align-items:center;gap:28px;padding:24px 26px;border-radius:17px;background:#810f0b;border:1px solid rgba(255,255,255,.23)}
.anz .band strong{font-size:20px;line-height:1.22;display:block}
.anz .band p{font-size:12px;color:#ffe2db;margin-top:9px;line-height:1.65}
.anz .band .buttons{margin:0;justify-content:flex-end}
.anz .placeholder{display:grid;place-items:center;text-align:center;min-height:255px;padding:25px;border:1.5px dashed rgba(255,255,255,.48);border-radius:15px;background:radial-gradient(circle at 100% 0%,rgba(255,255,255,.09),transparent 50%),#8b120e;color:white;margin-top:23px}
.anz .placeholder .placeholder-icon{font-size:41px;line-height:1}
.anz .placeholder b{display:block;font-size:20px;margin-top:14px;line-height:1.28}
.anz .placeholder p{max-width:480px;margin:7px auto 14px;color:#ffe6e1;font-size:13px}
.anz .placeholder a{color:#fff;font-weight:900;text-decoration:underline!important;text-underline-offset:4px;font-size:13px}
.anz .photos-grid{display:grid;grid-template-columns:repeat(3, minmax(0,1fr));gap:16px;margin-top:26px}
.anz figure.photo{margin:0;background:white;border-radius:14px;overflow:hidden;border:5px solid #fff;color:var(--ink)}
.anz .photo img{display:block;width:100%;height:230px;object-fit:cover}
.anz .photo figcaption{padding:12px 14px;font-size:12px;font-weight:750}
.anz .video-callout{background:#fff;color:var(--ink);border-radius:17px;padding:30px;display:grid;grid-template-columns:1fr auto;gap:25px;align-items:center;margin-top:22px}
.anz .video-callout strong{font-size:20px;font-weight:900;display:block}
.anz .video-callout p{color:#775556;font-size:13px;margin-top:7px;line-height:1.55}
.anz .video-callout .btn{background:var(--brand);color:#fff!important;box-shadow:none;white-space:nowrap}
.anz .area-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px;margin:26px 0 24px}
.anz .area{border:1px solid rgba(255,255,255,.32);border-radius:11px;background:rgba(255,255,255,.08);padding:19px 15px;display:flex;align-items:center;gap:11px;font-size:16px;font-weight:800}
.anz .area i{font-style:normal;background:#fff;color:var(--brand);width:33px;height:33px;border-radius:50%;display:grid;place-items:center;flex-shrink:0}
.anz .contact-panel{margin-top:18px;background:#fff;border-radius:18px;padding:38px;display:grid;grid-template-columns:1fr auto;gap:25px;align-items:center;color:var(--ink)}
.anz .contact-panel h2{font-size:clamp(26px,3vw,42px);font-weight:900;line-height:1.1;letter-spacing:-.035em}
.anz .contact-panel p{color:#7f5551;margin-top:12px;font-size:14px;line-height:1.7}
.anz .contact-panel .btn{background:var(--brand);color:#fff!important;white-space:nowrap}
.anz .foot{border-top:1px solid rgba(255,255,255,.3);padding:29px 4px 85px;margin-top:52px;display:flex;justify-content:space-between;align-items:flex-start;gap:23px;flex-wrap:wrap;color:#fff}
.anz .foot b{font-size:19px}
.anz .foot small{display:block;font-size:12px;opacity:.84;margin-top:8px}
.anz .foot a{color:#fff!important;text-decoration:underline!important;text-underline-offset:4px;font-weight:800}
.anz .foot .links{display:flex;gap:20px;flex-wrap:wrap;font-size:13px}
.anz .floating-cta{position:fixed;z-index:1000;right:clamp(12px,2vw,26px);bottom:22px;background:white;color:var(--brand)!important;border:2px solid var(--brand);border-radius:60px;padding:13px 18px;box-shadow:0 9px 40px rgba(47,0,0,.4);font:800 13px ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;display:flex;align-items:center;gap:8px;text-decoration:none!important}
.anz .floating-cta span{background:var(--brand);color:white;border-radius:50%;width:24px;height:24px;display:grid;place-items:center}
.anz a:hover{filter:brightness(.96)}
@media(max-width:880px){
.anz .navlinks a:not(.nav-cta){display:none}
.anz .hero{grid-template-columns:1fr;min-height:auto;padding:37px 4px 42px;gap:45px}
.anz .art-wrap{width:min(100%,420px)}
.anz .services{grid-template-columns:repeat(2,minmax(0,1fr))}
.anz .band,.anz .contact-panel{grid-template-columns:1fr}
.anz .band .buttons{justify-content:flex-start}
.anz .photos-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:570px){
.anz .topline{padding-top:8px;align-items:flex-start}
.anz .brandname{font-size:15px}
.anz .brandname small{font-size:8px;letter-spacing:.15em}
.anz .mark{width:42px;height:42px;flex-basis:42px;border-radius:11px}
.anz .navlinks .nav-cta{font-size:11px;padding:10px}
.anz h1{font-size:clamp(36px,11vw,51px)}
.anz .hero{gap:36px}
.anz .art-card{min-height:290px}
.anz .fallback-art{min-height:290px}
.anz .fallback-badge{padding:12px}
.anz .fallback-badge svg{width:50px;height:50px}
.anz .art-label{bottom:-12px;left:4px}
.anz .hero-foot{gap:12px}
.anz .ribbon{grid-template-columns:repeat(2,minmax(0,1fr))}
.anz .section{padding:50px 4px 10px}
.anz .services,.anz .photos-grid,.anz .area-grid{grid-template-columns:1fr}
.anz .service{min-height:145px}
.anz .band{padding:25px 18px}
.anz .video-callout{grid-template-columns:1fr;padding:25px}
.anz .video-callout .btn{white-space:normal}
.anz .contact-panel{padding:26px 20px}
.anz .contact-panel .btn{white-space:normal}
.anz .photo img{height:250px}
.anz .foot{padding-bottom:94px}
.anz .floating-cta{padding:12px 14px;bottom:12px;right:10px}
}
</style>
"""

# Símbolo usado somente quando não há imagem enviada pelo cliente.
PIPE_SVG = """<svg viewBox='0 0 100 100' fill='none' stroke-width='8' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true'><path d='M20 10v32a14 14 0 0014 14h32a14 14 0 0114 14v20'/><path d='M10 10h20M70 90h20'/><path d='M60 14c8 6 14 12 14 20' stroke-width='4'/></svg>"""


def image_data(path: Path, max_size: tuple[int, int] | None = None) -> str:
    """Converte uma imagem local para data URL. Opcionalmente reduz fotos enormes."""
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        if max_size:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        out = BytesIO()
        image.save(out, format="WEBP", quality=85, method=5)
    return "data:image/webp;base64," + base64.b64encode(out.getvalue()).decode("ascii")


def artwork_html() -> str:
    # Não estica a imagem em grandes telas: mantém tamanho natural e deixa a textura preencher o quadro.
    for name in ("arte_ancelmo.png", "arte_ancelmo.jpg", "arte_ancelmo.jpeg", "arte_ancelmo.webp"):
        artwork = ASSETS / name
        if artwork.exists():
            try:
                return f'<img class="art-image" src="{image_data(artwork, (900, 900))}" alt="Arte de divulgação do Desentupidor Ancelmo">'
            except Exception:
                continue
    return (
        '<div class="fallback-art"><div class="fallback-badge">'
        + PIPE_SVG
        + '</div><span class="fallback-small">Sua solução em desentupimento</span>'
          '<div class="fallback-big">DESENTUPIDOR<br>ANCELMO</div>'
          '<div class="fallback-caption">ATENDIMENTO 24 HORAS</div></div>'
    )


def header_services() -> str:
    return CSS + f"""
<div class="anz" id="inicio">
  <header class="topline">
    <div class="wordmark"><div class="mark">{PIPE_SVG}</div><div class="brandname">DESENTUPIDOR ANCELMO<small>ARACAJU E REGIÃO • SE</small></div></div>
    <nav class="navlinks" aria-label="Navegação principal">
      <a href="#servicos">SERVIÇOS</a><a href="#galeria">FOTOS</a><a href="#videos">VÍDEOS</a><a href="#atendimento">ÁREA DE ATENDIMENTO</a>
      <a class="nav-cta" href="{WHATSAPP_ORCAMENTO}" target="_blank" rel="noopener noreferrer">PEÇA UM ORÇAMENTO ↗</a>
    </nav>
  </header>
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-copy">
      <div class="kicker"><span class="live-dot"></span> ATENDIMENTO 24 HORAS • TODOS OS DIAS</div>
      <h1 id="hero-title">Entupiu?<br>O <span class="hero-highlight">Ancelmo</span><br>resolve.</h1>
      <p class="lead">Desentupimento de tubulações residenciais e comerciais em <b>Aracaju, Nossa Senhora do Socorro e Barra dos Coqueiros.</b> Atendimento com preço justo, qualidade e compromisso com você.</p>
      <div class="buttons"><a class="btn btn-primary" target="_blank" rel="noopener noreferrer" href="{WHATSAPP_ORCAMENTO}">✆ &nbsp; Orçamento grátis no WhatsApp ↗</a><a class="btn btn-outline" href="#servicos">Conheça os serviços ↓</a></div>
      <div class="hero-foot"><span>Visita gratuita</span><span>Emitimos nota fiscal</span><span>Atendemos 24h</span></div>
    </div>
    <div class="art-wrap"><div class="art-card">{artwork_html()}</div><div class="art-label"><b>24h</b><span>Todos os dias<br>da semana</span></div></div>
  </section>
  <div class="ribbon" aria-label="Diferenciais">
    <div><strong>24 HORAS</strong><span>7 dias por semana</span></div><div><strong>ORÇAMENTO GRÁTIS</strong><span>Fale pelo WhatsApp</span></div><div><strong>VISITA GRÁTIS</strong><span>Sem custo de visita</span></div><div><strong>NOTA FISCAL</strong><span>Serviço com documentação</span></div>
  </div>
  <section class="section" id="servicos">
    <span class="section-eyebrow">O QUE FAZEMOS</span><h2 class="section-title">Desentupimento para sua casa<br>ou seu comércio.</h2>
    <p class="section-description">Problemas com entupimentos? Conte com atendimento especializado para os principais pontos da tubulação.</p>
    <div class="services">
      <div class="service"><div class="service-icon">≋</div><h3>Pias e ralos</h3><p>Desobstrução de pontos de drenagem em cozinhas, banheiros e áreas de serviço.</p></div>
      <div class="service"><div class="service-icon">◉</div><h3>Vasos sanitários</h3><p>Atendimento para obstruções em vasos e ramais sanitários.</p></div>
      <div class="service"><div class="service-icon">▣</div><h3>Caixas de gordura</h3><p>Desentupimento de caixas de gordura e tubulações conectadas.</p></div>
      <div class="service"><div class="service-icon">▤</div><h3>Caixas de passagem</h3><p>Serviços em caixas de inspeção e passagem da rede de esgoto.</p></div>
      <div class="service"><div class="service-icon">↪</div><h3>Tubulações residenciais</h3><p>Desobstrução de redes de esgoto e tubulações em residências.</p></div>
      <div class="service"><div class="service-icon">▥</div><h3>Tubulações comerciais</h3><p>Atendimento a empresas, lojas e estabelecimentos comerciais.</p></div>
    </div>
    <div class="band"><div><strong>Preço justo. Trabalho bem feito.</strong><p>Priorizamos a qualidade dos procedimentos e a satisfação de cada cliente. Conte com a nossa equipe quando precisar.</p></div><div class="buttons"><a class="btn btn-primary" href="{WHATSAPP_ORCAMENTO}" target="_blank" rel="noopener noreferrer">Solicitar atendimento ↗</a></div></div>
  </section>
</div>
"""


def linhas_de_arquivo(nome: str) -> list[str]:
    """Lê links cadastrados no arquivo de texto, ignorando comentários."""
    arquivo = BASE / nome
    if not arquivo.exists():
        return []
    return [linha.strip() for linha in arquivo.read_text(encoding="utf-8").splitlines()
            if linha.strip() and not linha.strip().startswith("#")]


def endereco_publico(link: str) -> bool:
    """Aceita apenas endereços HTTP(S) para fotos publicadas na internet."""
    try:
        url = urlparse(link)
        return url.scheme in ("http", "https") and bool(url.netloc)
    except ValueError:
        return False


def gallery_html() -> str:
    photos = []
    photos_dir = ASSETS / "fotos"

    # Fotos enviadas à pasta assets/fotos (opcional).
    if photos_dir.exists():
        for arquivo in sorted(photos_dir.iterdir()):
            if not arquivo.is_file() or arquivo.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
                continue
            try:
                imagem = image_data(arquivo, (1100, 850))
                legenda = escape(arquivo.stem.replace("_", " ").replace("-", " ").title())
                photos.append(f'<figure class="photo"><img loading="lazy" src="{imagem}" alt="{legenda}"><figcaption>{legenda}</figcaption></figure>')
            except Exception:
                continue

    # Links diretos de imagens públicas em fotos.txt (um por linha).
    # É possível escrever: https://exemplo.com/foto.jpg | Limpeza de caixa de gordura
    for linha in linhas_de_arquivo("fotos.txt"):
        endereco, separador, descricao = linha.partition("|")
        link = endereco.strip()
        if not endereco_publico(link):
            continue
        legenda = descricao.strip() if separador and descricao.strip() else "Serviço realizado"
        legenda = escape(legenda)
        link_html = escape(link, quote=True)
        photos.append(f'<figure class="photo"><img loading="lazy" src="{link_html}" alt="{legenda}" referrerpolicy="no-referrer"><figcaption>{legenda}</figcaption></figure>')

    content = (
        '<div class="photos-grid">' + "".join(photos[:24]) + '</div>'
        if photos else
        f'<div class="placeholder"><div><div class="placeholder-icon">▧</div><b>Em breve: fotos dos nossos serviços</b><p>Adicionaremos aqui registros reais dos atendimentos. Enquanto isso, acompanhe nossas novidades no Instagram.</p><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Conheça nosso Instagram ↗</a></div></div>'
    )
    return f"""<div class="anz"><section class="section" id="galeria">
<span class="section-eyebrow">NA PRÁTICA</span><h2 class="section-title">Nosso trabalho em imagens.</h2><p class="section-description">Veja registros de serviços realizados pelo Desentupidor Ancelmo.</p>{content}
</section></div>"""


def video_heading_html() -> str:
    return """<div class="anz"><section class="section" id="videos"><span class="section-eyebrow">NO YOUTUBE</span><h2 class="section-title">Confira nossos vídeos.</h2><p class="section-description">Acompanhe o dia a dia da nossa equipe e conheça melhor o trabalho que realizamos.</p></section></div>"""


def video_placeholder_html() -> str:
    return f"""<div class="anz"><div class="placeholder"><div><div class="placeholder-icon">▶</div><b>Vídeos do nosso canal</b><p>Os vídeos individuais serão exibidos aqui quando seus links forem cadastrados. Você já pode acessar o canal no YouTube.</p><a href="{YOUTUBE}" target="_blank" rel="noopener noreferrer">Assistir no YouTube ↗</a></div></div></div>"""


def video_footer_html() -> str:
    return f"""<div class="anz"><div class="video-callout"><div><strong>Assista também no nosso canal!</strong><p>Vídeos dos serviços e atualizações do Desentupidor Ancelmo.</p></div><a class="btn" href="{YOUTUBE}" target="_blank" rel="noopener noreferrer">▶ Ver canal no YouTube ↗</a></div></div>"""


def footer_html() -> str:
    return f"""<div class="anz">
<section class="section" id="atendimento"><span class="section-eyebrow">ONDE ATENDEMOS</span><h2 class="section-title">Atendimento 24h em Sergipe.</h2>
<p class="section-description">Nossa equipe está à disposição todos os dias da semana nas seguintes cidades:</p>
<div class="area-grid"><div class="area"><i>⌖</i> Aracaju</div><div class="area"><i>⌖</i> Nossa Senhora do Socorro</div><div class="area"><i>⌖</i> Barra dos Coqueiros</div></div></section>
<section class="contact-panel" id="contato"><div><h2>Precisou desentupir?<br>Chame o Ancelmo.</h2><p>Entre em contato com nossa equipe para um orçamento gratuito. Visita gratuita, atendimento 24 horas e emissão de nota fiscal.</p><p><b>WhatsApp e telefone:</b> (79) 98167-7091</p></div><a class="btn" href="{WHATSAPP_ORCAMENTO}" target="_blank" rel="noopener noreferrer">✆ &nbsp;Falar no WhatsApp ↗</a></section>
<footer class="foot"><div><b>DESENTUPIDOR ANCELMO</b><small>Desentupimento residencial e comercial • Sergipe</small><small>Atendimento 24 horas, todos os dias da semana.</small></div><div class="links"><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">WhatsApp</a><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Instagram</a><a href="{YOUTUBE}" target="_blank" rel="noopener noreferrer">YouTube</a><a href="{TELEFONE}">Ligar</a></div></footer>
<a class="floating-cta" href="{WHATSAPP_ORCAMENTO}" target="_blank" rel="noopener noreferrer" aria-label="Solicitar orçamento no WhatsApp"><span>✆</span> Orçamento grátis</a>
</div>"""

# ===================== EXECUÇÃO DO SITE =====================
st.set_page_config(
    page_title="Desentupidor Ancelmo | Desentupimento 24h em Aracaju e região",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "Desentupidor Ancelmo • Atendimento 24h em Sergipe • (79) 98167-7091"},
)

st.html(header_services())
st.html(gallery_html())
st.html(video_heading_html())

# Cole em videos.txt os links individuais dos vídeos, um por linha.
# Exemplo: https://www.youtube.com/watch?v=IDENTIFICADOR
videos = []
for linha in linhas_de_arquivo("videos.txt"):
    url = linha.strip()
    if url.startswith(("https://www.youtube.com/watch?", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://m.youtube.com/watch?")):
        videos.append(url)

if videos:
    colunas = st.columns(2, gap="medium")
    for pos, url in enumerate(videos[:8]):
        with colunas[pos % 2]:
            st.video(url)
else:
    st.html(video_placeholder_html())

st.html(video_footer_html())
st.html(footer_html())
