import streamlit as st

from transcript import get_transcript
from chunking import split_text
from quiz_generator import generate_quiz


# ==========================================
# Extract Video ID
# ==========================================

def extract_video_id(url):

    if "watch?v=" in url:
        return url.split("v=")[1].split("&")[0]

    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    return None


# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="YouTube Quiz Generator",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Powered YouTube Quiz Generator")

st.write(
    "Generate MCQs automatically from YouTube videos using AI."
)

# ==========================================
# Input URL
# ==========================================

youtube_url = st.text_input(
    "Enter YouTube URL"
)

# ==========================================
# Generate Quiz
# ==========================================

if st.button("Generate Quiz"):

    try:

        video_id = extract_video_id(
            youtube_url
        )
        print(video_id)

        if not video_id:

            st.error(
                "Please enter a valid YouTube URL."
            )

        else:

            with st.spinner(
                "Fetching transcript..."
            ):

                transcript = get_transcript(
                    video_id
                )

            with st.spinner(
                "Processing transcript..."
            ):

                chunks = split_text(
                    transcript
                )

                context = ""

                for chunk in chunks[:3]:
                    context += chunk

            with st.spinner(
                "Generating quiz..."
            ):

                quiz = generate_quiz(
                    context
                )

            st.session_state.quiz = quiz
            st.session_state.submitted = False

            st.success(
                "Quiz generated successfully!"
            )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )


# ==========================================
# Display Quiz
# ==========================================

if "quiz" in st.session_state:

    quiz = st.session_state.quiz

    st.header("📝 Quiz")

    user_answers = []

    for i, question in enumerate(quiz):

        st.subheader(
            f"Q{i+1}. {question['question']}"
        )

        answer = st.radio(
            "Select Answer",
            question["options"],
            key=f"question_{i}"
        )

        user_answers.append(answer)

    # ======================================
    # Submit Quiz
    # ======================================

    if st.button("Submit Quiz"):

        score = 0

        results = []

        for i, question in enumerate(quiz):

            option_map = {
                "A": question["options"][0],
                "B": question["options"][1],
                "C": question["options"][2],
                "D": question["options"][3]
            }

            correct_answer = option_map[
                question["answer"].upper()
            ]

            selected_answer = user_answers[i]

            is_correct = (
                selected_answer.strip().lower()
                ==
                correct_answer.strip().lower()
            )

            if is_correct:
                score += 1

            results.append({

                "question":
                question["question"],

                "selected":
                selected_answer,

                "correct":
                correct_answer,

                "status":
                is_correct

            })

        st.session_state.score = score
        st.session_state.results = results
        st.session_state.submitted = True

        st.rerun()


# ==========================================
# Results Section
# ==========================================

if (
    "submitted" in st.session_state
    and
    st.session_state.submitted
):

    st.header("📊 Results")

    score = st.session_state.score

    total_questions = len(
        st.session_state.quiz
    )

    percentage = round(
        (score / total_questions) * 100,
        2
    )

    st.success(
        f"🏆 Score: {score}/{total_questions}"
    )

    st.info(
        f"📈 Percentage: {percentage}%"
    )

    st.divider()

    st.subheader(
        "📝 Quiz Review"
    )

    for i, result in enumerate(
        st.session_state.results
    ):

        st.markdown(
            f"## Question {i+1}"
        )

        st.write(
            f"**Question:** {result['question']}"
        )

        st.write(
            f"**Your Answer:** {result['selected']}"
        )

        st.write(
            f"**Correct Answer:** {result['correct']}"
        )

        if result["status"]:

            st.success(
                "✅ Correct"
            )

        else:

            st.error(
                "❌ Incorrect"
            )

        st.divider()