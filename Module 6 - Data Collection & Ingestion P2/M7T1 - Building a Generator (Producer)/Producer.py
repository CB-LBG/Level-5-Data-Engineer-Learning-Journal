import json, time, random, argparse
from datetime import datetime, timezone, timedelta
from faker import Faker
from schemas import SCHEMAS

# This imports the Faker library to generate realistic-looking fake data.
fake = Faker()


def now_iso():
    """Returns the current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def maybe_corrupt(record: dict, error_rate: float) -> dict:
    """Corrupts a record based on a given error rate."""
    if random.random() >= error_rate:
        return record

    choice = random.choice(["drop_ts", "bad_type", "malformed"])

    if choice == "drop_ts":
        record.pop("ts", None)
    elif choice == "bad_type":
        # Corrupts a specific field type, assuming an 'amount' field exists.
        if "amount" in record:
            record["amount"] = "N/A"
    else:
        # Adds a flag for a malformed, non-JSON record.
        record["_MALFORMED"] = True
    return record


def maybe_out_of_order(ts_iso: str, prob: float, max_skew: int) -> str:
    """
    Randomly skews a timestamp to simulate out-of-order data.
    """
    if random.random() > prob:
        return ts_iso

    dt = datetime.fromisoformat(ts_iso.replace("Z", "+00:00"))
    skew = random.randint(1, max_skew)

    if random.random() < 0.7:
        dt = dt - timedelta(seconds=skew)
    else:
        dt = dt + timedelta(seconds=skew)

    return dt.astimezone(timezone.utc).isoformat()


def add_envelope(payload, key=None):
    """Wraps the payload in an envelope with an optional key."""
    return {"key": key, "payload": payload}


def main():
    """
    Parses command-line arguments and generates a stream of events.
    The output can be directed to stdout or a file.
    """
    p = argparse.ArgumentParser(description="Generate a stream of fake events.")
    p.add_argument("--max", type=int, default=10, help="How many events to emit (0 = infinite)")
    p.add_argument("--rate", type=float, default=5.0, help="Events per second")
    p.add_argument("--dest", choices=["stdout", "file"], default="stdout", help="Output destination (stdout or file)")
    p.add_argument("--file-path", default="stream.jsonl", help="Path to the output file")
    p.add_argument("--schema", choices=SCHEMAS.keys(), default="clicks", help="Schema to use for events")
    p.add_argument("--key-field", default=None, help="Field to use as the envelope key")
    p.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    p.add_argument("--error-rate", type=float, default=0.0, help="Rate of intentional data corruption")
    p.add_argument("--out-of-order", type=float, default=0.0, help="Probability of out-of-order timestamps")
    p.add_argument("--max-skew-seconds", type=int, default=60, help="Max time skew for out-of-order timestamps")
    p.add_argument("--burst-every", type=int, default=0, help="Number of events between traffic bursts")
    p.add_argument("--burst-size", type=int, default=5, help="Number of events in each burst")
    args = p.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    sleep_s = (1.0 / args.rate if args.rate > 0 else 0.0)
    out = open(args.file_path, "w", encoding="utf-8") if args.dest == "file" else None

    try:
        i = 0
        # Loop to generate events
        while args.max == 0 or i < args.max:
            i += 1

            # Normal event generation
            payload = SCHEMAS[args.schema].generator(i)
            key = payload.get(args.key_field) if args.key_field else None

            # Out-of-order timestamp injection
            if "ts" in payload and args.out_of_order > 0:
                payload["ts"] = maybe_out_of_order(payload["ts"], args.out_of_order, args.max_skew_seconds)

            # Error injection
            payload = maybe_corrupt(payload, args.error_rate)

            line = ""
            if payload.get("_MALFORMED"):
                line = "this is not valid json\n"
            else:
                line = json.dumps(add_envelope(payload, key)) + "\n"

            if out:
                out.write(line)
            else:
                print(line, end="")

            # Traffic burst logic
            if args.burst_every > 0 and i % args.burst_every == 0:
                for _ in range(args.burst_size):
                    i += 1
                    burst_payload = SCHEMAS[args.schema].generator(i)
                    burst_key = burst_payload.get(args.key_field) if args.key_field else None
                    burst_line = json.dumps(add_envelope(burst_payload, burst_key)) + "\n"
                    if out:
                        out.write(burst_line)
                    else:
                        print(burst_line, end="")

            if sleep_s > 0:
                time.sleep(sleep_s)

    finally:
        if out:
            out.close()


if __name__ == "__main__":
    main()
