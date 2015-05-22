Title: A monad? Probably not what you need...
Subtitle: Just some random thoughts on "should I use monads for this"
Author: Karol Majta
Date: 2015-01-02 21:00
Tags: Programming, Monad

This morning my friend messaged me with a question if he should "use
monads" to solve his problem. I was just writing a short explanation for
him, but in some mysterious ways it grew longer and longer, to finally
become this beast. I've decided to put it online but first spread a sefty
net by placing a disclaimer paragraph.

So here it goes: my understanding of monads is fully intuitive and this
article may contain errors, or just plain nonsense. Yet I am insolent enough
to see it as a good thing (the intuition, not errors). I am an average
developer tackling day-to-day problems, and most of newcomers to monads
will be too. This article is also an obvious ripoff, but if you're a
self-learned programmer you have to learn *somewhere*. If you're curious
enough to care, links to some resources that I found informative/fun
are at the end of this article. To conclude, this thing is more anecdotal
than informative.

Getting a "monad" in Python
---------------------------

"Monads" in Python don't make much sense, so dont take any of this
very seriously:

    :::python
    def operator(lambda_and_arg, how_many=0):
        """
        Get lambda and arg from `lambda_and_arg` and call lambda with arg.
        In addition return incremented value of how_many (it denotes how_many
        times `operator` was called already.
        """
        _lambda, arg = lambda_and_arg
        return _lambda(arg), how_many+1

Now we can roll with it like this:

    :::python
    >>> operator((math.sqrt, 4))
    (2.0, 1)
    >>> operator((math.cos, 0), how_many=3)
    (1.0, 4)
    >>> operator((lambda x: x+1, 10), how_many=2)
    (11, 3)

Well, `operator` is beautiful, it's pure, so it's output depends solely
on its input, unittestable, etc, but nobody in the company wants to use
it because it actually needs manual bookkeeping of `how_many`:

    :::python
    >>> x1, n = operator((lambda x: x>0, -3))
    >>> # (False, 1)
    >>> x2, n = operator((math.sin, 0), how_many=n)
    >>> # (0.0, 2)

Aint noboty got time for that... So we can make our operator stateful, in
a weird way...

    :::python
    class Op(object):

    def __init__(self, val):
        self.transformed = False
        self.call_count = val.call_count if isinstance(val, Op) else 1
        self.value = val.value if isinstance(val, Op) else val

    def __repr__(self):
        return repr((self.value, self.call_count))

    def op(self, transformation):
        cc = 1 if not self.transformed else self.call_count + 1
        res = transformation(self.value)
        cc += 1 if res.transformed else 0
        res.transformed = True
        res.call_count = cc
        return res

This is how the usage mightt look:

    :::python
    >>> Op(10).op(lambda x: Op(x > 0)).op(lambda x: Op("YUP!" if x else "NAH..."))
    ("YUP!", 3)
    >>> Op([1, 2, 3])
    ([1, 2, 3], 1)
    >>> Op(Op(20))
    (20, 1)

I've explicitly omitted getting `self.value` in shell, as by default monads
are not obligated to povide any facility to "pull the value out".
They can, but dont have to. And if they do, its because they're nice
to you, not because they're monads.

Now let's have a look at Haskells monad typeclass. It is required to
define two functions:

- `return` which roughly translates to 'take my value and wrap it in
   a context (in our usecase take our value and add some implicit state)'
- `bind` which roughly translates to 'take my value and do some extra stuff'
   and return something that i can bind to again

At this point it should be clear, that `Op` is `return` and `op` is
`bind`. At this point we should also check that `Op` conforms to so-called
*monad laws*.

`Op(x).op(y)` should be same as `y(x)`.

    :::python
    >>> Op([1, 2, 3]).op(lambda x: Op(len(x)))
    (3, 1)
    >>> (lambda x: Op(len(x)))([1, 2, 3])
    (3, 1)

`Op(x).op(Op)` should be the same as Op(x).

    :::python
    >>> Op("hello")
    ("hello", 1)
    >>> Op("hello").op(Op)
    ("hello", 1)


