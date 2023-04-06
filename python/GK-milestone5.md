With Dr. B's help, we got our python to output a version of our xml file collection with named entities tagged as ```LOC```, ```FAC```, ```ORG```, ```GPE```, ```NORP```, and ```PERSON```. For our purposes, we might only end up needing the names tagged as ```PERSON```.

For our network analysis, we plan to map out which characters are present in which locations and which ones appear alongside one another in the same places. Since most of the game's locations have their own files that show the characters that appear there, we may not need to do anything else with them. The one of the only locations in the game that I can think of that does not have its own dedicated file is the Summit, so that one might need to be tagged.

As for the characters, I have already listed all 34 of the ones we are including in our analysis in the pattern list in python, so they should all be tagged properly. One exception that I am aware of is Kent. for some reason, python autotagged his name like this:

```<dialogue who="<name type="PERSON">K</name>ent">I'm glad you're a friend of the family, @. Sorry about my behavior before.\</dialogue>```

Only the K in his name is tagged. Including his full name in the pattern list did not fix this, so it will have to be fixed later with regex.

Overall, I am looking forward to seeing what more we can do with this and how we will integrate it into a cytoscape network.