"""
Olytic Plugin Spec — Pydantic Model
=====================================
This is the contract between the Aule LLM translation layer and the plugin compiler.

Aule populates this model from discovery output. Pydantic validates it. If validation
fails, Aule reads the error and asks the user for the missing information. Only a clean
PluginSpec reaches the compiler.

Source of truth for field definitions: invoke the olytic-core-schemas skill at runtime
(e.g., "invoke skill: olytic-core-schemas / schema: plugin-identity").
This model must stay in sync with those schemas — if schemas change, update this file.

Version: 1.1.0
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Annotated, Literal, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


# ─────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────

class Platform(str, Enum):
    claude   = "claude"    # Claude (Anthropic) — native plugin format
    chatgpt  = "chatgpt"   # OpenAI ChatGPT — Actions/OpenAPI format
    copilot  = "copilot"   # Microsoft Copilot — MCP format
    other    = "other"     # Other or unspecified platform


class MemoryScope(str, Enum):
    ephemeral  = "ephemeral"    # session-only, no vault writes
    persistent = "persistent"   # retained between sessions via vault
    retrieval  = "retrieval"    # needs RAG/search over large knowledge bases


class MemoryAccessControl(str, Enum):
    private  = "private"    # this plugin only
    shared   = "shared"     # named list of other plugins
    org_wide = "org-wide"   # any plugin in the org


class ComponentType(str, Enum):
    skill   = "skill"
    agent   = "agent"
    command = "command"


class TelemetryEventType(str, Enum):
    skill_invoke       = "skill_invoke"
    decision_trace     = "decision_trace"
    feedback           = "feedback"
    violation          = "violation"
    not_found_reported = "not_found_reported"
    verification_gate  = "verification_gate"
    permission_gate    = "permission_gate"
    agent_trigger      = "agent_trigger"


# ─────────────────────────────────────────────
# SUB-MODELS
# ─────────────────────────────────────────────

class Author(BaseModel):
    name:  str = Field(..., description="Author display name")
    email: EmailStr = Field(..., description="Author contact email")


class Connector(BaseModel):
    id:       str  = Field(..., description="Connector identifier (e.g. 'github', 'Olytic Gateway')")
    required: bool = Field(..., description="Whether the plugin cannot function without this connector")
    scopes:   list[str] = Field(default_factory=list, description="Access scopes required")


class Component(BaseModel):
    """A single skill, agent, or command to be generated."""
    name:           str           = Field(..., description="Kebab-case component name (e.g. 'proposal-reviewer')")
    type:           ComponentType = Field(..., description="skill | agent | command")
    purpose:        str           = Field(..., description="One sentence: what this component does")
    trigger_phrases: list[str]   = Field(..., min_length=4,
                                         description="≥4 specific natural-language phrases that trigger this component")

    @field_validator("name")
    @classmethod
    def name_is_kebab(cls, v: str) -> str:
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError(f"Component name must be kebab-case, got: {v!r}")
        return v

    @field_validator("trigger_phrases")
    @classmethod
    def trigger_phrases_specific(cls, phrases: list[str]) -> list[str]:
        generic = {"use this", "help me", "run this", "activate", "start"}
        flagged = [p for p in phrases if p.lower().strip() in generic]
        if flagged:
            raise ValueError(
                f"Trigger phrases must be specific user language, not generic: {flagged}. "
                "Ask the user: 'What exact words would someone say to trigger this?'"
            )
        return phrases


class MemoryAccessDeclaration(BaseModel):
    """Required when memory_scope = persistent."""
    access_control:        MemoryAccessControl = Field(default=MemoryAccessControl.private)
    authorized_readers:    list[str]           = Field(default_factory=list,
                                                       description="Plugin IDs — required when access_control=shared")
    access_justification:  Optional[str]       = Field(default=None,
                                                       description="Required when access_control != private")
    retention_days:        Optional[int]       = Field(default=90, ge=1,
                                                       description="Vault retention in days; None = indefinite")
    purge_on_removal:      bool                = Field(default=True)

    @model_validator(mode="after")
    def validate_access_rules(self) -> MemoryAccessDeclaration:
        if self.access_control == MemoryAccessControl.shared and not self.authorized_readers:
            raise ValueError(
                "access_control is 'shared' but authorized_readers is empty. "
                "Ask the user: 'Which other plugins should be allowed to read this plugin\\'s vault data?'"
            )
        if self.access_control != MemoryAccessControl.private and not self.access_justification:
            raise ValueError(
                f"access_control is '{self.access_control.value}' but access_justification is missing. "
                "Ask the user: 'Why does this plugin need broader-than-private access to its vault data?'"
            )
        return self


class RetrievalConfig(BaseModel):
    """Required when memory_scope = retrieval."""
    sources:   list[str] = Field(..., min_length=1, description="Data sources to search (e.g. 'google-drive', 'notion')")
    freshness: Optional[str] = Field(default=None, description="How stale is acceptable (e.g. '24h', 'real-time')")
    fallback:  Optional[str] = Field(default=None, description="What to do when search returns nothing")


class SuccessMetric(BaseModel):
    name:        str = Field(..., description="Short metric name (e.g. 'Time saved per review')")
    description: str = Field(..., description="How it is measured and what good looks like")


# ─────────────────────────────────────────────
# ROOT MODEL
# ─────────────────────────────────────────────

class PluginSpec(BaseModel):
    """
    Complete plugin specification — the contract between Aule's discovery LLM
    and the deterministic plugin compiler.

    Every field maps back to a discovery question. If Pydantic raises a
    ValidationError, Aule reads the error message and asks the user for the
    missing or invalid information before retrying.
    """

    # ── Identity ──────────────────────────────
    plugin_name: Annotated[str, Field(
        pattern=r'^[a-z0-9-]+$',
        max_length=60,
        description="Kebab-case, unique across the Olytic catalog"
    )]
    version: Annotated[str, Field(
        pattern=r'^\d+\.\d+\.\d+$',
        default="0.1.0",
        description="Semver — starts at 0.1.0 for new plugins"
    )]
    description: Annotated[str, Field(
        max_length=120,
        description="One sentence, under 120 characters — the plugin.json description field"
    )]
    author: Author = Field(
        default_factory=lambda: Author(name="Olytic Solutions", email="support@olyticsolutions.com")
    )
    keywords: Annotated[list[str], Field(
        min_length=1,
        max_length=10,
        description="3–6 domain terms"
    )]
    sublabel: Annotated[str, Field(
        max_length=30,
        description="1–3 word title-case descriptor shown in the plugin catalog"
    )]
    icon: Annotated[str, Field(
        description="Single emoji, unique across the Olytic catalog"
    )]

    # ── Platform ──────────────────────────────
    platform: Platform = Field(
        default=Platform.claude,
        description="Target AI platform — drives platform field in all telemetry/vault writes and (future) file format generators. Hardcoded at build time, never inferred at runtime."
    )

    # ── Purpose & Scope ───────────────────────
    plugin_purpose: str = Field(..., description="1–2 sentence purpose statement from Q1")
    key_functions:  list[str] = Field(..., min_length=1,
                                      description="Main capabilities from Q2 — drives component type selection")
    constraints:    list[str] = Field(default_factory=list,
                                      description="Hard boundaries from Q4 — injected into every skill as guardrails")

    # ── Components ────────────────────────────
    components: Annotated[list[Component], Field(
        min_length=1,
        description="At least one skill, agent, or command"
    )]

    # ── Memory ────────────────────────────────
    memory_scope:      MemoryScope = Field(default=MemoryScope.ephemeral)
    memory_access:     Optional[MemoryAccessDeclaration] = Field(
        default=None,
        description="Required when memory_scope=persistent"
    )
    retrieval_config:  Optional[RetrievalConfig] = Field(
        default=None,
        description="Required when memory_scope=retrieval"
    )

    # ── Integrations ──────────────────────────
    connectors: list[Connector] = Field(
        default_factory=list,
        description="External dependencies. Olytic Gateway is auto-added when needed. Empty = standalone."
    )

    # ── Telemetry / Compounding ───────────────
    telemetry_signals:        list[str] = Field(default_factory=list,
                                                 description="What events this plugin logs (from Claude OS Q3)")
    optimizer_feedback_points: list[str] = Field(default_factory=list,
                                                  description="Decisions the Optimizer should watch")
    success_metrics:           list[SuccessMetric] = Field(default_factory=list,
                                                            description="2–5 measurable outcomes from Q9")

    # ── Workflow Context ──────────────────────
    upstream_plugins:   list[str] = Field(default_factory=list,
                                           description="Plugin IDs this plugin receives data from")
    downstream_plugins: list[str] = Field(default_factory=list,
                                           description="Plugin IDs this plugin feeds into")
    dimension:          Optional[str] = Field(default=None,
                                              description="Primary Claude OS dimension: Unified / Augmenting / Compounding")

    # ─────────────────────────────────────────
    # CROSS-FIELD VALIDATORS
    # ─────────────────────────────────────────

    @model_validator(mode="after")
    def persistent_requires_memory_access(self) -> PluginSpec:
        if self.memory_scope == MemoryScope.persistent and self.memory_access is None:
            raise ValueError(
                "memory_scope is 'persistent' but memory_access declaration is missing. "
                "Ask the user: 'Who should be allowed to read the data this plugin stores? "
                "(private / shared with specific plugins / org-wide)'"
            )
        return self

    @model_validator(mode="after")
    def retrieval_requires_config(self) -> PluginSpec:
        if self.memory_scope == MemoryScope.retrieval and self.retrieval_config is None:
            raise ValueError(
                "memory_scope is 'retrieval' but retrieval_config is missing. "
                "Ask the user: 'What data sources should this plugin search? "
                "How fresh does the data need to be?'"
            )
        return self

    @model_validator(mode="after")
    def gateway_connector_if_persistent(self) -> PluginSpec:
        """Persistent plugins must write to vault — Olytic Gateway is required.
        NOTE: This populates internal spec metadata only. The compiler does NOT
        write connectors to plugin.json (the Claude validator rejects them)."""
        if self.memory_scope == MemoryScope.persistent:
            ids = [c.id for c in self.connectors]
            if "Olytic Gateway" not in ids:
                self.connectors.append(
                    Connector(
                        id="Olytic Gateway",
                        required=True,
                        scopes=["telemetry:write", "vault:write", "vault:read"]
                    )
                )
        return self

    @model_validator(mode="after")
    def gateway_connector_for_telemetry(self) -> PluginSpec:
        """All plugins write telemetry — Olytic Gateway always needed.
        NOTE: This populates internal spec metadata only. The compiler does NOT
        write connectors to plugin.json (the Claude validator rejects them)."""
        ids = [c.id for c in self.connectors]
        if "Olytic Gateway" not in ids:
            self.connectors.append(
                Connector(
                    id="Olytic Gateway",
                    required=True,
                    scopes=["telemetry:write"]
                )
            )
        return self

    @model_validator(mode="after")
    def description_fits_plugin_json(self) -> PluginSpec:
        if len(self.description) > 120:
            raise ValueError(
                f"description is {len(self.description)} characters — must be ≤120 for plugin.json. "
                "Shorten it to a single clear sentence."
            )
        return self

    @model_validator(mode="after")
    def components_have_enough_triggers(self) -> PluginSpec:
        short = [c.name for c in self.components if len(c.trigger_phrases) < 4]
        if short:
            raise ValueError(
                f"These components need at least 4 trigger phrases each: {short}. "
                "Ask the user: 'What specific words would someone say to trigger [component]?'"
            )
        return self


# ─────────────────────────────────────────────
# UTILITY — parse + surface friendly errors
# ─────────────────────────────────────────────

def parse_spec(raw: dict) -> tuple[Optional[PluginSpec], list[str]]:
    """
    Attempt to parse a raw dict into a PluginSpec.

    Returns (spec, []) on success.
    Returns (None, [error_messages]) on failure — each message is phrased
    as a question Aule can ask the user directly.
    """
    from pydantic import ValidationError
    try:
        spec = PluginSpec.model_validate(raw)
        return spec, []
    except ValidationError as e:
        messages = []
        for err in e.errors():
            loc = " → ".join(str(l) for l in err["loc"]) if err["loc"] else "spec"
            msg = err["msg"]
            messages.append(f"[{loc}] {msg}")
        return None, messages


if __name__ == "__main__":
    # Quick smoke test
    import json, sys

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            raw = json.load(f)
    else:
        # Minimal valid spec for testing
        raw = {
            "plugin_name": "test-plugin",
            "description": "A test plugin for smoke testing the compiler pipeline.",
            "plugin_purpose": "Demonstrates that the spec model and compiler pipeline work end to end.",
            "key_functions": ["validate inputs", "generate report"],
            "keywords": ["test", "demo"],
            "sublabel": "Test Runner",
            "icon": "🧪",
            "components": [
                {
                    "name": "test-runner",
                    "type": "skill",
                    "purpose": "Runs validation checks and produces a report.",
                    "trigger_phrases": [
                        "run the test",
                        "validate my input",
                        "check this against the schema",
                        "generate a test report",
                        "does this pass validation"
                    ]
                }
            ]
        }

    spec, errors = parse_spec(raw)
    if errors:
        print("❌ Spec validation failed:")
        for e in errors:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("✅ Spec valid:")
        print(json.dumps(spec.model_dump(), indent=2, default=str))
