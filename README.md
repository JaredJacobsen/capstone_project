Author: Jared Jacobsen
Project Title: Protigen

Protigen is a web server that predicts protein allergenicity based on amino acid sequence. It was developed as a capstone project for the Galvanize Data Science Immersive program. The server can be found at www.jaredjacobsen.space.

The dataset used for this project was built by combining allergens from AllerHunter (http://tiger.dbs.nus.edu.sg/AllerHunter/), AllergenOnline (http://www.allergenonline.org/), and the Uniprot Swiss-Prot database. The dataset was filtered to remove similar/redundant allergens.

In Protigen, protein sequences are represented as TFIDF vectors, and a multinomial naive bayes algorithm is used to predict whether a given protein sequence is an allergen. Protigen allows the user to input one or more protein sequences and receive back predictions. The probability threshold for prediction can be adjusted, and estimated precision and recall values are displayed for each threshold.

To learn more about Protigen, visit www.jaredjacobsen.space
