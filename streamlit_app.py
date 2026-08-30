import logging

import streamlit as st

from app.agents.gpt_teaching_agent import GPTTeachingAgent
from app.config.logging_config import configure_logging
from app.config.settings import settings
from app.coordinator.coordinator import Coordinator
from app.domain.messages import TutorRequest


configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="AI Teaching Tutor",
    page_icon="AI",
    layout="centered",
)


@st.cache_resource
def get_coordinator() -> Coordinator:
    teaching_agent = GPTTeachingAgent(settings=settings)
    return Coordinator(teaching_agent=teaching_agent)


st.title("AI Teaching Tutor")
st.caption("Phase 3: Streamlit → Coordinator → GPT Teaching Agent")

with st.sidebar:
    st.header("Settings")
    learner_level = st.selectbox(
        "Learner level",
        options=["beginner", "intermediate", "advanced"],
    )
    st.write(f"Model: `{settings.openai_model}`")

question = st.text_area(
    "What would you like to learn?",
    placeholder="For example: What is a Python list?",
)

if st.button("Ask Tutor", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        logger.info("Received tutor question")
        request = TutorRequest(
            question=question,
            learner_level=learner_level,
        )

        try:
            response = get_coordinator().handle_request(request)
        except Exception:
            logger.exception("Tutor request failed")
            st.error("The tutor could not complete the request.")
        else:
            if response.status == "success":
                st.subheader("Tutor response")
                st.write(response.answer)
            else:
                st.error(response.answer)
