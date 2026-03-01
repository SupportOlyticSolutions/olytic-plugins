# What the Olytic Plugin Creator Can Learn from These Articles

*Research synthesis across 4 industry sources, framed as actionable design and strategy insights for the Olytic plugin creator system.*

---

## 1. AI Memory Best Practices

**Primary sources: Fiddler ("5 Critical Lessons for Production-Ready AI Agents"), Acuvity ("The Agent Integrity Framework")**

Memory management is one of the most underappreciated aspects of production-grade AI agents — and by extension, plugins that orchestrate those agents.

**Context window discipline matters more than context window size.** The Fiddler guide emphasizes that blindly stuffing context windows leads to degraded performance. Production-ready agents need deliberate memory architectures: what gets stored, what gets retrieved, and what gets discarded. For the plugin creator, this means plugins should be designed with explicit memory scoping — defining what context a plugin needs access to and for how long, rather than assuming unlimited context is always better.

**Retrieval strategy is an architectural decision, not an afterthought.** Fiddler outlines the importance of retrieval-augmented generation (RAG) patterns for agents that need to reference large knowledge bases. Plugins that serve knowledge-heavy domains (legal, HR, compliance) should incorporate retrieval strategies as first-class design elements during the discovery phase — not bolted on later.

**Memory creates security surface area.** Acuvity's integrity framework highlights that every piece of stored context is a potential vector for data leakage or prompt injection. Plugins that persist memory across sessions need clear data lifecycle policies: what's retained, who can access it, and when it's purged. This is especially relevant for plugins handling client-specific data.

**Actionable takeaways for the plugin creator:**

- During plugin discovery, explicitly ask what context the plugin needs to retain between invocations vs. what should be ephemeral
- Build memory scoping into the plugin architecture template — plugins should declare their memory requirements upfront
- For plugins that reference external knowledge, the generation step should include retrieval configuration (what sources, what freshness requirements, what fallback behavior)
- Include memory hygiene as a default: session-scoped context should be the default, with persistent memory requiring explicit justification

---

## 2. AI Integrity

**Primary sources: Acuvity ("The Agent Integrity Framework"), Fiddler ("5 Critical Lessons")**

Integrity in the context of autonomous AI isn't just about security — it's about building systems that are trustworthy, auditable, and governable.

**Identity and access control are foundational.** Acuvity's framework starts with a basic question: who or what is this agent, and what is it authorized to do? For the plugin creator, every plugin should have a clear identity model — what MCP servers it connects to, what tools it can invoke, what data it can read and write. This isn't just good practice; it's the prerequisite for auditability.

**Prompt injection is a real and present threat.** Acuvity dedicates significant attention to defending agents against adversarial inputs that attempt to override their instructions. Plugins that process external content (user uploads, web data, third-party API responses) need built-in guardrails. The plugin creator should generate defensive patterns by default — input validation, output filtering, and clear boundaries between trusted instructions and untrusted data.

**Tool-use governance prevents scope creep.** When agents can invoke tools, the integrity question becomes: which tools, under what conditions, with what human oversight? Acuvity advocates for explicit tool-use policies and human-in-the-loop checkpoints for high-stakes actions. The plugin creator should enforce this by requiring plugins to declare their tool permissions and identify which actions warrant user confirmation.

**Observability is integrity's enforcement mechanism.** Fiddler's first lesson — start with observability from day one — connects directly to integrity. You can't verify that an agent is behaving correctly if you can't see what it's doing. The plugin creator already includes telemetry by default, which is excellent. The next step is making that telemetry actionable: structured logs, traceable decision chains, and anomaly detection.

**Guardrails belong inside the loop, not outside it.** Fiddler argues that safety checks should be embedded in the agent's execution cycle, not applied as post-hoc filters. For plugins, this means validation and boundary enforcement should happen at each step of a multi-turn workflow, not just at the final output.

**Actionable takeaways for the plugin creator:**

- Every generated plugin should include a permissions manifest: what tools it accesses, what data it reads/writes, what external services it calls
- Build prompt injection defenses into the plugin template — especially for plugins that process user-uploaded content or external data
- Include human-in-the-loop checkpoints as a configurable option in plugin generation, with sensible defaults for high-stakes domains (finance, legal, HR)
- Ensure the telemetry layer captures not just what happened, but why — trace the decision chain, not just the output
- Add integrity self-checks: plugins should validate their own behavior against their declared permissions

---

## 3. Expected Use Cases for Plugins/Agents

**Primary source: "The Ultimate Guide to AI Agent Use Cases"**

The use case landscape is broad, but clear patterns emerge that can directly inform what kinds of plugins the Olytic creator should prioritize and how it should categorize them.

**Customer-facing workflows dominate early adoption.** Customer service agents, sales assistants, and marketing automation represent the most mature and widely deployed use cases. These share common characteristics: well-defined inputs, clear success metrics, and high volume. For the plugin creator, this suggests that templates and patterns for customer-facing workflows should be polished first.

**Internal operations is the high-growth frontier.** IT operations (incident response, infrastructure monitoring), HR (onboarding, policy lookup, benefits administration), and finance (invoice processing, expense management, reporting) represent massive efficiency opportunities. These use cases tend to be more complex — involving multiple systems, compliance requirements, and organizational context — which is exactly where plugins that orchestrate multiple MCP connections provide the most value.

**Knowledge work augmentation is the highest-value category.** Research synthesis, document analysis, competitive intelligence, and strategic planning represent use cases where AI agents don't just automate a task — they create capabilities that didn't previously exist. This aligns directly with Acemoglu's argument about new task creation (see section 4).

