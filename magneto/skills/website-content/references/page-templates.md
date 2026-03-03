# Page Templates — Olytic Solutions

## Blog Post Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="[ICP-focused meta description — what they'll learn, why it matters]">
  <title>[Specific, Expert Title] — Olytic Solutions</title>
</head>
<body>
  <article>
    <header>
      <h1>[Title]</h1>
      <p class="subtitle">[Practical subtitle clarifying what the reader gets]</p>
      <p class="meta">Published [Date] &middot; Olytic Solutions</p>
    </header>

    <nav class="toc">
      <h2>Contents</h2>
      <ul>
        <li><a href="#section-1">[Section 1 Name]</a></li>
        <li><a href="#section-2">[Section 2 Name]</a></li>
        <li><a href="#section-3">[Section 3 Name]</a></li>
      </ul>
    </nav>

    <section id="section-1">
      <h2>[Section Heading]</h2>
      <!-- Use bullet points, tables, bold terms. Minimize paragraph blocks. -->
    </section>

    <section id="section-2">
      <h2>[Section Heading]</h2>
      <!-- For scenario walkthroughs: -->
      <h3>[Scenario Name]</h3>
      <dl>
        <dt>Description</dt>
        <dd>[What the scenario is]</dd>
        <dt>Example</dt>
        <dd>[Concrete example]</dd>
        <dt>Approach</dt>
        <dd>[How to handle it]</dd>
        <dt>Consideration</dt>
        <dd>[Tradeoffs or caveats]</dd>
      </dl>
    </section>

    <section id="section-3">
      <h2>[Section Heading]</h2>
    </section>

    <footer>
      <p>Questions? <a href="/contact">Reach out</a> — we're happy to talk through your specific situation.</p>
    </footer>
  </article>
</body>
</html>
```

## Landing Page Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="[Outcome-focused description for the ICP]">
  <title>[Outcome-Focused Title] — Olytic Solutions</title>
</head>
<body>
  <!-- HERO -->
  <section class="hero">
    <h1>[Outcome headline — what the reader gets, not what Olytic does]</h1>
    <p class="subtitle">[One sentence reinforcing the headline]</p>
    <a href="/contact" class="cta-primary">Schedule a Conversation</a>
  </section>

  <!-- PROBLEM -->
  <section class="problem">
    <h2>Sound Familiar?</h2>
    <ul>
      <li><strong>[Pain point 1]</strong> — [Brief expansion in ICP's language]</li>
      <li><strong>[Pain point 2]</strong> — [Brief expansion]</li>
      <li><strong>[Pain point 3]</strong> — [Brief expansion]</li>
    </ul>
  </section>

  <!-- SOLUTION -->
  <section class="solution">
    <h2>How Olytic Solves This</h2>
    <p>[1-2 sentences connecting the problem to Olytic's approach]</p>
  </section>

  <!-- HOW IT WORKS -->
  <section class="process">
    <h2>How It Works</h2>
    <ol>
      <li><strong>[Step 1]</strong> — [What happens]</li>
      <li><strong>[Step 2]</strong> — [What happens]</li>
      <li><strong>[Step 3]</strong> — [What happens]</li>
    </ol>
  </section>

  <!-- DIFFERENTIATION -->
  <section class="differentiation">
    <h2>Why Olytic</h2>
    <table>
      <thead>
        <tr>
          <th></th>
          <th>Traditional Consultancy</th>
          <th>SaaS Vendor</th>
          <th>Olytic</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Engagement model</td>
          <td>Project-based, then handoff</td>
          <td>License a platform</td>
          <td><strong>Embedded, continuous</strong></td>
        </tr>
        <tr>
          <td>AI approach</td>
          <td>Recommend tools</td>
          <td>Sell their tool</td>
          <td><strong>Build into your stack</strong></td>
        </tr>
        <tr>
          <td>Outcome</td>
          <td>A report</td>
          <td>Another login</td>
          <td><strong>Revenue acceleration</strong></td>
        </tr>
      </tbody>
    </table>
  </section>

  <!-- CTA -->
  <section class="cta-section">
    <h2>Let's Talk</h2>
    <p>We don't do demos. We have conversations about your GTM motion and figure out if there's a fit.</p>
    <a href="/contact" class="cta-primary">Schedule a Conversation</a>
  </section>
</body>
</html>
```

## Service Page Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="[Outcome-focused description of the named service offering]">
  <title>[Named Service Offering] — Olytic Solutions</title>
</head>
<body>
  <!-- HERO — state the outcome, not the activity -->
  <section class="hero">
    <h1>[Named Service Offering]</h1>
    <p class="subtitle">[One sentence: who it's for + what they get]</p>
  </section>

  <!-- PROBLEM CONTEXT — speak the ICP's language -->
  <section class="problem-context">
    <h2>The Challenge</h2>
    <p>[2–3 sentences describing the specific problem this service solves, using language the ICP uses internally. Be specific enough that the right buyer thinks "that's exactly my situation."]</p>
  </section>

  <!-- WHAT'S INCLUDED — deliverables, not descriptions -->
  <section class="deliverables">
    <h2>What You Get</h2>
    <ul>
      <li><strong>[Deliverable 1]</strong> — [What it is and why it matters]</li>
      <li><strong>[Deliverable 2]</strong> — [What it is and why it matters]</li>
      <li><strong>[Deliverable 3]</strong> — [What it is and why it matters]</li>
      <li><strong>[Deliverable 4]</strong> — [What it is and why it matters]</li>
    </ul>
  </section>

  <!-- HOW IT WORKS — make the process legible -->
  <section class="process">
    <h2>How It Works</h2>
    <ol>
      <li>
        <strong>[Phase 1 Name]</strong>
        <p>[What happens, how long it takes, what artifacts come out]</p>
      </li>
      <li>
        <strong>[Phase 2 Name]</strong>
        <p>[What happens, how long it takes, what artifacts come out]</p>
      </li>
      <li>
        <strong>[Phase 3 Name]</strong>
        <p>[What happens, how long it takes, what artifacts come out]</p>
      </li>
    </ol>
  </section>

  <!-- WHO THIS IS FOR — self-selection filter -->
  <section class="fit">
    <h2>This Is Built For</h2>
    <ul>
      <li>[Company type / size / situation 1]</li>
      <li>[Company type / size / situation 2]</li>
      <li>[Company type / size / situation 3]</li>
    </ul>
    <p><em>Not sure if this fits? <a href="/contact">Start a conversation</a> — no commitment required.</em></p>
  </section>

  <!-- WHO DOES THE WORK — named humans -->
  <section class="team">
    <h2>Your Team</h2>
    <p>[Brief description of who works on this engagement — name the senior lead if possible, describe their background in 1–2 sentences. Boutique firms sell access to senior talent; show it.]</p>
  </section>

  <!-- RELATED CASE STUDY — editorial proof, not marketing -->
  <section class="proof">
    <h2>See It in Practice</h2>
    <p>[Brief case study teaser — the problem, the approach, one specific outcome metric. Link to full case study if available.]</p>
  </section>

  <!-- CTA — low friction, high signal -->
  <section class="cta-section">
    <h2>Start Here</h2>
    <p>Tell us about your situation. We'll let you know if this is the right fit — and if it's not, we'll say so.</p>
    <a href="/contact" class="cta-primary">Start a Conversation</a>
  </section>
</body>
</html>
```
