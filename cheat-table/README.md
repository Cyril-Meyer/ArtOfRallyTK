# ArtOfRallyTK Cheat Table

Memory address for interesting values. Fixed address found using multiple
pointer scan.

**Warning :** the current cheat table is outdated.

### How to search for fixed adress ?

**Data types and possible values**

| Description | Type | Values |
|-|-|-|
| Speed    | Float   | speed is on ui |
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
5. Use saved pointermap

If you are lucky enough, you will get a fixed address.
