# Traffic report via SMS
Traftrack is a small program for traffic level reporting via SMS. It use information from [Yandex.Maps](https://yandex.com/maps/)
and can be configured to watch for any place you need and serve many users.

## Installation
### Requirements
- Python 3
- PIL (or Pillow)

You only need to clone the repository and you are ready to go.<br>
TBD: python package

## Configuration
Traftrack use a set of configuration files that you need to create by hand:
- users.json to describe every user we want to send our reports to
- places.json with user-specific locations and traffic levels
- l10n.json with the localization strings
- smsaero.json with a credentials for SMS reporting provider API ([SMSAero](https://smsaero.ru/) by default)
- mask images are a grayscale images with roads you need to track

### Creating a mask images
You need to create a mask image for every location you want to track.
Go to [Yandex.Maps](https://yandex.com/maps/) and search for a location you need to track. <br>
As an example, lets take a traffic intensive place in Nizhniy Novgorod [here](https://yandex.com/maps/47/nizhny-novgorod/?ll=43.933837%2C56.336255&z=14).
In the browser address bar you will see the parameters ll=43.933837%2C56.336255&z=14. 
These are a **latitude**, **longitude** and a **zoom** level of your location.
<br>
You also need to pick a **size** of the map. It can be arbitary and 450x450 is usually enough.
Increase it if you need a bigger area to track.

Then, use this link and download the image: you need to replace {lat}, {lon}, {zoom}, {size_x} and {size_y} 
with the lattitude, longitude, zoom and the size of your location.
```
https://static-maps.yandex.ru/1.x/?lang=en_US&ll={lat}%2C{lon}&z={zoom}&l=map&size={size_x},{size_y}
```
For a previus example it will give you a [link]:
TBD: image

Then use your favorite image editor and create a mask for every road you need to track, for example:
TBD: images

We will use them in places.json

### places.json
This configuration file describes the places to track.
We already know most of the parameters accept for the "max_levels". This parameter describes a maximum amount of
green-yellow-red areas for each traffic level.
In the example below we decide traffic level to be "AllGreen" (means "No traffic at all") if:
- red areas take <= 5%
- yellow areas take <= 10%
- green areas take <= 100% (always true)

These rules applied in same order as they appear in the config. 
The first rule matching the current traffic is considered to be the most appropriate traffic level.
For example, if we have a 10% of red, 50% of yellow and 40% of green, we decide that the traffic level is "BeCareful".

```json
{
    "places": [
        {
            "name": "Place #1",
            "lat": 43.933837,
            "lon": 56.336255,
            "size_x": 450,
            "size_y": 450,
            "zoom": 14,
            "mask_path": "/path/to/mask-1.png",
            "max_levels": {
                "AllGreen": {
                    "green":  100,
                    "yellow": 10,
                    "red":    5
                },
                "Minor": {
                    "green":  100,
                    "yellow": 100,
                    "red":    5
                },
                "BeCareful": {
                    "green":  100,
                    "yellow": 100,
                    "red":    15
                },
                "NoWay": {
                    "green":  100,
                    "yellow": 100,
                    "red":    30
                },
                "GetTheHellOutOfHere": {
                    "green":  100,
                    "yellow": 100,
                    "red":    100
                }
            }
        },
        {
            "name": "Place #2",
            "lat": 43.933837,
            "lon": 56.336255,
            "size_x": 450,
            "size_y": 450,
            "zoom": 14,
            "mask_path": "/path/to/mask-1.png",
            "max_levels": {
                "AllGreen": {
                    "green":  100,
                    "yellow": 10,
                    "red":    5
                },
                "Minor": {
                    "green":  100,
                    "yellow": 100,
                    "red":    5
                },
                "BeCareful": {
                    "green":  100,
                    "yellow": 100,
                    "red":    15
                },
                "NoWay": {
                    "green":  100,
                    "yellow": 100,
                    "red":    30
                },
                "GetTheHellOutOfHere": {
                    "green":  100,
                    "yellow": 100,
                    "red":    30
                }
            }
        }
    ]
}
```

### users.json
Configuration file with information about the users. Every user can have his own places.json config.
```json
{
    "user1" : {
        "places_config": "places1.json",
        "lang": "en_US",
        "phone": "+1XXXXXXXXXX"
    },
    "user2" : {
        "places_config": "places2.json",
        "lang": "ru_RU",
        "phone": "+7XXXXXXXXXX"
    }
}
```

### l10n.json
Localization strings. Every string has an ID and if you add an ID with a place name, places will be localized too.
```json
{
    "en_EN": {
        "Greetings": "Hi,",
        "AllGreen":  "No traffic at all.",
        "Minor":     "It's just a little bit slow.",
        "BeCareful": "Road is quite slow now, careful!",
        "NoWay":     "Traffic jam!",
        "GetTheHellOutOfHere": "You don't want to go here! It's a dead end!"
    },
    "ru_RU": {
        "Greetings": "Привет.",
        "AllGreen":  "Все свободно.",
        "Minor":     "Можно ехать.",
        "BeCareful": "Небольшая пробка.",
        "NoWay":     "Осторожно, там пробка!",
        "GetTheHellOutOfHere": "Большая пробка! Даже не думай туда ехать!",

        "Place #1": "Место #1",
        "Place #2": "Место #2"
    }
}
```

### smsaero.json
Configuration file with SMSAero credentials. Check with the [documentation](https://smsaero.ru/api/description/) on how to obtain username and password.
```json
{
    "user":"some.name@server.com",
    "password": "xxxxxxxxx",
    "signature": "TRAFFIC"
}
```
