# Atm-Cash-Distribution

### Using Python

![Image](https://github.com/user-attachments/assets/705eb747-22bb-4d8a-8141-e5f5d058129f)


----
### A bank wants to deliver cash to ATMs across the city via truck. The program should create a map of nodes and edges that represent ATMs and the paths between them. The goal is to design and implement an algorithm that finds the shortest path to fill the machines.
First, you need to create a random (chance) map. The nodes are the ATMs and the edges are the paths between them.

### The weight of each edge represents the distance of that path.

#### The number of ATMs in each run is a random number between 5 and 15, and the paths are between 1 and 20 km apart, which should be represented numerically on the edge or by the intensity of the edge color (longer paths are shown in bold). Also, each machine should have at least 2 and at most 4 paths. Then, randomly select 2 to 4 ATMs as the finished and prioritized machines and distinguish them by a different color or icon.

#### After building the platform from the initial node, the money truck starts moving and dispensing money at a constant speed of 60 km/h, filling priority nodes first and then visiting other nodes (only all priority nodes must be filled first). Regular nodes are visited and the order of visiting two nodes of the same type does not differ.) Note that filling each machine takes half an hour, but if you pass that node, no time is wasted.

#### As you fill each ATM, you should display the filling time, its attribute (which machine is it?), and the nodes passed to reach this machine. (Store the machines being serviced in a list and finally display them in order)

##The program ends when all the ATMs are filled.

Finally, display the average time taken to fill each machine (total time taken divided by the number of machines) and the list of machines in order of filling.

### We have statistics:

#### Statistics on filling all machines (which machine was filled at what time and passing through which nodes?), average filling time of machines and list of serviced machines are saved in a text file or CSV respectively. .

## Fast and furious literate thieves:

#### After 3 hours, thieves appear at a random node and start robbing with their fast car (100 km/h). They have to decide how to empty as many machines as possible in the remaining time (after the last machine is filled by the cash machine, their time runs out) (re-emptying them has no effect on the cash machine schedule). Note that the act of robbing your machine takes 1 hour. Record the emptying statistics of each machine with the same exact details as the cash machine. (Which device was stolen at what time and on what route (set of nodes that thieves have traveled), average theft time and list of stolen devices respectively)

### Create an understandable and beautiful graphical user interface
### Display reports (statistics) They should be readable and understandable
### Calculate and explain the time complexity of the algorithms used

#### Time complexity: (E(log)V+V).n+O^2(n)
