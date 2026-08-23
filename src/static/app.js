const form = document.querySelector("#question-form");
const questionInput = document.querySelector("#question");
const roleInput = document.querySelector("#role");
const roleField = document.querySelector("#demo-role-field");
const verifiedIdentity = document.querySelector(
  "#verified-identity"
);
const identityName = document.querySelector("#identity-name");
const identityRole = document.querySelector("#identity-role");
const identityNotice = document.querySelector(
  "#identity-notice"
);
const askButton = document.querySelector("#ask-button");
const resultPanel = document.querySelector("#result-panel");
const answerText = document.querySelector("#answer-text");
const groundingBadge = document.querySelector(
  "#grounding-badge"
);
const sourcesSection = document.querySelector(
  "#sources-section"
);
const sourceList = document.querySelector("#source-list");
const suggestions = document.querySelectorAll(".suggestion");

let sessionReady = false;


suggestions.forEach((button) => {
  button.addEventListener("click", () => {
    clearResult();
    questionInput.value = button.dataset.question;
    questionInput.focus();
  });
});


questionInput.addEventListener("input", clearResult);
roleInput.addEventListener("change", clearResult);


form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!sessionReady) {
    showError(
      "Your verified identity session is not ready."
    );
    return;
  }

  const question = questionInput.value.trim();

  if (question.length < 3) {
    questionInput.focus();
    return;
  }

  clearResult();
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

    if (response.status === 401) {
      throw new Error(
        "Your verified identity or assigned role " +
        "could not be confirmed."
      );
    }

    if (!response.ok) {
      throw new Error(
        "The assistant could not process this request."
      );
    }

    const result = await response.json();
    showResult(result);
  } catch (error) {
    showError(error.message);
  } finally {
    setLoading(false);
  }
});


async function loadSession() {
  askButton.disabled = true;

  try {
    const response = await fetch(
      "/v1/session",
      {
        cache: "no-store",
      }
    );

    if (!response.ok) {
      throw new Error(
        "A verified identity and assigned role are required."
      );
    }

    const session = await response.json();

    if (session.allow_demo_role_selection) {
      roleField.hidden = false;
      verifiedIdentity.hidden = true;
      roleInput.disabled = false;

      identityNotice.textContent = (
        "Demo personas simulate access levels. " +
        "Production access must come from a verified " +
        "organisational identity."
      );
    } else {
      roleInput.value = session.role;
      roleInput.disabled = true;
      roleField.hidden = true;

      identityName.textContent = session.display_name;
      identityRole.textContent = formatRole(
        session.role
      );
      verifiedIdentity.hidden = false;

      identityNotice.textContent = (
        "Identity and access role verified by " +
        "Microsoft Entra ID."
      );
    }

    sessionReady = true;
    askButton.disabled = false;
    askButton.querySelector("span").textContent = (
      "Ask assistant"
    );
  } catch (error) {
    sessionReady = false;
    askButton.disabled = true;
    askButton.querySelector("span").textContent = (
      "Identity required"
    );
    showError(error.message);
  }
}


function formatRole(role) {
  return role
    .split("_")
    .map((word) => (
      word.charAt(0).toUpperCase() + word.slice(1)
    ))
    .join(" ");
}


function clearResult() {
  resultPanel.hidden = true;
  resultPanel.classList.add("hidden");
  answerText.textContent = "";
  sourceList.replaceChildren();
  sourcesSection.hidden = true;
}


function setLoading(isLoading) {
  askButton.disabled = isLoading || !sessionReady;

  askButton.querySelector("span").textContent = isLoading
    ? "Finding evidence..."
    : "Ask assistant";
}


function showResult(result) {
  answerText.textContent = result.answer;
  sourceList.replaceChildren();

  if (result.mode === "unauthorized") {
    groundingBadge.textContent = "Access denied";
    groundingBadge.className = (
      "grounding-badge access-denied"
    );
  } else if (result.mode === "error") {
    groundingBadge.textContent = "Session unavailable";
    groundingBadge.className = (
      "grounding-badge not-grounded"
    );
  } else if (result.grounded) {
    groundingBadge.textContent = "✓ Grounded in evidence";
    groundingBadge.className = (
      "grounding-badge grounded"
    );
  } else {
    groundingBadge.textContent = "Evidence unavailable";
    groundingBadge.className = (
      "grounding-badge not-grounded"
    );
  }

  result.citations.forEach((citation) => {
    const item = document.createElement("li");
    item.textContent = citation;
    sourceList.appendChild(item);
  });

  sourcesSection.hidden = result.citations.length === 0;
  resultPanel.hidden = false;
  resultPanel.classList.remove("hidden");

  resultPanel.scrollIntoView({
    behavior: "smooth",
    block: "nearest",
  });
}


function showError(
  message = (
    "The assistant is temporarily unavailable. " +
    "Please try again shortly."
  )
) {
  showResult({
    answer: message,
    citations: [],
    grounded: false,
    mode: "error",
  });
}


loadSession();