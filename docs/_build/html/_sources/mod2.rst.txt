Module 2: Deeper Into Forward Mode
==================================

As we introduced in `Module 1 <mod1.html>`_, the forward mode of automatic differentiation computes derviatives by decomposing functions
into a series of elementary operations.  We can explicitly compute the derivative of each of these elementary operations,
allowing us to combine them using the chain rule to accurately compute the derivative of our function.  

As we have seen, in the computational graph, nodes represent inputs and outputs of elementary operations, and the edges correspond to the
elementary operations that join these nodes.  The inputs to our functions become the first nodes in our graph.  For each
subsequent node, we can consider an evaluation and derivative up to that point in the graph, allowing us to consider the
computation as a series of elementary traces.

I. The Computational Trace and Practice with the Visualization Tool
-------------------------------------------------------------------
At each step in the graph, we can consider the current function value and derivative up to that node.  Using the chain rule,
we compute the derivative at a particular node from the elementary operation that created that node as well as the value and
derivative of the input node to that elementary operation.  We'll return to our example from `Demo 1 <mod1.html#demo-1-errors-in-the-finite-difference-method>`_ 
in a moment. For now, let's work with a simpler function so we can see example how everything works out. 

A Basic Example
^^^^^^^^^^^^^^^
We worked with a fairly involved function in `Module 1 <mod1.html>`_. Now we want to understand how the graph is created and how derivatives
are really computed using automatic differentiation. A very friendly function to start with is,

.. math::
        f(x) = \sin(2x)

a. Evaluating the Function
""""""""""""""""""""""""""
We want to evaluate :math:`f(x)` at a specific point. We will choose the point :math:`a=2`. Throughout this documentation, we will
refer to a specific point with the name :math:`a`. It should be assumed that :math:`a` has a specific value, the point at which the function is being evaluated.  (This specific point is `2` in the example below.) How do we
evaluate this function?

1. Replace :math:`x` with the value :math:`2`.

2. Multiply: :math:`2\times 2 = 4`.

3. Apply the sine function: :math:`\sin(4)`.

4. Return the value of :math:`f`: :math:`f = \sin(4)`.

