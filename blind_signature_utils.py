import random
import hashlib
import json
from math import gcd

# --- Mock RSA-style Blind Signature Implementation ---
# NOTE: This uses small integers for demonstration and is NOT cryptographically secure
# for real-world use. It illustrates the mathematical principle (m^d mod N).

def is_prime(n):
    """Simple check for demonstration purposes."""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modular_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def generate_blind_keys():
    """Generates simple RSA-like keys (N, e, d) for demonstration."""
    # Using small prime numbers for quick calculation and demo
    p = 61
    q = 53
    N = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e such that 1 < e < phi and gcd(e, phi) = 1
    e = 17 
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1) 
    
    # Calculate d (modular inverse of e mod phi)
    d = modular_inverse(e, phi)
    
    return {'N': N, 'e': e, 'd': d}

def bytes_to_int(data):
    """Converts bytes to an integer for RSA operations."""
    # Use a secure hash (like SHA-256) of the data as the message (M)
    m_bytes = hashlib.sha256(data).digest()
    return int.from_bytes(m_bytes, 'big')

def blind_message(message_bytes, N, e):
    """Blinds the message (ZKP Commitment)."""
    M = bytes_to_int(message_bytes)
    
    # Generate random blinding factor r, where 1 < r < N and gcd(r, N) = 1
    # In a real system, 'r' is securely generated. Here, we mock it.
    r = random.randint(2, N - 1)
    while gcd(r, N) != 1:
        r = random.randint(2, N - 1)

    # Calculate Blinded Message (B): B = M * r^e mod N
    # pow(r, e, N) computes r^e mod N
    B = (M * pow(r, e, N)) % N
    
    return B, r

def sign_blinded_message(blinded_int, N, d):
    """Admin signs the blinded message (B^d mod N)."""
    # Calculate Signed Blinded Token (S): S = B^d mod N
    S = pow(blinded_int, d, N)
    return S

def unblind_signature(signed_blinded_int, r, N):
    """User unblinds the token to get the final signature (S' * r^-1 mod N)."""
    # Calculate Modular Inverse of r (r_inv): r_inv = r^-1 mod N
    r_inv = modular_inverse(r, N)
    
    # Calculate Final Signature (S_final): S_final = S * r_inv mod N
    S_final = (signed_blinded_int * r_inv) % N
    
    # For simplicity, return the integer value as hex string
    return hex(S_final)

def verify_unblinded_signature(signature_int, message_bytes, N, e):
    """Verifier checks if S_final^e mod N == M."""
    M = bytes_to_int(message_bytes)
    
    # Calculate Verification (V): V = S_final^e mod N
    V = pow(signature_int, e, N)
    
    # Check if V == M
    return V == M