`Op(x).op(f).op(g)` should be the same as Op(x).op(lambda x: f(x).op(g))`:

    :::python
    >>> # this one is much more clear if we define some helper functions
    >>> def f(x): return Op(x.strip())
    >>> def g(x): return Op(x.trim())
    >>> Op('  hello  ').op(f).op(g)
    ('HELLO', 2)
    >>> Op(' hello  ').op(lambda x: f(x).op(g))
    ('HELLO', 2)

What's in it for me?
--------------------

Alright, back to the point. What do "monads" give you? The answer is...
It depends.
If yo do OOP, the answer is probably...
*not very much*
If you program in dynamically typed language the answer is...
*not very much*
If you program in imperative language the answer is...
*not very much*

Let's elaborate on point 3 for a while as it yields some interesting
afterthougths. Imperative programming languages have strict order of
operations, so the flow of such thing in python is obvious:

    a(b(), c())

Both b and c need to be evaluated, because a needs them. The order of
operations is left-to-right, so b is evaluated first, c second, and
then, with their return values, a is evaluated. This means, that
if a, b or c hit stdio, they do it in particular order.

Haskell is a lazily evaluated language, which means, that if we never
use the value of a in IO context (which commonly means one of: print em,
store em, or send em over a wire) they will never execute their side effect.

Haskell compiler does arbitrary reordering of expressions according to
some rules, so if we call `a(b(), c())` there is no guarantee on the order
of calls to b and c (and while there is no memoization by default, there
is also no guarantee to the number of calls).

So basically, Haskells IO monad does two things. It says "execute this
stuff, I need it for side effects" and also takes care about the order
of execution (the order of execution seems to be the perk that actually
sprouts from the mathematical definition of monad).

If you're programming in imperative language you probably don't need
to care for any of these things (most of the time).

So, what's the deal with with dynamically typed languages? Well... I've
seen monads done in in perl, ruby, python, javascript and my only
thought was... seriously, give yourself a break. I mean, yes - you can do
that, but if your `return` is expected to return something you can bind to,
but the runtime allows you to return null, 32, or any random stuff, than you
have more serious problems to worry about. So stop bragging about your
understanding of monads and go write some unittests. Oh, and btw, yes
I do most of development in dynamically typed languages.

Just to stop ranting for a while. As I've stated in the second python
example, once you "put something into a monad" you can "do stuff
to it" but you can never "pull it out", this is like the number one rule
of monads (or more likely the n-th rule of monads, I don't know them
that well). So, in our python example, naming `Op` "a monad" is quite
pointless.

    :::python
    >>> a = Op(10).op(lambda x: Op(x+1)).op(lambda x: Op(2*x))
    (22, 2)
    >>> print a.value
    22
    >>> a.call_count = 10
    >>> a.op(lambda x: Op(0))
    (0, 11)

We've just messed internals of our "monad", so calling it "a monad" is just
introducing abstraction/complexity while gaining nothing. It's like
having a girlfriend with no benefits.

Don't do it. You will just confuse your coworkers.

It's my private opinion, but to have a proper monad you need at least
"private" member protection in your runtime. And to squeeze it to the max
you need a static type system.

Alright, so back to point 1. What can you get from monads if you're doing
OOP instead of functional-style programming? Our python example uses
"a monad" to manage state, but if you have a language that supports stateful
objects, then just use them (in a smart way). The State monad in Haskell
is there just to mitigate the fact, that the language has no variable state.

Some may argue this is a good thing. You are free to pick sides.

Of course there are some benefits of using monadic style with OOP. Most
of them relate to the "can't pull it out" rule and ordering of operations.

If you're doing scala you probably know something called Option. This is like
the most awesome and simple monad I've seen. It's super *useful* to mitigate
null return values in your code. You returne Some(thing) or Nothing instead. While
it might not seem like much, it guarantees that functions that use this value
will take Option as argument, and handle it explicitly. By the way... You
can exploit this behavior having no clue that Option actually is a monad.

The other thing are futures/deferreds/promises. I will give example in JS
because I feel most comfortable with kriskowal's Q deferred API. If you feel
uncomfortable reading this after I've criticized dynamic languages you are
free to stop here.

    :::javascript
    var d = Q.defer();
    jQuery.get("http://google.com", {}, function (resp) { d.resolve(resp); });

    // yeah, i know jquery ajax calls return promises by themselves, just
    // wanted to be more explicit
    //
    // now watch the magic...
    //

    var initialUppercased = d.promise
      .then(function (resp) { return resp.toUpperCase(); })
      .then(function (uppercased) { return uppercased.slice(100); });

We can say initialUppercased is a promise of some text
See the typeclass analogy?
`initialUppercased` is actually Promise(String)

The nice thing about promises is the fact that they show monads both in
context of "operation ordering" and "cant pull the value out".
(The Option/Maybe example above shows only the latter). While the
first one seems obvious (or should i make another http request inside
one of `then` calls?) the second one needs to be elaborated upon. Once
you get a promise, you can only "bind" to it by calling `then`. There is
no way to get `resp` or `uppercased`. In your code somewhere we would
probably see.

    :::javascript
    initialUppercased.then(function (val) { jQuery('body').text(val); });

The fact that you can use the actual value (you could have as well
assigned it to `window.property` instead of modifying DOM) is the
fact that JS allows arbitrary state mutations. What you definately
don't want in your code is:

    :::javascript
    var d = Q.defer();
    var result = undefined;
    jQuery.get("http://google.com", {}, function (resp) { result = resp; });
    console.log(result);

The only way you can access the response is by "binding" with then.
The fact that at some point you can store the raw value in global for
reuse is just a peculiarity of JS runtime.

Alright, so what comes out of this?

Basically I see monads fit for doing four things:

  - Making sure that things "are done" in some context and cannot
    be "pulled out of it" (for some languages the compiler will take
    care of it, for others you have to depend on developer's good will,
    so the benefit can be easily lost)
  - Assuring order of operations (in imperative programming useful in
    async contexts)
  - Implicit state handling (in OOP you probably have other means that
    are simple and easier to understand for most people).
  - Assuring that operations will happen at all (important with
    Haskell and it's lazy IO)

Of course monads (presumably) can do much more, but (please don't hate
me on me) I still cannot figure out how to use the fact that List are monads
in a *productive* way.

Isn't the right question a key to right answer?
-----------------------------------------------

It might be useful to know what monads are, but wouldn't it be even
better to know when to use them?

Let's ask a more perverse question: "When are monads developed?".

Well, for most of the time, people just solve problems, and notice that
the solution they came to is "monadic", which basically means:

    Hey Mike, method thing we call here looks like `return` and the second
    one looks like `bind`. It seems oure JavaScript promise API is monadic.

This is cool.

There is a sweet spot for monads in Haskell, but as I've stated before, I
see the IO and State as prosthesis. It's not a bad thing. Haskell has its
ways and is a super-interesting programming language, which compiles to
machine code, is garbage-collected yet fast, lazy and overally **seems
awesome**. You must expect a price to pay for this.

This is cool too.

And there is a camp of "monadistas", who will try to create monadic style
for assembly language while bragging about their PhD in mathematics
(just kidding, math people are usually super-nice and helpful, and
rarely know assembly).

The best you can do is just ignore the noise.

The links, and the disclaimer after disclaimer
----------------------------------------------

Ok, here go the links to interesting stuff:

- https://www.haskell.org/haskellwiki/IO_inside (paragraph 3 is what you're
  looking for)
- https://byorgey.wordpress.com/2009/01/12/abstraction-intuition-and-the-monad-tutorial-fallacy/
  (this is awesome stuff, not only for understanding monads, but also for
  anyone who ever plans to teach something to someone)
- http://learnyouahaskell.com/ (valuable examples are spread all across this book,
  and it's top notch by itself)

The last thing I want to add is the fact that our `Op` is the most dull
monad example. If I were to write this from scratch I would probably come up
with a more interesting one.

Oh and one more notion. I honestly think that the fact, that "hello world"
in Haskell requires using an IO monad is responsible for most of confustion
and hype around them!
