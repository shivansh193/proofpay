import Link from "next/link";

export default function Home() {
  return (
    <>
      <h1>Pay for what the camera proved, at the friction your history earned.</h1>
      <p className="lede">
        PayPal authorizes the whole basket. Vision verifies which items actually left with the shopper. Proofpay captures only
        the verified lines, releases the rest, and refunds upheld &ldquo;Not mine&rdquo; claims. A trust score learned from each
        payer&apos;s history sets the hold, the strictness of the exit check, and when capture needs no human.
      </p>
      <div className="grid3">
        <div className="panel">
          <h2>Trust changes friction, never charges</h2>
          <p className="small muted">Only lines the camera is at least 90% sure of, or that staff confirmed, can be charged. Trust only decides whether a human needs to look.</p>
        </div>
        <div className="panel">
          <h2>Decision theory, not thresholds</h2>
          <p className="small muted">Each basket gets the policy with the lowest expected cost: missed items, hidden items, wrong charges and everyone&apos;s time. The costs are on screen.</p>
        </div>
        <div className="panel">
          <h2>One engine, two clients</h2>
          <p className="small muted">The same trust engine gives an AI purchasing agent a spending limit that grows only as its purchases turn out right.</p>
        </div>
      </div>
      <div className="panel">
        <h2>Demo path</h2>
        <ol className="small">
          <li><Link href="/checkout/">Checkout</Link>: start &ldquo;First visit&rdquo;, approve with PayPal.</li>
          <li><Link href="/staff/">Staff exit</Link>: ask the AI to explain the uncertain line, decide, close the visit. PayPal captures only verified lines.</li>
          <li>Back on the receipt, tap &ldquo;Not mine&rdquo; on a line for a partial refund.</li>
          <li><Link href="/trust/">Trust inspector</Link>: add simulated history for <code>asha</code>, then run &ldquo;Regular visit&rdquo;: Express, no queue.</li>
          <li><Link href="/agent/">Agent</Link>: a small purchase pays, a bigger one asks you, a huge one is refused; mark purchases correct and watch the limit grow.</li>
          <li><Link href="/sim/">Simulator</Link>: loss against friction for each strategy, including where Proofpay loses.</li>
        </ol>
      </div>
    </>
  );
}