b. Visualizing the Evaluation
"""""""""""""""""""""""""""""
We can visualize this evaluation in a graph. Each node of the graph will represent a stage in evaluation of the function. The
nodes are connected together with edges. The parent value of a given node is the input to that node. The input to the entire
function will be denoted by :math:`x_{0}`. Intermediate values will be denoted by :math:`v_{i}`. The evaluation graph of our
simple function is shown in the figure below.

.. image:: simple_graph.PNG

We can convert this graph picture into a trace table, which "traces" out the computational steps. The trace table for this
function is shown in the following table.

.. list-table::
        :widths: 10 25 25
        :header-rows: 1
        
        * - Trace
          - Elementary Function
          - Current Value
        * - :math:`x_1`
          - :math:`x`, input
          - :math:`2`
        * - :math:`v_1`
          - :math:`2x_1`
          - :math:`4`
        * - :math:`v_2`
          - :math:`\sin(v_1)`
          - :math:`\sin(4)`

This table makes a connection between the evaluation that we normally do and the graph that we used to help us visualize the
function evaluation. So far there is nothing much new. These calculations are done almost automatically by our brains and by
the computer. All we've done so far is laid things out more algorithmically.

c. Introducing Derivatives
""""""""""""""""""""""""""
Let's add one more wrinkle. We can actually compute the derivatives as we go along at each step. The way we do this is by
applying the chain rule at each step. We'll add two more columns to the table. The first new column will represent the
elementary function derivative at that step. The second new column will represent the value of the derivative at that step.

.. list-table::
        :widths: 10 25 25 25 20
        :header-rows: 1
        
        * - Trace
          - Elementary Function
          - Current Value
          - Elementary Function Derivative
          - Current Derivative Value
        * - :math:`x_1`
          - x, input
          - :math:`2`
          - :math:`1`
          - :math:`1`
        * - :math:`v_1`
          - :math:`2x_1`
          - :math:`4`
          - :math:`2\dot{x}_1`
          - :math:`2`
        * - :math:`v_2`
          - :math:`\sin(v_1)`
          - :math:`\sin(4)`
          - :math:`\cos(v_1)\dot{v}_{1}`
          - :math:`\cos(4)\cdot 2`

The first thing to observe is that the derivative value of the output is precisely what we would expect it to be. The
derivative of our function is :math:`f^{\prime} = 2\cos(2x)`. Evaluated at our chosen point, this is :math:`f^{\prime} =
2\cos(4)`. So whatever we did in the table seems to have worked.

We introduced some new notation: we denoted a derivative with the overdot notation. This is the common notation in
forward mode. Therefore, the derivative of :math:`2x_{1}` is simply :math:`2\dot{x}_{1}`. The dot should be interpreted as a
derivative with respect to the independent variable. In the 1D case that we're doing here, the dot means a derivative with
respect to :math:`x`.

We used the chain rule at each step. This is most apparent in the last step where we took the derivative of :math:`v_{2}` to get
:math:`\dot{v}_{2}`, which is just :math:`f^{\prime}` in this case.

Finally, there is something interesting about how we set the initial derivative in the first step. What we have done is
"seeded" the derivative. Intuitively, it may help to think that in the first step we are taking the derivative of the input
with respect to itself. Since :math:`dx/dx=1`, the derivative in the first step should just be :math:`1`. However, we will see
later that this is actually not necessary. If we want to get the true derivative, then it is good to seed the derivative in
this way. However, automatic differentiation is more powerful than this, and choosing different seed values can give valuable
information. Stay tuned.

For this simple example, we can draw an accompanying graph to the original computational graph, which helps us visualize the
way the derivatives are carried through.

.. image:: simple_deriv_graph.PNG

The new graph shadows the original graph. Each node in the shadow graph represents the derivative at that step. Note that the
edges representing the elementary functions (in this case sine function) have been differentiated. Note too how the derivatives from
the previous node feed *forward* to the next node.


The Original Demo
^^^^^^^^^^^^^^^^^
Now we return to the `original demo <mod1.html#demo-1-errors-in-the-finite-difference-method>`_ from the first module.

.. math::
        f(x) = x - \exp(-2\sin^2(4x))

In `Module 1 <mod1.html>`_, we formed the corresponding computational graph. Now let's use that graph to write the computational table. Each
node in the table is the output of an elmentary function, whose derivative we can compute explicitly.

.. list-table::
        :widths: 10 25 25 25 25
        :header-rows: 1
        
        * - Trace
          - Elementary Function
          - Current Value
          - Elementary Function Derivative
          - Derivative Evaluated at x
        * - :math:`x_1`
          - x, input
          - :math:`\frac{\pi}{16}`
          - 1
          - 1
        * - :math:`v_1`
          - :math:`4x_1`
          - :math:`\frac{\pi}{4}`
          - :math:`4\dot{x_1}`
          - 4
        * - :math:`v_2`
          - :math:`\sin(v_1)`
          - :math:`\frac{\sqrt{2}}{2}`
          - :math:`\cos(v_1)\dot{v_1}`
          - :math:`2\sqrt{2}`
        * - :math:`v_3`
          - :math:`v_2^2`
          - :math:`\frac{1}{2}`
          - :math:`2v_2\dot{v_2}`
          - 4
        * - :math:`v_4`
          - :math:`-2v_3`
          - 1
          - :math:`-2\dot{v_3}`
          - -8
        * - :math:`v_5`
          - :math:`exp(v_4)`
          - :math:`\frac{1}{e}`
          - :math:`exp(v_4)\dot{v_4}`
          - :math:`\frac{-8}{e}`
        * - :math:`v_6`
          - :math:`-v_5`
          - :math:`\frac{-1}{e}`
          - :math:`-\dot{v_5}`
          - :math:`\frac{8}{e}`
        * - :math:`v_7`
          - :math:`x_1 + v_6`
          - :math:`\frac{\pi}{16}-\frac{1}{e}`
          - :math:`\dot{x_1}+\dot{v_6}`
          - :math:`1+\frac{8}{e}`
        
          

The visualization tool from the first module also computes the computational table. Input the function and
compare the forward mode graph to the forward mode table.

Notice how the computational trace corresponds to the nodes on the graph and the edges linking these nodes. Note that the
choices of labels for the traces might be different than the table we wrote by hand - compare the labels for the nodes in the
graph.


Multiple Inputs
^^^^^^^^^^^^^^^
Now let's consider an example with multiple inputs. The computed derivative is now the gradient vector. Instead of
maintaining an evaluation trace of a scalar derivative for a single input, we instead have a trace of the gradient for
multiple inputs. 

In the exercises in the previous module, we practiced drawing the graph for the function

.. math::
        f(x,y) = \exp(-(\sin(x)-\cos(y))^2).

Try to draw the graph by hand. The graph you drew should have the same structure as the graph below, which was produced with
the visualization tool (with the exception of possibly interchanging some of the labels).

.. image:: Mod1Ex3Sol.PNG

We can also use the visualization tool to see the computational table which corresponds to the graph. 

.. image:: Mod2Table.PNG

Observe that the derivative in our table is now a 2 dimensional vector, corresponding to the gradient, where each component is the derivative
with respect to one of our inputs. Also notice that this table does not include the columns for the elementary function or
its derivative. Those columns are useful for learning how things work, but ultimately automatic differentiation does not need
to store them; it only needs to store the value. Note too that the interpretation of :math:`\dot{x}` must be generalized. The
dot now represents a derivative with respect to one or the other input depending on the context. Lastly, the table does not
include any symbolic numbers. Instead, it presents values with as much precision as the computer allows to emphasize that
automatic differentiation computes derivatives to machine precision.


Note that computing the gradient for this multivariate function is done by assigning a seed vector to each input, where to
find the gradient we use the standard basis vectors as seeds.  We'll discuss more about what this means automatic
differentiation is computing in the next section.

II. More Theory
---------------
Review of the Chain Rule
^^^^^^^^^^^^^^^^^^^^^^^^
We already saw the chain rule in one dimension and we even saw it in action in the trace table examples. Here, we build up to
a more general chain rule.

a. Back to the Beginning
""""""""""""""""""""""""
Suppose we have a function :math:`h(u(t))` and we want the derivative of :math:`h` with respect to :math:`t`. The chain rule gives,

.. math::
        \dfrac{\partial h}{\partial t} = \dfrac{\partial h}{\partial u}\dfrac{\partial u}{\partial t}.

For example, consider :math:`h(u(t)) = \sin(4t)`. Then :math:`h(u) = \sin(u)` and :math:`u = 4t`. So 

.. math::
        \dfrac{\partial h}{\partial u} = \cos(u), \quad \dfrac{\partial u}{\partial t} = 4 \quad \Rightarrow \quad
        \dfrac{\partial h}{\partial t} = 4\cos(4t).

b. Adding an Argument
"""""""""""""""""""""
Now suppose that :math:`h` has another argument so that we have :math:`h(u(t), v(t))`. Once again, we want the derivative of :math:`h`
with respect to :math:`t`. Applying the chain rule in this case gives,

