"""Demonstrim i nënshkrimit të shkëputur RSA-PSS mbi një skedar fiktiv."""
import argparse
import hashlib
import platform
from pathlib import Path

import cryptography
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def new_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def verify(public_key, signature, document, pss):
    try:
        public_key.verify(signature, document, pss, hashes.SHA256())
    except InvalidSignature:
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, help="Dosje e re për skedarët publikë")
    args = parser.parse_args()
    source = Path(__file__).with_name("vendimi_fiktiv.txt")
    document = source.read_bytes()
    modified = document.replace(b"250 EUR", b"950 EUR", 1)
    if modified == document:
        parser.error("Dokumenti duhet të përmbajë shumën fillestare 250 EUR.")

    pss = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32)
    private_key = new_key()
    public_key = private_key.public_key()
    other_public_key = new_key().public_key()
    signature = private_key.sign(document, pss, hashes.SHA256())
    damaged_signature = bytes([signature[0] ^ 1]) + signature[1:]

    print(f"Python {platform.python_version()} | cryptography {cryptography.__version__}")
    print("RSA 2048 bit | e=65537 | SHA-256 | MGF1(SHA-256) | salt=32 bajte")
    print(f"SHA-256 origjinal  {hashlib.sha256(document).hexdigest()}")
    print(f"SHA-256 ndryshuar  {hashlib.sha256(modified).hexdigest()}")
    print(f"Gjatësia e nënshkrimit: {len(signature)} bajte")
    cases = [
        ("T1 Origjinali + çelësi i duhur", document, signature, public_key, True),
        ("T2 Dokumenti i ndryshuar", modified, signature, public_key, False),
        ("T3 Çelësi publik i gabuar", document, signature, other_public_key, False),
        ("T4 Nënshkrimi i dëmtuar", document, damaged_signature, public_key, False),
    ]
    passed = 0
    for label, payload, candidate, key, expected in cases:
        actual = verify(key, candidate, payload, pss)
        passed += actual == expected
        status = "PASS" if actual == expected else "FAIL"
        print(f"{label}: pritur={expected}, marrë={actual} [{status}]")
    print(f"Përmbledhje: {passed}/{len(cases)} teste kaluan.")
    if passed != len(cases):
        return 1

    if args.artifacts:
        args.artifacts.mkdir(parents=True, exist_ok=False)
        (args.artifacts / "origjinali.txt").write_bytes(document)
        (args.artifacts / "ndryshuar.txt").write_bytes(modified)
        (args.artifacts / "nenshkrimi.sig").write_bytes(signature)
        for filename, key in [("publik.pem", public_key), ("publik_tjeter.pem", other_public_key)]:
            pem = key.public_bytes(
                serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
            )
            (args.artifacts / filename).write_bytes(pem)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
