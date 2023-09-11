# NEVER-MIND

Never Mind is a  smart parking app, and one of its key features is an advanced license plate recognition program that can identify the plate number of any car in real-time. There is an already built-in program for capturing text from an image which is called a tesseract. However, as that program is not designed specifically for that purpose, the success rate with just testing tesseract was less than 5% and the average capture time was more than 10 seconds. After our additions, the success rate went up to 90 percent and the average capture time was less than 2 seconds. 

Why did we do it? 

Nowadays, there are license plate recognition cameras which are specifically designed for capturing plate numbers. A customer has no other choice but to buy that highly-price cameras to satisfy their purpose. To combat this problem, we decided to write a program which will turn any camera to a smart one.  

How did we do it?
          1. Post-Processing 
          2. Pre-Processing 
          3. Testing

The part that we mostly devoted time to be the post-processing section. We used different cropping, image filtering techniques for the program to easily capture the license plate number of the car.  For the pre-processing, we added license plate specifications for each country so that it would be easier for tesseract to find the plate number. We also added character whitelist that only lets tesseract to guess from the specified range of letters and digits. Let’s assume that one uses our program in an app which is designed to automatically allow the cars in the parking spot. When the person gets registered, he/she must enter the country where his/her car plate from. Thus, the program for this user will be implemented under the specifications/conditions of that country. We also used a lot of testing, to get the result what we wanted. The videos are attached in our GitHub, you can use the testing to check the results. 