.. math::
        \dfrac{\partial h}{\partial t} = \dfrac{\partial h}{\partial u}\dfrac{\partial u}{\partial t} + \dfrac{\partial
        h}{\partial v}\dfrac{\partial v}{\partial t}.

c. Accounting for Multiple Inputs
"""""""""""""""""""""""""""""""""
What if we replace :math:`t` by a vector :math:`x\in\mathbb{R}^{m}`? Now what we really want is the *gradient* of :math:`h` with respect to
:math:`x`. We write :math:`h = h(u(x), v(x))` and the derivative is now,

.. math::
        \nabla_{x}h = \dfrac{\partial h}{\partial u}\nabla u + \dfrac{\partial h}{\partial v}\nabla v, 

where we have written :math:`\nabla_{x}` on the left hand size to avoid any confusion with arguments. The gradient operator on the
right hand side is clearly with respect to :math:`x` since :math:`u` and :math:`v` have no other arguments.

As an example, consider :math:`h = \sin(x_{1}x_{2})\cos(x_{1} + x_{2})`. Let's say :math:`u(x) = u(x_{1}, x_{2}) =
x_{1}x_{2}` and :math:`v(x) = v(x_{1}, x_{2}) = x_{1} + x_{2}`. We can re-write :math:`h` as :math:`h = \sin(u(x))\cos(v(x))`.
Then,

.. math::
        \dfrac{\partial h}{\partial u} = \cos(u)\cos(v), \quad \dfrac{\partial h}{\partial v} = -\sin(u)\sin(v),

and

.. math::
        \nabla u = \begin{bmatrix} x_{2} \\ x_{1} \end{bmatrix}, \quad \nabla v = \begin{bmatrix} 1 \\ 1 \end{bmatrix},

so 

.. math::
        \nabla_{x}h = \cos(x_{1}x_{2})\cos(x_{1} + x_{2})\begin{bmatrix} x_{2} \\ x_{1} \end{bmatrix} - \sin(x_{1} +
        x_{2})\sin(x_{1} + x_{2})\begin{bmatrix} 1 \\ 1 \end{bmatrix}.

d. The (Almost) General Rule
""""""""""""""""""""""""""""
More generally, :math:`h = h(y(x))` where :math:`y \in \mathbb{R}^{n}` and :math:`x \in \mathbb{R}^{m}`. Now :math:`h` is a
function of possibly :math:`n` other functions, themselves a function of :math:`m` variables. The gradient of :math:`h` is now given by,

