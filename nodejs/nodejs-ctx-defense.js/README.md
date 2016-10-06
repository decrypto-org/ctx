# nodejs-ctx-defense

A simple integration of the CTX defence for nodejs projects.
It has been tested for the following:
* Express/express-Handlebars
* Express/pug(jade)
* Express/EJS
* Koa/koa-pug

## Installation

Run ``` npm install --save nodejs-ctx-defense ```

## Basic Usage for an Express-Handlerbars project

Import *nodejs-ctx-defense* to your Express project

```{createCtxObject} = require('./nodejs-ctx-defense');```
initialise the ctxObject

```
let CtxObject = createCtxObject();
```
and add ctxProtect and ctxPermutations in your helpers:

```
helpers: {
    ctxProtect: CtxObject.ctxProtect,
    ctxPermutations: CtxObject.ctxPermutations
}
```

Use *ctxProtect* helper in your Handlebars template to use ctx on secrets:

```html
{{ ctxProtect 'a secret' 'an origin' }}}
```

*secret* is a string containing the secret that needs to be protected and
*origin* is a string uniquely identifying the CTX origin for the secret.


Add the *ctxPermutations* helper in your Handlebars template
to include the used permutations for each origin:
 ```html
 {{ ctxPermutations }}
```

The *ctxPermutations* helper needs to be included after all *ctxProtect*
helpers that use an origin for the first time. It is proposed that it is
included before the *</body>* HTML tag.


### Example

app.js
```
const express = require('express'),                                                                                                         
      exphbs  = require('express-handlebars'),
      {createCtxObject} = require('nodejs-ctx-defense');

let app = express();

let hbs = exphbs.create();

app.engine('handlebars', hbs.engine);
app.set('view engine', 'handlebars');

app.get('/', function (req, res) {

    let CtxObject = createCtxObject();

    res.render('index', {
        showTitle: true,

        helpers: {
            ctxProtect: CtxObject.ctxProtect,
            ctxPermutations: CtxObject.ctxPermutations
        }
    });
});

app.listen(3000);

```

views/index.handlebars

```
<!DOCTYPE html>                                                                                                                                       
<html>
    <head>
        <meta charset="utf-8">
        <title>express-nodejs-ctx-defense Example</title>
    </head>

    <body>
        <div id="entry-template" type="text/x-handlebars-template">
            Secret no.1 from user1 {{{ ctxProtect 'lorem ipsum' 'user1'}}}
            Secret no.2 from user1 {{{ ctxProtect 'dolor sit amet' 'user1' }}}
            Secret no.1 from user2 {{{ ctxProtect 'Lorem ipsum dolor sit amet' 'user2' }}}
        </div>
        {{{ctxPermutations}}}
    </body>
</html>

```

Output:

```
ecret no.1 from user1
G^}(?0d9qO?
Secret no.2 from user1
X^G^}0qd-0B?(-
Secret no.1 from user2
ML19vT6B~%vTdL L1T~6gTKv9g
```
HMTL output:

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
        <title>express-handlebars-ctx Example</title>
        </head>

        <body>
            <div id="entry-template" type="text/x-handlebars-template">
                Secret no.1 from user1
                <div data-ctx-origin="0">G^}(?0d9qO?</div>
                Secret no.2 from user1
                <div data-ctx-origin="0">X^G^}0qd-0B?(-</div>
                Secret no.1 from user2
                <div data-ctx-origin="1">ML19vT6B~%vTdL L1T~6gTKv9g</div>
            </div>
            <script type="application/json" id="ctx-permutations">
            ["0$C\"Uy[S\\2wZFDsYH8aj_gk)fQT1K7e@6EWhn+#%5lrci]v.3`Rx~'/&J*N!MutAzBI{X(>b;dP,G?<^9L}q-O4|
            =:oVpm","T:CWRneI(pt0?#-7{38]kN;ZqwSF@r'sh/o>2\\&EQa5XMui_J$*mly,O}[jY|fb+`K!4d9^VD6.z
            vxLBU1~g%\"G)H=cP<A"]</script>
        </body>
    </html>
```

## Basic Usage for an Express/pug(jade) project

Import *nodejs-ctx-defense* to your Express/pug project,

``` {createCtxObject} = require('./nodejs-ctx-defense'); ```

initialise the ctxObject inside app.get

```
let CtxObject = createCtxObject();
```
and add ctxProtect and ctxPermutations in your app.locals

```
app.locals.ctxProtect = ctxObject.ctxProtect;
app.locals.ctxPermutations = ctxPermutations;
```

Use *ctxProtect* to your pug templates to use ctx on secrets:

```html
div ctxProtect('a secret' 'an origin')
```

*secret* is a string containing the secret that needs to be protected and
*origin* is a string uniquely identifying the CTX origin for the secret.


Add the *ctxPermutations* to your pug templates to
to include the used permutations for each origin:
 ```html
        div=ctxPermutations()
 ```

The *ctxPermutations* helper needs to be included after all *ctxProtect*
helpers that use an origin for the first time. It is proposed that it is
included before the *</body>* HTML tag.

### Example

app.js

```
const express = require('express'),
      pug = require('pug'),
      {createCtxObject} = require('nodejs-ctx-defense');

    let app = express();

    app.set('view engine', 'pug');

    app.get('/', function (req, res) {
        let ctxObject = createCtxObject()
        app.locals.ctxProtect = ctxObject.ctxProtect;
        app.locals.ctxPermutations = ctxObject.ctxPermutations;
        res.render('index', {
        });
    });

app.listen(3000);
```


/view/index.pug

```
Html
    Head
        title pug ctx exapmle
    Body
        div secret1 from user1
            div!=ctxProtect('lorem ipsum', 'user1')
        div secret1 from user1
            div!=ctxProtect('dolor sit amet', 'user1')
        div secret2 from user2
            div!=ctxProtect('Lorem ipsum dolor sit amet',o 'user2')
        div!=ctxPermutations()
```

### Basic Usage in Express/EJS projects

Import *nodejs-ctx-defense* to your Express/EJS project, initialise ctxObject and
add ctxProtect and ctxPermutations in your app.locals,
as decribed for the Express/Jade projects.

Add ctxProtect tag in your EJS template

```
<%- ctxProtect('secret', 'origin') %>
```

and ctxPermutations tag before </body>

```
<%- ctxPermutations() %>
```

### Basic Usage in Koa/koa-pug projects

Import *nodejs-ctx-defense* to your Koa/koa-pug project,

``` {createCtxObject} = require('nodejs-ctx-defense'); ```

initialise the ctxObject inside app.use

```
let CtxObject = createCtxObject();
```
and add ctxProtect and ctxPermutations in your pug.locals

```
pug.locals.ctxProtect = ctxObject.ctxProtect;
pug.locals.ctxPermutations = ctxPermutations;
```
The tag in the pug template are the same as metioned above
for the Express/pug projects


#### Example

app.js

```
const koa = require('koa'),
      router = require('koa-route'),
      Pug = require('koa-pug'),
      {createCtxObject} = require('nodejs-ctx-defense');

   const app = koa()

   const pug = new Pug({
       viewPath: './views',
       app: app
    })

   app.use(router.get('/', function* () {
        let ctxObject = createCtxObject();
        pug.locals.ctxProtect = ctxObject.ctxProtect;
        pug.locals.ctxPermutations = ctxObject.ctxPermutations;   
        this.render('index', true)
    }));
    app.listen(3000);
```

