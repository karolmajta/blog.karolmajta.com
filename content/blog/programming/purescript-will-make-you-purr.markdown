Title: Purescript will make you purr like a kitten
Subtitle: The perils of purescript, npm and browserify combo
Author: Karol Majta
Date: 2015-05-28 14:30
Tags: Purescript, Javascript, npm, browserify

I love Javascript, I really do. It gives you this warm fuzzy feeling in your
belly that you also get when looking at pictures of munchkin cats, unicorns or
budgie parrots. It's totally awesome, like for real, you can show a clock next
to your mouse cursor or allow your users to build a snowman on your landing page
 during Christmas time.

Unfortunately parrots, cats, puppies and unicorns suck at supporting the
economy, and are near to useless during wartime (well, this actually doesn't
apply to unicorns, as facing your enemies riding one would absolutely rock).
It's horses, mules, sheep, pigs and cows that keep the cogs turning with their
daily grind at factories, mills, mines and farms -- just like PHP and Java fuel
the Internet, getting much less love than they deserve.

This *was* the state of affairs for a long time, but somewhere along the way
**frontend** became really *serious business*... and the developers delivered.
They put on their shiny armors of *design patterns*, grabbed shields of
*best practices*, sharpened their swords of *data structures knowledge* and
went to a war for a better web. Riding a munchkin cat.

## Growing a cat into a war stallion

