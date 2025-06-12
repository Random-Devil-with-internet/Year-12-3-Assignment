# Evidence Guide

## Design Process and Prototyping
I decided to make my website about reviewing books.

To get inspiration for my user interface I used the imdb website specifically the pages on a specific movie to model my website off.

Dune as an example of a movie on imdb

![Html Dune as example of a movie on imdb](https://github.com/Random-Devil-with-internet/Year-12-3-Assignment/blob/main/Dune.png)

The page consists of the title, year of publication and rating. Below that there is a poster image of the movie with a brief description of it. And this is also a separate page for the user reviews.

So for my user interface I decided to put the title and average star rating on the top. With the author, genre and publishing date just below. The description and the cover image side by side. Why this design is because the two most important elements of the page are the description and the cover image. Which are placed in the centre to get the most attention form the users and since they take up the most space. While the title and the average star rating are the first elements that the user sees when they open the page. To set what the page is going to be about.

![Html The book page](https://github.com/Random-Devil-with-internet/Year-12-3-Assignment/blob/main/Book%20page.png)

The yellow stars in contrast with the grey stars help the users to distinguish between them two. Plus the yellows are made extra dark to help the user contrast them with the background. I also added half stars to allow users to make a more precise rating. For the review section the reviews are listed below in order form when they were made. The review layout consists of the review header. Which has a title paired with the user profile picture, date of publication and the rating of the respective book just below. The main body of text of the review is in the centre since it is the most important element in the review layout and takes up the most space. After that are the likes and dislikes for each review which are placed at the bottom. Because most users will read the review before liking or disliking it. So it makes the most sense for the likes and dislikes to be at the bottom with the review above it. 

![Html The review page](https://github.com/Random-Devil-with-internet/Year-12-3-Assignment/blob/main/Review%20page.png)

At first I had a problem with the web page reloading each time I liked or disliked a review which was annoying. So instead of using a normal post request I tried to use a get request. Which would not reload the page. But I couldn't get it to work since maybe get requests can only request data not modify it as I was doing with the like and dislike counts. So I was suggested to use AJAX or htmx to stop the page from refreshing. I chose the latter to work with since it was less complicated than AJAX. How htmx works is that it uses the javascript library called AJAX which allows sending and retrieving data to and back from the server. But without the webpage refreshing when a request is made to the server. But the difference between them two is that htmx makes it so that you don't have to write javascript instead you just add write htmx attributes in the html file and that's it.

The buttons are colored blue to make them stand out from the background so that the user can see them better. The buttons and images also have curved corners to make them approachable to the users and to make the website feel high quality.

## Technology Theories

The database that I used in my application passes first normal from because all of the tables have primary keys, none of the cells contain more than one value and there are no duplicates. For the second normal from all of the tables have no partial dependency inspect for maybe the like table which includes dislikes in it. I could make a separate table for dislikes but I was lazy too and just put them in the same table. And same for the third normal from, none of the tables in the database have transitive partial dependency.
 
The EDR of my database

![Html The EDR of my database](https://github.com/Random-Devil-with-internet/Year-12-3-Assignment/blob/main/EDR.png)

For the star rating system in my application I used a modified input slider in html. The input slider was modified with css to make it as a bunch of stars instead of a normal input slider which is a track. The stars also change when you drag your mouse along it with half stars being in between. For displaying the stars I used svgs that are shaped as stars. This was done though using the polygon tag in html and by using these Coordinates "12.5, 1.25 5.0, 24.75 23.75, 9.75 1.25, 9.75 20.0, 24.75". To make the half yellow and grey star I used a linear gradient that has a 50% offset on each color in the gradient and is then mapped on to the star shaped svg. I did ues these two attributes in the svg tage "xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" in the assignment but then I realised that they weren't needed for the code to work.

```html
  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="23" height="25">
  <defs>
      <linearGradient id="grad">
         <stop offset="50%" stop-color="#fbff00"/>
         <stop offset="50%" stop-color="#989898"/>
     </linearGradient>
  </defs>
  <polygon fill="url(#grad)" points="12.5, 1.25 5.0, 24.75 23.75, 9.75 1.25, 9.75 20.0, 24.75"/>
  </svg>
```

For the file extraction which is used for getting the images form the user to the application. I used an input tage with the attributes of type image, onchange="loadFile(event)" and accept="image/*". Which filters for only files that are images. Also in the html file the form tage has an extra attribute enctype="multipart/form-data" which encodes the data for you to be able to send a file though the form. Next in the server side code I used this code snippet to acquire the image from the frontend and save it to the static folder.

```python
 image = request.files['imagePicker']
 if image and allowed_file(image.filename):
   filename = secure_filename(image.filename)
   image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
```
To not allow users to send the incorrect file type or malware into the application. There is a list of allowed extension types "{'png', 'jpg', 'jpeg', 'gif'}" which are put into a function called allowed_file() to check if the file extension is in the allowed list.

## Testing Processes

The testing process that I used in the assignment was to see the goals that I had for the functionality and the requirements of a component of the softwear. I will then work out what my plan will be to test the software so that I can answer the objectives better if I had not done it. Testing was done using multiple users that were given a prompt to an objective that they should complete. While the users are testing the software I record the questions and compliments that the user has about the software. Watch them use the software to see how they struggle and have ease with using the softwear. Once all of this has been finished I reflect on all the data that I have just gathered and change the software accordingly.

## Design Implications - Ethical / Sustainable / Accessible

The accessibility and usability of the website was done by making my website have a high contrast color scheme which consists of black for the text, white for the main body of the website and a light grey for the background.

![Html Contrast checker](https://github.com/Random-Devil-with-internet/Year-12-3-Assignment/blob/main/Contrast%20checker.png)

As you can see from above I got the highest contrast ratio that you can get by using black and white. As well as getting the highest contrast ratio it also completed all of the contrast tests. Meaning that it is easy on the eyes of the users which makes users like the website more, use it more and easier navigation. It also allows users with visual impairments to use the website which expands the user base of the website.

The passwords in the website are stored using the werkzeug.security module that has the generate_password_hash() and check_password_hash() functions to encrypt the passwords from attackers. The generate_password_hash() function uses the scrypt hashing algorithm to turn the password into a string of random characters which are all of the same size no matter the input. Which is designed to be hard for attackers who use brute-force attack to get the password because of the high resource it needs compared to other hashing algorithms like PBKDF2. In which an attacker could use a parallel attack by creating multiple simulations of it on different computers to crack the hashing algorithm. The module uses the check_password_hash() which compares the hashed password in the database with the password that you get from the login page.

## References
