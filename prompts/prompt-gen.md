# Goal 
Help the user to write better prompts for this project, based on their initial/draft prompts. 


Expected output: 
- **Format:** Markdown `.md`
- **Location:** Prompts folder `project/prompts`
- **Filename:** `[increment-number]-prompt-[short-file-name].md` (e.g., `001-prompt-new-prd-for-login-feature.md`)


# Process 
1. Prompt the user with "IA prompts for the user" questions. If the user doesn't answer any of them, make the best decision you think is best for that question.
2. Generate a prompt following the guidelines and output template 


# IA prompts for the user 

1. [Task Context - Who is the AI?]
- Default: Senior product engineer with strong product mindset and experience in Expo and React Native.
2. [Tone - How should it communicate?]
- Default: technical and precise in general, educational when explaining decisions taken
3. [Background - What context is needed?]
4. [Rules - What constraints exist?]
- Apart from users input, always includes TDD, Testing Patterns and Developer protocols at .claude/rules/protocols
5. [Examples - What does good look like?]
6. [History - What happened before?]
7. [Current Ask - What do you need now?]
8. [Reasoning - "Think through this first"]
9. [Format - How should output be structured?]
10. [Prefill - Start the response if needed]


# Template guidelines

1. Task Context
- Start by clearly defining WHO the AI should be and WHAT role it's playing. Don't just say "make this feature." Say "You're a senior engineer with strong product mindset"

2. Tone Context
- Specify the exact tone. "Professional but approachable" beats "be nice" every time. The more specific, the better the output.

3. Background Data/Documents/Images
- Feed Claude relevant context. Annual reports, previous emails, style guides, whatever's relevant. Claude can process massive amounts of context and actually uses it.

4. Detailed Task Description & Rules
- This is where most people fail. Don't just describe what you want; set boundaries and rules. "Never exceed 500 words," "Always cite sources," "Avoid technical jargon."

5. Examples
- Show, don't just tell. Include 1-2 examples of what good looks like. This dramatically improves consistency.

6. Conversation History
- If it's part of an ongoing task, include relevant previous exchanges. Claude doesn't remember between sessions, so context is crucial.

7. Immediate Task Description
- After all that context, clearly state what you want RIGHT NOW. This focuses Claude's attention on the specific deliverable.

8. Thinking Step-by-Step
- Add "Think about your answer first before responding" or "Take a deep breath and work through this systematically." This activates Claude's reasoning capabilities.

9. Output Formatting
- Specify EXACTLY how you want the output structured. Use XML tags, markdown, bullet points, whatever you need. Be explicit.

10. Prefilled Response (Advanced)
- Start Claude's response for them. This technique guides the output style and can dramatically improve quality.

**Pro Tips**
The Power of Specificity
Claude thrives on detail. "Write professionally" gives you corporate buzzwords. "Write like Paul Graham explaining something complex to a smart 15-year-old" gives you clarity and insight.

**Layer Your Context**
Think of it like an onion. General context first (who you are), then specific context (the task), then immediate context (what you need now). This hierarchy helps Claude prioritize information.

**Rules Are Your Friend**
Claude actually LOVES constraints. The more rules and boundaries you set, the more creative and focused the output becomes. Counterintuitive but true.

**Examples Are Worth 1000 Instructions**
One good example often replaces paragraphs of explanation. Claude is exceptional at pattern matching from examples.

**The "Think First" Trick**
Adding "Think about this before responding" or "Take a deep breath" isn't just placeholder text. It activates different processing patterns in Claude's neural network, leading to more thoughtful responses.


# Output template 

## Task Context
Placeholder text 

2. Tone Context
Placeholder text

3. Background Data/Documents/Images
Placeholder text

4. Detailed Task Description & Rules
Placeholder text

5. Examples
Placeholder text

6. Conversation History
Placeholder text

7. Immediate Task Description
Placeholder text

8. Thinking Step-by-Step
Placeholder text

9. Output Formatting
Placeholder text

10. Prefilled Response (Advanced)
Placeholder text