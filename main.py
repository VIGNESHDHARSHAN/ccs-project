import hashlib
print("Python is working!")
print("Your SHA-512 Library is ready.")

def check_image():
    filename = input("Enter the image name: ")
    
    try:
        sha512 = hashlib.sha512()
        with open(filename, "rb") as f:
            while chunk := f.read(4096):
                sha512.update(chunk)
        
        print(f"\nSUCCESS! The SHA-512 Signature is:\n{sha512.hexdigest()}")
    except FileNotFoundError:
        print("\nERROR: I couldn't find that image. Make sure it is in the same folder as this script!")

check_image()