Don't get me wrong... Javascript did get better and with ES6 goodness it is
usable on it's own right here and right now. It has sane package management,
support for modules (you name it,
  [ES6 modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import)
with [traceur](https://github.com/google/traceur-compiler), or CommonJS with [browserify](http://browserify.org/)), promises coming as part of standard, some
sensible data structures being core part of the language. It's not a kitten that
you used to know. On top of that there is a great amount of love from the
community that does its best to support JS with top notch libraries like [ImmutableJs](http://facebook.github.io/immutable-js/),
[React](https://facebook.github.io/react/) and [Angular](https://angularjs.org/)
(despite it recently became community's favorite whipping boy).

Yet, Javascript never was (and honestly, I doubt it can ever become) a language that is a field of serious research of what is possible within a programming language. This is why, while I don't want it to be seen only as *assembly of the web*, I am really sympathetic towards many Javscript
transpilers that have been created. Before we talk purescript let's take a peek at them.

### CoffeScript - *Just make an armor made of sugar!*

I spent a lot of time doing [CoffeeScript](http://coffeescript.org/) and, although I didn't find it a bad experience, I would not ever consider employing it in my own project. Yet, you have to do it justice: it was probably the first *to javascript* transpiler that gained major adoption.

Arrow and fat arrow function syntax, files wrapped in anonymous functions, list comprehensions and other syntactic sugar is what got it fame (and a serious amount of hate too...).

Today CoffeeScript does not give you any extra power in comparison with standard Javascript leveraging [lodash](https://lodash.com/) or [underscore](http://underscorejs.org/). The only good thing about it is that it didn't deviate very far from original language, so entry barrier for Javscript developers that know what they are doing is almost nonexistent. Entry barrier for Ruby developers that had no idea what they're doing was also a bit too low...

### Google Closure Compiler - *Throw out the cat and ride Java!*

[Google Closure Compiler](https://developers.google.com/closure/compiler/) is driving fueling maps and gmail. I didn't spend much time with it, but basically it made a self-contained ecosystem in which employing an external library was a pain. It allows you to do "Java" instead of Javascript, which most Javascript developers find distasteful. Most Java developers that would benefit from it didn't give a damn about good frontend experience anyway. If you ever see the ugliest corporate intranet page you probably know what I'm talking about.

On the bright side, it had sane module system and finally made webapps look more like real applications (with single entrypoint etc.), and made a foundation for Clojurescript and [ScalaJS](http://www.scala-js.org/).

### TypeScript - *Give the cat a type and ride it to the rainbow!*

[Typescript](http://www.typescriptlang.org/) seems to me like an idea that was deliberately crafted for failure since conception. Google Closure Compiler at least came with a handful of libraries and data structures that could be used together in a coherent way. Typescript gives you *types*. Seriously, that's all there is. It also gives you classes (so you can create types, duh), and generics, so you can store and iterate over collection of any type (which basically you can already do in JS, because there is are no static types).

If type-related errors are the biggest problem of your team then you should probably consider splitting the project into more malleable chunks.

If I was to name one on good thing about it is the fact that it integrates with `npm`, but I've seen better anyway.

### Clojurescript - *In land of lisp the cat rides you!*

[Clojurescript](https://github.com/clojure/clojurescript) is actually nice. If you didn't yet, give it a spin. It's dynamicaly typed, has great data abstractions, good libraries and nice learning curve. I'm telling you, it's great. Oh and btw... it's a lisp.

Once you start using it you won't be able to stop. That's a shame, because installing jQuery from *maven central* (yup, in a **jar**) will eventually give you cancer. And your coworkers will be glad to watch "the lisp guy" die.


## Say hi to Purescript

With all these choices, who would ever want a new kid on the block? I'm not going to bullshit you on this one -- it's probably more likely that your boss will let you use interns as drug mules, than that he will allow you to do stuff with Purescript during company time. It's a small language that only few companies use, with small (but bright, believe me) community, and quite a learning curve.

Yet, it's awesome. It has **great language features** and its **integration with npm and node is exceptional**. You don't have to take my word for it -- let's try it now!

### "Hello Purescript"

Installation of `psc` and `psci` is as simple as doing:

    $ mkdir purr
    $ cd purr
    $ npm install purescript
    $ $(npm bin)/psci

This will drop you into purescript repl that has a nice toast too!

     ___                  ___             _       _
    |  _ \ _   _ _ __ ___/ ___|  ___ _ __(_)_ __ | |_
    | |_) | | | | '__/ _ \___ \ / __| '__| | '_ \| __|
    |  __/| |_| | | |  __/___) | (__| |  | | |_) | |_
    |_|    \__,_|_|  \___| ___/ \___|_|  |_| .__/ \__|
                                           |_|

    >

Try doing some basic math:

    > 2 + 2
    4
    > "Hello " ++ "World"
    "Hello World"
    > 2 + "hello"
    Error in module $PSCI:
    Error in value declaration it:
    Error at  line 1, column 1 - line 1, column 6:
      Expression
        "hello"
      does not have type
        Prim.Number

Whoa! Our first type error. The repl shouts at us that it can only perform addition on numbers. This is... convenient.

I've randed a whole lot about employing static type checks for javascript, but Purescript's type system is here to actually give you power, not constrains.

### The toolchain you love. Hello gulp! Hello bower!

Let's look how we can use our old friend **gulp** to make our build process faster and more interactive. Let's start with this little gulpfile:

    var gulp = require('gulp');
    var purescript = require('gulp-purescript');

    gulp.task('purescript:node', function () {
      return gulp.src(['src/**/*.purs', 'bower_components/**/src/**/*.purs'])
        .pipe(purescript.pscMake({output: 'purescript_modules'}))
    });

    gulp.task('purescript:psci', function () {
      return gulp.src(['src/**/*.purs', 'bower_components/**/src/**/*.purs', '!src/**/Main.purs'])
        .pipe(purescript.dotPsci());
    });

    gulp.task('default', ['purescript:node', 'purescript:psci']);

It's dead simple. `pscMake` takes care of compiling your purescript sources into CommonJS compatible modules. We output them into `purescript_modules` directory, so that they do not clash with our own `node_modules` that we use for development. `dotPsci` is a handy utility that will follow all modules that were compiled and add them to `.psci` dotfile in root directory of your project. This way when you run the repl, you won't have to load them using `:m`. Notice how we also added sources from `bower_components` directory -- the pattern used follows convention used by purescript libraries, you only need what is contained in libraries' `src` directory. We also explicitly ignore our main module **Main.purs**, because adding it to our dotfile would cause the repl to go bananas.

And now, we compile!

    $ $(npm bin)/gulp
    [14:10:51] Using gulpfile ~/tmp/purr/gulpfile.js
    [14:10:51] Starting 'purescript:node'...
    [14:10:51] Starting 'purescript:psci'...
    [14:10:51] Finished 'purescript:psci' after 11 ms
    [14:10:51] Finished 'purescript:node' after 162 ms
    [14:10:51] Starting 'default'...
    [14:10:51] Finished 'default' after 154 μs

You should already see some standard library modules in `purescript_modules`, but we do not have any code of our own yet. Let's add it. Pick your favorite editor and add `src/Main.purs` and `src/Math.purs`.


This file will be the enrtypoin of our application. It only contains the `main` function. It imports **Math** module that we will use to store some functions for doing pretty advanced math. It also imports **Debug.Trace** which is a part of standard library.

    -- src/Main.purs

    module Main where

    import Debug.Trace
    import Math

    main = trace $ "Hi fellas! See my magic number! " ++ (show $ quadruple 5)

Our math module will allow us to quadruple a number.

    -- src/Math.purs
    -- Just a module for doing maths. How about quadrupling a number?

    module Math where

    quadruple :: Number -> Number
    quadruple x = x * 4

Rebuild it with gulp and drop into `psci` to check if our quadruple really works as expected:

    $ $(npm bin)/gulp
    ...
    $ $(npm bin)/psci
    ...
    > import Math
    Compiling Math
    > quadruple 10
    40

That's sweet, but nothing fancy yet, how about checking it out in node? Let's drop into node interpreter and see how we can use our compiled purescript from JS.

    $ NODE_PATH=$(pwd)/purescript_modules node
    >

Don't be too araid of this invocation. Adding `purescript_modules` to `NODE_PATH` will just tell the interpreter to also look into that directory when looking for modules. We need that, because that's where we compiled our purescript sources into.

    > var Math = require('Math');
    undefined
    > Math.quadruple(6);
    24

Isn't that awesome? The interop is dead simple. If you didn't have a chance to try interop with stuff like Clojurescript or Google Closure Compiler you can take my word for it -- *it cannot get anny simpler*.

Alrighty, let's also try our **Main** module:

    > var Main = require('Main');
    undefined
    > Main.main();
    Hi fellas! See my magic number! 20
    {}

Our simple math module feels quite lacking, let's see how many pints of beer does an Irishman drink on average during a week. We will need **purescript-foldable-traversable** to sum this stuff up and **purescript-arrays** to easily count them.

    $ $(npm bin)/bower install purescript-foldable-traversable purescript-arrays
    $ $(npm bin)/gulp

Now we can do some more serious math in our **Math** module.

    module Math where

    import Data.Foldable
    import Data.Array

    quadruple :: Number -> Number
    quadruple x = x * 4

    avgBeers :: [Number] -> Number
    avgBeers xs = (sum xs) / (length xs)

Let's compile with `$(npm bin)/gulp` and check it out in the repl!

    $ $(npm bin)/ghci
    ...
    > avgBeers [1, 8, 13, 12.5, 10, 9, 1.5]
    7.857142857142857

Awesome. Managing dependencies also could not get any easier (I'm looking
at you Clojurescript...).

### Browserify all the things

Browserify is *da shizzle* amongst js build systems, and purescript makes using it exceptionally pleasant. Just check these little changes in our gulpfile:

    var gulp = require('gulp');
    var browserify = require('browserify');
    var source = require('vinyl-source-stream');
    var purescript = require('gulp-purescript');

    process.env['NODE_PATH'] = __dirname + '/purescript_modules';

    gulp.task('purescript:node', function () {
      return gulp.src(['src/**/*.purs', 'bower_components/**/src/**/*.purs'])
        .pipe(purescript.pscMake({output: 'purescript_modules'}))
    });

    gulp.task('purescript:psci', function () {
      return gulp.src(['src/**/*.purs', 'bower_components/**/src/**/*.purs', '!src/**/Main.purs'])
        .pipe(purescript.dotPsci());
    });

    gulp.task('browserify', function () {
      var b = browserify({
        entries: './src/app.js',
        debug: true,
      });

      return b.bundle()
        .pipe(source('app.js'))
        .pipe(gulp.dest('./build/'));
    });

    gulp.task('default', ['purescript:node', 'purescript:psci']);

Now in our `src/app.js` we can make use of the combined power of purescript, browser javascript and CommonJS modules! Watch this:

    // src/app.js

    var Math = require('Math');

    void function () {
      window.alert(Math.quadruple(18));
    }();

Just do `$(npm bin)/gulp browserify` and you will have an `build/app.js` that you can include in your browser and enjoy a beautiful alert!

## Purescript - the poor parts

Well, I've showed you bits and pieces of purescript toolchain that took my heart by storm (lets call them **the pure parts**), but it's obvious that it must still suffer some infancy problems (**the poor parts**?).

Firstly -- no sourcemaps. Are you kidding me? Just let me quote Phil Freeman, one of maintainers (taken from github issue):

> Here's my take:  
> 1) The Javascript should be easily debugged without source maps anyway -
> that's the point of the project.  
> 2) I would probably leave source maps until after PS-in-PS is done.
> That's probably a long way off, but I don't see source maps as a very
> high priority to be honest.

To address the first point -- he is totally right. Generated code is easy to understand, let me show you what our **Math** module compiled into:

    // Generated by psc-make version 0.6.9.5
    "use strict";
    var Prelude = require("Prelude");
    var Data_Foldable = require("Data.Foldable");
    var Data_Array = require("Data.Array");
    var quadruple = function (x) {
        return x * 4;
    };
    var avgBeers = function (xs) {
        return Data_Foldable.sum(Data_Foldable.foldableArray)(xs) / Data_Array.length(xs);
    };
    module.exports = {
        avgBeers: avgBeers,
        quadruple: quadruple
    };

`quadruple` is just a JS function, that's easy. `avgBeers` is also a simple function thet uses `sum` from **Data.Foldable** and `length` from **Data.Array**. The invocation of `sum` is a bit complicated, because before actually being called, the function get's partially applied with a typeclass instance that should be used for summing stuff up -- you don't have to concen yourself with it too much. So it's simple, but still... c'mon! I want sourcemaps if I do anything serious in the browser, and putting them on waiting list can be a showstopper for many people who might consider using Purescript for their frontend projects.

The other thing that bothers me is lack of love for great documentation amongst library maintainers. Don't get me wrong -- [Purescript by Example by Phil Freeman](https://leanpub.com/purescript) is an excellent piece, and I cannot underestimate the amount of work that was put into it. It's a great introductory tutorial to the language and some libraries. It's actually better than *ClojureScript: Up and Running*, which is like "the book" for people who want to start with Clojurescript. So, in terms of language introduction, Purescript shines! But... c'mon, look at the readme of any purescript library on github, it's almost always autogenerated summary of types and functions. This doesn't help, especially with a language that is takes some will to comprehend. I feel that Purescript community really overlooks the fact, that *people often start learning stuff simply by "repeating the moves"* (if it's good or bad is not for me to judge, but I definately consider it a fact of life). Literate documentation for libraries would really lower entry barrier.

## Further reading

Anyhow, Purescript is absolutely worth checking out. If you liked how it integrates with **bower** and **npm** you might also check out [pulp by Bodil Stokke](https://github.com/bodil/pulp).

Already mentioned [Purescript by Example](https://leanpub.com/purescript) is a good starting point.

I've put the template project that i used in this article on github at
[https://github.com/karolmajta/purescript-browserify-template](https://github.com/karolmajta/purescript-browserify-template), so feel free to use it as a starting point.

Feel free to share your thoughts on this one [@karolmajta](https://twitter.com/karolmajta) and [@Sigmapoint_pl](https://twitter.com/Sigmapoint_pl).
