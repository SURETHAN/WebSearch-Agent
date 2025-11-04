import asyncio
import streamlit as st
import time
from datetime import datetime
from agents import Agent, Runner, WebSearchTool

# ------------------- Load Instructions --------------------------
with open("instruction.txt", "r") as f:
    instructions = f.read().strip()
# ---------------------------------------------------------------

# ------------------- Initialize Agent ---------------------------
agent = Agent(
    name="WebSearchTool - Agent",
    instructions=instructions,
    tools=[WebSearchTool()]
)
# ---------------------------------------------------------------

# ------------------- Streamlit UI Setup -------------------------
st.set_page_config(page_title="🌍 WebSearch Assistant", page_icon="🌍")
st.title("🌍 WebSearch Assistant")
st.write("Ask any question — the assistant will search the web and summarize reliable results for you.")
# ---------------------------------------------------------------

user_input = st.text_input("🔎 Enter your prompt:")

# ------------------- Utility Functions --------------------------
def is_websearch_query(text: str) -> bool:
    """Detect if query requires a web search."""
    if not text.strip():
        return False
    keywords = [
        "who", "what", "when", "where", "why", "how", "latest",
        "news", "update", "today", "price", "release", "?", "trend"
    ]
    text_lower = text.lower()
    return any(k in text_lower for k in keywords)


def current_time_with_ms():
    """Return current time with milliseconds precision."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
# ---------------------------------------------------------------

# ------------------- Button Logic -------------------------------
if st.button("Run Agent"):
    if not user_input.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Thinking..."):
            try:
                start_time = time.perf_counter()

                # Safely manage asyncio event loop
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                # Run the agent with WebSearchTool
                result = loop.run_until_complete(Runner.run(agent, user_input))

                end_time = time.perf_counter()
                response_time_ms = (end_time - start_time) * 1000

                # Display result
                st.subheader("🧠 Result:")
                st.write(result.final_output)

                # Show response time based on query type
                if is_websearch_query(user_input):
                    st.markdown(f"**Response Time:** {response_time_ms:.2f} ms")
                    st.markdown(f"**Current Time:** {current_time_with_ms()}")
                else:
                    st.markdown(
                        f"<small style='color:gray;'>Response time: {response_time_ms:.2f} ms</small>",
                        unsafe_allow_html=True
                    )

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
# ---------------------------------------------------------------
