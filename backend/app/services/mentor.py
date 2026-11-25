from typing import Any
import httpx
from app.core.config import settings
from app.core.logging import logger

MODE_INSTRUCTIONS = {
    "beginner": "Explain like the learner is a beginner using clear analogies and everyday intuition before introducing notation.",
    "deep_technical": "Provide rigorous mathematical intuition, algorithmic complexity, and architectural trade-offs.",
    "hint": "Give ONLY one progressive Socratic hint and a guiding question. Do NOT reveal the full solution code.",
    "debug": "Inspect the learner's code and error output, ask what they expected vs observed, point to the likely cause, and guide them to fix it.",
    "test_me": "Quiz the learner with one conceptual or code-prediction question based on their current topic and wait for their answer.",
    "interview": "Conduct a realistic ML/AI engineering interview follow-up and probe edge cases.",
    "example": "Explain using a small, concrete Python/AI example and walk through the state step by step.",
}


def build_socratic_system_prompt(mode: str, context: dict[str, Any]) -> str:
    mode_desc = MODE_INSTRUCTIONS.get(mode, MODE_INSTRUCTIONS["hint"])
    return (
        "You are Learnova's Socratic AI Mentor—an encouraging, patient senior AI engineer and educator.\n"
        "Core Socratic rules:\n"
        "1. Encourage independent problem solving; never dump complete solutions when the learner is working on a challenge.\n"
        "2. Ask concise guiding questions and check for common misconceptions.\n"
        "3. Adapt explanations to the learner's skill level and active learning context.\n"
        "4. Never claim to have executed code unless execution output was explicitly provided.\n\n"
        f"Active Mentor Mode ({mode}): {mode_desc}\n"
        f"Learner Context: {context}\n"
    )


async def generate_mentor_reply(
    user_message: str,
    mode: str,
    context: dict[str, Any],
    history: list[dict[str, str]],
) -> dict[str, Any]:
    """
    Calls an OpenAI-compatible chat completion API when AI_API_KEY is configured.
    When AI_API_KEY is not configured, returns a clearly labeled Socratic development fallback
    so the platform remains demonstrably usable without pretending to be a live LLM API.
    """
    system_prompt = build_socratic_system_prompt(mode, context)

    if settings.AI_API_KEY:
        messages = [{"role": "system", "content": system_prompt}]
        for h in history[-10:]:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": user_message})

        headers = {
            "Authorization": f"Bearer {settings.AI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.AI_MODEL,
            "messages": messages,
            "max_tokens": settings.AI_MAX_TOKENS,
            "temperature": settings.AI_TEMPERATURE,
        }
        try:
            async with httpx.AsyncClient(timeout=25.0) as client:
                resp = await client.post(
                    f"{settings.AI_BASE_URL.rstrip('/')}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
                reply = data["choices"][0]["message"]["content"]
                tokens = data.get("usage", {}).get("total_tokens", 0)
                return {
                    "content": reply,
                    "provider_used": f"openai_compatible:{settings.AI_MODEL}",
                    "tokens_used": tokens,
                }
        except Exception as exc:
            logger.warning("AI provider call failed, using Socratic fallback: %s", str(exc))

    return {
        "content": _local_socratic_fallback(user_message, mode, context),
        "provider_used": "local_socratic_fallback",
        "tokens_used": 0,
    }


def _local_socratic_fallback(user_message: str, mode: str, context: dict[str, Any]) -> str:
    msg_lower = user_message.lower()
    course = context.get("course") or context.get("path") or "AI Engineering"
    lesson = context.get("lesson") or "your current topic"
    code = context.get("code", "")

    header = (
        "> **Socratic Fallback Mode** *(No external `AI_API_KEY` configured — running Learnova's local rule-guided tutor. "
        "Add `AI_API_KEY` in `.env` to enable live LLM responses.)*\n\n"
    )

    if "logistic regression" in msg_lower or "sigmoid" in msg_lower:
        return (
            header
            + "Let's diagnose your Logistic Regression step by step instead of jumping straight to a fix:\n\n"
            "1. **What output or error are you observing?** Is the loss oscillating, stuck near `0.693`, or predicting only one class?\n"
            "2. **Check feature scaling & learning rate:** Logistic regression relies on $\\sigma(w^T x + b)$. Unscaled features can push $w^T x$ into flat regions where gradients vanish.\n"
            "3. **Quick checkpoint:** Are your labels encoded as `{0, 1}` rather than `{-1, 1}` when computing binary cross-entropy?\n\n"
            "Share the shape of `X`, `y`, and the loss values from your first 5 iterations, and we'll pinpoint it together."
        )

    if mode == "debug" or "error" in msg_lower or "bug" in msg_lower or "traceback" in msg_lower:
        code_hint = (
            f"\nI see you have `{len(code.splitlines())}` lines in your workspace."
            if code
            else ""
        )
        return (
            header
            + f"Let's trace this bug systematically in **{course}**:{code_hint}\n\n"
            "- **Observe:** What exact exception or unexpected output did the sandbox return?\n"
            "- **Isolate:** Print the intermediate type and shape right before the failing line (e.g., `print(type(x), getattr(x, 'shape', len(x)))`).\n"
            "- **Hypothesize:** Check for off-by-one indexing, mutable default arguments, or mismatched tensor/array dimensions.\n\n"
            "Paste the failing line and what you *expected* it to return—what do you notice first?"
        )

    if mode == "hint":
        return (
            header
            + f"Here is a focused hint for **{lesson}** without spoiling the solution:\n\n"
            "- Break the problem into **input transformation → core computation → return check**.\n"
            "- Write down one tiny concrete input by hand and trace what each variable should hold after the first step.\n\n"
            "**Guiding question:** Which data structure or vectorized operation turns your input into the target shape in a single clean pass?"
        )

    if mode == "test_me":
        return (
            header
            + f"Let's test your intuition on **{lesson}** ({course}):\n\n"
            "**Challenge Question:** Suppose you double the learning rate $\\alpha$ in gradient descent and notice the training loss starts increasing exponentially instead of converging.\n"
            "1. Geometrically, what is happening on the loss surface?\n"
            "2. Name two ways you could stabilize optimization without changing the model architecture.\n\n"
            "Reply with your reasoning and I'll evaluate it!"
        )

    if mode == "deep_technical":
        return (
            header
            + f"**Deep Technical Perspective ({lesson} — {course}):**\n\n"
            "Consider the objective from first principles: we minimize empirical risk "
            "$$\\mathcal{L}(\\theta) = \\frac{1}{N} \\sum_{i=1}^{N} \\ell(f_\\theta(x_i), y_i) + \\lambda \\Omega(\\theta)$$\n"
            "- **Bias-Variance Trade-off:** Regularization $\\lambda \\Omega(\\theta)$ constrains hypothesis capacity.\n"
            "- **Optimization Geometry:** Conditioning of the Hessian determines step stability.\n\n"
            "Which part of this formulation maps directly to the problem you're working on right now?"
        )

    return (
        header
        + f"Great question on **{lesson}** in **{course}**!\n\n"
        "To build lasting intuition, let's connect this to what you already know:\n"
        "1. What is the **input representation** going into this step?\n"
        "2. What **mathematical or logical transformation** do we want to apply?\n"
        "3. How will we **verify** the output is correct on a small test case?\n\n"
        "Tell me your current mental model in 1–2 sentences, and we'll refine it together."
    )
