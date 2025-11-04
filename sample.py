import asyncio
import streamlit as st
from openai_agents import Agent, Runner, WebSearchTool

# Load instructions
with open("instruction.txt", "r") as f:
    instructions = f.read().strip()

agent = Agent(
    name="Assistant",
    instructions=instructions,
    tools=[WebSearchTool()]
)

st.set_page_config(page_title="WebSearch Assistant", page_icon="🌍")
st.title("🌍 WebSearch Assistant")
st.write("Ask your question below, and the assistant will search the web and summarize results for you.")

user_input = st.text_input("🔎 Enter your prompt:")

if st.button("Run Agent"):
    if not user_input.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Thinking..."):
            try:
                # Try to get or create an event loop safely
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                result = loop.run_until_complete(Runner.run(agent, user_input))
                st.subheader("🧠 Result:")
                st.write(result.final_output)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
