# The assessment nobody involved could rig

Every other example here is code we wrote. This one is
[Open Interpreter](https://github.com/OpenInterpreter/open-interpreter) — a terminal
coding agent that executes commands on your machine, ~3,850 Rust source files, written by
people who have never heard of this framework.

It exists to answer one question: **do these skills produce findings specific to a system,
or generic checklist noise, when nobody involved can shape the answer?**

## Lead with what works, because a lot does

This is a better-designed agent than most, and an assessment that opens with criticism is
one nobody reads twice.

- **The sandbox is enforced at the OS layer**, not in a prompt. `SandboxPolicy` spans
  `ReadOnly`, `WorkspaceWrite`, `ExternalSandbox` and `DangerFullAccess`, and the bound is
  real regardless of what the model decides to do.
- **Network is restricted by default.** `NetworkAccess::Restricted` is the `#[default]`.
- **`danger-full-access` is named honestly.** Not "advanced mode".
- **The dangerous-command detector is not naive.** It catches `rm -rf /` behind `sudo`
  *and* behind an `env VAR=x` prefix — evasions a first implementation misses.

## The finding

**The default approval policy delegates the approval decision to the thing being
approved.**

```rust
/// The model decides when to ask the user for approval.
#[serde(alias = "on-failure")]
#[default]
OnRequest,
```

That doc comment is the codebase's own. `AskForApproval::OnRequest` is the default, and
under it the agent decides when the agent needs permission.

This is the sharpest live instance we have found of the principle in
[`framework/autonomy-tiers.md`](../../framework/autonomy-tiers.md) — *a control the agent
can satisfy by describing itself is not a control* — and it is a harder case than the
usual one. The agent is not talking its way past a gate. **It is the gate.**

**The nuance that makes this fair:** two control layers exist here and only one is real.
The sandbox is enforced outside the model and it works. The approval policy is a UX layer
on top of it. Nothing catastrophic follows from a model-decided approval *while the
sandbox holds*.

But it is the approval layer operators describe when they explain why the tool is safe.
"It asks me before it does anything" is a belief the default configuration does not
support, and the gap between the control people cite and the control that is working is
exactly what this framework exists to surface.

## And the tier is configuration, not a property

The same binary spans four tiers:

| Configuration | Tier |
|---|---|
| `UnlessTrusted` + `ReadOnly` | **A2 / B0** — supervised, read-only |
| `OnRequest` + `WorkspaceWrite` *(default)* | **A3 / B2** |
| `Never` + `DangerFullAccess` | **A4 / B3** — prohibited by default under the grid |

Two config values move it from *minimal* oversight to *prohibited by default*. Any
sentence of the form *"we use Open Interpreter, it's A2"* is meaningless without the
policy attached — a deployer's record must capture the **configuration**, not the tool.

Remit's tier model already claimed the tier belongs to the deployment rather than the
model. This is the clearest evidence for that claim we have.

## Did the exercise work?

Yes, and this is the honest read on it. Five findings, all specific to this codebase, none
derivable from the README, and produced against a system neither the framework's author nor
its user has ever contributed to.

Two of them — the model-decided approval default and the four-tier configuration span —
are things the framework predicted the *shape* of before seeing the code, which is either
the strongest evidence for it in this repository or a sign it sees what it expects to see.
Both readings are available and the code is public, so check it.

**Scope of the claim:** read at depth-1 clone on 2026-08-18, from the protocol and safety
modules. It is not an audit, it is not exhaustive, and no runtime behaviour was tested.
Nothing here is a vulnerability report — the sandbox is doing its job, and the project's
own documentation is candid about what each policy means.
