Module 3: The Reverse Mode of Automatic Differentiation
=======================================================
So far we have considered one mode of automatic differentiation, forward mode.  In forward mode, we carried derivatives along as we traversed the graph so that  the graph itself did not need to be explicitly stored in memory.  In reverse mode, we build the graph and store derivative information at each node but do not compute the derivative until the backward pass of the graph.  We will see that this approach can have computational advantages over forward mode and hence is commonly used, most well known in the backpropagation algorithm.


The Basics of Reverse Mode
--------------------------
At each node,


Practice with the Visualization Tool
------------------------------------
Let's revisit our typical example.  As with forward mode, we input the function into the interface in the same way and can compute the function value and derivative, but now we know a little bit about what reverse mode computes.

Press the Reverse Computational Graph button.  You'll see a graph that looks very similar to the one produced in forward mode.  Notice that the only difference is the direction of the errors, representing the fact that derivatives are propagated in different directions.

Now let's dynamically visualize the process of reverse mode.  Press the df/dx button.  Use the arrow keys to step through the process of reverse mode.  At each step you'll see the edge that the computation traverses being highlighted.  

Let's consider another example but with multiple inputs.  Note that this function also has a branch in its underlying graph structure.
(SOME NOTE HERE ABOUT BRANCHING)

**Key Takeaways**
- Reverse mode and forward mode propagate the derivative in different directions.
- The underlying graph structure of the function is the same for both modes of automatic differentiation.
- Reverse mode computes derivatives by making a backward pass starting at the output.


More Theory
-----------


A Comparison of Forward and Reverse Mode
----------------------------------------
As the names suggest, the primary difference between forward and reverse mode is the direciton in which the computational graph is traversed, as we saw in the direction of the errors of the visualization tool.  This has implications for the computational efficiency of the two approaches.

As we just showed, reverse mode computes ????, while in module 2, we learned that forward mode computes ????.  This means that reverse mode will be more efficient (require fewer operations) for functions with a ???? outputs and ??? inputs, while forward mode will be more efficient for functions with ???? outputs and ??? inputs.  Let's consider an example of this.

**Demo**
operation counting demo from lecture


Going Forward
-------------
