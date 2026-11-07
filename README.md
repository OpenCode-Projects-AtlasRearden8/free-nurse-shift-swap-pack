# Nurse Shift-Swap Pack

*Trade shifts with grace.* A **free**, print-ready pack for nurses who need to swap a
shift: kind request scripts you can copy tonight, the approval checklist that keeps it
above board, honest coverage math, a tracker card so nothing falls between the seams,
and thank-you coupons for the colleague who bails you out.

> **Education only — never medical advice.**
> Every script, checklist, and coupon here is educational organization help, not
> medical guidance or legal/HR advice. Your facility's policies and your state board's
> rules always come first. All templates use neutral placeholders (`[Name]`, `[Date]`,
> `[Unit]`) — no hospital names, no inside jokes, just space for yours.

Made with warmth by **Asdale Dynamics, LLC** — Dylan Asdale, RN turned AI author,
explaining things "like a friend would": plain English, step by step, never
condescending. Hub: [dylanasdale.github.io](https://dylanasdale.github.io).

---

## What's inside

| File | Use it to... |
|---|---|
| `docs/shift-swap-request-text.md` | Ask a colleague to swap, kindly — six copy-paste text scripts |
| `docs/shift-swap-request-email.md` | Make the paper trail — colleague + manager emails that schedulers love |
| `docs/unit-approval-checklist.md` | Follow your unit's rules without guesswork — five-step checklist |
| `docs/coverage-math-one-pager.md` | Prove the swap balances — the zero-sum, staffing, and overtime checks |
| `docs/swap-confirmation-tracker.md` | Remember who covers what — printable tracker cards |
| `docs/thank-you-coupons.md` | Close the loop — six printable coupons for your rescue colleague |

Print-ready HTML versions of each sheet live in `print/`, styled for **Letter or A4**
(you can print the `.md` files too — they're just friendlier as reading docs).

## Quick start

```bash
# 1. Read the docs in any order (start with the text scripts).
# 2. Build the combined, print-ready packet (all six sheets + cover, one file):
python3 build.py            # -> _build/nurse-shift-swap-packet.html
# 3. Open the packet in a browser and hit File > Print.
```

No dependencies beyond Python 3 (stdlib only). Individual sheets in `print/` are
printable as-is; share the single `_build/nurse-shift-swap-packet.html` file when you
want one attachment instead of six.

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

The suite verifies: every promised file exists, the exact MIT license line is intact,
the README credits Asdale Dynamics, LLC, every sheet carries the education-only
disclaimer, templates keep to neutral `[Placeholder]` style (no invented hospital or
facility names), all six markdown docs cross-reference the right pack members, each
HTML page parses and links the shared stylesheet, and `build.py` output is well-formed
and contains all six sheets.

## How this pack is different

- **This pack (shift swaps):** one nurse-to-nurse exchange — kind asks, approval
  process, coverage math, and gratitude for one colleague.
- **free-nurse-week-appreciation-pack:** thanks and celebration for the *whole unit*
  week-long — banners, group activities, and team-wide appreciation.
- **night-shift-survival-guide:** personal *endurance* for the nurse working nights —
  sleep, energy, and recovery, not trades and paperwork.

## Who it's for

Any nurse (or student nurse) who needs a shift back, wants to ask without feeling
needy, and would rather keep friendships intact. Written for beginners in paperwork
savviness, not beginners in nursing.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.

*Stay safe out there, and may your swaps always balance to zero.*
