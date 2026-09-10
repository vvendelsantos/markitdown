from pathlib import Path

app_code = r'''import io
import zipfile
from pathlib import Path

import streamlit as st
from markitdown import MarkItDown, StreamInfo


MAX_PDFS = 10

st.set_page_config(
    page_title="PDF para Markdown",
    page_icon="📄",
    layout="wide",
)

st.title("📄 PDF para Markdown")
st.caption("Conversão com Microsoft MarkItDown")

arquivos = st.file_uploader(
    f"Envie até {MAX_PDFS} arquivos PDF",
    type=["pdf"],
    accept_multiple_files=True,
)

# Limpa resultados antigos se o conjunto de uploads mudar.
assinatura_atual = tuple(
    (arquivo.name, arquivo.size) for arquivo in arquivos
) if arquivos else ()

if st.session_state.get("assinatura_uploads") != assinatura_atual:
    st.session_state["assinatura_uploads"] = assinatura_atual
    st.session_state.pop("resultados", None)
    st.session_state.pop("erros", None)

if arquivos:
    st.write(f"**Selecionados:** {len(arquivos)} PDF(s)")

    if len(arquivos) > MAX_PDFS:
        st.error(
            f"Você selecionou {len(arquivos)} PDFs. "
            f"O limite é {MAX_PDFS} por lote."
        )
        st.stop()

    tamanho_total_mb = sum(a.size for a in arquivos) / (1024 * 1024)
    st.write(f"**Tamanho total:** {tamanho_total_mb:.2f} MB")

    if st.button("Converter PDFs", type="primary"):
        conversor = MarkItDown()
        resultados = []
        erros = []

        barra = st.progress(0)
        status = st.empty()

        for indice, arquivo in enumerate(arquivos, start=1):
            status.write(
                f"Convertendo {indice}/{len(arquivos)}: **{arquivo.name}**"
            )

            try:
                stream = io.BytesIO(arquivo.getvalue())

                info = StreamInfo(
                    filename=arquivo.name,
                    extension=".pdf",
                    mimetype="application/pdf",
                )

                resultado = conversor.convert_stream(
                    stream,
                    stream_info=info,
                )

                markdown = resultado.markdown or ""

                resultados.append(
                    {
                        "arquivo_original": arquivo.name,
                        "nome_md": f"{Path(arquivo.name).stem}.md",
                        "markdown": markdown,
                    }
                )

            except Exception as erro:
                erros.append(
                    {
                        "arquivo": arquivo.name,
                        "erro": str(erro),
                    }
                )

            barra.progress(indice / len(arquivos))

        status.empty()
        barra.empty()

        st.session_state["resultados"] = resultados
        st.session_state["erros"] = erros

        if resultados:
            st.success(
                f"{len(resultados)} de {len(arquivos)} PDF(s) "
                "convertido(s) com sucesso."
            )

        if erros:
            st.warning(
                f"{len(erros)} PDF(s) não pôde/puderam ser convertido(s)."
            )

resultados = st.session_state.get("resultados", [])
erros = st.session_state.get("erros", [])

if resultados:
    st.divider()
    st.subheader("Resultados")

    # Evita nomes repetidos dentro do ZIP.
    nomes_usados = {}
    arquivos_zip = []

    for item in resultados:
        nome_base = item["nome_md"]
        quantidade = nomes_usados.get(nome_base, 0) + 1
        nomes_usados[nome_base] = quantidade

        if quantidade == 1:
            nome_zip = nome_base
        else:
            caminho = Path(nome_base)
            nome_zip = f"{caminho.stem}_{quantidade}{caminho.suffix}"

        arquivos_zip.append((nome_zip, item["markdown"]))

    # Cria o ZIP inteiramente em memória.
    buffer_zip = io.BytesIO()

    with zipfile.ZipFile(
        buffer_zip,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zip_saida:
        for nome_zip, markdown in arquivos_zip:
            zip_saida.writestr(
                nome_zip,
                markdown.encode("utf-8"),
            )

    buffer_zip.seek(0)

    st.download_button(
        label="⬇️ Baixar todos os Markdown em ZIP",
        data=buffer_zip.getvalue(),
        file_name="markdown_convertidos.zip",
        mime="application/zip",
        type="primary",
    )

    for indice, item in enumerate(resultados):
        with st.expander(
            f"✅ {item['arquivo_original']}",
            expanded=len(resultados) == 1,
        ):
            markdown = item["markdown"]

            if not markdown.strip():
                st.warning(
                    "O MarkItDown não encontrou texto neste PDF. "
                    "Ele pode ser um PDF escaneado/imagem e exigir OCR."
                )
            elif len(markdown.strip()) < 100:
                st.warning(
                    "Foi extraído muito pouco texto. Confira o resultado; "
                    "o PDF pode ser escaneado ou ter um layout difícil."
                )

            tab_visualizacao, tab_markdown = st.tabs(
                ["Visualização", "Markdown bruto"]
            )

            with tab_visualizacao:
                if markdown.strip():
                    st.markdown(markdown)
                else:
                    st.info("Nenhum conteúdo textual foi extraído.")

            with tab_markdown:
                st.code(markdown, language="markdown")

            st.download_button(
                label=f"Baixar {item['nome_md']}",
                data=markdown.encode("utf-8"),
                file_name=item["nome_md"],
                mime="text/markdown",
                key=f"download_md_{indice}_{item['arquivo_original']}",
            )

if erros:
    st.divider()
    st.subheader("Erros")

    for item in erros:
        st.error(f"**{item['arquivo']}**: {item['erro']}")
'''

requirements = '''streamlit
markitdown[pdf]==0.1.7
'''

base = Path("/mnt/data")
files = {
    "mark.py": app_code,
    "mark_pdf.txt": app_code,
    "requirements.txt": requirements,
}

for name, content in files.items():
    (base / name).write_text(content, encoding="utf-8")

compile(app_code, "mark.py", "exec")

print("Arquivos criados e sintaxe validada:")
for name in files:
    print(f"- /mnt/data/{name}")