.. math::
        \nabla_{x}h = \sum_{i=1}^{n}{\dfrac{\partial h}{\partial y_{i}}\nabla y_{i}(x)}.

We can repeat the example from the previous section to help reinforce notation. This time, say :math:`y_{1} = x_{1}x_{2}` and
:math:`y_{2} = x_{1} + x_{2}`. Then,

.. math::
        \dfrac{\partial h}{\partial y_{1}} = \cos(y_{1})\cos(y_{2}), \quad \dfrac{\partial h}{\partial y_{2}} =
        -\sin(y_{1})\sin(y_{2}),

and

.. math::
        \nabla y_{1} = \begin{bmatrix} x_{2} \\ x_{1} \end{bmatrix}, \quad \nabla y_{2} = \begin{bmatrix} 1 \\ 1
        \end{bmatrix}.

Putting everything together gives the same result as in the previous section.

The chain rule is more general than even this case. We could have nested compositions of functions, which would lead to a
more involved formula of products. We'll stop here for now and simply comment that automatic differentiation can handle
nested compositions of functions as deep as we want for arbitrarily large inputs.

     
What Does Forward Mode Compute?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By now you must be wondering what forward mode *actually* computes. Sure, it gives us the numerical value of the derivative
at a specific evaluation point of a function. But it can do even more than that.

In the most general case, we are interested in computing Jacobians of vector valued functions of multiple variables. To
compute these individual gradients, we started our evaluation table with a seed vector, :math:`p`. One way to think about this is
through the directional derivative, defined as: 

.. math::
        D_{p}f = \nabla f \cdot p

where :math:`D_{p}` is the directional derivative in the direction of :math:`p` and :math:`f` is the function we want to differentiate.
In two dimensions, we have :math:`f = f(x_{1},x_{2})` and 

.. math::
        \nabla f = \begin{bmatrix} \dfrac{\partial f}{\partial x} \\ \dfrac{\partial f}{\partial y}\end{bmatrix}.

The seed vector (or "direction") is :math:`p = (p_{1}, p_{2})`. Carrying out the dot product in the directional derivative
gives, 

.. math::
        D_{p}f = \dfrac{\partial f}{\partial x}p_{1} + \dfrac{\partial f}{\partial y}p_{2}.

Now here comes the cool part. *We can choose* `p`. If we choose :math:`p=(1,0)` then we get the partial with respect to :math:`x`.
If we choose :math:`p=(0,1)` then we get the partial with respect to :math:`y`. This is really powerful! For arbitrary choices of :math:`p`, we
get a linear combination of the partial derivatives representing the gradient in the direction of :math:`p`.


