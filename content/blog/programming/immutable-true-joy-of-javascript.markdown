Title: Immutable.js
Subtitle: The True Joy of JavaScript
Author: Karol Majta
Date: 2015-09-27 17:30
Tags: Immutable.js, EcpaScript, JavaScript, ES6

I remember when a few years ago I bumped into *Beginning Scala by David Pollak*. At the time I had no idea how this book would impact my future choices on which programming languages to learn, which technologies to invest my time in, and what I consider "good stuff" in general. Reading it must have been one of these movie-like moments of enlightment, with a heavenly beam of light striking you from above Mr. Bean style. Even today I can clearly remember the title of chapter that made the strongest impression. It was *Collections and the Joy of Immutability*.

I've re-read this chapter, just to be sure my thoughts are not driven by pure nostalgia, and well... it's still a valuable piece. Some of the stuff that are shown there, like simple map/reduce operations and option type, would now seem obvious to me, but it definately did preserve it's main virtue -- it shows how to do stuff right. I remember that the excitation was fueled by a feeling that what I just read is **right**. Please let me rephrase: I didn't feel that it was how Scala works, I didn't feel that it just made sense, although what I saw was correct, I could not care less, I just had the feeling that **this is right, this is how you do stuff**, because it complements the nature of things.

In the end I didn't become a successful Scala programmer hacking distributed systems and doing cross-domain stuff related with physics, science, big data, gazillions of dollars and unicorns. I pursued a much more humble career of frontend developer instead.

In the meantime I kind of fell in love with Clojure, and there I was... Dreaming about doing programming the way I feel it should be done, while struggling with relatively fragile and lacking Javascript ecosystem. Even though I can't stress more that JS did and still does get better, you have to admit that when it comes to serious work it's still behind. Some of the problems are not endemic to Javascript -- you can get subtle *hindenbugs* related to weak type system in Python or virtually any language that does not actively prohibit implicit casting or type promotion (does statically typed ANSI C ring a bell?). Some of them are a result of a long lasting neglect on the side of both community and commitees, that led to current state of affairs, when doing fixed precision or big number arithmetics is a no-no and will almost always *take you on an adventure*, to put things mildly. This is even more evident in the browser, because in contrary to NodeJS, you cannot utilize bindings to quality math libraries.

## High Hopes

