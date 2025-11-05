import streamlit as st
from PIL import Image
import datetime
import io
import pandas as pd
import plotly.express as px

from db_utils import init_db, save_detection_to_db, get_current_inventory_df, get_inventory_log_df
from detection_utils import run_yolo_inference
from llm_utils import call_gemini

# Initialize database
init_db()

st.set_page_config(page_title="Smart Inventory", layout="wide")
st.title("Smart Inventory Management Dashboard")

tab1, tab2, tab3 = st.tabs(["📸 Upload & Detect", "📊 Analytics Dashboard", "💬 AI Chatbot"])

with tab1:
    st.subheader("Upload Image and Detect Items")
    uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    detect_btn = st.button("Run Detection")

    if uploaded and detect_btn:
        image = Image.open(uploaded).convert("RGB")
        annotated, counts, boxes = run_yolo_inference(image)
        st.image(annotated, use_container_width=True)
        st.markdown("### Detected Items")
        cols = st.columns(3)
        i = 0
        for item, cnt in counts.items():
            with cols[i % 3]:
                st.metric(label=item, value=cnt)
            i += 1

        image_id = f"uploaded_{int(datetime.datetime.utcnow().timestamp())}"
        save_detection_to_db(image_id, counts)
        st.success("Detection saved to database ✅")
    else:
        st.info("Upload an image and click 'Run Detection'")

with tab2:
    st.subheader("Inventory Overview")
    df_curr = get_current_inventory_df()
    df_log = get_inventory_log_df()

    if df_curr.empty:
        st.warning("No inventory data found. Run detection to populate data.")
    else:
        total_items = df_curr['stock_count'].sum()
        unique_items = len(df_curr)
        low_stock = len(df_curr[df_curr['stock_count'] < 10])
        last_update = df_curr['last_updated'].max()

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Items", total_items)
        k2.metric("Unique SKUs", unique_items)
        k3.metric("Low Stock (<10)", low_stock)
        k4.metric("Last Updated", last_update)

        st.markdown("---")
        st.markdown("### Top 5 Products by Stock")
        top5 = df_curr.sort_values("stock_count", ascending=False).head(5)
        fig = px.bar(top5, x="item_name", y="stock_count", title="Top 5 Products")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Stock Trends Over Time")
        if not df_log.empty:
            products = sorted(df_log['item_name'].unique())
            sel_prod = st.selectbox("Select product", products)
            prod_df = df_log[df_log['item_name'] == sel_prod]
            fig2 = px.line(prod_df, x="timestamp", y="count", title=f"Trend for {sel_prod}")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Low Stock Alerts")
        low_df = df_curr[df_curr['stock_count'] < 10]
        if not low_df.empty:
            st.table(low_df)
        else:
            st.success("All stocks are healthy!")

with tab3:
    st.subheader("Gemini AI Chatbot")
    user_query = st.text_input("Ask something about your inventory:")

    if st.button("Ask Gemini"):
        df_curr = get_current_inventory_df()
        df_log = get_inventory_log_df(200)
        snapshot = {
            "current_inventory": df_curr.to_dict(orient="records"),
            "recent_logs": df_log.to_dict(orient="records"),
        }
        prompt = f"User question: {user_query}\nDatabase snapshot:\n{snapshot}\nProvide concise insights."
        with st.spinner("Thinking..."):
            response = call_gemini(prompt)
        st.markdown("**Gemini Response:**")
        st.write(response)
