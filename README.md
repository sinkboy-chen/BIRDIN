# BIRDIN

This web application serves as a demonstration of the BIRDIN project.
The api part is in [https://github.com/sinkboy-chen/BIRDIN-api](https://github.com/sinkboy-chen/BIRDIN-api).

live demo: [https://birdin-demo.vercel.app/](https://birdin-demo.vercel.app/) (the analyze part is no longer serving)

detailed article: [https://appliedmusanth.wordpress.com/2023/12/12/group-6-birdin-project/](https://appliedmusanth.wordpress.com/2023/12/12/group-6-birdin-project/)

#### Objectives:

The aim of this initiative is to facilitate interaction between individuals at NTU and the environment, thereby promoting observation, understanding, and preservation of the campus.

  

#### Abstract:

Users are encouraged to collect audio recordings of bird species within the campus. This initiative prompts users to attentively listen to the sounds within the campus, fostering an understanding of the diverse environmental and ecological aspects across various corners of the campus.

  

#### Case Studies and Methods:

1.  eBird ([https://ebird.org/home](https://ebird.org/home)): This website allows users to upload recorded observations of bird species, with a substantial community contributing numerous records (as of December 11, 2023, there are over 5300 records for NTU Main Campus). However, the user base tends to lean towards scholars, as detailed observation records and bird identification are prerequisites.
    
2.  BirdNET([https://birdnet.cornell.edu](https://birdnet.cornell.edu)): This project enables users to identify bird sounds using its trained AI. However, there have been less than 10 uploads in the past 24 hours.
    

In light of these considerations, we propose the BIRDIN project, utilizing AI for bird sound recognition while incorporating interactive gaming features. This approach removes the necessity for a background in biology, making it accessible to the general public. Simultaneously, the allure of community gaming is leveraged to engage users in understanding and appreciating the environment.

  

#### Features:

We strive to provide maximum enjoyment without disconnecting from environmental interaction. Our main features include:

1.  Collections: Users can collect bird guides, encouraging exploration of various corners of the campus.
2.  Nicknaming and Voting: Users can suggest names for various bird species, and the most popular name will become the adopted way to refer to that bird.

  

#### Disclaimer:

To ensure fairness in the game, we will cross-reference data with GPS, month, time, weather, and the database to verify the authenticity of the recorded sounds. The initial comparison data will be collected in this demo.

  

#### Tools Used:

1.  [BirdNET-Analyzer](https://github.com/kahst/BirdNET-Analyzer#setup-birdnetlib)
2.  [Vercel](https://vercel.com/)
3.  [Cloudinary](https://console.cloudinary.com/)
4.  [CSIE WSLab](https://wslab.csie.ntu.edu.tw/)
