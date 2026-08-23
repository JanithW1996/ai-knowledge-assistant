const form = document.querySelector("#question-form");
const questionInput = document.querySelector("#question");
const roleInput = document.querySelector("#role");
const askButton = document.querySelector("#ask-button");
const resultPanel = document.querySelector("#result-panel");
const answerText = document.querySelector("#answer-text");
const groundingBadge = document.querySelector("#grounding-badge");
const sourcesSection = document.querySelector("#sources-section");
const sourceList = document.querySelector("#source-list");
const suggestions = document.querySelectorAll(".suggestion");


suggestions.forEach((button) => {
  button.addEventListener("click", () => {
    questionInput.value = button.dataset.question;
    questionInput.focus();
  });
});


form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = questionInput.value.trim();

  if (question.length < 3) {
    questionInput.focus();
    return;
  }

  setLoading(true);

  try {
    const response = await fetch("/v1/answers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        role: roleInput.value,
      }),
    });

    if (!response.ok) {
      throw new Error("The assistant could not process this request.");
    }

    const result = await response.json();
    showResult(result);
  } catch (error) {
    showError();
  } finally {
    setLoading(false);
  }
});


function setLoading(isLoading) {
  askButton.disabled = isLoading;
  askButton.querySelector("span").textContent = isLoading
    ? "Finding evidence..."
    : "Ask assistant";
}


function showResult(result) {
  answerText.textContent = result.answer;
  sourceList.replaceChildren();

  groundingBadge.textContent = result.grounded
    ? "✓ Grounded in evidence"
    : "Evidence unavailable";

  groundingBadge.className = result.grounded
    ? "grounding-badge grounded"
    : "grounding-badge not-grounded";

  result.citations.forEach((citation) => {
    const item = document.createElement("li");
    item.textContent = citation;
    sourceList.appendChild(item);
  });

  sourcesSection.hidden = result.citations.length === 0;
  resultPanel.classList.remove("hidden");
  resultPanel.scrollIntoView({
    behavior: "smooth",
    block: "nearest",
  });
}


function showError() {
  showResult({
    answer: (
      "The assistant is temporarily unavailable. " +
      "Please try again shortly."
    ),
    citations: [],
    grounded: false,
  });
}