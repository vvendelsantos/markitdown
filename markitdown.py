import io
from pathlib import Path

import streamlit as st
from markitdown import MarkItDown, StreamInfo


st.set_page_config(
    page_title="MarkItDown",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Conversor de documentos para Markdown")
st.caption("Conversão usando Microsoft MarkItDown.")

EXTENSOES_PERMITIDAS = [
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
    "jpg",
    "jpeg",
    "png",
    "wav",
    "mp3",
]

arquivo = st.file_uploader(
    "Selecione um arquivo",
    type=EXTENSOES_PERMITIDAS,
)

if arquivo is not None:
    nome_arquivo = arquivo.name
    extensao = Path(nome_arquivo).suffix.lower()

    st.write(f"**Arquivo:** {nome_arquivo}")
    st.write(f"**Tamanho:** {arquivo.size / 1024:.1f} KB")

    if st.button("Converter para Markdown", type="primary"):
        try:
            with st.spinner("Convertendo..."):
                # O MarkItDown espera um stream binário.
                stream = io.BytesIO(arquivo.getvalue())

                # A API atual do MarkItDown recomenda StreamInfo para
                # informar metadados do arquivo ao convert_stream().
                stream_info = StreamInfo(
                    filename=nome_arquivo,
                    extension=extensao,
                )

                conversor = MarkItDown(enable_plugins=False)

                resultado = conversor.convert_stream(
                    stream,
                    stream_info=stream_info,
                )

                markdown = resultado.markdown

                # Guarda o resultado para sobreviver aos reruns do Streamlit.
                st.session_state["markdown_convertido"] = markdown
                st.session_state["nome_markdown"] = (
                    f"{Path(nome_arquivo).stem}.md"
                )

            st.success("Arquivo convertido com sucesso.")

        except Exception as erro:
            st.error(f"Não foi possível converter o arquivo: {erro}")

if "markdown_convertido" in st.session_state:
    markdown = st.session_state["markdown_convertido"]
    nome_markdown = st.session_state["nome_markdown"]

    aba_visualizacao, aba_codigo = st.tabs(
        ["Visualização", "Markdown bruto"]
    )

    with aba_visualizacao:
        st.markdown(markdown)

    with aba_codigo:
        st.code(markdown, language="markdown")

    st.download_button(
        label="Baixar arquivo Markdown",
        data=markdown.encode("utf-8"),
        file_name=nome_markdown,
        mime="text/markdown",
        type="primary",
    )
