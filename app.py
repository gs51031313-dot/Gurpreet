import streamlit as st
import pandas as pd
import plotly.express as px
import hashlib
import json
import os
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="FoodAI Premium Dashboard",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# LOAD DATA
# =========================================================
df = pd.read_csv("Cleaned_Zomato_Dataset.csv")

# =========================================================
# LOGIN DATABASE
# =========================================================
USER_FILE = "users.json"
ORDER_FILE = "orders.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(ORDER_FILE):
    with open(ORDER_FILE, "w") as f:
        json.dump([], f)


def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


def load_orders():
    with open(ORDER_FILE, "r") as f:
        return json.load(f)


def save_orders(orders):
    with open(ORDER_FILE, "w") as f:
        json.dump(orders, f, indent=4)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# =========================================================
# ADVANCED CUSTOM UI
# =========================================================
st.markdown("""
<style>

.stApp {
    background:
        linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
        url("https://images.unsplash.com/photo-1504674900247-0877df9cc836");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* =========================
   TOP BAR BLACK + BLUR
========================= */
header {
    background: rgba(0,0,0,0.85) !important;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
/* SIDEBAR LIGHT PINK + BLUR */

section[data-testid="stSidebar"] {
    background: rgba(255, 182, 193, 0.18) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255,255,255,0.15);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.glass-card {
    background: rgba(255,255,255,0.08);
    border-radius: 24px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    padding: 25px;
    margin-bottom: 20px;
}

.main-title {
    text-align: center;
    font-size: 65px;
    font-weight: 800;
    background: linear-gradient(to right,#ff9966,#ff5e62,#f9d423);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: rgba(255,255,255,0.8);
    font-size: 20px;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}

.login-box {
    background: rgba(255,255,255,0.08);
    padding: 40px;
    border-radius: 25px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.08);
}

.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(to right,#ff9966,#ff5e62);
    color: white;
    font-size: 17px;
    font-weight: 700;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 15px rgba(255,94,98,0.6);
}

.stTextInput input {
    border-radius: 12px !important;
}

[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
}

.js-plotly-plot {
    border-radius: 20px;
    overflow: hidden;
}

.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    font-weight: 600;
}

h1,h2,h3,h4,p,label,span {
    color: white !important;
}
/* SIDEBAR INPUTS BLACK */

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    background-color: rgba(0,0,0,0.9) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

/* SELECTBOX */

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: rgba(0,0,0,0.9) !important;
    color: white !important;
    border-radius: 12px !important;
}

/* MULTISELECT TAGS */

section[data-testid="stSidebar"] span {
    color: white !important;
}

/* DROPDOWN MENU */

div[role="listbox"] {
    background-color: rgba(0,0,0,0.95) !important;
}

div[role="option"] {
    background-color: rgba(0,0,0,0.95) !important;
    color: white !important;
}

/* SLIDER */

section[data-testid="stSidebar"] .stSlider {
    background: rgba(0,0,0,0.25);
    padding: 10px;
    border-radius: 12px;
}
    background: rgba(0,0,0,0.85) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
}

/* DROPDOWN OPTIONS */

div[role="listbox"] {
    background: rgba(0,0,0,0.95) !important;
    color: white !important;
}

/* SIDEBAR LABELS */

section[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)
# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =========================================================
# LOGIN + SIGNUP PAGE
# =========================================================
if not st.session_state.logged_in:

    st.markdown("<h1 class='main-title'>🍽️ FoodAI Premium</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>AI Powered Restaurant Recommendation Platform</p>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1.2,1])

    with col2:

        tab1, tab2 = st.tabs(["🔐 Login", "🚀 Signup"])

        with tab1:

            st.markdown("<div class='login-box'>", unsafe_allow_html=True)

            st.subheader("Welcome Back 👋")

            login_user = st.text_input("Username")
            login_pass = st.text_input("Password", type="password")

            if st.button("Login"):

                users = load_users()

                if login_user in users and users[login_user] == hash_password(login_pass):
                    st.session_state.logged_in = True
                    st.session_state.username = login_user
                    st.success("Login Successful ✅")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")

            st.markdown("</div>", unsafe_allow_html=True)

        with tab2:

            st.markdown("<div class='login-box'>", unsafe_allow_html=True)

            st.subheader("Create New Account 🚀")

            new_user = st.text_input("Create Username")
            new_pass = st.text_input("Create Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")

            if st.button("Signup"):

                users = load_users()

                if new_user in users:
                    st.warning("Username already exists")

                elif new_pass != confirm_pass:
                    st.warning("Passwords do not match")

                elif len(new_pass) < 4:
                    st.warning("Password too short")

                else:
                    users[new_user] = hash_password(new_pass)
                    save_users(users)
                    st.success("Account Created Successfully ✅")

            st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# MAIN DASHBOARD
# =========================================================
else:

    st.sidebar.image(
        "https://cdn-icons-png.flaticon.com/512/1046/1046784.png",
        width=120
    )

    st.sidebar.title("🍔 FoodAI Dashboard")
    st.sidebar.success(f"Welcome {st.session_state.username}")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "📂 Navigation",
        [
            "🏠 Dashboard",
            "🛒 Order Food",
            "📜 Order History"
        ]
    )

    city_list = sorted(df['City'].dropna().unique())

    city = st.sidebar.selectbox(
        "📍 Select City",
        ["All"] + city_list
    )

    all_foods = (
        df['Cuisines'].dropna().str.split(', ').sum() +
        df['primary_cuisines'].dropna().str.split(', ').sum()
    )

    food_series = pd.Series(all_foods)
    top_foods = food_series.value_counts().head(10).index.tolist()
    all_unique_foods = sorted(set(food_series))

    food_list = ["All"] + top_foods + [
        f for f in all_unique_foods if f not in top_foods
    ]

    food = st.sidebar.selectbox("🍕 Select Food", food_list)

    cost = st.sidebar.multiselect(
        "💰 Cost Category",
        df['cost_category'].unique(),
        default=df['cost_category'].unique()
    )

    rating_range = st.sidebar.slider(
        "⭐ Rating Range",
        float(df['Rating'].min()),
        float(df['Rating'].max()),
        (2.5, 4.5)
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    filtered_df = df.copy()

    if city != "All":
        filtered_df = filtered_df[
            filtered_df['City'].str.contains(city, case=False, na=False)
        ]

    filtered_df = filtered_df[
        (filtered_df['cost_category'].isin(cost)) &
        (filtered_df['Rating'].between(rating_range[0], rating_range[1]))
    ]

    if food != "All":
        filtered_df = filtered_df[
            filtered_df['Cuisines'].str.contains(food, case=False, na=False) |
            filtered_df['primary_cuisines'].str.contains(food, case=False, na=False)
        ]

    if filtered_df.empty:
        st.warning("No data found")
        st.stop()

    # =========================================================
    # DASHBOARD PAGE
    # =========================================================
    if page == "🏠 Dashboard":

        st.markdown("<h1 class='main-title'>🍽️ Smart Restaurant Recommendation System</h1>", unsafe_allow_html=True)

        st.markdown(
            f"<p class='subtitle'>Advanced AI Analytics Dashboard • {datetime.now().strftime('%d %B %Y')}</p>",
            unsafe_allow_html=True
        )

        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("🍴 Restaurants", len(filtered_df))
        col2.metric("⭐ Avg Rating", round(filtered_df['Rating'].mean(), 2))
        col3.metric("🗳️ Avg Votes", int(filtered_df['Votes'].mean()))
        col4.metric("💰 Avg Cost", int(filtered_df['Average_Cost_for_two'].mean()))

        st.markdown("---")

        st.subheader("🔥 AI Top Recommendations")

        filtered_df['norm_rating'] = filtered_df['Rating'] / 5
        filtered_df['norm_votes'] = filtered_df['Votes'] / filtered_df['Votes'].max()
        filtered_df['norm_value'] = filtered_df['Value-for-money'] / filtered_df['Value-for-money'].max()

        filtered_df['recommend_score'] = (
            0.5 * filtered_df['norm_rating'] +
            0.3 * filtered_df['norm_votes'] +
            0.2 * filtered_df['norm_value']
        )

        st.dataframe(
            filtered_df.sort_values(by='recommend_score', ascending=False)
            [[
                'RestaurantName',
                'City',
                'Cuisines',
                'Rating',
                'Votes',
                'cost_per_person'
            ]]
            .head(15),
            use_container_width=True,
            height=500
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("⭐ Popularity vs Quality")

            fig1 = px.scatter(
                filtered_df,
                x='Rating',
                y='Votes',
                color='cost_category',
                size='Votes',
                template="plotly_dark",
                hover_data=['RestaurantName']
            )

            fig1.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig1, use_container_width=True)

        with col2:

            st.subheader("🍜 Top Cuisines")

            top_cuisines = (
                filtered_df.groupby('primary_cuisines')['Votes']
                .mean()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            fig4 = px.bar(
                top_cuisines,
                x='primary_cuisines',
                y='Votes',
                template="plotly_dark"
            )

            fig4.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig4, use_container_width=True)

        st.markdown("---")

        st.subheader("🚚 Business Insights")

        col3, col4 = st.columns(2)

        with col3:

            delivery_votes = filtered_df.groupby('Has_Online_delivery')['Votes'].mean().reset_index()

            fig2 = px.bar(
                delivery_votes,
                x='Has_Online_delivery',
                y='Votes',
                template="plotly_dark"
            )

            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig2, use_container_width=True)

        with col4:

            fig3 = px.box(
                filtered_df,
                x='cost_category',
                y='Rating',
                template="plotly_dark"
            )

            fig3.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("---")

        st.subheader("🌆 Market Competition")

        fig5 = px.scatter(
            filtered_df,
            x='city_competition_norm',
            y='Rating',
            template="plotly_dark",
            color='cost_category'
        )

        fig5.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig5, use_container_width=True)

        st.markdown("---")

        col5, col6 = st.columns(2)

        with col5:

            st.subheader("🏆 Top Restaurants")

            st.dataframe(
                filtered_df.sort_values(by='popularity_score', ascending=False)
                [[
                    'RestaurantName',
                    'Rating',
                    'Votes',
                    'popularity_score'
                ]]
                .head(10),
                use_container_width=True
            )

        with col6:

            st.subheader("💎 Best Value for Money")

            st.dataframe(
                filtered_df.sort_values(by='Value-for-money', ascending=False)
                [[
                    'RestaurantName',
                    'Rating',
                    'cost_per_person',
                    'Value-for-money'
                ]]
                .head(10),
                use_container_width=True
            )

    # =========================================================
    # ORDER FOOD PAGE
    # =========================================================
    elif page == "🛒 Order Food":

        st.markdown("<h1 class='main-title'>🛒 Order Food Online</h1>", unsafe_allow_html=True)

        st.markdown("---")

        order_restaurant = st.selectbox(
            "🍴 Select Restaurant",
            filtered_df['RestaurantName'].unique()
        )

        restaurant_data = filtered_df[
            filtered_df['RestaurantName'] == order_restaurant
        ].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="glass-card">
            <h3>🍽️ Restaurant Details</h3>
            <p>⭐ Rating: {restaurant_data['Rating']}</p>
            <p>🍜 Cuisine: {restaurant_data['Cuisines']}</p>
            <p>🏙️ City: {restaurant_data['City']}</p>
            <p>💰 Cost Per Person: ₹{restaurant_data['cost_per_person']}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            quantity = st.number_input(
                "🍽️ Quantity",
                min_value=1,
                max_value=20,
                value=1
            )

            delivery_address = st.text_area("🏠 Delivery Address")

            payment_method = st.selectbox(
                "💳 Payment Method",
                ["Cash on Delivery", "UPI", "Debit Card", "Credit Card"]
            )

            total_price = int(restaurant_data['cost_per_person']) * quantity

            st.success(f"💵 Total Amount: ₹{total_price}")

            if st.button("✅ Place Order"):

                if delivery_address.strip() == "":
                    st.warning("Please Enter Delivery Address")

                else:
                    orders = load_orders()

                    new_order = {
                        "username": st.session_state.username,
                        "restaurant": order_restaurant,
                        "city": restaurant_data['City'],
                        "cuisine": restaurant_data['Cuisines'],
                        "quantity": quantity,
                        "payment_method": payment_method,
                        "total_price": total_price,
                        "address": delivery_address,
                        "status": "Preparing",
                        "order_time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    }

                    orders.append(new_order)
                    save_orders(orders)

                    st.success("🎉 Order Placed Successfully!")
                    st.balloons()

    # =========================================================
    # ORDER HISTORY PAGE
    # =========================================================
    elif page == "📜 Order History":

        st.markdown("<h1 class='main-title'>📜 Order History</h1>", unsafe_allow_html=True)

        st.markdown("---")

        orders = load_orders()

        user_orders = [
            order for order in orders
            if order['username'] == st.session_state.username
        ]

        if len(user_orders) == 0:
            st.warning("No Orders Found")

        else:

            for i, order in enumerate(user_orders):

                st.markdown(f"""
                <div class="glass-card">
                    <h3>🍴 {order['restaurant']}</h3>
                    <p>📍 City: {order['city']}</p>
                    <p>🍜 Cuisine: {order['cuisine']}</p>
                    <p>🍽️ Quantity: {order['quantity']}</p>
                    <p>💳 Payment Method: {order['payment_method']}</p>
                    <p>💰 Total Amount: ₹{order['total_price']}</p>
                    <p>🏠 Address: {order['address']}</p>
                    <p>🚚 Status: {order['status']}</p>
                    <p>🕒 Ordered On: {order['order_time']}</p>
                </div>
                """, unsafe_allow_html=True)

                if order['status'] != "Cancelled":

                    if st.button(f"❌ Cancel Order {i+1}"):

                        orders_index = orders.index(order)
                        orders[orders_index]['status'] = "Cancelled"

                        save_orders(orders)

                        st.success("Order Cancelled Successfully")
                        st.rerun()

    st.markdown("---")

    st.markdown("""
    <center>
        <h3>🚀 FoodAI Premium Analytics Dashboard</h3>
        <p>Advanced Restaurant Recommendation & Visualization System using Streamlit + AI</p>
    </center>
    """, unsafe_allow_html=True)