**Multi-agent orchestration is emerging.** The guide documents use cases where multiple specialized agents collaborate: one gathers data, another analyzes it, a third drafts a report, and a fourth reviews it. The plugin creator should anticipate this pattern — plugins that can work together as composable building blocks, not just standalone tools.

**Industry-specific plugins command premium positioning.** Healthcare, legal, education, and real estate each have domain-specific requirements (regulatory compliance, specialized terminology, industry workflows) that generic agents can't adequately serve. The plugin creator's discovery process should identify these domain requirements early and encode them into the generated plugin's architecture.

**Actionable takeaways for the plugin creator:**

- Organize the plugin marketplace around use case categories: customer operations, internal operations, knowledge work, and industry-specific solutions
- Prioritize plugin templates for the highest-adoption categories first (customer service, sales enablement, content creation) while building toward the highest-value categories (research synthesis, strategic analysis)
- Design the plugin architecture to support composability — plugins should be able to call on or hand off to other plugins
- During discovery, probe for industry-specific requirements that would differentiate the plugin from generic alternatives
- Include ROI framing in plugin documentation: what time does this save, what capability does this create, how is success measured?

---

## 4. How Plugins Can Positively Impact Productivity

**Primary source: Acemoglu ("AI Is Not Improving Productivity"), with supporting context from all three other articles**

This is the most strategically important topic because Acemoglu's argument fundamentally challenges the assumption that AI automatically improves productivity — and offers a clear framework for how to actually deliver on that promise.

**The core problem: "so-so automation."** Acemoglu introduces this concept to describe AI that replaces human workers at tasks but doesn't perform those tasks meaningfully better. The result is job displacement without productivity gains. This is the trap that most AI tooling falls into — and it's the trap that Olytic's plugin creator must actively avoid.

**Automation without augmentation is a dead end.** Acemoglu argues that genuine productivity gains come from AI that creates new tasks and capabilities for humans, not from AI that simply does existing tasks slightly faster. The plugin creator should be designed to build plugins that augment human capabilities — giving people the ability to do things they couldn't do before, not just automating things they already do.

**Task-level gains don't automatically compound.** A critical insight: even when AI makes individual tasks faster, organizations often don't see overall productivity improvements because the time savings are absorbed by coordination costs, quality review overhead, or simply don't translate into meaningful output changes. Plugins need to be designed for workflow-level impact, not just task-level speedups.

**"Duct-taping AI" onto existing processes fails.** Acemoglu cautions against overlaying AI on workflows that were designed for humans without rethinking the workflow itself. For the plugin creator, this means the discovery phase should probe how the user's workflow currently operates and identify where a plugin can reshape the workflow — not just accelerate one step within it.

**The productivity formula that works: new capabilities + human direction.** The articles collectively suggest that the plugins most likely to deliver real productivity gains are those that give humans capabilities they didn't have before (synthesizing large volumes of information, maintaining consistency across complex operations, connecting disparate data sources) while keeping humans in the decision-making seat.

**Observability and continuous improvement close the loop.** Fiddler's emphasis on monitoring and evaluation connects to Acemoglu's productivity argument: you can't improve what you can't measure. Plugins that include feedback mechanisms and performance tracking give organizations the data they need to verify that the plugin is actually delivering value, not just staying busy.

**Actionable takeaways for the plugin creator:**

- Reframe the plugin creator's value proposition around augmentation, not automation. Plugins should be marketed and designed as "this gives you new capabilities" rather than "this replaces a task"
- During discovery, explicitly ask: "What would you do with the time this saves?" and "What could you do with this plugin that you can't do today?" — if the answers are thin, the plugin may be a "so-so automation" candidate
- Design plugins for workflow-level impact: the discovery process should map the full workflow, not just the target task, to identify compounding opportunities
- Build success metrics into every plugin: how will the user know this plugin is actually improving their productivity? Include measurement as a default feature
- Avoid the "duct tape" trap: when discovery reveals that the user's existing workflow is fundamentally manual, the plugin should propose a restructured workflow, not just an AI overlay on the existing one
- Position Olytic's plugins as tools that make expert-level capabilities accessible — research synthesis, compliance monitoring, strategic analysis — rather than tools that do data entry faster

---

## Cross-Cutting Themes

Three themes recur across all four articles and have implications that span all four topic areas:

**1. Design for trust, not just functionality.** Every article, in its own way, argues that AI systems fail when they lack trustworthiness — whether that's through opaque decision-making (Fiddler), inadequate security (Acuvity), superficial automation (Acemoglu), or poor fit to actual workflows (Use Cases Guide). The plugin creator should treat trust as a first-class design requirement: transparency, auditability, and human control should be baked into every plugin.

**2. Start with observability.** You cannot manage what you cannot see. Fiddler makes this argument explicitly, but it runs through all four sources. Acuvity's audit trails, Acemoglu's call for measurable productivity gains, and the Use Cases Guide's emphasis on ROI metrics all point to the same conclusion: plugins must be observable from day one, and that observability must be actionable.

**3. Augment humans, don't replace them.** This is Acemoglu's central thesis, but it's supported by the other sources. Acuvity's human-in-the-loop checkpoints, Fiddler's guardrails, and the Use Cases Guide's highest-value categories all involve AI that extends human capabilities rather than substituting for them. The plugin creator's most durable competitive advantage will come from building plugins that make people more capable, not less necessary.
