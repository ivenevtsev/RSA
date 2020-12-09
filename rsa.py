import random
q=0
p=0
e=0

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multi_inv(e, phi):
    x=0
    y=1
    lx = 1
    ly = 0
    oe = e
    ophi = phi
    while phi!=0:
        q = e//phi
        (e,phi) = (phi,e%phi)
        (x,lx) = ((lx - (q*x)),x)
        (y,ly) = ((ly - (q*y)),y)
    if lx<0:
        lx += ophi
    if ly < 0:
        ly += oe
    return lx

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multi_inv(e, phi)
    return ((e, n), (d, n),e)

def crt(c,dp, dq,qinv):
    m1 = pow(c,dp,p)
    m2 = pow(c,dq,q)
    h = (qinv*(m1-m2))%p
    m = m2+h*q
    return m
    
def encrypt(public_key, plaintext):
    key, n = public_key
    cipher = [pow(ord(char) , key , n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    key, n = private_key
    dp = 0
    dp = multi_inv(e, (p-1))
    dq = multi_inv(e, (q-1))
    qinv = multi_inv(q, p)
    plain = [chr(crt(char,dp,dq,qinv)) for char in ciphertext]
    return ''.join(plain)
    
p = int(input("Enter first prime number: "))
q = int(input("Enter second prime number: "))
print ("Generating your public/private keypairs now . . .")
public, private,e = generate_keypair(p, q)
print ("Your public key is ", public ," and your private key is ", private)
message = input("Enter a message to encrypt with your public key: ")
encrypted_msg = encrypt(public, message)
print ("Your encrypted message is: ")
print (''.join(map(lambda x: str(x), encrypted_msg)))
print ("Your decrypted message is:")
print (decrypt(private, encrypted_msg))