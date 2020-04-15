{
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "autosize": {"type": "fit-x", "contains": "padding"},
  "background": "#A67D3D",
  "padding": 5,
  "height": 400,
  "title": {"text": "NYTIMES COVID-19 DATA", "frame": "group"},

  "data": [
    {"name": "state_store"},
    {
      "name": "source_1",
      "async": false,
      "url": {"signal": "data_url"},
      "format": {"type": "csv", "delimiter": ",","parse": {"date": "utc:'%Y-%m-%d'"}},
    "transform": [{
          "type": "filter",
          "expr": "inrange(datum[\"date\"], [feb1, day])"
      }]
    },
    {
      "name": "source_0",
      "async":false,
      "url": "https://vega.github.io/editor/data/us-10m.json",
      "format": {"type": "topojson", "feature": {"signal": "boundary"}},
      "transform": [
        {"type": "identifier", "as": "_vgsid_"},
        {
          "type": "formula",
          "expr": "datum.id<digit_format?0+''+datum.id:datum.id",
          "as": "digit"
        },
        {
          "type": "lookup",
          "from": "source_1",
          "key": "fips",
          "fields": ["digit"],
          "values": ["date", "county", "state", "fips", "cases", "deaths"],
          "default": "0"
        },
        {
          "type": "filter",
          "expr": "isValid(datum[\"cases\"]) && isFinite(+datum[\"cases\"])"
        },
        {
          "type": "filter",
          "expr": "!(length(data(\"state_store\"))) || (vlSelectionTest(\"state_store\", datum))"
        }
      ]
    }
  ],

  "signals": [
    { "name": "boundary", "value": "states",
      "bind": {"input": "radio", "options": ["states", "counties"]} 
    },
    {
      "name": "feb1",
      "value": "1580533200000"
    },
    {
      "name": "datetime",
      "update": "datetime(day)"
    },
    { "name": "data_url", 
      "update": "'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-'+boundary+'.csv'" 
    },
    { "name": "metric", "value": "cases",
      "bind": {"input": "radio", "options": ["cases", "deaths"]} 
    },
    { "name": "digit_format", "update": "boundary=='states'?10:10000"},
    { "name": "metric_range", "value": 50000,
      "bind": {"input": "radio", "options": [100, 500, 1000, 5000, 10000, 50000]} },
    { "name": "day", "value": 1586899300000,
      "bind": {"input": "range", "min": 1580533200000, "max": 1596240000000, "step": 8.64e+7} },
    {
      "name": "width",
      "init": "isFinite(containerSize()[0]) ? containerSize()[0] : 200",
      "on": [
        {
          "update": "isFinite(containerSize()[0]) ? containerSize()[0] : 200",
          "events": "window:resize"
        }
      ]
    },
    {
      "name": "unit",
      "value": {},
      "on": [
        {"events": "mousemove", "update": "isTuple(group()) ? group() : unit"}
      ]
    },
    {
      "name": "state_state",
      "value": null,
      "bind": {
        "input": "select",
        "name": "state",
        "options": [
          null,
          "Alabama",
          "Alaska",
          "Arizona",
          "Arkansas",
          "California",
          "Colorado",
          "Connecticut",
          "Delaware",
          "Florida",
          "Georgia",
          "Hawaii",
          "Idaho",
          "Illinois",
          "Indiana",
          "Iowa",
          "Kansas",
          "Kentucky",
          "Louisiana",
          "Maine",
          "Maryland",
          "Massachusetts",
          "Michigan",
          "Minnesota",
          "Mississippi",
          "Missouri",
          "Montana",
          "Nebraska",
          "Nevada",
          "New Hampshire",
          "New Jersey",
          "New Mexico",
          "New York",
          "North Carolina",
          "North Dakota",
          "Ohio",
          "Oklahoma",
          "Oregon",
          "Pennsylvania",
          "Rhode Island",
          "South Carolina",
          "South Dakota",
          "Tennessee",
          "Texas",
          "Utah",
          "Vermont",
          "Virginia",
          "Washington",
          "West Virginia",
          "Wisconsin",
          "Wyoming"
        ]
      }
    },
    {
      "name": "state_tuple",
      "update": "state_state !== null ? {fields: state_tuple_fields, values: [state_state]} : null"
    },
    {"name": "state_tuple_fields", "value": [{"type": "E", "field": "state"}]},
    {
      "name": "state_modify",
      "on": [
        {
          "events": {"signal": "state_tuple"},
          "update": "modify(\"state_store\", state_tuple, true)"
        }
      ]
    }
  ],

  "projections": [
    {
      "name": "projection",
      "size": {"signal": "[width, height]"},
      "fit": {"signal": "data('source_0')"},
      "type": "albersUsa"
    }
  ],

  "marks": [
    {
      "name": "marks",
      "type": "shape",
      "style": ["geoshape"],
      "interactive": true,
      "from": {"data": "source_0"},
      "encode": {
        "update": {
          "fill": [
            {
              "test": "datum.cases > 100000 || datum.deaths > 5000",
              "value": "black"
            },
            {"scale": "color", "field": {"signal": "metric"}}
          ],
          "tooltip": {
            "signal": "{\"county\": isValid(datum[\"county\"]) ? datum[\"county\"] : \"\",\"state\": isValid(datum[\"state\"]) ? datum[\"state\"] : \"\"+datum[\"state\"], \"cases\": format(datum[\"cases\"], \"\"), \"deaths\": format(datum[\"deaths\"], \"\")}"
          }
        }
      },
      "transform": [{"type": "geoshape", "projection": "projection"}]
    },
    {
      "type": "text",
      "encode": {
        "update": {
          "fill": {
            "value": "#000"
          },
          "text": {
            "signal": "''+datetime"
          },
          "fontSize": {
            "value": 20
          }, 
          "y": {"signal":"height"}
        }
      }
    }  
  ],
  "scales": [
    {
      "name": "color",
      "type": "quantize",
      "domain": [0, {"signal":"metric_range"}],
      "range": {"scheme": "greens", "count": 10},
      "interpolate": "hcl",
      "zero": true
    }
  ],
  "legends": [{"fill": "color", "symbolType": "circle", "title": {"signal":"metric"}, "padding":10}]
}
