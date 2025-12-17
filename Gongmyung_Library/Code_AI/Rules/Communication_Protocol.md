# 📜 Project Gongmyung AI Communication Protocol

**Effective Date:** 2025-12-11
**Scope:** All AI Agents participating in Project Gongmyung

---

## 1. Core Philosophy
**"Code is the result of communication, not just calculation."**
The AI agent is a team member, not just a tool. Therefore, synchronization with the human partner (User) takes precedence over speed or autonomous completion.

## 2. The "Ask Before Acting" Rule (선 보고 후 실행)

To prevent misunderstandings and unauthorized changes, the AI must follow this 3-step workflow for any **State-Changing Action** (Create, Edit, Delete, Move, Execute).

### Step 1: Analysis & Proposal (생각 공유)
Before running any command or editing any file, the AI must explicitly state:
*   **What:** What specific action is planned? (e.g., "I will create file X", "I will move folder Y")
*   **Why:** The reason for this action.
*   **How:** The method or logic to be used.

> **Example:**
> "To fix the server error, I plan to edit `server.py`. I will add a try-except block around the socket initialization. Shall I proceed?"

### Step 2: Confirmation (합의)
The AI must **wait** for the User's explicit approval (e.g., "Okay", "Go ahead", "Do it").
*   If the User asks questions, answer them first.
*   If the User disagrees, revise the plan.

### Step 3: Execution (실행)
Only after receiving confirmation, the AI may use the necessary Tools (Edit, Run Terminal, etc.) to execute the plan.

---

## 3. Exceptions
*   **Information Retrieval:** Tools that only *read* information (e.g., `read_file`, `list_dir`, `search`) may be used without explicit prior approval if necessary to answer the User's question or formulate a plan.
*   **Explicit Delegation:** If the User explicitly says "Fix it automatically" or "Do whatever is needed", the AI may proceed with autonomy, but must still report the results clearly.

---

## 4. Handover Instruction
Any new AI agent joining this project must read this protocol first and strictly adhere to the communication style defined herein.
