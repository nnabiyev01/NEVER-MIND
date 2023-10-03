# NEVER-MIND: The Future of Smart Parking

NEVER-MIND is a state-of-the-art smart parking solution that redefines the parking experience. Say goodbye to manual interactions with parking barriers; with NEVER-MIND, everything is automated.

Overview
Utilizing the power of CCTV cameras, NEVER-MIND employs an advanced license plate recognition system that detects vehicle plate numbers in real-time. This triggers an automatic response, unlocking the parking barrier without any manual intervention.

While the foundation of our system is built on the Tesseract program, which captures text from images, we've enhanced its capabilities significantly. The initial success rate with Tesseract alone was a mere 5%, with an average capture time exceeding 10 seconds. Post our enhancements, we've achieved a staggering 90% success rate, slashing the capture time to under 2 seconds.

Why NEVER-MIND?
In today's market, specialized license plate recognition cameras are available but come with a hefty price tag. Our vision was to democratize this technology, enabling any standard camera to be transformed into a smart license plate recognition system. With NEVER-MIND, you don't need to invest in expensive hardware; our software does the magic.

How We Achieved This
Our journey to perfection was three-fold:

Post-Processing: This was our primary focus. We employed various cropping and image filtering techniques to enhance the clarity and visibility of license plates, making it easier for the system to recognize them.

Pre-Processing: We incorporated license plate specifications for different countries. This tailoring, combined with a character whitelist, optimized Tesseract's recognition capabilities. For instance, when a user registers, they specify their vehicle's country of registration. The system then uses the specific conditions of that country to enhance recognition accuracy.

Testing: Rigorous testing was the key to our success. We've documented our testing process and results extensively. For a visual representation, we've uploaded videos on our GitHub repository showcasing the system in action.

See It In Action
We invite you to witness the efficiency of NEVER-MIND. Check out our testing videos on our GitHub repository and experience the future of smart parking.