Everyone in the community is talking about ECMAScript 6. I don't want to sound like a grumpy software developer, but let's do a quick walthrough of ES6 goodies (following [ES6 features by Luke Hoban](https://github.com/lukehoban/es6features)).

*Arrows*, *enhanced object literals*, *destructuring*, *default/rest/spread parameters*, *binary/octal literals* and *template strings* are all basically sugar. You can have most of it in ES5, but you have to pay a price of additional boilerplate and following some convention.

*Symbols* without dedicated syntax really look like a bad joke. *TCO* is neat, but you can live without it.

*Promises*? It's a nice-to-have, but since there is already at least a handful of quality promise libraries in the wild, I see no clear motivation behind putting them into language core. Let's look at the interface that ES6 authors chose to implement:

    new Promise(function(resolve, reject) { ... });

Unfortunately this proposal is lacking in comparison to some community created sulutions. It forces the user into assumption that the party that creates (makes) the promise is the same one that is responsible for delivering it. Unfortunately this is not always the case, and an explicit notion of **deferred** (as introduced by [Kris Kowal's Q](https://github.com/kriskowal/q)) allows much more flexibility:

    // defer some computation:
    var d = Q.defer();
    // pass the promise of the computation result into a component
    // responsible of handling the result
    someResultHandler(d.promise);
    // someone else can be responsible for delivering the result,
    // receiving both success and error callback functions to call
    // at the end of computation
    taskExecutor(d.reject, d.resolve);

Yes, it's not difficult to roll your own deferreds, but why not provide them out of the box?

*"Classes"* are a pretty neat sugar over prototypal inheritance, but I am pretty sure that syntax and keywords similar to Java/C++ will lure newcomers into thinking they are doing traditional class based OOP, while they're not. *Proxy objects* seem like a good idea, and might be a useful alternative for things like magic methods in Python. The fact that builtins are extensible is also a good thing.

*Modules* and *module loaders* are a really neat stuff, and they might change the way we develop and structure applications. The only problem is, for ES6 modules to actually work, we need wide adoption of ES6 across all browsers in the wild.

New ES6 features are all long awaited, but they don't have the potential to radicaly change the way we build web applications. There's nothing wrong about it. Modifying a software project that's running in production is like fixing a flying plane. With JavaScript -- a language that fuels millions of webpages, it's more like having a whole airline. You have to move very carefully, and in essence, it's better to introduce less features, than to have harmful impact on what's already in the wild.

## Silent Revolution vs. Loud Evolution

It's hard to fight a thought, that although widely discussed, and quite "loud", ES6 is no revolution and has no potential on really broadening the JS horizon. Bulk of features seem to be bolted on top of language core as an afterthought in a somewhat random fashion, similar to true biological evolution, where fenotypes (features) show up as a result of mutation just to disappear a few generations later.

At the same time, just before our eyes, in a much more humble manner, Immutable.js sprouts. In my personal opinion it can have much wider impact than all ES6 features altogether. Just let me get there...

I've ommited new JS data types (namely *Map*, *Set* and their *Weak* counterparts) in the previous paragraph above on purpose, along with *iterators* and *generators*. This is because they are in close relation to Immutable.js.

*Generators* and *iterators* are a really long awaited feature, and with **yield** keyword they provide a succint way for working with unrealized sequences. Immutable's **Seq** makes heavy use out of it when dealing with lazy sequence processing and generation. ES7 with **await** might shed new light on how we deal with async in JS.

Let's get to the data structures. We will leave out *WeakMap* and *WeakSet*. They have their use-cases, and rightfuly found their way into JS runtime (every garbage collected language I know has some data structure that allows storing objects without incrementing the ref-count, so JS deserves one too). However they are only fit for fraction of use-cases. For majority of cases, you want to use *Map* and *Set*. It's good they're here but...

Let's start with *Set*. The API is lacking. We have some barebone `add`, `delete`, `entries` and `clear` methods, but that's basically it. I can't even find proper words to describe how I feel about the fact, that all set operations (*union*, *difference*, *intersect*) are missing. Let me quote MDN code sample:

    // intersect can be simulated via  
    var intersection = new Set([x for (x of set1) if (set2.has(x))]);

Simulated? Really? It really sounds like someone who designed this API was trying to simulate giving everyone a finger.

*Map*? As a data container it's lightyears in front of the good old *Object*. It can be keyed with in essence anything (both primitives and compound types, and you are safe, that the key won't get casted to string). On the other hand, it provides a bare minimum API while being insanely permissive. In a bad way.

Even Python, a language that embraces dynamic approach to programming, will sometimes prevent you from doing weird stuff with its standard containers:

    >>> a = dict()
    >>> a[dict()] = 1
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unhashable type: 'dict'

You'd get the same error for lists, but let's stick with dict example for reference. Aside for alert 
readers -- I leave out the discussion of using objects (class instances) as keys, because they're not data containers of the first choice. I think of objects as "bags of functionality".

You get the errors, because identity based equality makes no sense for dicts, lists or any mutable piece of *data*. Let's bring a quote from *The Joy of Clojure* to back my words:

> Equality in the presence of mutability has no meaning. (...) If any two objects resolve as
> being equal now, then there’s no guarantee that they will a moment from now. And if two
> objects aren’t equal forever, then they’re technically never equal.

Of course in JS you can do:

    > a = new Map()
    {}
    > a.set({}, 10)
    {}
    > a.get({})
    undefined // obviously, {} != {} in identity terms

This is not all that bad. I've already mentioned, that `Object` is primarily a container for code, not data (and JS used to make no distinction). But since, in ES6 we have hashmaps that are data containers by virtue, so let's try them out:

    > a = new Map()
    {}
    > a.set(new Map(), 10)
    {}
    > a.get(new Map())
    undefined

This is expected, but plain stupid. If you introduce a new construct like **Map** why not sprinkle it with some sanity, like disallowing other maps as keys?

Anyhow, this discussion can be directly translated to JS *Set*, and all charges still hold. *Map* and *Set*, although have some distinctive features, don't provide much more than plain old *Objects* when it comes to modelling and operating on real life data.

In contrary, modelling data is where Immutable.js brings genuine novelty to the table.

## Immutable.js is for Data

There is more than enough resources describing both inner workings of the library and it's API. It's about how you can use it for your advantage when modelling your domain problem as data.

Value based and independent of time (mutation) equality, as given by Immutable, is the key to proper data modelling. Some people will be excited, about immutability and structural sharing, others will talk about proper sequence abstractions, but **sane equality semantics**, is a thing that will give you amazing power, and should not be underestimated.

Let's do some chess moves with Immubale to see how simple it is compared to plain Javascript.

We'll have a black and white knight on a chessboard. Let's define our game state:

    var I = require('immutable'); // use `I` as Immutable's alias
    var assert = require('assert'); // for further use
 
    // in `game` variable we will track whole state of the game 
    var game = I.fromJS({
      currentMove: 'white', // so we know who's move it is, whites start
      board: I.Map([
        [I.List.of(0, 0), 'white'],
        [I.List.of(7, 7), 'black']
      ])
      // we don't need to track all fields in a chessboard. It's sufficient to
      // track only ones that have pieces on them. Instead of (letter, digit)
      // notation we will use numeric indexes. At the beginning we have two
      // knights in adjacent fields of the board
    });

This kind of data structure could be easily build either with plain *Objects* or *Maps*, however leaky equality semantics would make it painful to use in the future (this should become obvious as soon as we start making moves on the board).

First, let's create a little helper for generating valid knight moves:

    var validKnightMoves = function (from) {
      var from = I.List(from);
      var x = from.first();
      var y = from.last();
      return I.Set.of(
        I.List.of(x-1, y+2),
        I.List.of(x+1, y+2),
        I.List.of(x+2, y+1),
        I.List.of(x+2, y-1),
        I.List.of(x+1, y-2),
        I.List.of(x-1, y-2),
        I.List.of(x-2, y-1),
        I.List.of(x-2, y+1)
      );
   };

That's not truly interesting on it's own, yet notice, that although we're using a 3rd party library, the code did not gain much verbosity compared to a pure JS version. Let's do some real moves:

    var makeMove = function (game, from, to) {
      var from = I.List(from);
      var to = I.List(to);
      // let's assert, that what we're trying to do is a valid
      assert(game.getIn(['board', from]), "There is no piece at given field");
      assert(game.getIn(['board', from]) == game.get('currentMove'), "It's the other player's move");
      var inBounds = to.first() >= game.getIn(['bounds', 'x', 0])
                  && to.first() <= game.getIn(['bounds', 'x', 1])
                  && to.last() >= game.getIn(['bounds', 'y', 0])
                  && to.last() <= game.getIn(['bounds', 'y', 1]);
      assert(inBounds, "Move outside board");
      assert(validKnightMoves(from).has(to), "This is not a vald knight move");
      // at this point everyting is valid, so we only need to change
      // associations in our map (which, by accident also handles
      // capturing)
      return game
        .setIn(['board', to], game.getIn(['board', from]))
        .removeIn(['board', from])
        .update('currentMove', function (c) { return c == 'white' ? 'black' : 'white'; });
    };

There are at least a handful of things that are worth noting here. Obviously, this function is referentialy transparent, which means it depends solely on it's inputs and outputs. It is possible to employ such pure functions in pure JS, but please note, how Immutable's API with `setIn`, `removeIn`, and  `update` methods allow us to operate on an *immutable* map in a manner that is really similar to modifying a mutable one (no need to perform explicit copying).

Convenient use of `validKnightMoves` is only possible because of value based equality and rich collections API. Please note, that generating a collection of valid moves, and checking if it contains one would be a really tedious task using just JS primitives, while with Immutable.js it becomes a no-brainer.

Last but not least, each returned *game* is immutable, and I mean it. It effectively cannot be changed as a whole (yet it, or it's parts can be assigned to mutable vars). Immutable data structures are in general thread safe, and can be cheaply and safely shared with everyone. While multithreading is not the case in JS runtime, ease of sharing without fear of unwanted mutation provides great value (and it's not a made up case, you could for example display two initial boards sharing same state, without fear of future moves on the first one interfering with the second one).

And by *immutable* I mean *really immutable*, which means there exists no way to change it once it's returned. Compared to this "true" immutability, the good old `Object.freeze` looks like a toy. By the way, do you know that JavaScript's *Set* and *Map* effectively cannot be frozen? `Object.freeze` only freezez accessor methods, still allowing mutation of internal state.

I've talked a bit about a well designed *Seq* API which abstracts (possibly infinite) sequences. Combined with ES6 *Iterators* and *Generators* this it's a powerful tool (that's why I am really enthusiastic towards this two particular ES6 features), and sprouts elegant solutions. Let's have a look how we could employ Immutable's `Range` to our benefit if we wanted to generate valid bishop's moves.

      var validBishopMoves = function (from) {
        var from = I.List(from);
        var x = from.first();
        var y = from.last();
        var infiniteMoves = I.Range().flatMap(function (i) {
          return [
            I.List.of(x+1+i, y+1+i),
            I.List.of(x+1+i, y-1-i),
            I.List.of(x-1-i, y-1-i),
            I.List.of(x-1-i, y+1+i)
          ];
        });
        return I.Set.of(infiniteMoves.take(7*4));
     };

`infiniteMoves` contains a lazy sequence of bishop's moves that go infinitely north-east, south-east, south-west, and north-west. When we `take` 28 initial elements of this sequence we guarantee that a set can be created in a finite time (sets and maps by design cannot be lazy sequences, so anything you pass to the constructor will be attempted to be eagerly evaluated), and by making the number of items **7*4** we guarantee, that it will allways cover all possibilities on the board, disregarding the initial bishops position (`from`).

Summing things up -- not only does Immutable.js provide succint, well designed API over basic data structures, it does it using persistent, fast, immutable implementation that works well with lazy sequences and ES6 *Iterators* and *Generators*. You might think that's all you could wish for, but to your surprise, there's something more.

## Immutable.js is a rebel

You can think of Immutable.js as of data-structure library. A damn handy, and damn well done library, but only a library. It's can be thought like a screwdriver -- a tool that's great at doing precisely one thing, namely *storing and transforming transient (in-memory) data*. Yet, from time to time we see emergence of a tool that is not only a workflow improvement, but changes how you do stuff in general (think conveyer belts or currency). In my opinion Immutable has this valuable trait: It's inductive to positive change in how we design our JS applications. It can serve as a backbone for data manipulation logic of your application, but it can also improve it's other areas.

We're already seeing an emergence of great libraries and frameworks build on top of Immutable, with Immstruct and Omniscient being really interesting ones. There seems to be great synergy between React.js and Immutable (this is exactly what Omniscient exploits), and I can bet dollars against rupees, that this is just a beginning.
