from pathlib import Path

app_code = '''import io
from pathlib import Path

import streamlit as st
from markitdown import MarkItDown, StreamInfo


st.set_page_config(
    page_title="MarkItDown",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Conversor para Markdown")
st.caption("Microsoft MarkItDown + Streamlit")

TIPOS_PERMITIDOS = [
    "pdf",
    "docx",
    "pptx",
    "xlsx",
    "xls",
    "html",
    "htm",
    "csv",
    "json",
    "xml",
    "txt",
    "md",
    "zip",
    "epub",
    "msg",
]

arquivo = st.file_uploader(
    "Envie um documento",
    type=TIPOS_PERMITIDOS,
)

if arquivo is not None:
    nome = arquivo.name
    extensao = Path(nome).suffix.lower()

    st.write(f"**Arquivo:** {nome}")
    st.write(f"**Tamanho:** {arquivo.size / 1024:.1f} KB")

    if st.button("Converter", type="primary"):
        try:
            with st.spinner("Convertendo..."):
                stream = io.BytesIO(arquivo.getvalue())

                info = StreamInfo(
                    filename=nome,
                    extension=extensao,
                )

                md = MarkItDown()

                resultado = md.convert_stream(
                    stream,
                    stream_info=info,
                )

                st.session_state["markdown"] = resultado.markdown
                st.session_state["nome_saida"] = (
                    f"{Path(nome).stem}.md"
                )

            st.success("Conversão concluída.")

        except Exception as erro:
            st.exception(erro)

if "markdown" in st.session_state:
    markdown = st.session_state["markdown"]
    nome_saida = st.session_state["nome_saida"]

    tab1, tab2 = st.tabs(
        ["Visualização", "Markdown bruto"]
    )

    with tab1:
        st.markdown(markdown)

    with tab2:
        st.code(markdown, language="markdown")

    st.download_button(
        "Baixar Markdown",
        data=markdown.encode("utf-8"),
        file_name=nome_saida,
        mime="text/markdown",
        type="primary",
    )
'''

requirements = '''streamlit
markitdown[pdf,docx,pptx,xlsx,xls,outlook]==0.1.7
'''

base = Path("/mnt/data")
(base / "mark_corrigido.txt").write_text(app_code, encoding="utf-8")
(base / "requirements_corrigido.txt").write_text(requirements, encoding="utf-8")

compile(app_code, "mark_corrigido.txt", "exec")

print("Arquivos corrigidos criados.")
print(requirements)
