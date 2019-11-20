# SoftwareArchitecture #

## 2.7.2 Safety ##
The safety critical application runs inside a special kernel which enforces all the (or critical) I/O operations to pass through the shell. While enforcing, the kernel can perform dynamic verifcation of safety specifc properties. Create through the shell. While enforcing, the kernel can perform dynamic verifcation of safety specifc properties. Create an application container using Python (or Java) that arbitrarily makes i) ssh connections ii) http call (to an internet site) iii) network access. It is not important to consider any algorithm, just random external calls in a loop, in a periodic manner is good enough.

Now consider another container that acts as a safety wrapper of this application container. This container, collocated with the application container, intercepts these I/O calls and selectively allows these calls to pass through. Define certain access rules for valid ssh, http, network access of your own. For instance, you must implement rules such as: a) excessive calls: If network access, http or ssh call frequency > threshold, then do not allow such calls to happen b) port: If the port for htto is not 8080, then do not allow this http call to take place c) address: if the network calls are outside a particular subnet (you defne the subnet), then do not allow the network call to initiate. Network calls are outside a particular subnet (you defne the subnet), then do not allow the network call to initiate. Architecture First, identify the pattern that's most suitable here. 

* Describe the architecture using appropriate views.
* Dynamics Show and describe the most important usage scenario using a sequence diagram
