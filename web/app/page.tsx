import Link from "next/link";

export default function Home() {
  return (
    <>
      <h1>PayPal for in-person handovers: camera evidence becomes the tracking number that in-person sales never have.</h1>
      <p className="lede">
        A shipped parcel has a tracking number. An item handed over at a counter, a pickup shelf or a cashierless store has
        nothing. PayPal&apos;s Seller Protection asks in-person sellers for &ldquo;alternative evidence of delivery&rdquo;.
        Witnessed makes that evidence. PayPal holds the basket, cameras record which items were actually handed over, and
        Witnessed captures only those lines, releases the rest, and keeps a per-line evidence record next to each PayPal capture.
      </p>
      <div className="grid3">
        <div className="panel">
          <h2>Evidence, then money</h2>
          <p className="small muted">A line can be charged only if the camera is at least 90% sure it left with the buyer, or a staff member confirmed it. Each charged line keeps its timestamps and the decision behind it.</p>
        </div>
        <div className="panel">
          <h2>Holds that don&apos;t lapse</h2>
          <p className="small muted">The <Link href="/holds/">holds timeline</Link> tracks every PayPal authorization through its honor period and expiry. The AI reauthorizes or captures the verified lines before a hold is lost.</p>
        </div>
        <div className="panel">
          <h2>Trust sets the friction</h2>
          <p className="small muted">A reputation learned from each payer&apos;s history decides how big the hold is and whether a human checks the exit. It never changes what is charged.</p>
        </div>
      </div>
      <div className="panel">
        <h2>Demo path</h2>
        <ol className="small">
          <li><Link href="/checkout/">Checkout</Link>: start &ldquo;First visit&rdquo; and approve the hold with PayPal.</li>
          <li><Link href="/staff/">Staff exit</Link>: ask the AI to explain the uncertain line, decide, and close the visit. PayPal captures only the verified lines.</li>
          <li>On the receipt, open the evidence record, or tap &ldquo;Not mine&rdquo; on a line for a partial refund.</li>
          <li><Link href="/holds/">Holds</Link>: open PayPal authorizations on a timeline; let the AI rescue the ones at risk.</li>
          <li><Link href="/agent/">Agent</Link>: an AI shopping agent buys real products through the same hold-then-capture flow, inside a spending limit it earns.</li>
          <li><Link href="/trust/">Trust inspector</Link> and <Link href="/sim/">Simulator</Link>: how the reputation works, and where it loses.</li>
        </ol>
      </div>
    </>
  );
}
