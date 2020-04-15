{
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "autosize": {"type": "fit-x", "contains": "padding"},
  "background": "#A67D3D",
  "padding": 5,
  "height": 400,
  "title": {"text": "NYTIMES COVID-19 DATA", "frame": "group"},

  "data": [
    {"name": "highlight_store"},
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
      "format": {"type": "topojson", "feature": {"signal": "data_type"}},
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
    { "name": "data_type", "value": "states",
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
      "update": "'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-'+data_type+'.csv'" 
    },
    { "name": "metric_type", "value": "cases",
      "bind": {"input": "radio", "options": ["cases", "deaths"]} 
    },
    { "name": "digit_format", "update": "data_type=='states'?10:10000"},
    { "name": "metric_range", "value": 100000,
      "bind": {"input": "radio", "options": [100, 500, 1000, 5000, 10000, 100000]} },
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
      "name": "highlight",
      "update": "vlSelectionResolve(\"highlight_store\", \"union\")"
    },
    {
      "name": "highlight_tuple",
      "on": [
        {
          "events": [{"source": "scope", "type": "mouseover"}],
          "update": "datum && item().mark.marktype !== 'group' ? {unit: \"\", fields: highlight_tuple_fields, values: [(item().isVoronoi ? datum.datum : datum)[\"_vgsid_\"]]} : null",
          "force": true
        },
        {"events": [{"source": "scope", "type": "dblclick"}], "update": "null"}
      ]
    },
    {
      "name": "highlight_tuple_fields",
      "value": [{"type": "E", "field": "_vgsid_"}]
    },
    {
      "name": "highlight_modify",
      "on": [
        {
          "events": {"signal": "highlight_tuple"},
          "update": "modify(\"highlight_store\", highlight_tuple, true)"
        }
      ]
    },
    {
      "name": "state_state",
      "value": null,
      "bind": {
        "input": "select",
        "name": "Pick a State",
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
              "test": "(vlSelectionTest(\"highlight_store\", datum))",
              "value": "darkred"
            },
            {"scale": "color", "field": {"signal": "metric_type"}}
          ],
          "tooltip": {
            "signal": "{\"county\": isValid(datum[\"county\"]) ? datum[\"county\"] : \"\"+datum[\"county\"],\"state\": isValid(datum[\"state\"]) ? datum[\"state\"] : \"\"+datum[\"state\"], \"cases\": format(datum[\"cases\"], \"\"), \"deaths\": format(datum[\"deaths\"], \"\")}"
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
    }  ],
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
  "legends": [{"fill": "color", "symbolType": "circle", "title": {"signal":"metric_type"}, "padding":10}]
}