Simple Demo
"""""""""""
To see this in action, let's consider the function :math:`f(x,y) = xy`. The figure below shows the graph and the trace table
evaluating the function at the point :math:`(a,b)`. The difference between the previous versions of the table is the
introduction of an arbitrary seed vector :math:`p = (p_{1},p_{2}`. Notice that the result is :math:`ap_{2} + bp_{1}` and make
sure you verify this. If we choose :math:`p=(1,0)` we simply get :math:`b`, which is just :math:`\dfrac{\partial f}{\partial x}`.
Depending on how we choose the vector :math:`p`, we can evaluate the the gradient in any direction.

.. image::
         fxy_seed.PNG

Now, you have likely noticed that choosing :math:`p=(0,1)` will give :math:`a`, which is :math:`\dfrac{\partial f}{\partial y}`. So even
though it's really cool that we can get the directional derivative, we might just want the regular gradient. This can be
accomplished by first selecting the seed :math:`p=(1,0)` and then selecting :math:`p=(0,1)`, but of course this is too much work. We
don't want to rebuild the graph for every new seed if we don't have to. Another option is to just define as many seeds as we
want and carry them along at each step. The next figure shows what this could look like for two seeds. Observe that using
:math:`p=(1,0)` and :math:`q=(0,1)` gives the actual gradient.

.. image::
         fxy_all_seeds.PNG

Two-Dimensional Demo
""""""""""""""""""""
Here's another example to show that the forward mode calculates :math:`Jp`, the Jacobian-vector product. Consider the
following function,

.. math::
        f(x,y) = \begin{bmatrix} x^{2} + y^{2} \\ e^{x+y} \end{bmatrix}.

We can calcuate the Jacobian by hand just to have it in our back pocket for comparison purposes.

.. math::
        J = \begin{bmatrix} 2x & 2y \\ e^{x+y} & e^{x+y} \end{bmatrix}.

The Jacobian-vector product with a vector :math:`p` (our seed) is,

.. math::
        Jp = \begin{bmatrix} 2x & 2y \\ e^{x+y} & e^{x+y} \end{bmatrix} \begin{bmatrix} p_{1} \\ p_{2} \end{bmatrix} =
             \begin{bmatrix} 2x p_{1} + 2y p_{2} \\ e^{x+y} p_{1} + e^{x+y} p_{2} \end{bmatrix}.

Before we launch into our manual automatic differentiation, let's say we want to evaluate all of this at the point :math:`(1,1)`.
Then,

.. math::
        f(1,1) &= \begin{bmatrix} 2 \\ e^{2} \end{bmatrix} \\
        J &= \begin{bmatrix} 2 & 2 \\ e^{2} & e^{2} \end{bmatrix} \\
        Jp &= \begin{bmatrix} 2p_{1} + 2p_{2} \\ e^{2}p_{1} + e^{2}p_{2} \end{bmatrix}.

The next figure shows a table representing the computational trace for this function using an arbitrary seed. The result is
precisely the Jacobian-vector product.

.. image::
         jac_prod_seed.PNG

Similarly, the figure below depicts the same table using two arbitrary seeds. Make note of what happens when :math:`p=(1,0)`
and :math:`q=(0,1)`.

.. image::
         jac_prod_all_seeds.PNG



III. Exercises
--------------
Exercise 1: Neural Network Problem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Artificial neural networks take as input the values of an input layer of neurons and combine these inputs in a series of layers to compute an output.  A small network with a single hidden layer is drawn below.

.. image::
        NNFigNoPhi.png

The network can be expressed in matrix notation as

.. math::
        f(x,y) = w_{out}^Tz\left(W\begin{bmatrix} x \\ y \end{bmatrix} + \begin{bmatrix}b_1 \\ b_2 \end{bmatrix}\right)+b_{out}

where

.. math::
        W = \begin{bmatrix} w_{11} & w_{12} \\ w_{21} & w_{22}\end{bmatrix}

is a (real) matrix of weights, and

.. math::
        w_{out} = \begin{bmatrix}w_{out,1} \\ w_{out,2}\end{bmatrix}

is a vector representing output weights, :math:`b_i` are bias terms and :math:`z` is a nonlinear function that acts component wise.

The above graph helps us visualize the computation in different layers.  This visualization hides many of the underlying operations which occur in the computation of :math:`f` (e.g. it does not explicitly express the elementary operations).

**Your Tasks**

In this part, you will completely neglect the biases.  The mathematical form is therefore

.. math::
        f(x,y) = w_{out}^Tz\left(W\begin{bmatrix}x \\ y \end{bmatrix}\right).

Note that in practical applications the biases play a key role.  However, we have elected to neglect them in this problem so that your results are more readable.  You will complete the two steps below while neglecting the bias terms.

1. Draw the complete forward computational graph.  You may treat :math:`z` as a single elementary operation.  You should explicitly show the multiplications and additions that are masked in the schematic of the network above.
2. Use your graph to write out the full forward mode table, including columns for the trace, elementary function, current function value, elementary function, derivative, partial :math:`x` derivative, and partial :math:`y` derivative.

Exercise 2: Operation Count Problem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Count the number of operations required to compute the derivatives in the `Simple Demo <#simple-demo>`_ and the `Two-Dimensional Demo <#two-dimensional-demo>`_ above. For
each demo, only keep track of the additions and multiplications.
