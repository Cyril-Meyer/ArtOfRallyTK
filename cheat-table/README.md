# ArtOfRallyTK Cheat Table

Memory addresses for interesting values. Fixed address found using multiple
pointer scan.

| Version                    | Speed | RPM | Gear | Steering |
|----------------------------|:-----:|:---:|:----:|:--------:|
|[1.3.5](artofrally_1_3_5.CT)| ✅ | ✅ | ✅ |    |
|[1.3.4](artofrally_1_3_4.CT) (outdated) | ✅ | ✅ | ✅ | ✅ |


### How to search for fixed addresses ?

**Data types and possible values**

| Description | Type | Values |
|-------------|------|--------|
| Speed    | Float   | speed is on ui (use truncated) |
| RPM      | Float   | min is arround 1000, max is less than 10000 |
| Gear     | 4 Bytes | neutral = 1, 2nd = 3, 3rd = 4, etc |
| Steering | Float   | max left = -1.0, max right = 1.0, middle = 0.0 |

**Multiple pointer scan**

1. Start the game
2. Attach cheat engine
3. Search for the value in cheat engine
4. Generate pointermap
5. Restart the game

Do this 4 or 5 times.

1. Start the game
2. Attach cheat engine
3. Search for the value in cheat engine
4. Pointer scan for this address
5. Compare results with other saved pointermaps

If you are lucky enough, you will get a list of fixed address.  
If you do not, you may increase maximum offset level to 8 or 9.
Using a higher maximum offset level causes an increase in search time, this can take several days, you can stop the
search once you have found a satisfactory number of results.
