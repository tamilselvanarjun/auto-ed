Module 4: Beyond the Basics: Extensions and Software Development
================================================================

We have presented one way of thinking about automatic differentiation and the graph structure of functions which underly the
computations in both forward and reverse mode.  This section includes another way of thinking about automatic differentiation
through dual numbers and considerations about how to implement automatic differentiation in software.

The Dual Numbers
----------------
Another way to think about automatic differentiation is through the dual numbers.  Like complex numbers, which are written
a+bi with real and imaginary part, we write the dual numbers as :math:`a+b\epsilon` with real and dual part.  Similarly to
the imaginary numbers where :math:`i^2 = -1`, we have :math:`\epsilon^2=0` for the dual numbers.  Note that :math:`\epsilon`
is not equal to zero, but is a nonreal constant defined by this property.  We will now see why this is useful when we
consider the relationship between the dual numbers and differentiation.

Consider the function y=x^2 whose derivative we know to be 2x.  Let's evaluate y at the dual number :math:`a+b\epsilon`.  

.. math::
        y = (a+b\epsilon)^2 = a^2+2ab\epsilon+b^2\epsilon^2.  
        
By the property of :math:`\epsilon`, this is just the dual number :math:`a^2+2ab\epsilon`.  Taking b=1, the real part of the
dual number y is the function y evaluated at x=a, and the dual part of the dual number y is the derivative of y evaluated at
x=a.

Let's consider a second example.  This time let :math:`y=sin(x)`.  Again, let's evaluate at :math:`x=a+b\epsilon`.  Using the
angle addition formula,

.. math::
        y = sin(a+b\epsilon) = sin(a)cos(\epsilon b)+cos(a)sin(b\epsilon)

To further simplify this expression, we can write :math:`sin(b\epsilon)` and :math:`cos(b\epsilon)` as Taylor series.

.. math::
        sin(b\epsilon) = b\epsilon + (\epsilon b)^3/3! + ...
        cos(b\epsilon) = 1+(\epsilon b)^2/2+ ...

By the property of \epsilon, powers of \epsilon greater than 2 are 0, giving us :math:`sin(b\epsilon) = \epsilon b` and
:math:`cos(b\epsilon) = 1`.  Substituting these expressions back into y, we have :math:`y = sin(a)+cos(a)b\epsilon`, and as
in the previous example, the real part is the function evaluated at a and the dual component is the derivative evaluated at
a.

Toward Software Implementation
------------------------------
In our discussion of automatic differentiation, we noted that automatic differentiation is possible because functions can be
decomposed into elementary functions whose derivatives we know explicitly.  Implementing this in software requires code so
that these known derivatives are coded as part of the function.  We can do this through operator overloading.

In operator overloading, we use different implementation of operators depending on the class of the object that is being
operated on.  This can be done easily in Python by redefining the dunder methods for basic operations (i.e., __add__,
__radd__, __pow__, __rpow__, etc.) for a class of automatic differentiation objects.

We can see an example of operator overloading in rewriting addition for a class defined for complex numbers.

.. code-block:: py

        class Complex():
            def __init__(self, a, b):
                self.a = a #real part
                self.b = b #imaginary part

            def __add__(self, other):
                #overload addition, addition for complex numbers is component-wise
                return Complex(self.a+other.a, self.b+other.b)

In our computational tables, we saw that each node of the graph in foward mode had a function evaluation and a derivative
component, similar to the dual numbers.  We can use operator overloading to specify how the different elementary operations
and functions act on these two components to produce a new node with a function evaluation and derivative.

Exercises
---------
Exercise 1: Dual Numbers
++++++++++++++++++++++++
Using the dual numbers, find the derivative of :math:`y=e^{x^2}`.  Note that you will need to use Taylor series.

Exercise 2: Toy AD Example
++++++++++++++++++++++++++
Write a forward mode automatic differentiation class capable of handling functions composed of addition and multiplication
operations.  The class AutoDiffToy should return the value and derivative of functions of the form :math:`f(x)=\alpha
x+\beta` for :math:`\alpha , \beta` real constants.

Some thoughts on implementation:

* The constructor should set the value of the function and the derivative.  This is similar to the first row in the
  computational tables.
* Overload operations as appropriate.  Note that Python's __add__(self, other) and __mul__(self, other) methods are meant to
  be defined for objects of the same type, so your implementation should not assume that other is a real number but be robust
  enough to handle the case where it is.
* Handle exceptions appropriately.  You may want to use duck-typing, where rather than checking if an argument to a special
  method is an instance of the object, you instead use a try-except block and catch an AttributeError.
* Make your implementation robust encough to handle functions written as ``f = alpha*x+beta, f=x*alpha+beta,
  f=beta+alpha*x, f=beta+x*alpha``.

Example Use Case:

.. code-block:: py

        a = 2.0 #value to evaluate at
        x = AutoDiffToy(a)

        alpha = 2.0
        beta = 3.0
        f = alpha*x + beta #define function

        print(f.val, f.der)

        >>> 7.0 2.0

