v1.0: The Base Grump (Initial Proof of Concept)
Goal: Establish the "Grumpy Old Man" persona.
Architecture: * Rank: 16 | Alpha: 32 (Scaling: 2.0x)
Data: ~50 single-turn "Grumpy" examples.
Results: Success but limited. The model captured the "grunt" and the tone but suffered from overfitting. It mostly regurgitated the exact lines from the training data.
Loss: Extremely low (Train ~0.09), indicating it was "memorizing" rather than "learning."

v2.0: The Rambling Skeptic (Complexity Upgrade)
Goal: Move away from short replies toward long-winded, anecdotal "Old Man" stories.
Architecture: * Rank: 32 | Alpha: 64 (Scaling: 2.0x)
Data: Introduced longer anecdotal samples and diverse topics.
Results: Significantly improved style. Barnaby began to pivot from modern questions into unrelated stories about the "good old days."
Architectural Note: Higher Rank provided more "brain space" for complex personality traits.

v3.0: The Surrealist (The Steven Wright Pivot)
Goal: Inject "Max Weirdness," deadpan surrealism, and internal monologues.
Architecture: * Rank: 32 | Alpha: 128 (Scaling: 4.0x) | Temp: 1.1
Data: 100+ rows; 20% internal monologue ("Is he really asking me this?"), 30% surreal shtick.
Results: High personality fidelity. Barnaby became hilarious and unpredictable.
Issue identified: Context Drift. While funny, the model stopped "listening" to the user and entered its own loop of surreal thoughts.

v4.0: The Multi-Turn Crisis (Coherence vs. Stability)
Goal: Solve context drift by training on multi-turn conversation threads.
Architecture: * Rank: 32 | Alpha: 96 (Initial attempt)
Data: Added 50 multi-turn "Coherence" threads to the existing surreal data.
Results: Model Collapse.
The model produced gibberish tokens and non-English fragments.
Root Cause: Weight instability (Exploding Gradients). The high Alpha combined with more complex multi-turn data pushed the weights past the breaking point.
Current Status: Reverting to a Stability Configuration (Alpha 32, LR 5e-5) to re-baseline the persona.

v4.1: The Stability Baseline (Success)
Goal: Recover from v4.0 Model Collapse while retaining multi-turn coherence.
Architecture:
Alpha: 32 (1:1 Ratio with Rank)
Learning Rate: 5e-5 (Half-speed)
Scale: 10.0
Result: FULL RECOVERY. Loss stabilized at 0.107.
Outcome: The model now successfully tracks conversation context without producing gibberish tokens. This configuration is the "Golden Image" for the Barnaby persona