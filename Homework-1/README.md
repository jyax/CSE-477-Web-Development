# [Web Application Development](https://gitlab.msu.edu/cse477-fall-2023/course-materials/): Homework 1



## Purpose

The purpose of this assignment is to provide with hands-on experience with frontend development including:

1. How to write and structure HTML documents.
2. Best practices for styling reactive HTML documents using CSS.
3. Building interactive client-side applications using HTML, CSS, and Javascript.



## Before you begin

Before you begin this assignment, please complete the following steps.



##### 1. Update your local copy of the Course Materials Repository

Navigate to the <u>course materials repository</u> on your local machine, and pull any updates by running the following command from the terminal:

```bash
git pull https://gitlab.msu.edu/cse477-fall-2023/course-materials.git
```



##### 2. Compose the Homework container locally 

1. Navigate to the `Homework-1` directory of your <u>Personal Course Repository</u> (that's the one with the same name as your netID). 

2. Use `docker-compose` to host the web application locally by executing the following command from you terminal:

   ```bash
   docker-compose -f docker-compose.yml -p hw1-container up
   ```

3. Visit [http://0.0.0.0:8080/home.html](http://0.0.0.0:8080/home.html) to ensure the template is running.



##### 3. Explore the Template subdirectories

In this assignment, you will modify the web application template provided in `Homework-1/flask-app/`. More specifically, you will author a number of `HTML`, `CSS`, and `Javascript` files that will fulfill the assignment criteria. All of your files for this assignment should be contained in:

* `/templates` : where you will store your `.html` files 
* `/static` : where you will store your `.css`, `.js` and other files.

As you explore these directories, you will notice some images, and template files you can will work with for the assignment; we'll call out these files in the assignment requirements, below.



## Assignment Goals

Your high-level goal in this assignment is to develop a mobile-friendly professional webpage with:

1. **A Home page**: providing information about you, and your professional background. 
2. **A Projects page**:  providing descriptions and links to functional web projects you are working on.
3. **A Piano project:** providing a fully functional piano web application built in HTML CSS and Javascript (with a hidden twist.)  

Your implementation should satisfy both the General Requirements, and Specific Requirements detailed in the sections below;  to help you grasp the overarching goal and requirements more concretely, [see the Homework overview video](https://youtu.be/RxyNQgcdNiY). Please note; your implementation does not have to look identical to the example solution. As long as you achieve the Specific and General requirement below, your assignment is complete.



## General Requirements

As a general requirement, we would like you to following good programming practice, this includes (but is not limited to):

* All code should be commented, organized, and thoughtfully structured.
* `HTML` content should be placed in the `flask_app/templates/` directory.
* `CSS`, `Javascript`, `Images`, `Documents` and other content should be placed in the `flask_app/static` directory.
* Don't mix `HTML`, `CSS`, and `Javascript` in single files.

Please see the General Requirements section of the [assignment rubric](documentation/rubric.md) for other elements of good programming practice in HTML, CSS and Javascript that we'd like you you to pay attention to.



## Specific Requirements

For each of the three assignment goals listed above, we provide a section that outlines the specific requirements associated with that goal, below: 



##### Home page requirements

We've provided a placeholder home page for your application called [`home.html`](flask_app/templates/home.html); You will need to add a [`<header>`]([](https://www.w3schools.com/tags/tag_header.asp))  [`<nav>`](https://www.w3schools.com/tags/tag_nav.asp)  [`<main>`](https://www.w3schools.com/tags/tag_main.asp) and  [`<footer>`](https://www.w3schools.com/tags/tag_footer.asp) section to this template. Each HTML sections should satisfy the *Structure*, *Content*, *Style*, and *Interactivity* requirements outlined in the table below. Any `CSS` and `Javascript` should be imported separately, not included in your HTML file. 

|                          | [`<header>`]([](https://www.w3schools.com/tags/tag_header.asp)) | [`<nav>`](https://www.w3schools.com/tags/tag_nav.asp)        | [`<main>`](https://www.w3schools.com/tags/tag_main.asp)      | [`<footer>`](https://www.w3schools.com/tags/tag_footer.asp)  |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Structure**            | -  always appears at the top of the page                     | - appears beneath the `<header>`                             | - appears beneath the`<nav>`                                 | - always at the bottom of the page.                          |
| **Content**              | - a banner image (e.g. [this one](flask_app/static/main/images/banner.jpg)) | - Name of the assignment<br /><br />- Link to the `home.html` page <br /><br />- Link to the `projects.html` page <br /><br />- Link to your resume.<br />- Link to your LinkedIn page (embedded in [an icon](flask_app/static/main/images/social-linkedin.png)) <br /> | - your name<br /><br />- photo of you<br /><br />- brief description of you<br /><br />- fun fact about you | - the copyright symbol © , followed by your name             |
| **Style**                | - banner images should cover the entire header area; i.e. no [margin](https://www.w3schools.com/css/css_margin.asp) and no [padding](https://www.w3schools.com/css/css_padding.asp)<br />- banner size should scale with screen [viewing height](https://www.w3schools.com/cssref/css_units.asp) and [viewing width](https://www.w3schools.com/cssref/css_units.asp) | - name of the assignment should be on the left of the nav bar<br /><br /> - All links should appear on the right of the nav<br /><br />- The [opacity](https://www.w3schools.com/css/css_image_transparency.asp) of the links should change on [hover](https://www.w3schools.com/cssref/sel_hover.asp).<br /><br />- navbar size should scale with screen [viewing height](https://www.w3schools.com/cssref/css_units.asp) and [viewing width](https://www.w3schools.com/cssref/css_units.asp) | - all text should be centered and [justified](https://www.w3schools.com/cssref/css3_pr_text-justify.asp)<br /><br />- the name, photo and breif description should appear  in a row of content with two equal sized columns. The row should have a maximum [viewing height](https://www.w3schools.com/cssref/css_units.asp) of 50vh, and [viewing width](https://www.w3schools.com/cssref/css_units.asp) of 80vw.<br /><br />- the photo should cover the entire area of the left column; the name and description should appear on the right column; [text overflow](https://www.w3schools.com/cssref/css3_pr_overflow-y.asp) should be handled with the scroll bar.<br /><br />- the fun fact should appear in seperate line of content.<br /> | - should have a color that is distinct from the color of `<main>`.<br /><br />- all text should be centered and justified. |
| **Mobile Interactivity** | - None required                                              | - the nav links should disappear when the screen size is less than `650px`, and be replaced with a [menu bar](flask_app/static/main/images/menu-bar.png) that, when clicked, displays the links.<br /><br />- the LinkedIn Icon should be replaced with text that says "LinkedIn" | - any two column content should transition into single column content when the screen size less than `650px`; [text overflow](https://www.w3schools.com/cssref/css3_pr_overflow-y.asp) should be `visible`; all single column content should have a viewing width of 80vh. | - None required                                              |



##### Projects page requirements

We've provided a placeholder projects page for your application called [`projects.html`](flask_app/templates/projects.html);  it will use the same *Structure*, *Style*, and *Interactivity* conventions as the Home page. The only section that will differ between the Projects page and the Home page is the *Content* in `<main>`. The *Content* requirements include:

* A single column row of content explaining the purpose of the page (i.e. to show off your project work).

* A two-column row of content that shows an [image of a piano](flask_app/static/main/images/piano.jpeg) on the left; and a description of the piano project on the right, with a link to `piano.html`
* clicking the image of the piano should take you to the `piano.html` page.



**Piano project requirements**

We've provided a placeholder page for your piano application called [`piano.html`](flask_app/templates/piano.html);  it should use the same *Structure*, *Style*, and *Interactivity* conventions as the Home page. Within  `<main>`, you will place:

* <u>In HTML:</u> At the top of the page should be the following poem: ""*Behold piano great and old, it's master slumbers in far off cold, If you wish to see anew, call out to it - we see you.*""
* <u>In HTML and CSS:</u> Under the poem will be your piano. It should have 10 white keys, 7 black keys, and the name "The Great Old One". The piano can be constructed by [layering HTML elements](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Positioning/Understanding_z_index/Adding_z-index). For instance, you can make each key in the piano a separate `<div>` with an appropriate size, ID, etc. It should look something like this at the end:

![piano-1](documentation/piano-1.png)

* <u>In Javascript:</u>  Create [a mouseover event listener](https://developer.mozilla.org/en-US/docs/Web/API/Element/mouseover_event) to detect when the mouse hovers over any key of the piano, and temporarily reveal the keyboard keys that control the piano; it should look something like this when your mouse is hovered over any of the keys:

![piano-2](documentation/piano-2.png)

* <u>In Javascript:</u> Create a [keydown event listener](https://developer.mozilla.org/en-US/docs/Web/API/Document/keydown_event) to detect when a given key is pressed (e.g. the S key), and alter the style of the corresponding HTML element that represents that key to indicate it was pressed. If the S key were pressed, for instance, you should temporarily see something like the image below. I suggest looking into the [transform](https://developer.mozilla.org/en-US/docs/Web/CSS/transform) and [box-shadow](https://developer.mozilla.org/en-US/docs/Web/CSS/box-shadow) in CSS if you want to replicate the effect in my example, but you can choose to style it another way too; for instance, by temporarily changing the key's [background color](https://www.w3schools.com/cssref/pr_background-color.asp), or changing the key's size. 

![piano-2](documentation/piano-3.png)

* <u>In Javascript:</u> Use the [keyCode](https://keycode.info/) from keypress events captured by the keydown event listener to identify which key was pressed. Next, use the following [JSON object](https://www.w3schools.com/whatis/whatis_json.asp) to map the keyCode to a url containing the sound of the note you need to play. You can play these notes by passing the corresponding url to an [Audio() constructor](https://developer.mozilla.org/en-US/docs/Web/API/HTMLAudioElement/Audio) in Javascript:

```json
const sound = {65:"http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
                87:"http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
                83:"http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
                69:"http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
                68:"http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
                70:"http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
                84:"http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
                71:"http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
                89:"http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
                72:"http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
                85:"http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
                74:"http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
                75:"http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
                79:"http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
                76:"http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
                80:"http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
                186:"http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"};
```

* <u>In Javascript:</u> When the sequence of keys "weseeyou" is typed on your piano it should awaken the great old one! More specifically, (1) your piano should gradually fade away and be replaced by the [image of the great old one](flask_app/static/piano/images/texture.jpeg), (2) you should play the following [creepy audio](https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1) and (3) the piano should no longer respond to key presses; at the end, the piano should look something like this:

![piano-4](documentation/piano-4.png)



## Submitting your assignment

##### Submit Homework 1 Code

1. Submit your assignment by navigating to the main directory of your <u>Personal Course Repository</u> and Pushing your repo to Gitlab; you can do this by running the following commands:

   ```bash
   git add .
   git commit -m 'submitting Homework 1'
   git push
   ```

2. You have now submitted Homework 1's code; you can run the same commands to re-submit anytime before the deadline. Please check that your submission was successfully uploaded by navigating to the corresponding directory in Personal Course Repository online.



**Deploy your web application to Google Cloud**

Deploy your Dockerized App to Google Cloud by running the commands below from the Homework-1 directory.

```bash
gcloud builds submit --tag gcr.io/cse477-fall-2023/homework
gcloud run deploy --image gcr.io/cse477-fall-2023/homework --platform managed
```

* When prompted for service name, press enter.
* When prompted for the `region` choose `us-central1`
* When prompted regarding `unauthenticated invocations` choose  `y`

when the application has completed deploying, it will provide provide an output like this:

```bash
Deploying container to Cloud Run service [homework] in project [cse477-fall-2023] region [us-central1]
✓ Deploying new service... Done.                                            
  ✓ Creating Revision...                                                    
  ✓ Routing traffic...                                                      
  ✓ Setting IAM Policy...                                                   
Done.                                                                       
Service [homework] revision [homework-00001-qol] has been deployed and is serving 100 percent of traffic.
Service URL: https://homework-z7tywrhkpa-uc.a.run.app
```

 The last line in the above output is the <u>Service URL</u>; You can visit the <u>Service URL</u> above to see a live version of your web application. 



##### Submit Homework 1 Survey:

[Submit the Service URL for your live web application in this Google Form](https://docs.google.com/forms/d/e/1FAIpQLSc60M6luRRUMUMW4EaMHc-7Stb7Bm9yPlXt9P5IMrRKiTwxxw/viewform). 



