import streamlit as st # type: ignore
import random
import time
import pandas as pd # type: ignore

def naive_search(l, target):
    for i in range(len(l)):
        if l[i] == target:
            return i
    return -1

def binary_search(l, target, low=None, high=None):
    if low is None:
        low = 0
    if high is None:
        high = len(l) - 1
    
    if high < low:
        return -1
    
    midpoint = (low + high) // 2
    
    if l[midpoint] == target:
        return midpoint
    elif target < l[midpoint]:
        return binary_search(l, target, low, midpoint - 1)
    else:
        return binary_search(l, target, midpoint + 1, high)

# Custom Streamlit Theme
st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
        text-align: center;
        font-family: Arial, sans-serif;
    }
    .stButton>button {
        background-color: #ff5733;
        color: white;
        font-size: 18px;
        border-radius: 12px;
        padding: 10px;
    }
    
    .stDataFrame>div {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Binary Search vs. Naive Search")
st.write("### ⚡ Fast vs. Slow Searching Techniques")

# Select list length
length = st.slider("📏 Select List Length", min_value=10, max_value=10000, value=1000)

# User input for target
target = st.number_input("🔢 Enter a number to search", value=0)

# Generate sorted list
sorted_list = sorted(random.sample(range(-3 * length, 3 * length), length))

if st.button("🚀 Start Search"):
    iterations = 1000
    
    # Measure Naive Search Time
    start_time = time.perf_counter()
    for _ in range(iterations):
        naive_result = naive_search(sorted_list, target)
    naive_time = (time.perf_counter() - start_time) / iterations
    
    # Measure Binary Search Time
    start_time = time.perf_counter()
    for _ in range(iterations):
        binary_result = binary_search(sorted_list, target)
    binary_time = (time.perf_counter() - start_time) / iterations
    
    # Display results in a grid
    result_df = pd.DataFrame({
        "🔍 Search Method": ["Naive Search", "Binary Search"],
        "📍 Result Index": [naive_result, binary_result],
        "⏳ Time Taken (s)": [f"{naive_time:.10f}", f"{binary_time:.10f}"]
    })
    
    st.write("### 🏆 Search Performance")
    st.dataframe(result_df, width=700, height=150)
    
    if binary_time < naive_time:
        st.success("🚀 Binary Search is significantly faster for large lists! 🎯")
    else:
        st.warning("⚠️ Naive Search might be slow! Try increasing the list size.")
    
# Footer
st.write("\n---")
st.write("💻 Developed by **Asma Khan** ✨")