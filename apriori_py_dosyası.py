import pandas as pd
import streamlit as st
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import networkx as nx
from io import BytesIO

st.set_page_config(page_title="Excel Veri İşleyici", layout="wide")
st.title("Excel Dosya Yükleyici ve Apriori Analizi")


st.sidebar.header("Apriori Parametreleri")

min_support = st.sidebar.slider(
    "Minimum Support",
    min_value=0.01,
    max_value=0.50,
    value=0.20,
    step=0.01
)

min_confidence = st.sidebar.slider(
    "Minimum Confidence",
    min_value=0.10,
    max_value=1.00,
    value=0.60,
    step=0.05
)

rule_sizes = st.sidebar.multiselect(
    "Toplam Kural Uzunlukları",
    options=[3, 4, 5, 6, 7],
    default=[3, 4]
)


uploaded_file = st.file_uploader(
    "Bir Excel dosyası seçin",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("Ham Veri")
    st.dataframe(df.head())

    selected_columns = st.multiselect(
        "Görmek istediğiniz sütunları seçin:",
        df.columns.tolist(),
        default=df.columns.tolist()
    )

    df = df[selected_columns]

    
    df = df.dropna()

    
    
    st.subheader("Likert Dağılımı – Histogram")

    selected_hist_col = st.selectbox(
        "Histogram için sütun seçin:",
        df.columns
    )

    fig, ax = plt.subplots()
    ax.hist(df[selected_hist_col], bins=5)
    ax.set_xlabel("Likert Değeri")
    ax.set_ylabel("Frekans")
    ax.set_title(f"{selected_hist_col} Dağılımı")
    st.pyplot(fig)

    
    
    
    threshold = st.slider("1 kabul eşiği (>=)", 1, 5, 4)

    df_bin = (df >= threshold).astype(int)

    st.subheader("Binary (0-1) Veri")
    st.dataframe(df_bin)

    
    
    
    freq_items = apriori(
        df_bin,
        min_support=min_support,
        use_colnames=True
    )

    if freq_items.empty:
        st.warning("Bu support değeri için sık öğe kümesi bulunamadı.")
        st.stop()

    rules = association_rules(
        freq_items,
        metric="confidence",
        min_threshold=min_confidence
    )

    if rules.empty:
        st.warning("Bu confidence değeri için kural bulunamadı.")
        st.stop()

    
    
    
    filtered_rules = rules[
        (rules["consequents"].apply(len) == 1) &
        ((rules["antecedents"].apply(len) + 1).isin(rule_sizes))
    ]

    filtered_rules = filtered_rules.sort_values("lift", ascending=False)

    st.subheader("Filtrelenmiş Birliktelik Kuralları")
    st.dataframe(
        filtered_rules[
            ["antecedents", "consequents", "support", "confidence", "lift"]
        ]
    )

    
    
    
    export_df = filtered_rules.copy()

    export_df["Antecedents"] = export_df["antecedents"].apply(
        lambda x: " + ".join(sorted(x))
    )
    export_df["Consequents"] = export_df["consequents"].apply(
        lambda x: " + ".join(sorted(x))
    )

    export_df = export_df[
        ["Antecedents", "Consequents", "support", "confidence", "lift"]
    ]

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        export_df.to_excel(
            writer,
            index=False,
            sheet_name="Apriori_Kurallari"
        )
    output.seek(0)

    st.download_button(
        label="📥 Kuralları Excel olarak indir",
        data=output,
        file_name="apriori_kurallari.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    
    
    
    st.subheader("Support - Confidence Grafiği")

    fig, ax = plt.subplots()
    ax.scatter(filtered_rules["support"], filtered_rules["confidence"])
    ax.set_xlabel("Support")
    ax.set_ylabel("Confidence")
    st.pyplot(fig)

    
    
    
    st.subheader("Birliktelik Kuralları Ağ Grafiği (En Güçlü 10 Kural)")

    top10_for_graph = filtered_rules.head(10)

    if len(top10_for_graph) > 0:
        G = nx.DiGraph()

        for _, row in top10_for_graph.iterrows():
            ant = " + ".join(sorted(row["antecedents"]))
            con = " + ".join(sorted(row["consequents"]))
            G.add_edge(ant, con, weight=round(row["lift"], 2))

        pos = nx.spring_layout(G, seed=42)

        fig_net, ax_net = plt.subplots(figsize=(10, 8))
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=900,
            font_size=9,
            ax=ax_net
        )

        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            font_size=8
        )

        ax_net.axis("off")
        st.pyplot(fig_net)

    else:
        st.info("Gösterilecek kural bulunamadı.")
