Expanded the basic blockhain structure with a few improvements:
1. Users
2. Transactions
3. Special User called SecretPrinter, which adds 50 to the vault every 30 seconds. 

I sort of wanted to add like a basic cryptocurrency to my blockchain, hence why I added Users and Transactions. I also thought the idea of the SecretPrinter account was kind of neat, since it was different than all the other cryptocurrencys like bitcoin, which have a maximum possible amount of currency. 

A class is like a builder or general form that helps to create objects ("data") of a certain type. It also allows you to run functions on these specific objects. These objects are incredibly helpful, since they can intuitively simulate real life objects—like a user simulates a person—leading to more tangible coding and results. 

An endpoint is links an app/server to the actual API. It is where client computers communicate with the servers. A server is a computer that gives data and resources to client computers, when they make requests to the endpoints. When we run our Flask app, it instatiates a server. Flask is used to create a web application, using things such as endpoints and servers. Postman is a tool to test API code, and we used it to send requests to the enpoints.

I acheived much of what I set out to do. I really wanted to sort of make a basic implementation of a cryptocurrency, with a coin data, users, and transactions. I suceeded on this front and while these systems aren't super robust (no password for Users as an exmple), they work really well, and I am really happy with how they turned out. Adittionally, I also wanted to make some sort of interesting quirk about my project, and I had toyed with the idea of a money printer. As a result, I created the SecretPrinter account, which "prints" money every thirty seconds. The idea was sort of inspired by the real world, with the government printing money each yera (not much of course, but I still found it interesting, especially in contrast to bitcoin for example).