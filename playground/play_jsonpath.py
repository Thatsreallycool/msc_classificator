from jsonpath_rw_ext import parse

import json

#json_string = '{"id":1, "name":"Pankaj"}'

#json_data = json.loads(json_string)

#jsonpath_expression = parse('$.id')

#match = jsonpath_expression.find(json_data)

#print(match)
#print("id value is", match[0].value)


json_data = {
  "employees": [
    {
      "id": 1,
      "name": "Pankaj",
      "salary": "10000"
    },
    {
      "name": "David",
      "salary": "5000",
      "id": 2
    },
    {
      "name": "David",
      "salary": "5000",
      "id": 3
    }
  ]
}

new_data = {
  "store": {
    "book": [
      { "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      { "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 12.99
      },
      { "category": "fiction",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 8.99
      },
      { "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  }
}

my_string = '$..category'
for match in parse(my_string).find(new_data):
    print(f'{my_string}: {match.value}')
print("\n")

my_string = '$.store.*'
for match in parse(my_string).find(new_data):
    print(f'{my_string}: {match.value}')
print("\n")

my_string = '$.store..price'
for match in parse(my_string).find(new_data):
    print(f'{my_string}: {match.value}')
print("\n")

my_string = '$..book[-1:]'
for match in parse(my_string).find(new_data):
    print(f'{my_string}: {match.value}')
print("\n")

my_string = '$..book[:2]'
for match in parse(my_string).find(new_data):
    print(f'{my_string}: {match.value}')
print("\n")

my_string = '$..book[*].isbn'
for match in parse(my_string).find(new_data):
    print(f'{my_string}: {match.value}')
print("\n")

my_string = '$..*'
for match in parse(my_string).find(new_data):
    print(f'{my_string}: {match.value}')
print("\n")

my_string = '$..book[?(@.price<10)]'
for match in parse(my_string).find(new_data):
    print(f'{my_string}: {match.value}')
print("\n")


data_set_2 = {
  "firstName": "John",
  "lastName" : "doe",
  "age"      : 26,
  "address"  : {
    "streetAddress": "naist street",
    "city"         : "Nara",
    "postalCode"   : "630-0192"
  },
  "phoneNumbers": [
    {
      "type"  : "iPhone",
      "number": "123-4567-8888"
    },
    {
      "type"  : "home",
      "number": "123-4567-8910"
    },
    {
      "type"  : "mobile",
      "number": "123-4567-1233"
    }
  ]
}
my_string = "$.phoneNumbers[?(@.type=='home')]"
for match in parse(my_string).find(data_set_2):
    print(f'{my_string}: {match.value}')
print("\n")
