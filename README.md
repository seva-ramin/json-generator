# Random JSON Generator

Generates random JSON objects, either from command line or as a RESTful web server.

- Requires Python3
- Run `pip3 install -r requirements.txt` to ensure you have all the packages

## Command Line Usage

To generate from command line:

```
$ cd randjson
$ python3 generate.py assets/template.json     <-- generates 1
$ python3 generate.py assets/template.json 6    <-- generates 6
```

You can replace the `assets/template.json` with your own template.

## Run As Server

Run `index.py` at the project parent directory. (Did you run `pip3 install`? See above.)

```
$ python3 index.py
```

To post a template:

```
$ curl -d '{ "user": "__RANDOM__firstname" }' -H "Content-Type: application/json" -X POST http://localhost:8080/template
{
    "links":[
        {"href":"/template/558363","rel":"1"},
        {"href":"/template/558363/5","rel":"5"},
        {"href":"/template/558363/25","rel":"25"}
    ],
    "status":"success"
}

$ curl localhost:8080/template/558363
[{"user": "Hollie"}]

$ curl localhost:8080/template/558363/3
[{"user": "Adan"}, {"user": "Eliza"}, {"user": "Beth"}]
```

## Run As Docker Container

From project parent directory:

```
$ docker pull python
$ docker build -t randomjson .
$ docker run -p 8080:8080 randomjson
```

## Template Reference Guide

The template can be any json file. A JSON value that begins with `__RANDOM__`, followed 
by a type, indicates that you wish to randomize this value. Sample template is <a href="randjson/assets/template.json">template.json</a>

Types are case insensitive and are listed below:

| Type | Comment |
| :---------------------------: | :----- |
| firstname | `__RANDOM__firstname` |
| lastname | `__RANDOM__lastname` |
| street | `__RANDOM__street`: generate random street number and name |
| city, state, zip | `__RANDOM__city`, `__RANDOM__state`, `__RANDOM__zip`: These are tied together since they are real cities and states. If you need multiple, you can label each to tie them `__RANDOM__city__1`, `__RANDOM__city__2`, `__RANDOM__state__1`, `__RANDOM__state__2`. |
| phone | guess the syntax |
| phrase | guess |
| date | `__RANDOM__date` will generate a random date. `__RANDOM__date__12/01/1999__01/01/2000` will generate a date between those.|
| number | `__RANDOM__number`: Same as date, you can provide a range: `__RANDOM__number__500__1000` will generate a whole number from 500 to 1,000.|
| money | `__RANDOM__money`: Same as number, you can provide a range: `__RANDOM__money__-500__500` will generate a double precision number from -500 to 500.|
| noun | |
| adjective | |
| choice | `__RANDOM__choice__Good__Bad__OK__UNKNOWN FACT`, `__RANDOM__choice__YES__NO`, you decide the choices. |
